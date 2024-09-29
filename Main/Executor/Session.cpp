/*
Copyright (C) 2024 The XLang Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include "Session.h"
#include "start.h"
#include "xMindAPI.h"
#include "xlang.h"

namespace xMind
{
    SESSION_ID SessionManager::createSession(const std::string& strSessionId) {
        std::lock_guard<std::mutex> lock(m_session_mtx);
        int64_t createdTime = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
        auto sid = nextSid++;
		SessionIDInfo info = { sid, 0, 0 };
		SESSION_ID sessionId = ToSessionID(info);
        m_sessions[sessionId] = { sessionId, createdTime, strSessionId };
        m_sessionIdToSidMap[strSessionId] = sessionId;
        return sessionId;
    }
    //each chat request in same session but will start with a input index from 1
    X::Value SessionManager::HandleChatRequest(X::Value& reqData)
    {
		ChatRequest request = parseChatRequest(reqData);
		SESSION_ID sid = getSessionId(request.sessionId);
		if (sid == NO_SESSION_ID)
		{
            X::Package utils(xMind::MindAPISet::I().RT(), "utils", "xlang_os");
            X::Value uuid = utils["generate_uid"]();
            std::string strSessionId = uuid.ToString();
			sid = createSession(strSessionId);
            request.sessionId = strSessionId;
		}
		X::Value graph = Starter::I().GetOrCreateRunningGraph(request.model);
        X::XPackageValue<AgentGraph> packGraph(graph);
		AgentGraph* pGraph = packGraph.GetRealObj();
		if (pGraph == nullptr)
		{
			return X::Value();
		}
		//set input index ( not input Pin index)
		SessionIDInfo idInfo = FromSessionID(sid);
        idInfo.inputIndex++;
		idInfo.iterationCount = 0;
        sid = ToSessionID(idInfo);
        {
			//set back to remember the input index increased
			std::lock_guard<std::mutex> lock(m_session_mtx);
			m_sessionIdToSidMap[request.sessionId] = sid;
			//we don't change m_sessions, so if need sessionInfo, use {sid, 0, 0} to get
        }
		X::Value retMsg = pGraph->RunInputs(sid, request.messageList);
        ChatCompletionResponse response;
		response.sessionId = request.sessionId;
		response.object = "text";
		response.created = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
		response.model = request.model;
		response.choices.push_back({ 0, { "assistant", retMsg.ToString(), "" }, "", "complete" });

        X::Value retData = createChatResponse(response);
        return retData;
    }
    X::Value SessionManager::HandleCompletionRequest(X::Value& reqData)
    {
		CompletionRequest request = parseCompletionRequest(reqData);
		X::Value graph = Starter::I().GetOrCreateRunningGraph(request.model);
		X::XPackageValue<AgentGraph> packGraph(graph);
		AgentGraph* pGraph = packGraph.GetRealObj();
		if (pGraph == nullptr)
		{
            return X::Value();
		}
		X::Value valInput = request.prompt;
		pGraph->RunInputs(NO_SESSION_ID, valInput);
        return X::Value();
    }
    X::Value SessionManager::createChatResponse(const ChatCompletionResponse& response) {
        // Create the main dictionary
        X::Dict mainDict;
        mainDict->Set("sessionId", response.sessionId);
        mainDict->Set("object", response.object);
        mainDict->Set("created", response.created);
        mainDict->Set("model", response.model);

        // Create the choices list
        X::List choicesList;

        // Fill the choices list
        for (const auto& choice : response.choices) {
            X::Dict choiceDict;
            choiceDict->Set("index",choice.index);

            // Create and add the message dictionary
            X::Dict messageDict;
            messageDict->Set("role", choice.message.role);
            messageDict->Set("content", choice.message.content);
            messageDict->Set("refusal", choice.message.refusal);

            choiceDict->Set("message", messageDict);
            choiceDict->Set("logprobs", choice.logprobs);
            choiceDict->Set("finish_reason", choice.finish_reason);

            choicesList->append(choiceDict);
        }

        // Add the choices list to the main dictionary
        mainDict->Set("choices", choicesList);

        // Create the usage dictionary
        X::Dict usageDict;
        usageDict->Set("prompt_tokens", response.usage.prompt_tokens);
        usageDict->Set("completion_tokens", response.usage.completion_tokens);
        usageDict->Set("total_tokens", response.usage.total_tokens);

        // Add the usage dictionary to the main dictionary
        mainDict->Set("usage", usageDict);

        // Return the main dictionary as X::Value
        return X::Value(mainDict);
    }
    ChatRequest SessionManager::parseChatRequest(X::Value& reqData) {
        ChatRequest request;

		X::Dict reqDict = reqData;
        // Extract "model"
        request.model = reqDict["model"].ToString();

        // Extract "messages"
        X::List messageList = reqDict["messages"];
		request.messageList = messageList;//still keep for agent use
        for (const auto& item : *messageList) {
            X::Dict messageDict = item;
            Message msg;
            msg.role = messageDict["role"].ToString();
            msg.content = messageDict["content"].ToString();
            request.messages.push_back(msg);
        }

        // Extract "temperature"
		X::Value varTemperature = reqDict["temperature"];
        if (varTemperature.IsValid())
        {
            request.temperature = varTemperature.ToDouble();
        }

		X::Value varSessionId = reqDict["sessionId"];
        if (varSessionId.IsValid()) {
            request.sessionId = varSessionId.ToString();
        }

        return request;
    }
    CompletionRequest SessionManager::parseCompletionRequest(X::Value& reqData) {
        CompletionRequest request;

        // Extract "model"
        request.model = reqData["model"].ToString();

        // Extract "prompt"
        request.prompt = reqData["prompt"].ToString();
        // Extract "temperature"
        X::Value varTemperature = reqData["temperature"];
        if (varTemperature.IsValid())
        {
            request.temperature = varTemperature.ToDouble();
        }

        // Extract "max_tokens"
        request.max_tokens = reqData["max_tokens"].ToInt();

        // Optional: Extract "stream" if present
        if (reqData.contains("stream")) {
            request.stream = reqData["stream"].ToBool();
        }
        else {
            request.stream = false;  // Default value
        }

        return request;
    }
    X::Value SessionManager::createCompletionResponse(const CompletionResponse& response) {
        // Create the main dictionary
        X::Dict mainDict;
        mainDict->Set("id", response.id);
        mainDict->Set("object", response.object);
        mainDict->Set("created", response.created);
        mainDict->Set("model", response.model);

        // Create the choices list
        X::List choicesList;

        // Fill the choices list
        for (const auto& choice : response.choices) {
            X::Dict choiceDict;
            choiceDict->Set("text", choice.text);
            choiceDict->Set("index", choice.index);
            choiceDict->Set("logprobs", choice.logprobs);
            choiceDict->Set("finish_reason", choice.finish_reason);

            choicesList->append(choiceDict);
        }

        // Add the choices list to the main dictionary
        mainDict->Set("choices", choicesList);

        // Create the usage dictionary
        X::Dict usageDict;
        usageDict->Set("prompt_tokens", response.usage.prompt_tokens);
        usageDict->Set("completion_tokens", response.usage.completion_tokens);
        usageDict->Set("total_tokens", response.usage.total_tokens);

        // Add the usage dictionary to the main dictionary
        mainDict->Set("usage", usageDict);

        // Return the main dictionary as X::Value
        return X::Value(mainDict);
    }

} // namespace xMind