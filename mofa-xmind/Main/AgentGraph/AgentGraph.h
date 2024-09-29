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

#include "Callable.h"
#include "Locker.h"
#include "xpackage.h"
#include <unordered_map>
#include <vector>
#include <memory>
#include <condition_variable> 
#include "type_def.h"

namespace xMind
{
	struct Connection
	{
		unsigned long long fromCallableId;
		int fromPinIndex;
		unsigned long long toCallableId;
		int toPinIndex;
		bool connected;//if disconnected, set to false
	};
	struct CallableInfo
	{
		Callable* callable;
		X::Value varCallable;
	};
	struct SessionData
	{
		Callable* callable;
		int outputIndex;
		X::Value data;
		unsigned long iterationCount;
	};
	class AgentGraph
	{
		BEGIN_PACKAGE(AgentGraph)
			APISET().AddVarFunc("addNode", &AgentGraph::AddNode);
			APISET().AddFunc<1>("removeNode", &AgentGraph::RemoveCallable);
			APISET().AddVarFunc("connect", &AgentGraph::AddConnection);
			APISET().AddFunc<4>("disconnect", &AgentGraph::RemoveConnection);
			APISET().AddVarFunc("run", &AgentGraph::Run);
			APISET().AddVarFunc("startOnce", &AgentGraph::StartOnce);
			APISET().AddVarFunc("startFrom", &AgentGraph::StartFrom);
			APISET().AddVarFunc("isRunning", &AgentGraph::IsRunning);
			APISET().AddFunc<0>("stop", &AgentGraph::Stop);
			APISET().AddFunc<0>("waitToStop", &AgentGraph::WaitToStop);
		END_PACKAGE
	public:
		AgentGraph() :
			m_ID(++s_idCounter)
		{

		}
		~AgentGraph();

