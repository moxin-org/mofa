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
#include <vector>
#include <unordered_map>
#include <string>
#include "singleton.h"
#include "Callable.h"
#include "AgentGraph.h"
#include "Locker.h"
#include "port.h"

namespace xMind
{
	//Module has name(treat as alias),
	//blueprint is a yaml description file
	//and a few codebehind can be python(.py) or xlang(.x) and shared lib(.so/.dll/.dylib)
	//mapCallables is a map with callable name as key

	//the Relationship between blueprint and codebehind is one to many

	struct ModuleInfo
	{
		std::string moduleName;
		std::string blueprint;
		std::vector<std::string> codebehinds;
		std::unordered_map<std::string, X::Value> mapCallables;
	};

	class NodeManager : public Singleton<NodeManager>
	{
		Locker m_lock;
		std::unordered_map<int, ModuleInfo> m_modules; // Map with ModuleId as key
		std::vector<X::Value> m_graphs;
		int m_nextModuleId = 1; // To auto-increment ModuleId

	public:
		NodeManager() = default;
		~NodeManager() = default;

		// Register a Module and return its ModuleId
		int RegisterModule(const std::string& moduleName, const std::string& blueprintFilePath)
		{
			AutoLock lock(m_lock);

			// Check if the module with the same file path already exists
			for (const auto& [id, module] : m_modules)
			{
				if (module.blueprint == blueprintFilePath)
				{
					return id; // Return existing ModuleId if found
				}
			}

			// Create a new ModuleInfo and insert into map with a new ModuleId
			ModuleInfo moduleInfo;
			moduleInfo.moduleName = moduleName;
			moduleInfo.blueprint = blueprintFilePath;
			int moduleId = m_nextModuleId++;
			m_modules[moduleId] = moduleInfo;

			return moduleId; // Return the new ModuleId
		}

		void SetCodebehinds(int moduleId, const std::vector<std::string>& codebehinds)
		{
			AutoLock lock(m_lock);

			// Find the module by ModuleId
			auto it = m_modules.find(moduleId);
			if (it != m_modules.end())
			{
				it->second.codebehinds = codebehinds;
			}
		}
		// Old addCallable method
		bool addCallable(const std::string& moduleName,
			const std::string& moduleFilePath,
			const std::string& name, X::Value& callable)
		{
			// First, register the module (or find its existing ModuleId)
			int moduleId = RegisterModule(moduleName, moduleFilePath);

			// Then, use the moduleId to add the callable
			return addCallable(moduleId, name, callable);
		}

		// New addCallable method with ModuleId
		bool addCallable(int moduleId, const std::string& name, X::Value& callable)
		{
			AutoLock lock(m_lock);

			// Find the module by ModuleId
			auto it = m_modules.find(moduleId);
			if (it == m_modules.end())
			{
				return false; // ModuleId not found
			}

			ModuleInfo& moduleInfo = it->second;

			// Check if mapCallables has the same name
			if (moduleInfo.mapCallables.find(name) != moduleInfo.mapCallables.end())
			{
				return false; // Callable with the same name already exists
			}

			// Add the callable to the map
			moduleInfo.mapCallables[name] = callable;
			return true;
		}

		// Old queryCallable method
		X::Value queryCallable(const std::string& moduleName, const std::string& name)
		{
			AutoLock lock(m_lock);

			// Find the module by name and get its ModuleId
			int moduleId = -1;
			for (const auto& [id, module] : m_modules)
			{
				if (module.moduleName == moduleName)
				{
					moduleId = id;
					break;
				}
			}

			if (moduleId != -1)
			{
				// Use the ModuleId to query the callable
				return queryCallable(moduleId, name);
			}

			return X::Value(); // Return empty X::Value if not found
		}

		// New queryCallable method with ModuleId
		X::Value queryCallable(int moduleId, const std::string& name)
		{
			AutoLock lock(m_lock);

			// Find the module by ModuleId
			auto it = m_modules.find(moduleId);
			if (it != m_modules.end())
			{
				auto it2 = it->second.mapCallables.find(name);
				if (it2 != it->second.mapCallables.end())
				{
					return it2->second;
				}
			}
			return X::Value(); // Return empty X::Value if not found
		}

		void AddGraph(X::Value& graph)
		{
			m_lock.Lock();
			m_graphs.push_back(graph);
			m_lock.Unlock();
		}

		// Build JSON representation of the graph
		std::string BuildGraphAsJson()
		{
			const int online_len = 20;
			char convertBuf[online_len];

			X::List listNodes;
			// Collect all callables with module names
			for (const auto& [id, module] : m_modules)
			{
				for (const auto& it : module.mapCallables)
				{
					X::XPackageValue<Callable> varCallable(it.second);
					Callable* callable = (Callable*)varCallable.GetRealObj();
					if (!callable)
					{
						continue;
					}
					X::Dict dict;
					dict->Set("moduleName", (std::string)module.moduleName);
					dict->Set("blueprint", (std::string)module.blueprint);
					dict->Set("name", callable->GetName());
					dict->Set("instanceName", callable->GetInstanceName());
					dict->Set("type", static_cast<int>(callable->Type()));
					dict->Set("id", callable->ID());
					dict->Set("inputs", callable->GetInputs());
					dict->Set("outputs", callable->GetOutputs());
					listNodes += dict;
				}
			}

			X::Dict graphDict;
			for (auto& graph : m_graphs)
			{
				if (!graph.IsObject())
				{
					continue;
				}
				X::XPackageValue<AgentGraph> varGraph(graph);
				AgentGraph* pGraph = (AgentGraph*)varGraph.GetRealObj();
				auto graphId = pGraph->ID();
				// Collect all connections
				X::List connList;
				for (const auto& connection : pGraph->GetConnections())
				{
					X::Dict oneConn;
					oneConn->Set("fromCallableId", connection.fromCallableId);
					oneConn->Set("fromPinIndex", connection.fromPinIndex);
					oneConn->Set("toCallableId", connection.toCallableId);
					oneConn->Set("toPinIndex", connection.toPinIndex);
					connList += oneConn;
				}

				SPRINTF(convertBuf, online_len, "%llu", graphId);
				std::string graphIdStr = convertBuf;
				X::Value graphIdValue(graphIdStr);
				graphDict->Set(graphIdValue, connList);
			}
			X::Dict all;
			all->Set("Nodes", listNodes);
			all->Set("Graphs", graphDict);
			std::string graphJson = all->ToString(true);
			return graphJson;
		}
	}; // class NodeManager
} // namespace xMind

