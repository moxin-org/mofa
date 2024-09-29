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
#include <thread>
#include <vector>
#include <condition_variable>
#include <optional>
#include "Callable.h"


namespace xMind
{
	class AgentGroup;

	struct InputData
	{
		Status status;
		int inputIndex;
		SESSION_ID sessionId;
		X::Value data;
	};
	using SessionValue = std::pair<SESSION_ID, X::Value>;

	class BufferedProcessor : public Callable
	{
		BEGIN_PACKAGE(BufferedProcessor)
			ADD_BASE(Callable);
			APISET().AddVarFunc("waitInputs", &BufferedProcessor::WaitInputs);
			APISET().AddVarFunc("isRunning", &BufferedProcessor::IsRunning);
			APISET().AddFunc<3>("pushToOutput", &Callable::PushToOutput);
			APISET().AddPropL("TrigerCondition",
				[](auto* pThis, X::Value v) {
					if (v.IsNumber())
					{
						pThis->m_trigerCondition = (TrigerCondition)(int)v;
					}
					else
					{
						std::string condi = v.ToString();
						if (condi == "WaitEitherInput")
						{
							pThis->m_trigerCondition = TrigerCondition::WaitEitherInput;
						}
						else if (condi == "WaitAllInputs")
						{
							pThis->m_trigerCondition = TrigerCondition::WaitAllInputs;
						}
					}
				},
				[](auto* pThis) {
					return (int)pThis->m_trigerCondition;
				});
		END_PACKAGE
	protected:
		inline virtual bool ReceiveData(SESSION_ID sessionId, int inputIndex, X::Value& data) override
		{
			PushEvent(inputIndex, X::Value());//just notify if there is subscriber
			std::unique_lock<std::mutex> lock(m_mutex);
			if(inputIndex < 0 || inputIndex >= static_cast<int>(m_inputQueues.size()))
			{
				return false;
			}
			m_inputQueues[inputIndex].push_back(std::pair(sessionId,data));
			m_condVar.notify_all();
			return true;
		}

		virtual X::Value GetOwner() = 0;

		X::Value CreateXlangStructInputData(InputData& inputData)
		{
			X::Struct xStruct;
			xStruct->addField("status", "int");
			xStruct->addField("inputIndex", "int");
			xStruct->addField("data", "xvalue");
			xStruct->Build();

			InputData* data = (InputData*)xStruct->Data();
			data->status = inputData.status;
			data->inputIndex = inputData.inputIndex;
			data->data = inputData.data;

			return X::Value(xStruct);
		}

	public:
		BufferedProcessor() : m_running(false){}