		bool AddNode(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
		unsigned long long AddCallable(X::Value& varCallable, Callable* callable = nullptr);
		void RemoveCallable(int index);
		void AddConnection(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
		void RemoveConnection(const std::string& fromInstanceName, const std::string& fromPinName, const std::string& toInstanceName, const std::string& toPinName);
		void PushDataToCallable(Callable* fromCallable, SESSION_ID sessionId,int outputIndex, X::Value& data);
		bool Run(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
		bool StartOnce(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
		bool StartFrom(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
		void Stop()
		{
			std::unique_lock<std::mutex> lock(m_mutex);
			m_running = false;
			m_condVar.notify_all(); // Notify all waiting threads
		}
		bool IsRunning(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
		{
			int timeout = 0;
			if (params.size() > 0)
			{
				timeout = (int)params[0];
			}
			else
			{
				auto it = kwParams.find("timeout");
				if (it)
				{
					timeout = (int)it->val;
				}
			}
			std::unique_lock<std::mutex> lock(m_mutex);

			if (timeout == 0)
			{
				retValue = int(m_running ? Status::Running : Status::Stopped);
			}
			else
			{
				bool bRun = m_condVar.wait_for(lock, std::chrono::milliseconds(timeout), [this] {
					return m_running ? true : false;
					});
				retValue = int(bRun ? Status::Running : Status::Stopped);
			}
			return true;
		}
		void WaitToStop()
		{
			std::unique_lock<std::mutex> lock(m_mutex);
			m_condVar.wait(lock, [this] { return !m_running; });
			for(auto& info : m_callables)
			{
				info.callable->Stop();
			}
		}
		inline unsigned long long ID()
		{
			return m_ID;
		}
		inline std::vector<Connection>& GetConnections()
		{
			return m_connections;
		}
		inline Callable* GetCallableByIndex(int idx)
		{
			return m_callables[idx].callable;
		}
		X::Value RunInputs(SESSION_ID sid,X::Value& inputs);
		Callable* FindCallable(unsigned long long id)
		{
			AutoLock lock(m_locker);
			for (auto& info : m_callables)
			{
				if (info.callable->ID() == id)
				{
					return info.callable;
				}
			}
			return nullptr;
		}
		void BreakConnection(Callable* pFromCallable, int outputPinIndex)
		{
			AutoLock lock(m_locker);
			for (auto& connection : m_connections)
			{
				if (connection.fromCallableId == pFromCallable->ID()
					&& connection.fromPinIndex == outputPinIndex)
				{
					connection.connected = false;
					break;
				}
			}
		}
		bool AgentGraph::IsTerminalNodeWithLoopBackConnections(Callable* pCallable, 
			std::vector<int>& loopBackOutputPins)
		{
			loopBackOutputPins.clear(); // Clear the output list to start fresh
			bool hasDownstreamConnections = false;

			AutoLock lock(m_locker); // Lock for thread safety

			// Iterate through all connections in the graph
			for (const auto& connection : m_connections)
			{
				// Check if this callable has an output connection
				if (connection.fromCallableId == pCallable->ID())
				{
					Callable* downstreamCallable = FindCallable(connection.toCallableId);

					if (downstreamCallable)
					{
						// Check if this downstream node eventually loops back to pCallable
						if (HasLoopBackToCallable(downstreamCallable, pCallable))
						{
							// Add this output index to the list of loop-back connections
							loopBackOutputPins.push_back(connection.fromPinIndex);
						}
						else
						{
							// If we find a downstream node that does not loop back, it's not terminal
							hasDownstreamConnections = true;
						}
					}
				}
			}

			// If we found no downstream connections except for loop-backs, this node is terminal
			return !hasDownstreamConnections;
		}

		bool AgentGraph::IsTerminalNode(Callable* pCallable)
		{
			AutoLock lock(m_locker); // Lock for thread safety

			// Iterate through all connections in the graph
			for (const auto& connection : m_connections)
			{
				// If this callable has an output connection
				if (connection.fromCallableId == pCallable->ID())
				{
					Callable* downstreamCallable = FindCallable(connection.toCallableId);

					if (downstreamCallable)
					{
						// Check if this downstream node is just part of a loop-back connection
						if (!HasLoopBackToCallable(downstreamCallable, pCallable))
						{
							// If the downstream callable does NOT loop back to pCallable, this means it has a real downstream node
							return false; // This node is not terminal
						}
					}
				}
			}

			// If no downstream connections were found (except loop-back), it's a terminal node
			return true;
		}

		std::vector<int> FindLoopBackConnectionsForCallable(Callable* pCallable)
		{
			std::vector<int> loopBackOutputPins;
			AutoLock lock(m_locker); // Lock for thread safety

			// Iterate through all the output pins of the given callable
			for (const auto& connection : m_connections)
			{
				if (connection.fromCallableId == pCallable->ID())
				{
					// This is an output from pCallable, now find the downstream node
					Callable* downstreamCallable = FindCallable(connection.toCallableId);

					if (downstreamCallable)
					{
						// Check if this downstream node (or its downstream nodes) eventually loops back to pCallable
						if (HasLoopBackToCallable(downstreamCallable, pCallable))
						{
							loopBackOutputPins.push_back(connection.fromPinIndex);
						}
					}
				}
			}

			return loopBackOutputPins;
		}

	private:
		bool HasLoopBackToCallable(Callable* currentCallable, Callable* targetCallable)
		{
			// Base case: if the current node is the target callable, we have a loop-back
			if (currentCallable->ID() == targetCallable->ID())
			{
				return true;
			}

			// Otherwise, explore the downstream connections of the current node
			for (const auto& connection : m_connections)
			{
				if (connection.fromCallableId == currentCallable->ID())
				{
					Callable* downstreamCallable = FindCallable(connection.toCallableId);
					if (downstreamCallable && HasLoopBackToCallable(downstreamCallable, targetCallable))
					{
						return true; // We found a loop-back path
					}
				}
			}

			return false; // No loop-back found
		}

		std::vector<std::pair<Callable*, int>> AgentGraph::GetNodesWithUnconnectedOutputPins() 
		{
			std::vector<std::pair<Callable*, int>> nodesWithUnconnectedOutputPins;
			AutoLock lock(m_locker); // Lock for thread safety

			for (auto& info : m_callables) {
				Callable* callable = info.callable;
				int outputPinCount = (int)callable->GetOutputs().size();
				bool hasUnconnectedOutputPin = false;

				for (int i = 0; i < outputPinCount; ++i) {
					bool isConnected = false;
					for (const auto& connection : m_connections) {
						if (connection.fromCallableId == callable->ID() && connection.fromPinIndex == i) {
							isConnected = true;
							break;
						}
					}
					if (!isConnected) {
						nodesWithUnconnectedOutputPins.push_back(std::make_pair(callable, i));
						hasUnconnectedOutputPin = true;
						break;
					}
				}
			}

			return nodesWithUnconnectedOutputPins;
		}

		std::vector<std::pair<Callable*, int>> AgentGraph::GetNodesWithUnconnectedInputPins() 
		{
			std::vector<std::pair<Callable*, int>> nodesWithUnconnectedInputPins;
			AutoLock lock(m_locker); // Lock for thread safety

			for (auto& info : m_callables) {
				Callable* callable = info.callable;
				int inputPinCount = (int)callable->GetInputs().size();

				for (int i = 0; i < inputPinCount; ++i) {
					bool isConnected = false;
					for (const auto& connection : m_connections) {
						if (connection.toCallableId == callable->ID() && connection.toPinIndex == i) {
							isConnected = true;
							break;
						}
					}
					if (!isConnected) {
						nodesWithUnconnectedInputPins.push_back(std::make_pair(callable, i));
						break; // Only add the first unconnected input pin
					}
				}
			}

			return nodesWithUnconnectedInputPins;
		}

		void RunAllCallables(X::XRuntime* rt0 = nullptr);

		Callable* FindCallable(const std::string& instanceName)
		{
			AutoLock lock(m_locker);
			for (auto& info : m_callables)
			{
				if (info.callable->GetInstanceName() == instanceName)
				{
					return info.callable;
				}
			}
			return nullptr;
		}
		static std::atomic<unsigned long long> s_idCounter;
		unsigned long long m_ID;
		bool m_running = false;
		std::vector<CallableInfo> m_callables;
		std::vector<Connection> m_connections;
		Locker m_locker;
		std::mutex m_mutex; // Mutex for condition variable
		std::condition_variable m_condVar; // Condition variable

		//Session Data
		std::unordered_map<SESSION_ID, std::vector<SessionData>> m_sessionData;
		std::condition_variable m_sessionDataCondVar;
		std::mutex m_sessionDataMutex;
		void AddSessionData(SESSION_ID sessionId, Callable* pCallable, int outputIndex,X::Value& data);
	};
}
