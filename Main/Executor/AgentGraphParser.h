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
#include "Callable.h"
#include "BaseAction.h"
#include "BaseAgent.h"
#include "NodeManager.h"
#include "varible.h"
#include "LlmPool.h"

//use this for agent no module name
#define NO_MODULE_NAME "module"
#define keystore_tag "$keystore$"

namespace xMind
{
    struct GroupInfo {
        std::string name;
        std::vector<std::string> agents;
    };
    struct ConnectionInfo {
        std::string fromNodeName;
        std::string fromPinName;
        std::string toNodeName;
        std::string toPinName;
    };
    struct Group {
        std::string name;
        std::vector<std::string> agents;
    };
    // Parser class definition
    class Parser
    {
        //for example: Bearer ${openai_key}
		//replace the ${var} with the value of varible's value
        std::string RepVar(const std::string& input, const std::string& moduleName)
        {
            std::string result = input;
            std::regex varPattern(R"(\$\{([^\}]+)\})");
            std::smatch matches;

            while (std::regex_search(result, matches, varPattern))
            {
                std::string varName = matches[1].str();
                X::Value replacement;

                // Check if the variable name contains a scope
                size_t pos = varName.find("::");
                if (pos != std::string::npos)
                {
                    replacement = VariableManager::I().Query(varName);
                }
                else
                {
                    replacement = VariableManager::I().Query(moduleName, varName);
                }
                if (replacement.IsValid())
                {
                    result.replace(matches.position(0), matches.length(0), replacement.ToString());
                }
            }

            return result;
        }
    public:
        // Function to parse imports
        bool ParseImports(const std::string& curModuleName, 
            std::string& curModule_FileName,
            const X::Value& importsValue)
        {
            if (!importsValue.IsList())
            {
                return false;
            }
            X::List list(importsValue);
            for (const auto item : *list)
            {
                X::Dict importItem(item);
                auto fileName = RepVar(importItem["file"].ToString(),curModuleName);
                auto alias = RepVar(importItem["alias"].ToString(), curModuleName);
				if (alias.empty())
				{
					//use the file name exclude the extension as the alias
					size_t pos = fileName.find_last_of('.');
					if (pos != std::string::npos)
					{
						alias = fileName.substr(0, pos);
					}
                    else
                    {
                        alias = fileName;
                    }
				}
                // Check if fileName is an absolute path
                std::filesystem::path filePath(fileName);
                if (!filePath.is_absolute())
                {
                    // If not absolute, construct the absolute path using curModule_FileName's directory
                    std::filesystem::path modulePath(curModule_FileName);
                    filePath = modulePath.parent_path() / fileName;
                    fileName = filePath.string();
                }
				// Parse the file
				ParseAgentGraphDesc(alias, fileName);
            }
            return true;
        }
        bool ParsePrompts(BaseAgent* pAgent,const std::string& curModuleName, X::Value& prompts)
        {
            if (prompts.IsList())
            {
                X::List promptList(prompts);
                for (const auto prompt : *promptList)
                {
                    X::Dict promptDict(prompt);
                    std::string name = RepVar(promptDict["name"].ToString(), curModuleName);
                    std::string role = RepVar(promptDict["role"].ToString(), curModuleName);
                    std::string content = RepVar(promptDict["content"].ToString(), curModuleName);
					//todo: we skip name now
					pAgent->AddPrompt(role, content);
                }
            }
            return true;
        }
        bool ParseCodebehinds(const std::string& curModuleName, 
            const std::string& curModule_FileName, 
            X::Value& root, std::vector<std::string>& codebehindList)
        {
            X::Dict rootDict(root);
            // Parse variables
            X::Value codebehind = rootDict["codebehinds"];
            if (codebehind.IsList())
            {
                X::List varList(codebehind);
                for (const auto var : *varList)
                {
                    X::Dict varDict(var);
                    std::string fileName = varDict["file"].ToString();
                    fileName = RepVar(fileName, curModuleName);
                    // Check if fileName is an absolute path
                    std::filesystem::path filePath(fileName);
                    if (!filePath.is_absolute())
                    {
                        // If not absolute, construct the absolute path using curModule_FileName's directory
                        std::filesystem::path modulePath(curModule_FileName);
                        filePath = modulePath.parent_path() / fileName;
                        fileName = filePath.string();
						codebehindList.push_back(fileName);
                    }
                }
            }
            return true;
        }
        std::string QueryKeyStore(std::string key);
        bool ParseVariables(const std::string& curModuleName, X::Value& root)
        {
            X::Dict rootDict(root);
            // Parse variables
            X::Value variables = rootDict["varibles"];
            if (variables.IsList())
            {
                X::List varList(variables);
                for (const auto var : *varList)
                {
                    X::Dict varDict(var);
					//name can't use ${} inside
                    std::string name = varDict["name"].ToString();
                    X::Value value = varDict["value"];
                  
                    if (value.IsString() || value.IsObject() && value.GetObj()->GetType() == X::ObjType::Str)
                    {
						std::string strValue = RepVar(value.ToString(), curModuleName);
                        if (strValue == keystore_tag)
                        {
                            strValue = QueryKeyStore(name);
                        }
                        value = strValue;
                    }
                    std::string description = RepVar(varDict["description"].ToString(),curModuleName);
                    VariableManager::I().Add(curModuleName, name, description, value);
                }
            }
            return true;
        }
        bool ParseLlmPool(const std::string& curModuleName, X::Value& root)
        {
            X::Dict rootDict(root);
            // Parse LLM pool
            X::Value llmPool = rootDict["llm_pool"];
            if (llmPool.IsList())
            {
                X::List llmList(llmPool);
                for (const auto llm : *llmList)
                {
                    X::Dict llmDict(llm);
                    std::string name = RepVar(llmDict["name"].ToString(),curModuleName);
                    std::string tag = RepVar(llmDict["tag"].ToString(),curModuleName);
                    std::string contentType = RepVar(llmDict["content_type"].ToString(),curModuleName);
                    std::string url = RepVar(llmDict["url"].ToString(),curModuleName);
                    X::Dict headers0 = llmDict["headers"];
                    X::Dict headers;
					//for headers, need to check if need call RepVar with value is string
                    headers0->Enum([&](const std::string& key, X::Value& value)
                        {
                            if (value.IsString())
                            {
                                value = RepVar(value.ToString(), curModuleName);
                                X::Value valKey(key);
                                headers->Set(valKey, value);
                            }
                            else
                            {
								headers->Set(key.c_str(), value);
                            }
                        }
                    );
					LlmPool::I().Add(name,url,tag, contentType,headers);
                }
            }
            return true;
        }
        X::Value QueyNode(const std::string& curModuleName,std::string combineName)
        {
			std::string moduleName;
			std::string callableName;
            size_t pos = combineName.find('.');
            if (pos != std::string::npos)
            {
                moduleName = combineName.substr(0, pos);
                callableName = combineName.substr(pos + 1);
            }
            else
            {//if no module prefix use current module name
                moduleName = curModuleName;
                callableName = combineName;
            }
            //check from NodeManager to find the callable with the name
            return NodeManager::I().queryCallable(moduleName, callableName);
        }
        // Function to parse agents/actions/functions
        bool ParseNodes(X::Value& firstAgent,const X::Value& nodesValue,
            const std::string& moduleName, const std::string& fileName);
        // Function to parse connections
        std::vector<ConnectionInfo> ParseConnections(const X::Value& connectionsValue)
        {
            std::vector<ConnectionInfo> connections;
            if (connectionsValue.IsList())
            {
				X::List list(connectionsValue);
                for (const auto item : *list)
                {
					X::Dict connectionItem(item);
                    ConnectionInfo connection;
                    connection.fromNodeName = connectionItem["fromNodeName"].ToString();
                    connection.fromPinName = connectionItem["fromPinName"].ToString();
                    connection.toNodeName = connectionItem["toNodeName"].ToString();
                    connection.toPinName = connectionItem["toPinName"].ToString();
                    connections.push_back(connection);
                }
            }
            return connections;
        }

