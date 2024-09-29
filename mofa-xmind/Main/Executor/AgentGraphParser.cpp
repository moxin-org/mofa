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

#include "AgentGraphParser.h"
#include "xMindAPI.h"
#include <filesystem>

namespace xMind
{
    bool Parser::ParseRootAgent(const std::string& fileName, X::Value& graph)
    {
        X::Package yaml(xMind::MindAPISet::I().RT(), "yaml", "xlang_yaml");
        X::Value root = yaml["load"](fileName);
        if (root.IsObject() && root.GetObj()->GetType() == X::ObjType::Error)
        {
            return false;

        }
        std::filesystem::path fsPath(fileName);
		std::string moduleName = fsPath.stem().string();
        return ParseAgentGraphDescFromRoot(true, graph, root, moduleName, fileName);
    }
    bool Parser::ParseAgentGraphDesc(const std::string& moduleName, const std::string& fileName)
    {
        X::Package yaml(xMind::MindAPISet::I().RT(), "yaml", "xlang_yaml");
        X::Value root = yaml["load"](fileName);
        if (root.IsObject() && root.GetObj()->GetType() == X::ObjType::Error)
        {
            return false;

        }
        X::Value agentGraph;
        return ParseAgentGraphDescFromRoot(false, agentGraph,root, moduleName, fileName);
    }
    bool Parser::ParseAgentGraphDescFromString(const std::string& desc)
    {
        X::Package yaml(xMind::MindAPISet::I().RT(), "yaml", "xlang_yaml");
        X::Value root = yaml["loads"](desc);
        if (root.IsObject() && root.GetObj()->GetType() == X::ObjType::Error)
        {
            return false;

        }
        X::Value agentGraph;
        std::string moduleName;
		std::string blueprintName;
        return ParseAgentGraphDescFromRoot(false, agentGraph,root, moduleName, blueprintName);
    }
    
    std::string Parser::QueryKeyStore(std::string key)
    {
        std::string strRet;
        X::Value keystore = MindAPISet::I().GetXModule("keystore");
        if (keystore.IsObject())
        {
            X::Value val = keystore["query"](key);
            strRet = val.ToString();
        }
        return strRet;
    }

