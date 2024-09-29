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
#include <string>
#include "singleton.h"
#include <mutex>
#include "port.h"
#include "xpackage.h"
#include <vector>
#include <thread>
#include <queue>
#include <condition_variable>
#include <future>
#include <algorithm>

namespace xMind
{
	class LlmRequest
	{
		friend class LlmPool;
	public:
		LlmRequest()
		{

		}
		~LlmRequest()
		{

		}
		//prompts is a list of role/content pairs, or a string
		X::Value MakeRequest(const std::string& model, const X::Value& prompts, double temperature = 0.7);
	private:
		X::Value m_request;
		std::string m_name;
		std::string m_url; //for example: https://api.openai.com/v1/chat/completions
		std::string m_tag;//like openai, used for select
		X::Dict m_headers;//for request headers
		std::string m_content_type = "application/json";//data request mime type
	};

	class LlmPool : public Singleton<LlmPool>
	{
		std::mutex m_mutex;
		std::vector<LlmRequest*> m_requests;
		std::vector<std::thread> m_threadPool;
		std::queue<std::function<void()>> m_tasks;
		std::condition_variable m_condition;
		bool m_stop = false;

		void ThreadWorker()
		{
			while (true)
			{
				std::function<void()> task;
				{
					std::unique_lock<std::mutex> lock(m_mutex);
					m_condition.wait(lock, [this] { return m_stop || !m_tasks.empty(); });
					if (m_stop && m_tasks.empty())
						return;
					task = std::move(m_tasks.front());
					m_tasks.pop();
				}
				task();
			}
		}

	public:
		LlmPool()
		{
			// Initialize thread pool with a fixed number of threads
			for (int i = 0; i < (int)std::thread::hardware_concurrency(); ++i)
			{
				m_threadPool.emplace_back(&LlmPool::ThreadWorker, this);
			}
		}

		~LlmPool()
		{
			{
				std::lock_guard<std::mutex> lock(m_mutex);
				m_stop = true;
			}
			m_condition.notify_all();
			for (auto& thread : m_threadPool)
			{
				if (thread.joinable())
				{
					thread.join();
				}
			}
		}

		void Add(const std::string& name, 
			const std::string& url, 
			const std::string& tag,
			std::string content_type,
			X::Value headers)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			LlmRequest* pRequest = new LlmRequest();
			pRequest->m_name = name;
			pRequest->m_url = url;
			pRequest->m_tag = tag;
			pRequest->m_content_type = content_type;
			pRequest->m_headers = headers;
			m_requests.push_back(pRequest);
		}
		//llmSelections empty means choose all
		X::Value RunTask(const std::string& model, 
			const X::Value& prompts, double temperature, 
			const std::vector<std::string>& llmSelections)
		{
			std::promise<X::Value> promise;
			std::future<X::Value> future = promise.get_future();
			{
				std::lock_guard<std::mutex> lock(m_mutex);
				for (auto& request : m_requests)
				{
					if (llmSelections.size() == 0 ||
						std::find(llmSelections.begin(), llmSelections.end(), request->m_tag) 
							!= llmSelections.end())
					{
						m_tasks.emplace([request, &model, &prompts, temperature, &promise]() {
							try {
								X::Value result = request->MakeRequest(model, prompts, temperature);
								promise.set_value(result);
							} catch (...) {
								promise.set_exception(std::current_exception());
							}
						});
						break; // Only run the first matching task
					}
				}
				m_condition.notify_all();
			}

			return future.get();
		}

		void Test();
	};
}