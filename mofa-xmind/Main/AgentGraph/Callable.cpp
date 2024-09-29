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

#include "Callable.h"
#include "AgentGraph.h"
#include "xMindAPI.h"

namespace xMind
{
	std::atomic<unsigned long long> Callable::s_idCounter{ 1 };
	void Callable::Copy(Callable* other)
	{
		m_implObject = other->m_implObject;
		m_params = other->m_params;
		m_rt = other->m_rt;
		m_agentGraph = other->m_agentGraph;
		if (m_agentGraph)
		{
			auto* pXPack = AgentGraph::APISET().GetProxy(m_agentGraph);
			m_varGraph = X::Value(pXPack);
		}
		m_name = other->m_name;
		m_description = other->m_description;
		m_type = other->m_type;
		m_inputs = other->m_inputs;
		m_outputs = other->m_outputs;
	}
	void Callable::PushEvent(int inputIndex, X::Value data)
	{
		MindAPISet::I().PushEvent(m_ID, inputIndex, data);
	}
	void Callable::SetAgentGraph(AgentGraph* agentGraph)
	{
		m_agentGraph = agentGraph;
		auto* pXPack = AgentGraph::APISET().GetProxy(m_agentGraph);
		m_varGraph = X::Value(pXPack);
	}
	void Callable::PushToOutput(SESSION_ID sessionId,int outputIndex, X::Value data)
	{
		if (m_agentGraph)
		{
			m_agentGraph->PushDataToCallable(this, sessionId,outputIndex, data);
		}
	}
	void Callable::BreakConnection(std::string outputPinName)
	{
		int outputPinIndex = GetOutputIndex(outputPinName);
		if (outputPinIndex < 0)
		{
			//if not found, LLM make errors
			std::vector<int> loopBackOutputPins;
			bool isTerminalNode = m_agentGraph->IsTerminalNodeWithLoopBackConnections(this,
				loopBackOutputPins);
			if (isTerminalNode)
			{
				for (auto outputPinIndex : loopBackOutputPins)
				{
					m_agentGraph->BreakConnection(this, outputPinIndex);
				}
			}
		}
		else if (m_agentGraph)
		{
			m_agentGraph->BreakConnection(this, outputPinIndex);
		}
	}
}