		virtual ~BufferedProcessor()
		{
			Stop();
		}
		inline bool Create()
		{
			auto it = m_params.find("inputs");
			if (it)
			{
				SetInputs(it->val);
			}
			it = m_params.find("outputs");
			if (it)
			{
				SetOutputs(it->val);
			}

			return true;
		}
		inline virtual void SetInputs(X::Value v) override
		{
			Callable::SetInputs(v);
			m_inputQueues.resize(m_inputs.size());
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
					return m_running?true:false;
					});
				retValue = int(bRun ? Status::Running : Status::Stopped);
			}
			return true;
		}
		bool WaitInputs(X::XRuntime* rt, X::XObj* pContext,
			X::ARGS& params, X::KWARGS& kwParams, X::Value& retValue)
		{
			int timeoutMs = -1;
			bool either = (m_trigerCondition != TrigerCondition::WaitAllInputs);

			if (params.size() > 0)
			{
				timeoutMs = (int)params[0];
			}
			else
			{
				auto it = kwParams.find("timeout");
				if (it)
				{
					timeoutMs = (int)it->val;
				}
			}

			// Check for "Either" parameter
			//override again with Keyword parameter
			auto itEither = kwParams.find("Either");
			if (itEither && itEither->val.IsBool())
			{
				either = itEither->val.ToBool();
			}

			std::unique_lock<std::mutex> lock(m_mutex);

			auto waitCondition = [this, &retValue, either] {
				if (!m_running)
				{
					return true;
				}

				if (m_inputQueues.empty())
				{
					return false;
				}

				std::optional<SESSION_ID> commonSessionId;
				std::vector<SessionValue> matchedItems(m_inputQueues.size());

				for (size_t i = 0; i < m_inputQueues.size(); ++i)
				{
					auto& vec = m_inputQueues[i];
					for (auto it = vec.begin(); it != vec.end(); ++it)
					{
						SESSION_ID sessionId = it->first;
						bool isCommon = true;

						if (either)
						{
							// If 'Either' is true, return as soon as we find a session ID in one vector
							commonSessionId = sessionId;
							matchedItems[i] = *it;

							X::List outerList;
							X::List innerList;
							innerList += it->first;  // sessionId
							innerList += static_cast<int>(i); // inputIndex
							innerList += it->second; // data
							outerList->AddItem(innerList);
							retValue = outerList;

							// Remove the matched item from the vector
							vec.erase(it);

							return true;
						}

						// Check if this sessionId exists in all other vectors
						for (size_t j = 0; j < m_inputQueues.size(); ++j)
						{
							if (i == j)
							{
								matchedItems[j] = *it; // save the match for this vector
								continue;
							}

							auto& otherVec = m_inputQueues[j];
							auto found = std::find_if(otherVec.begin(), otherVec.end(),
								[sessionId](const SessionValue& pair) {
									return pair.first == sessionId;
								});

							if (found == otherVec.end())
							{
								isCommon = false;
								break;
							}
							else
							{
								matchedItems[j] = *found; // save the match for the other vector
							}
						}

						if (isCommon)
						{
							commonSessionId = sessionId;
							break;
						}
					}

					if (commonSessionId.has_value())
					{
						X::List outerList;
						for (size_t k = 0; k < m_inputQueues.size(); ++k)
						{
							const auto& data = matchedItems[k];
							X::List innerList;
							innerList += data.first;  // sessionId
							innerList += static_cast<int>(k); // inputIndex
							innerList += data.second; // data
							outerList->AddItem(innerList);

							// Remove the matched item from the vector
							auto& vec = m_inputQueues[k];
							auto it = std::find_if(vec.begin(), vec.end(),
								[commonSessionId](const SessionValue& pair) {
									return pair.first == commonSessionId.value();
								});

							if (it != vec.end())
							{
								vec.erase(it);
							}
						}

						retValue = outerList;
						return true;
					}
				}

				return false;
				};

			bool isNotTimeout = true;
			if (timeoutMs == -1)
			{
				m_condVar.wait(lock, waitCondition);
			}
			else
			{
				isNotTimeout = m_condVar.wait_for(lock, std::chrono::milliseconds(timeoutMs), waitCondition);
			}

			if (!isNotTimeout || !m_running)
			{
				retValue = X::Value();  // return an empty value if timed out or stopped
				return false;
			}

			return true;
		}


		inline virtual void Stop() override
		{
			m_running = false;
			m_condVar.notify_all();
			if (m_implObject.IsObject() && m_thread.joinable())
			{
				m_thread.join();
			}
		}

		virtual bool Run() override
		{
			m_running = true;
			//for python non-threading mode,we don't run in thread
			//it will not pass in m_implObject
			if (m_RunInThread || m_implObject.IsObject())
			{
				m_thread = std::thread(&BufferedProcessor::ThreadRun, this);
			}
			return true;
		}

		void ThreadRun()
		{
			while (m_running)
			{
				X::Value retData = RunOnce();
				if (retData.IsObject() && retData.GetObj()->GetType() == X::ObjType::Error)
				{
					//error happened
					break;
				}
			}
		}
		virtual X::Value RunOnce()
		{
			X::Value retData;
			if (m_implObject.IsValid())
			{
				X::KWARGS kwParams;
				X::Value varOwner = GetOwner();
				kwParams.Add("owner", varOwner);
				X::ARGS params(0);
				retData = m_implObject.ObjCall(params, kwParams);
			}
			return retData;
		}

	protected:
		bool m_RunInThread = false;
		AgentGroup* m_group;
		std::vector<std::vector<SessionValue>> m_inputQueues;
		std::thread m_thread;
		std::atomic<bool> m_running;
		std::mutex m_mutex;
		std::condition_variable m_condVar;
	};
}
