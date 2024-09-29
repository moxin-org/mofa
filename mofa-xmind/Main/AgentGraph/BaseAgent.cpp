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

#include "BaseAgent.h"
#include "AgentGraph.h"

namespace xMind
{
    X::Value BaseAgent::RunOnce()
    {
        if (m_implObject.IsValid())
        {
            return BufferedProcessor::RunOnce();
        }

        // We are an agent; if no process function, we still use input as prompts,
        // combine other prompts to LLM, and return result from LLM inference
        std::vector<std::string> llmSelections;
        for (auto selection : *m_selections)
        {
            llmSelections.push_back(selection.ToString());
        }
        X::ARGS params(0);
        X::KWARGS kwParams;
        X::Value varData;

        X::Value retValue;
        SESSION_ID data_SessionId = 0;
        LOG5 << "Agent: " << m_instanceName << " WaitInputs" << LINE_END;
        if (WaitInputs(nullptr, nullptr, params, kwParams, varData))
        {
            X::List prompts;
            for (auto prompt : *m_prompts)
            {
                prompts += prompt;
            }

            if (varData.IsList())
            {
                X::List dataList = varData;
                if (dataList.Size() > 0)
                {
                    X::Value sessionIdValue = dataList.GetItemValue(0).GetItemValue(0);
                    data_SessionId = (unsigned long long)sessionIdValue;

                    for (int i = 0; i < dataList.Size(); ++i)
                    {
                        X::Value listEntry = dataList[i];
                        if (listEntry.IsList() && listEntry.Size() == 3)
                        {
                            X::Value data = listEntry[2];
                            if (data.IsList())
                            {
                                X::List listData = data;
                                for (auto prompt : *listData)
                                {
                                    prompts += prompt;
                                }
                            }
                            else if (data.IsDict())
                            {
                                prompts += data;
                            }
                            else
                            {
                                std::string strData = data.ToString();
                                X::Dict dictPrompt;
                                dictPrompt->Set("role", "user");
                                dictPrompt->Set("content", strData);
                                prompts += dictPrompt;
                            }
                        }
                    }
                }
            }

            LOG5 << "Agent: " << m_instanceName << " Have prompts:" << prompts.ToString() << LINE_END;
            retValue = LlmPool::I().RunTask(m_model, prompts, m_temperature, llmSelections);
            if (retValue.IsObject() && retValue.GetObj()->GetType() == X::ObjType::Error)
            {
                LOG5 << "Agent: " << m_instanceName << " Got Error" << LINE_END;
                return retValue;
            }
            std::string strRet = retValue.ToString();
            //check if has xmind-cmd, if have, run them first
            auto cmds = parseCmd(strRet);
            if (cmds.size() > 0)
            {
                for (auto cmd : cmds)
                {
                    executeCmd(this, cmd);
                }
            }
            //check if has xmind-cmd
            //we increase the iterationCount per each node finish the calc
            SessionIDInfo idInfo = FromSessionID(data_SessionId);
            auto it_cnt = idInfo.iterationCount++;
            if (m_iterationLimit > 0)//have the iteration limit
            {
                if (idInfo.iterationCount >= m_iterationLimit)
                {
                    LOG5 << "Agent: " << m_instanceName << " Reach iteration limit" << LINE_END;
                    //break the connection with its outputs
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
            }
            LOG5 << "Agent: " << m_instanceName << " Results:" << strRet <<",iterationCount:"<< it_cnt << LINE_END;

            // Need to parse the result and then push it to the next node
            data_SessionId = ToSessionID(idInfo);
            int outputIndex = 0;//TODO: decide which output to use
            PushToOutput(data_SessionId, outputIndex, retValue);
        }

        return retValue;
    }

}