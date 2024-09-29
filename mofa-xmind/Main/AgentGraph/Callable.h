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
#include <queue>
#include <vector>
#include <string>
#include <unordered_map>
#include <filesystem>
#include <regex>
#include <atomic>
#include <fstream>
#include <iostream>
#include <algorithm>
#include "xpackage.h"
#include "Locker.h"
#include "type_def.h"

namespace xMind
{
	enum class CallableType
	{
		callable, function, action, agent, compositeAgent
	};
	struct Pin
	{
		std::string name;
		std::vector<std::string> formats;
	};
	struct Source
	{
		std::string python;
		std::string xlang;
		std::string shared_lib;
	};
	class AgentGraph;
	class Callable
	{
		friend class Parser;

		BEGIN_PACKAGE(Callable)
			APISET().AddPropWithType<unsigned long long> ("ID", &Callable::m_ID);
			APISET().AddPropWithType<std::string>("name", &Callable::m_name);
			APISET().AddPropWithType<X::Value>("graph", &Callable::m_varGraph);
			APISET().AddProp0("nodeDesc", &Callable::m_nodeYamlDesc);
			APISET().AddPropWithType<std::string>("description", &Callable::m_description);
			APISET().AddPropL("inputs",
				[](auto* pThis, X::Value v) { pThis->SetInputs(v); },
				[](auto* pThis) { return pThis->GetInputs(); });
			APISET().AddPropL("outputs",
				[](auto* pThis, X::Value v) { pThis->SetOutputs(v); },
				[](auto* pThis) { return pThis->GetOutputs(); });
		END_PACKAGE

	protected:
		static std::atomic<unsigned long long> s_idCounter;
		//real object such as Xlang func/class
		//or native lib's function
		X::Value m_implObject;
		X::KWARGS m_params;
		X::XRuntime* m_rt;
		X::Value m_varGraph;
		AgentGraph* m_agentGraph;
		unsigned long long m_ID;//unique ID inside XMind not just the graph
		std::string m_name; // Callable Name
		std::string m_instanceName;
		std::string m_description;//ability description
		CallableType m_type;
		Source m_source;
		X::Value m_nodeYamlDesc;//all node info pack as X::Value put here
		std::vector<Pin> m_inputs;
		std::vector<Pin> m_outputs;
		TrigerCondition m_trigerCondition = TrigerCondition::Default;
		unsigned long m_iterationLimit = 0;//default to 0, mean no limit
		Locker m_locker;

		void Copy(Callable* other);
		void PushEvent(int inputIndex, X::Value data);
	public:
		Callable() :
			m_type(CallableType::callable),
			m_agentGraph(nullptr), m_rt(nullptr),
			m_ID(++s_idCounter)
		{
		}

		virtual ~Callable()
		{
		}
		inline unsigned long long ID()
		{
			return m_ID;
		}
		inline void SetTriggerCondition(TrigerCondition trigerCondition)
		{
			m_trigerCondition = trigerCondition;
		}
		inline TrigerCondition GetTriggerCondition()
		{
			return m_trigerCondition;
		}
		inline void SetIterationLimit(unsigned long limit)
		{
			m_iterationLimit = limit;
		}
		inline unsigned long GetIterationLimit()
		{
			return m_iterationLimit;
		}
		inline void SetSource(const Source& source)
		{
			m_source = source;
		}
		inline Source& GetSource()
		{
			return m_source;
		}
		inline X::Value& GetNodeYamlDesc()
		{
			return m_nodeYamlDesc;
		}
		inline void SetNodeYamlDesc(X::Value& v)
		{
			m_nodeYamlDesc = v;
		}
		inline CallableType Type()
		{
			return m_type;
		}
		inline void SetImplObject(X::Value implObject)
		{
			m_implObject = implObject;
		}
		inline void SetName(const std::string& name)
		{
			m_name = name;
		}
		inline X::XRuntime* GetRT()
		{
			return m_rt;
		}
		inline void SetRT(X::XRuntime* rt)
		{
			m_rt = rt;
			if (m_implObject.IsObject())
			{
				m_implObject.GetObj()->SetRT(rt);
			}
		}
		inline std::string GetName()
		{
			return m_name;
		}
		inline void SetParams(X::KWARGS params)
		{
			m_params = params;
		}
		inline void SetInstanceName(const std::string& instanceName)
		{
			m_instanceName = instanceName;
		}
		inline std::string GetInstanceName()
		{
			return m_instanceName.empty()? m_name: m_instanceName;
		}
		inline void SetDescription(const std::string& description)
		{
			m_description = description;
		}
		inline std::string GetDescription()
		{
			return m_description;
		}
		void PushToOutput(SESSION_ID sessionId,int outputIndex, X::Value data);
		void BreakConnection(std::string outputPinName);
		virtual bool ReceiveData(SESSION_ID sessionId,int inputIndex, X::Value& data) = 0;
		virtual void Stop() = 0;
		virtual bool Run() = 0;
		virtual X::Value Clone() = 0;

