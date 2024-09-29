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

#include "LlmPool.h"
#include "xMindAPI.h"

namespace xMind
{
	X::Value LlmRequest::MakeRequest(const std::string& model, const X::Value& prompts, double temperature)
	{
		if (m_request.IsInvalid())
		{
			X::Package http(xMind::MindAPISet::I().RT(), "http", "xlang_http");
			m_request = http["Client"](m_url);
			m_request["setHeaders"](m_headers);
		}
		X::Dict dictData;
		X::Value varModel((std::string&)model);
		dictData->Set("model", varModel);
		if (prompts.IsList())
		{
			dictData->Set("messages", prompts);
		}
		else//treat as string
		{
			std::string strPrompt = ((X::Value&)prompts).ToString();
			X::List listMsg;
			X::Dict prompt;
			prompt->Set("role", "user");
			prompt->Set("content", strPrompt);
			listMsg += prompt;
			dictData->Set("messages", listMsg);
		}
		dictData->Set("temperature", temperature);
		std::string data = dictData.ToString(true);
		m_request["post"]("", m_content_type, data);
		int status = (int)m_request["status"]();
		X::Value body;
		if (status == 200)
		{
			body = m_request["body"]();
			X::Package json(xMind::MindAPISet::I().RT(), "json");
			X::Value jsonBody =json["loads"](body);
			X::Dict dictBody(jsonBody);
			X::Value choices = dictBody["choices"];
			if (choices.IsList())
			{
				X::Value first = choices[(long long)0];
				if (first.IsValid())
				{
					X::Dict dictFirst(first);
					X::Value msg = dictFirst["message"];
					if (msg.IsValid())
					{
						X::Dict dictMsg(msg);
						body = dictMsg["content"];
					}
				}
			}
		}
		else
		{
			X::Error error(status, "");
			LOG << "Request '" << m_url << "' failed with status code : " << status << LINE_END;
			body = error;
		}
		return body;
	}
}