    bool Parser::ParseNodes(X::Value& firstAgent,const X::Value& nodesValue,
        const std::string& moduleName, const std::string& fileName)
    {
        if (!nodesValue.IsList())
        {
            return false;
        }
        std::vector<std::pair<std::string, std::string>> instancePairs;
        X::List list(nodesValue);
        for (const auto item : *list)
        {
            X::Dict nodeItem(item);
            std::string name = nodeItem["name"].ToString();
            std::string instanceName = nodeItem["instanceName"].ToString();
            std::string typeStr = nodeItem["type"].ToString();
            std::string strTrigerCondition = nodeItem["TrigerCondition"].ToString();

			TrigerCondition trigerCondition = StrToEnum<TrigerCondition>(strTrigerCondition);
            CallableType callableType = CallableType::callable;
            Callable* callable = nullptr;
            X::Value varCallable;
            if (typeStr == "agent")
            {
                callableType = CallableType::agent;
                X::XPackageValue<BaseAgent> valNode;
                callable = valNode.GetRealObj();
                varCallable = valNode;
                if (firstAgent.IsInvalid())
                {
					firstAgent = varCallable;
                }
            }
            else if (typeStr == "action")
            {
                callableType = CallableType::action;
                X::XPackageValue<BaseAction> valNode;
                callable = valNode.GetRealObj();
                varCallable = valNode;
            }
            else if (typeStr == "function")
            {
                callableType = CallableType::function;
                X::XPackageValue<Function> valNode;
                callable = valNode.GetRealObj();
                varCallable = valNode;
            }
            else if (!name.empty())
            {
                //push back when all nodes added,and check back
                instancePairs.push_back(std::make_pair(name, instanceName));

            }
            if (callable == nullptr)
            {
                std::cerr << "Error: Unknown node type: " << typeStr << std::endl;
                continue;
            }
			callable->SetTriggerCondition(trigerCondition);
            callable->SetNodeYamlDesc((X::Value&)item);
            callable->SetName(name);
            callable->SetDescription(nodeItem["description"].ToString());

            X::Value varIterationLimit = nodeItem["IterationLimit"];
            if (varIterationLimit.IsValid())
            {
                unsigned long iterationLimit = (unsigned long)varIterationLimit;
                if (iterationLimit > 0)
                {
                    callable->SetIterationLimit(iterationLimit);
                }
            }

            if (instanceName.empty())
            {
                instanceName = name;
            }
            callable->SetInstanceName(instanceName);
			//Check if has prompts if this is an agent
			if (callableType == CallableType::agent)
			{
                BaseAgent* pAgent = dynamic_cast<BaseAgent*>(callable);
                X::Value promptsValue = nodeItem["prompts"];
                if (promptsValue.IsValid())
                {
                    ParsePrompts(pAgent,moduleName, promptsValue);
                }
				//also for model,selections,temperature
				X::Value modelValue = nodeItem["model"];
				if (modelValue.IsValid())
				{
					pAgent->SetModel(modelValue.ToString());
				}
				X::Value selectionsValue = nodeItem["selections"];
				if (selectionsValue.IsValid())
				{
					pAgent->SetSelections(selectionsValue);
				}
				X::Value temperatureValue = nodeItem["temperature"];
				if (temperatureValue.IsValid())
				{
					pAgent->SetTemperature((double)temperatureValue);
				}
			}
            // Parse inputs
            callable->SetInputs(nodeItem["inputs"]);

            // Parse outputs
            callable->SetOutputs(nodeItem["outputs"]);

            // Parse source
            X::Value sourceValue = nodeItem["source"];
            if (sourceValue.IsDict())
            {
				Source source;
				X::Dict sourceDict(sourceValue);
                //we support python,xlang and shared_lib
				X::Value pythonValue = sourceDict["python"];
                if (pythonValue.IsValid())
                {
					source.python = pythonValue.ToString();
                }
				X::Value xlangValue = sourceDict["xlang"];
                if (xlangValue.IsValid())
                {
                    source.xlang = xlangValue.ToString();
                }
				X::Value sharedLibValue = sourceDict["shared_lib"];
				if (sharedLibValue.IsValid())
				{
					source.shared_lib = sharedLibValue.ToString();
				}
				callable->SetSource(source);
            }

            // Parse parameters
            X::Value parametersValue = nodeItem["parameters"];
            if (parametersValue.IsDict())
            {
                X::Dict parameters(parametersValue);
                X::KWARGS params;
                parameters->Enum([&](X::Value& key, X::Value& value) {
                    params.Add(key.ToString().c_str(), value);
                    });
                callable->SetParams(params);
            }

            // Parse group
            //TODO:
            // callable->SetGroup(nodeItem["group"].ToString());

            NodeManager::I().addCallable(moduleName, fileName, name, varCallable);
            //we add twice, one with instance name, one with name if not identical
            //so for reference we can use either name or instance name
            if (instanceName != name)
            {
                NodeManager::I().addCallable(moduleName, fileName, instanceName, varCallable);
            }
        }
        for (auto& pair : instancePairs)
        {
            X::Value valNodeRefer = QueyNode(moduleName, pair.first);
            //check from NodeManager to find the callable with the name
            X::XPackageValue<Callable> packNodeRefer(valNodeRefer);
            Callable* callableRefer = packNodeRefer.GetRealObj();
            if (callableRefer != nullptr)
            {
                X::Value cloneCallable = callableRefer->Clone();
                X::XPackageValue<Callable> valNode(cloneCallable);
                Callable* pCloneCallable = valNode.GetRealObj();
                pCloneCallable->SetInstanceName(pair.second);
                NodeManager::I().addCallable(moduleName, fileName, pair.second, cloneCallable);
            }
        }

        return true;
    }

}