		int GetOutputIndex(const std::string& pinName)
		{
			m_locker.Lock();
			for (size_t i = 0; i < m_outputs.size(); ++i)
			{
				if (m_outputs[i].name == pinName)
				{
					m_locker.Unlock();
					return (int)i;
				}
			}
			m_locker.Unlock();
			return -1;
		}
		int GetInputIndex(const std::string& pinName)
		{
			m_locker.Lock();
			for (size_t i = 0; i < m_inputs.size(); ++i)
			{
				if (m_inputs[i].name == pinName)
				{
					m_locker.Unlock();
					return (int)i;
				}
			}
			m_locker.Unlock();
			return -1;
		}
		inline bool InGraph()
		{
			return m_agentGraph != nullptr;
		}
		void SetAgentGraph(AgentGraph* agentGraph);
		inline X::Value GetGraph()
		{
			return m_varGraph;
		}
		inline X::Value GetInputs()
		{
			m_locker.Lock();
			X::List list;
			for (auto& pin : m_inputs)
			{
				X::Dict dict;
				dict->Set("name",pin.name);
				X::List formats;
				for (auto& format : pin.formats)
				{
					formats += format;
				}
				dict->Set("formats",formats);
				list += dict;
			}
			m_locker.Unlock();
			return list;
		}

		inline virtual void SetInputs(X::Value v)
		{
			m_locker.Lock();
			X::List list(v);
			m_inputs.clear();
			for (size_t i = 0; i < (size_t)list.Size(); ++i)
			{
				auto item = list[i];
				Pin pin;
				pin.name = item["name"].ToString();
				X::Value varFormats = item["formats"];
				if (varFormats.IsList())
				{
					X::List formats(varFormats);
					for (auto format : *formats)
					{
						pin.formats.push_back(format.ToString());
					}
				}
				else
				{
					pin.formats.push_back(varFormats.ToString());
				}
				m_inputs.push_back(pin);
			}
			m_locker.Unlock();
		}

		inline X::Value GetOutputs()
		{
			m_locker.Lock();
			X::List list;
			for (auto& pin : m_outputs)
			{
				X::Dict dict;
				dict->Set("name", pin.name);
				X::List formats;
				for (auto& format : pin.formats)
				{
					formats += format;
				}
				dict->Set("formats", formats);
				list += dict;
			}
			m_locker.Unlock();
			return list;
		}

		inline void SetOutputs(X::Value v)
		{
			m_locker.Lock();
			X::List list(v);
			m_outputs.clear();
			for (auto item : *list)
			{
				Pin pin;
				pin.name = item["name"].ToString();
				X::Value varFormats = item["formats"];
				if (varFormats.IsList())
				{
					X::List formats(varFormats);
					for (auto format : *formats)
					{
						pin.formats.push_back(format.ToString());
					}
				}
				else
				{
					pin.formats.push_back(varFormats.ToString());
				}
				m_outputs.push_back(pin);
			}
			m_locker.Unlock();
		}
	};
}
