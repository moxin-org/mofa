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

#pragma once
#include "singleton.h"
#include <string>
#include <vector>
#include <unordered_map>
#include "xlang.h"
#include <mutex>
#include <chrono>
#include "type_def.h"

namespace xMind
{
    #define NO_SESSION_ID 0
    struct Message {
        std::string role;
        std::string content;
        std::string refusal;// Optional, used in the response context
    };

    struct Choice {
        int index;
        Message message;
        std::string logprobs;
        std::string finish_reason;
    };

    struct Usage {
        int prompt_tokens;
        int completion_tokens;
        int total_tokens;
    };

    struct ChatCompletionResponse {
        std::string sessionId;
        std::string object;
        int64_t created;
        std::string model;
        std::vector<Choice> choices;
        Usage usage;
    };
    struct ChatRequest {
        std::string model;
        std::vector<Message> messages;
        X::List messageList;
        double temperature;
        std::string sessionId;  // Optional sessionId
    };
	//for completion, no session
    struct CompletionRequest {
        std::string model;
        std::string prompt;
        double temperature;
        int max_tokens;
        bool stream;  // Optional, default is false
    };
    struct CompletionChoice {
        std::string text;
        int index;
        std::string logprobs;
        std::string finish_reason;
    };

    struct CompletionUsage {
        int prompt_tokens;
        int completion_tokens;
        int total_tokens;
    };

    struct CompletionResponse {
        std::string id;
        std::string object;
        int64_t created;
        std::string model;
        std::vector<CompletionChoice> choices;
        CompletionUsage usage;
    };
    struct SessionInfo {
        SESSION_ID id;
        int64_t created;
        std::string sessionId;
    };
    class SessionManager : public Singleton<SessionManager>
    {
		X::Value createChatResponse(const ChatCompletionResponse& response);
        ChatRequest parseChatRequest(X::Value& reqData);
        CompletionRequest parseCompletionRequest(X::Value& reqData);
        X::Value createCompletionResponse(const CompletionResponse& response);
        SESSION_ID createSession(const std::string& sessionId);
        SESSION_ID getSessionId(const std::string& sessionId)
        {
            std::lock_guard<std::mutex> lock(m_session_mtx);
            if (m_sessionIdToSidMap.find(sessionId) != m_sessionIdToSidMap.end())
            {
                return m_sessionIdToSidMap[sessionId];
            }
            return NO_SESSION_ID;
        }
    public:
		X::Value HandleChatRequest(X::Value& reqData);
		X::Value HandleCompletionRequest(X::Value& reqData);
    private:
        std::unordered_map<std::string, SESSION_ID> m_sessionIdToSidMap;
        std::unordered_map<SESSION_ID, SessionInfo> m_sessions;
		//used for non-session request
		SessionIDInfo m_noSessionInfo = { NO_SESSION_ID, 0, 0 };
        unsigned long nextSid = 1;
        std::mutex m_session_mtx;
    };
}