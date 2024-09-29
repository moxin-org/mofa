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
#include "BufferedProcessor.h"
#include "LlmPool.h"
#include "log.h"
#include "XMindCmd.h"
#include <vector>

namespace xMind
{
    class BaseAgent: public BufferedProcessor
    {
        BEGIN_PACKAGE(BaseAgent)
            ADD_BASE(BufferedProcessor);
            APISET().AddProp0("prompts", &BaseAgent::m_prompts);
            APISET().AddFunc<2>("addPrompt", &BaseAgent::AddPrompt);
            APISET().AddVarFunc("llm", &BaseAgent::RunLlm);
        END_PACKAGE

        inline virtual X::Value GetOwner() override
        {
            auto* pXPack = BaseAgent::APISET().GetProxy(this);
            return X::Value(pXPack);
        }
    public:
        BaseAgent():
			BufferedProcessor()
        {
			m_RunInThread = true;
        }

        virtual ~BaseAgent()
        {
        }
		virtual X::Value RunOnce() override;
        virtual X::Value Clone() override
        {
			BaseAgent* pAgent = new BaseAgent();
			pAgent->Copy(this);
			auto* pXPack = BaseAgent::APISET().GetProxy(pAgent);
			X::Value retValue = X::Value(pXPack);
			return retValue;
		}
        void AddPrompt(const std::string& role, const std::string& content)
        {
			X::Dict prompt;
            prompt->Set("role", (std::string&)role);
			prompt->Set("content", (std::string&) content);
			m_prompts += prompt;
        }
        bool RunLlm(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
            std::vector<std::string> llmSelections;
			std::string model = m_model;
            double temperature = m_temperature;
			auto it = kwParams.find("model");
			if (it)
			{
				model = it->val.ToString();
			}
			it = kwParams.find("selections");
			X::List selections(it?it->val:m_selections);
			for (auto selection : *selections)
			{
				llmSelections.push_back(selection.ToString());
			}
			it = kwParams.find("temperature");
			if (it)
			{
				temperature = (double)it->val;
			}
			X::List prompts = m_prompts;
			if (params.size() > 0)
			{
				std::string strData = params[0].ToString();
				X::Dict dictPrompt;
				dictPrompt->Set("role", "user");
				dictPrompt->Set("content", strData);
				prompts += dictPrompt;
			}
			retValue = LlmPool::I().RunTask(model, prompts, temperature, llmSelections);
            return true;
        }
		inline void SetTemperature(double temperature)
		{
			m_temperature = temperature;
		}
		inline double GetTemperature()
		{
			return m_temperature;
		}
		inline void SetSelections(const X::List& selections)
		{
			m_selections = selections;
		}
		inline X::List GetSelections()
		{
			return m_selections;
		}
		inline void SetModel(const std::string& model)
		{
			m_model = model;
		}
		inline std::string GetModel()
		{
			return m_model;
		}
	private:
		X::List m_prompts;
		double m_temperature = 0.7;
		X::List m_selections;
		std::string m_model;
    };
}
