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

#include "AgentGraph.h"
#include <iostream>
#include "xlang.h"
#include "xMindAPI.h"
#include "BaseAgent.h"

namespace xMind
{
	std::atomic<unsigned long long> AgentGraph::s_idCounter{ 0 };
	AgentGraph::~AgentGraph()
	{
		for (auto& info : m_callables)
		{
			delete info.callable;
		}
		m_callables.clear();
	}

	bool AgentGraph::AddNode(X::XRuntime* rt, X::XObj* pContext,
		X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
	{
		X::Value varObj;
		if (params.size() >= 1)
		{
			varObj = params[0];
		}
		else
		{
			retValue = X::Value(false);
			return false;
		}

		X::XPackageValue<Callable> varCallable(varObj);
		Callable* callable = (Callable*)varCallable.GetRealObj();
		//check if callable exists in Graph, if exists, clone a new one
		if (callable->InGraph())
		{
			X::Value cloneCallable = callable->Clone();
			X::XPackageValue<Callable> varCallableClone(cloneCallable);
			callable = (Callable*)varCallableClone.GetRealObj();
		}
		if (params.size() >= 2)
		{
			callable->SetInstanceName(params[1].ToString());
		}
		AddCallable(varObj, callable);
		retValue = X::Value(true);
		return true;
	}

	unsigned long long AgentGraph::AddCallable(X::Value& varCallable, Callable* callable)
	{
		if (callable == nullptr)
		{
			X::XPackageValue<Callable> packObj(varCallable);
			callable = packObj.GetRealObj();
		}
		auto id = callable->ID();
		AutoLock lock(m_locker); // Lock for thread safety
		for (auto& info : m_callables)
		{
			if (info.callable->ID() == id)
			{
				return id;
			}
		}
		m_callables.push_back({ callable,varCallable });
		callable->SetAgentGraph(this);
		return id;
	}

	void AgentGraph::RemoveCallable(int id)
	{
		AutoLock lock(m_locker); // Lock for thread safety

		for (auto& callInfo : m_callables)
		{
			if (callInfo.callable->ID() == id)
			{
				delete callInfo.callable;
				callInfo.callable = nullptr;
				callInfo.varCallable.Clear();
				break;
			}
		}
	}

	void AgentGraph::AddConnection(X::XRuntime* rt, X::XObj* pContext,
		X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
	{
		unsigned long long fromCallableId = 0;
		unsigned long long toCallableId = 0;
		int fromPinIndex=-1;
		int toPinIndex=-1;
		if (params.size() == 2)
		{
			auto fromInstanceName = params[0].ToString();
			auto toInstanceName = params[1].ToString();
			Callable* fromCallable = FindCallable(fromInstanceName);
			Callable* toCallable = FindCallable(toInstanceName);
			if (fromCallable == nullptr || toCallable == nullptr)
			{
				retValue = X::Value(false);
				return;
			}
			fromCallableId = fromCallable->ID();
			toCallableId = toCallable->ID();
		}
		else if (params.size() == 4)
		{
			auto fromInstanceName = params[0].ToString();
			auto fromPinName = params[1].ToString();
			auto toInstanceName = params[2].ToString();
			auto toPinName = params[3].ToString();
			Callable* fromCallable = FindCallable(fromInstanceName);
			Callable* toCallable = FindCallable(toInstanceName);
			if (fromCallable == nullptr || toCallable == nullptr)
			{
				retValue = X::Value(false);
				return;
			}
			fromCallableId = fromCallable->ID();
			toCallableId = toCallable->ID();
			fromPinIndex = fromCallable->GetOutputIndex(fromPinName);
			toPinIndex = toCallable->GetInputIndex(toPinName);
		}
		if(fromPinIndex == -1 || toPinIndex == -1)
		{
			retValue = X::Value(false);
			return;
		}
		AutoLock lock(m_locker);
		Connection newConnection{ fromCallableId, fromPinIndex, toCallableId, toPinIndex,true};
		m_connections.push_back(newConnection);
		retValue = X::Value(true);
	}

	void AgentGraph::RemoveConnection(const std::string& fromInstanceName, const std::string& fromPinName, const std::string& toInstanceName, const std::string& toPinName)
	{
		Callable* fromCallable = FindCallable(fromInstanceName);
		Callable* toCallable = FindCallable(toInstanceName);
		int fromPinIndex = fromCallable->GetOutputIndex(fromPinName);
		int toPinIndex = toCallable->GetInputIndex(toPinName);
		AutoLock lock(m_locker); // Lock for thread safety

		for (auto it = m_connections.begin(); it != m_connections.end(); ++it)
		{
			if (it->fromCallableId == fromCallable->ID() &&
				it->fromPinIndex == fromPinIndex &&
				it->toCallableId == toCallable->ID() &&
				it->toPinIndex == toPinIndex)
			{
				m_connections.erase(it);
				break;
			}
		}
	}

	void AgentGraph::PushDataToCallable(Callable* fromCallable, 
		SESSION_ID sessionId,int outputIndex, X::Value& data)
	{
		AutoLock lock(m_locker);
		if (!m_running)
		{
			return;
		}
		auto fromCallableId = fromCallable->ID();
		bool hasReceiver = false;
		for (const auto& connection : m_connections)
		{
			if (connection.connected && connection.fromCallableId == fromCallableId
				&& connection.fromPinIndex == outputIndex)
			{
				Callable* toCallable = FindCallable(connection.toCallableId);
				toCallable->SetRT(fromCallable->GetRT());
				toCallable->ReceiveData(sessionId,connection.toPinIndex, data);
				hasReceiver = true;
			}
		}
		if (!hasReceiver)
		{//cache to quque for each session
			AddSessionData(sessionId, fromCallable,outputIndex, data);
		}
	}
	bool AgentGraph::Run(X::XRuntime* rt, X::XObj* pContext, 
		X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
	{
		RunAllCallables(rt);
		return true;
	}
	bool AgentGraph::StartOnce(X::XRuntime* rt, X::XObj* pContext, 
		X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
	{
		AutoLock lock(m_locker);
		m_running = true;
		auto& startNodes = GetNodesWithUnconnectedInputPins();
		//call each with ReceiveData
		for (const auto& it : startNodes)
		{
			X::Value dummyData;
			auto* pCallable = it.first;
			pCallable->SetRT(rt);
			//TODO: sessionId  need to set
			SESSION_ID sessionId = 0;
			pCallable->ReceiveData(sessionId, it.second, dummyData);
		}
		return true;
	}
	bool AgentGraph::StartFrom(X::XRuntime* rt, X::XObj* pContext, 
		X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
	{
		AutoLock lock(m_locker);
		m_running = true;
		//for each Callable inside params, call ReceiveData
		X::Value dummyData;
		for (auto& param : params)
		{
			std::string instanceName = param.ToString();
			auto* pCallable = FindCallable(instanceName);
			if (pCallable)
			{
				pCallable->SetRT(rt);
				//TODO: sessionId  need to set
				SESSION_ID sessionId = 0;
				pCallable->ReceiveData(sessionId,0, dummyData);
			}
		}
		return true;
	}
	X::Value AgentGraph::RunInputs(SESSION_ID sid, X::Value& inputs)
	{
		m_locker.Lock();
		if (!m_running)
		{
			m_locker.Unlock();
			RunAllCallables();
		}
		else
		{
			m_locker.Unlock();
		}
		auto& startNodes = GetNodesWithUnconnectedInputPins();

		for (const auto& startNode : startNodes)
		{
			X::Value dummyData;
			auto* pCallable = startNode.first;
			if (pCallable)
			{
				pCallable->SetRT(xMind::MindAPISet::I().RT());
				LOG5 << "Put inputs:" << inputs.ToString() << "To:" << pCallable->GetInstanceName()<<LINE_END;
				pCallable->ReceiveData(sid, 0, inputs);
			}
		}

		//check sessionData for this SessionID
		{
			std::unique_lock<std::mutex> lock(m_sessionDataMutex);
			auto it = m_sessionData.find(sid);
			if (it != m_sessionData.end())
			{
				if (it->second.size() > 0)
				{
					X::Value retData = it->second[0].data;
					it->second.erase(it->second.begin());
					return retData;
				}
			}
			m_sessionDataCondVar.wait(lock, [this, sid] {
				auto it = m_sessionData.find(sid);
				if (it != m_sessionData.end())
				{
					return it->second.size() > 0;
				}
				return false;
				});
			it = m_sessionData.find(sid);
			if (it != m_sessionData.end())
			{
				if (it->second.size() > 0)
				{
					X::Value retData = it->second[0].data;
					it->second.erase(it->second.begin());
					return retData;
				}
			}
		}

		return X::Value();
	}
	void AgentGraph::RunAllCallables(X::XRuntime* rt)
	{
		if (rt == nullptr)
		{
			rt = xMind::MindAPISet::I().RT();
		}
		m_locker.Lock();
		m_running = true;
		//call run all Callables
		for (auto& info : m_callables)
		{
			info.callable->SetRT(rt);
			info.callable->Run();
		}
		m_locker.Unlock();
	}

	//when AddSessionData Called, the pass in sessionId
	//will include valid input index and loop count
	//but the wait side will not use loop count,so we move loop count to
	// SessionData
	void AgentGraph::AddSessionData(SESSION_ID sessionId, Callable* pCallable,
		int outputIndex,X::Value& data)
	{
		SessionIDInfo idInfo = FromSessionID(sessionId);
		SessionData sessionData{ pCallable ,outputIndex ,data,idInfo.iterationCount };
		idInfo.iterationCount = 0;
		SESSION_ID sessionIdNoIt = ToSessionID(idInfo);
		std::lock_guard<std::mutex> lock(m_sessionDataMutex);
		m_sessionData[sessionIdNoIt].push_back(sessionData);
		m_sessionDataCondVar.notify_all();
	}
}