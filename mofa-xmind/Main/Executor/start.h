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
#include "port.h"
#include "xlang.h"
#include <unordered_map>
#include <string>
#include <mutex>
#include <vector>

namespace xMind
{
	struct RootAgentDetail
	{
		std::string filename;
		X::Value varRunningGraph;//for this root agent
	};

	class Starter : public Singleton<Starter>
	{
		bool ParseConfig(X::Value& root);
		void RunService(const std::string& serviceEntry,int port =9901);
	public:
		Starter() = default;
		~Starter() = default;

		void Start(std::string& appPath);
		void Stop();
		std::vector<std::string> GetRootAgents();
		X::Value GetOrCreateRunningGraph(const std::string& rootAgent);
	private:
		std::string m_appPath;
		std::string m_configPath;
		std::mutex m_rootAgents_mtx;
		std::unordered_map<std::string, RootAgentDetail> m_rootAgents;
	};
}