        // Function to parse groups
        std::vector<Group> ParseGroups(const X::Value& groupsValue)
        {
            std::vector<Group> groups;
            if (groupsValue.IsList())
            {
				X::List list(groupsValue);
                for (const auto item : *list)
                {
					X::Dict groupItem(item);
                    Group group;
                    group.name = groupItem["name"].ToString();

                    X::Value agentsValue = groupItem["agents"];
                    if (agentsValue.IsList())
                    {
						X::List agent_lists(agentsValue);
                        for (auto agentNameValue : *agent_lists)
                        {
							std::string name = agentNameValue.ToString();
                            group.agents.push_back(name);
                        }
                    }
                    groups.push_back(group);
                }
            }
            return groups;
        }
        //for top agent, if no connections, add one graph with first Agent
        bool ParseRootAgent(const std::string& fileName, X::Value& graph);
        // Main function to parse the agent graph description
        bool ParseAgentGraphDesc(const std::string& moduleName = "", const std::string& fileName = "");
        bool ParseAgentGraphDescFromString(const std::string& desc);
		bool ParseAgentGraphDescFromRoot(bool needCreateGraph,
            X::Value& agentGraph,X::Value& root,
            const std::string& moduleName, 
            const std::string& blueprintFileName)
        {
            // Check if root is a Dict
            if (!root.IsDict())
            {
                std::cerr << "Error: Invalid yaml format." << std::endl;
                return false;
            }
			std::string strModuleName = moduleName;

            // Extract basic information
            std::string name = root["name"].ToString();
            if (strModuleName.empty())
            {
                strModuleName = root["module"].ToString();
				// if no module name is provided,
				// use a default module name
				if (strModuleName.empty())
				{
					strModuleName = NO_MODULE_NAME;
				}
            }

            std::string type = root["type"].ToString();
            std::string version = root["version"].ToString();
            std::string description = RepVar(root["description"].ToString(),moduleName);

			int moduleId = NodeManager::I().RegisterModule(strModuleName, blueprintFileName);
			std::vector<std::string> codebehindList;
            ParseCodebehinds(strModuleName, blueprintFileName, root,codebehindList);
			NodeManager::I().SetCodebehinds(moduleId, codebehindList);

			ParseVariables(strModuleName, root);
			ParseLlmPool(strModuleName, root);
            // Process 'prompts' if any (assuming it's a list or dict)
            X::Value prompts = root["prompts"];
            // TODO: Process prompts as needed

            // Parse imports
            X::Value importsValue = root["imports"];
            ParseImports(moduleName, (std::string&)blueprintFileName,importsValue);

            // Parse agents/actions/functions
            X::Value nodesValue = root["nodes"];
			X::Value firstAgent;
            ParseNodes(firstAgent,nodesValue, moduleName, blueprintFileName);

            // Parse connections
            X::Value connectionsValue = root["connections"];
            std::vector<ConnectionInfo> connections = ParseConnections(connectionsValue);
            if (connections.size() > 0) 
            {
                X::XPackageValue<AgentGraph> packGraph;
                AgentGraph* graph = packGraph.GetRealObj();
                for (auto& connection : connections)
                {
                    //Add into Graph
                    X::Value CallableFrom = QueyNode(moduleName, connection.fromNodeName);
                    X::Value CallableTo = QueyNode(moduleName, connection.toNodeName);
                    if (!CallableFrom.IsObject() || !CallableTo.IsObject())
                    {
                        continue;
                    }
                    graph->AddCallable(CallableFrom);
                    graph->AddCallable(CallableTo);

                    X::ARGS params(4);
                    params.push_back(connection.fromNodeName);
                    params.push_back(connection.fromPinName);
                    params.push_back(connection.toNodeName);
                    params.push_back(connection.toPinName);
                    X::KWARGS kwParams;
                    X::Value retValue;
                    graph->AddConnection(nullptr, nullptr, params, kwParams, retValue);
                }
				X::Value valGraph(packGraph);
                NodeManager::I().AddGraph(valGraph);
				agentGraph = valGraph;
            }
            else if(needCreateGraph && firstAgent.IsValid())
            { 
                X::XPackageValue<AgentGraph> packGraph;
                AgentGraph* graph = packGraph.GetRealObj();
                graph->AddCallable(firstAgent);
                X::Value valGraph(packGraph);
                NodeManager::I().AddGraph(valGraph);
                agentGraph = valGraph;
            }

            // Parse groups
            X::Value groupsValue = root["groups"];
            std::vector<Group> groups = ParseGroups(groupsValue);

            return true;

        }

    private:
        // Helper function to convert CallableType to string
        std::string CallableTypeToString(CallableType type)
        {
            switch (type)
            {
            case CallableType::callable:
                return "callable";
            case CallableType::function:
                return "function";
            case CallableType::action:
                return "action";
            case CallableType::agent:
                return "agent";
            case CallableType::compositeAgent:
                return "compositeAgent";
            default:
                return "unknown";
            }
        }
    };
}
