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
#include "xpackage.h"
#include "log.h"
#include "Locker.h"
#include "AgentGraph.h"
#include "BaseAgent.h"
#include "Function.h"
#include "BaseAction.h"
#include "type_def.h"
#include <map>
#include "AgentGraphParser.h"
#include "start.h"

namespace xMind
{
	struct SubscriptionInfo
	{
		int subId;
		std::vector<int> nodeIds;
		std::vector<X::Value> dataList;//list of [id,inputIndex,data]
        std::condition_variable condVar;
	};
    class MindAPISet :
        public Singleton<MindAPISet>
    {
        std::string m_RootPath;
        X::Runtime* m_defaultRuntime = nullptr;
        std::mutex m_mutex;
        std::map<int, SubscriptionInfo*> m_subscriptions;
        int m_nextSubscriptionId = 1;
		std::unordered_map<std::string,X::Value> m_xlangModules;

        BEGIN_PACKAGE(MindAPISet)
            APISET().AddConst("OK", (int)Status::Ok);
            APISET().AddConst("Fail", (int)Status::Fail);
            APISET().AddConst("Timeout", (int)Status::Timeout);
            APISET().AddConst("Running", (int)Status::Running);
            APISET().AddConst("Stopped", (int)Status::Stopped);
            APISET().AddConst("WaitAllInputs", (int)TrigerCondition::WaitAllInputs);
            APISET().AddConst("WaitEitherInput", (int)TrigerCondition::WaitEitherInput);
            APISET().AddEvent("OnReady");
            APISET().AddEvent("OnShutdown");
            APISET().AddVarFunc("SubscribeEvents", &MindAPISet::SubscribeEvents);
            APISET().AddFunc<1>("UnsubscribeEvents", &MindAPISet::UnsubscribeEvents);
            APISET().AddFunc<0>("IsRunning", &MindAPISet::IsRunning);
            APISET().AddFunc<1>("LoadBlueprintFromFile", &MindAPISet::LoadBlueprintFromFile);
            APISET().AddFunc<1>("LoadAgentFlowFromString", &MindAPISet::LoadAgentFlowFromString);
            APISET().AddFunc<0>("QueryAgentFlow", &MindAPISet::QueryAgentFlow);
            APISET().AddVarFunc("PullEvents", &MindAPISet::PullEvents);
            APISET().AddVarFunc("Test", &MindAPISet::Test);
            APISET().AddVarFunc("log", &MindAPISet::Log);
            APISET().AddVarFunc("logV", &MindAPISet::LogV);
            APISET().AddVarFunc("log_nolineend", &MindAPISet::Log_nolineend);
            APISET().AddFunc<0>("GetRootPath", &MindAPISet::GetRootPath);
            APISET().AddVarFuncEx("Function", &MindAPISet::Create<Function>);
            APISET().AddVarFuncEx("Action", &MindAPISet::Create<BaseAction>);
            APISET().AddVarFuncEx("Agent", &MindAPISet::Create<BaseAgent>);
            APISET().AddVarFunc("AddGraph", &MindAPISet::AddGraph);
            APISET().AddVarFunc("AddNode", &MindAPISet::AddNode);
            APISET().AddClass<0, AgentGraph>("Graph");
            APISET().AddClass<0, Function>("MindFunction");
            APISET().AddClass<0, BaseAction>("MindAction");
            APISET().AddClass<0, BaseAgent>("MindAgent");

            APISET().AddFunc<0>("GetRootAgents", &MindAPISet::GetRootAgents);
            APISET().AddVarFunc("ChatRequest", &MindAPISet::ChatRequest);
            APISET().AddVarFunc("CompletionRequest", &MindAPISet::CompletionRequest);

            APISET().AddFunc<1>("GetXModule", &MindAPISet::GetXModule);
        END_PACKAGE
    public:
        inline X::Value GetXModule(std::string name)
        {
			auto it = m_xlangModules.find(name);
			if (it != m_xlangModules.end())
			{
				return it->second;
			}
			return X::Value();
        }
		inline void AddXlangModule(const std::string& name, X::Value module)
		{
			m_xlangModules[name] = module;
		}
        inline bool IsRunning()
        {
            return true;
        }
        bool AddGraph(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
        bool AddNode(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
        bool ChatRequest(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
        bool CompletionRequest(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue);
        inline bool SubscribeEvents(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
            if (params.size() == 0)
            {
                retValue = false;
                return true;
            }

            X::List listID(params[0]);
            if (listID)
            {
                std::unique_lock<std::mutex> lock(m_mutex);
                int subscriptionId = m_nextSubscriptionId++;
                SubscriptionInfo* info =new SubscriptionInfo;
                info->subId = subscriptionId;

                for (auto id : *listID)
                {
                    info->nodeIds.push_back(id);
                }
                m_subscriptions.emplace(subscriptionId, info);
                retValue = subscriptionId;
            }
            else
            {
                retValue = false;
            }

            return true;
        }
        inline bool UnsubscribeEvents(int id)
        {
            std::unique_lock<std::mutex> lock(m_mutex);
            auto it = m_subscriptions.find(id);
            if (it != m_subscriptions.end())
            {
				SubscriptionInfo* info = it->second;
                info->condVar.notify_all();
                delete info;
                m_subscriptions.erase(it);
                return true;
            }
            return false;
        }
        inline bool PullEvents(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
            int timeout = -1;
            if (params.size() < 1)
            {
                retValue = false;
                return true;
            }

            int subscriptionId = params[0];
            if (params.size() > 1)
            {
                timeout = params[1];
            }
			std::unique_lock<std::mutex> lock(m_mutex);
			auto it = m_subscriptions.find(subscriptionId);
            if (it == m_subscriptions.end())
            {
                retValue = false;
            }
			else
			{
				auto& info = *it->second;
				if (info.dataList.empty())
				{
					if (timeout > 0)
					{
						info.condVar.wait_for(lock, std::chrono::milliseconds(timeout));
					}
                    else
					{
						info.condVar.wait(lock);
					}
				}
				if (info.dataList.empty())
				{
					retValue = false;
				}
				else
				{
					X::List retList;
					for (auto& dataEntry : info.dataList)
					{
						retList->AddItem(dataEntry);
					}
					info.dataList.clear();
					retValue = retList;
				}
			}

            return true;
        }

        void PushEvent(unsigned long long ID, int inputIndex, X::Value data)
        {
            X::List dataEntry;
			dataEntry += ID;
			dataEntry += inputIndex;
			dataEntry += data;

            std::unique_lock<std::mutex> lock(m_mutex);
			for (auto& it : m_subscriptions)
			{
				auto& info = *it.second;
				if (std::find(info.nodeIds.begin(), info.nodeIds.end(), ID) != info.nodeIds.end())
				{
					info.dataList.push_back(dataEntry);
					info.condVar.notify_all();
				}
			}
        }

        inline bool Test(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
			std::cout << "xMind->Test" << std::endl;
            if (params.size() > 0)
            {
				X::Value obj = params[0];
                obj.GetObj()->SetRT(rt);
                X::ARGS args(1);
				args.push_back("call from host side");
				X::Value retFromClient = obj.ObjCall(args);
                if (!retFromClient.IsObject())
                {
					std::cout << "retFromClient is not object" << std::endl;
                }
                retValue = retFromClient;
            }
            else
            {
				X::ARGS args(0);
				X::KWARGS kwargs;
                Fire(0, args, kwargs);
            }
            std::cout << "End xMind->Test" << std::endl;
            return true;
        }
        void SetRootInfo(std::string path)
        {
            m_RootPath = path;
        }
        std::string GetRootPath()
        {
            return m_RootPath;
        }
        X::Runtime& RT() { return *m_defaultRuntime; }
        bool Start();
        void Shutdown();
        void CalcDecoratorParameter(X::ARGS& expres, X::KWARGS* pKwParams);

        template<class T>   
        inline void Create(X::XRuntime* rt, X::XObj* pThis, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& trailer, X::Value& retValue)
        {   
            X::Value realObj;
            std::string name;
            //if trailer is valid, it means it is a decorator
            //and params is the expression objects of the decorator
            if (trailer.IsValid())
            {
                CalcDecoratorParameter(params, &kwParams);
                auto it = kwParams.find("name");
                if (it)
                {
                    name = it->val.ToString(); 

                }
                else
                {
                    it = kwParams.find("Name");
                    if(it)
					{
						name = it->val.ToString();
					}
                    else
                    {
                        if (trailer.IsObject() 
                            && trailer.GetObj()->GetType() == X::ObjType::Function)
                        {
                            X::Func func(trailer);
                            name = func->GetName().ToString();
                        }
                    }
                }
                realObj = trailer;
            }
            else
            {
                if (params.size() >= 2)
                {
                    realObj = params[0];
                    name = params[1].ToString();
                }
                else if(params.size() == 1)
				{
					realObj = params[0];
                    if(realObj.IsObject())
					{
                        X::Func func(realObj);
						name = func->GetName().ToString();
					}
				}
                else 
                {
                    auto it = kwParams.find("name");
                    if (it)
                    {
                        name = it->val.ToString();
                    }
                    else
                    {
                        it = kwParams.find("Name");
                        if (it)
                        {
                            name = it->val.ToString();
                        }
                    }
                }
            }
            T* pObj = new T();
            pObj->SetName(name);
            pObj->SetParams(kwParams);
            pObj->SetImplObject(realObj);
            pObj->Create();
            auto* pXPack = T::APISET().GetProxy(pObj);
            retValue = X::Value(pXPack);
        }
        inline bool Log(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
            int level = 0;
            auto it = kwParams.find("level");
            if (it)
            {
                level = it->val;
            }
            Cantor::log.LineBegin();
            Cantor::log.SetLevel(level);
            for (auto& p : params)
            {
                Cantor::log << p.ToString();
            }
            Cantor::log << LINE_END;
            return true;
        }
        inline bool LogV(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
            std::string moduleFileName = rt->GetXModuleFileName();
            int line = rt->GetTopStackCurrentLine();

            int level = 0;
            auto it = kwParams.find("level");
            if (it)
            {
                level = it->val;
            }
            Cantor::log.SetCurInfo(moduleFileName.c_str(), (const int)line, level);
            Cantor::log.SetLevel(level);
            for (auto& p : params)
            {
                Cantor::log << p.ToString();
            }
            Cantor::log << LINE_END;
            return true;
        }
        inline bool Log_nolineend(X::XRuntime* rt, X::XObj* pContext,
            X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
        {
            int level = 0;
            auto it = kwParams.find("level");
            if (it)
            {
                level = it->val;
            }
            Cantor::log.LineBegin();
            Cantor::log.SetLevel(level);
            for (auto& p : params)
            {
                Cantor::log << p.ToString();
            }
            Cantor::log.LineEndUnlock();
            return true;
        }
        inline bool LoadBlueprintFromFile(const std::string& fileName)
        {
            std::filesystem::path filePath(fileName);
			std::string moduleName = filePath.stem().string();
            xMind::Parser parser;
            bool bOK = parser.ParseAgentGraphDesc(moduleName, fileName);
            return bOK;
        }
        inline bool LoadAgentFlowFromString(const std::string& desc)
        {
            xMind::Parser parser;
            X::Package yaml(xMind::MindAPISet::I().RT(), "yaml", "xlang_yaml");
            X::Value root = yaml["loads"](desc);
            bool bOK = parser.ParseAgentGraphDesc(root);
            return bOK;
        }
        inline std::string QueryAgentFlow()
        {
            return NodeManager::I().BuildGraphAsJson();
        }
		inline X::Value GetRootAgents()
		{
			auto list = Starter::I().GetRootAgents();
			X::List retList;
			for (auto& item : list)
			{
				retList+=item;
			}
			return retList;
		}
    };
}