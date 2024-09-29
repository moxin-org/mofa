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

#include "start.h"
#include <iostream>
#include <string>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include "xlang.h"
#include "xMindAPI.h"
#include "AgentGraphParser.h"

namespace xMind
{
	static std::string ReadFileContent(const std::string& fileName) {
		std::filesystem::path fsFile(fileName);
		// Open the file
		std::ifstream file(fsFile, std::ios::in | std::ios::binary);
		if (!file) {
			throw std::runtime_error("Failed to open the file: " + fsFile.string());
		}

		// Read the entire file content into a string
		std::ostringstream contentStream;
		contentStream << file.rdbuf();

		// Close the file
		file.close();

		return contentStream.str();
	}

	std::vector<std::string> Starter::GetRootAgents()
	{
		std::vector<std::string> ret;
		for (auto& item : m_rootAgents)
		{
			ret.push_back(item.first);
		}
		return ret;
	}
	X::Value Starter::GetOrCreateRunningGraph(const std::string& rootAgent)
	{
		std::lock_guard<std::mutex> lock(m_rootAgents_mtx);
		auto it = m_rootAgents.find(rootAgent);
		if (it != m_rootAgents.end())
		{
			if (it->second.varRunningGraph.IsValid())
			{
				return it->second.varRunningGraph;
			}
		}
		Parser parser;
		X::Value graph;
		if (parser.ParseRootAgent(it->second.filename, graph))
		{
			it->second.varRunningGraph = graph;
			return graph;
		}
		return X::Value();
	}
	inline std::string MakeAbsPath(std::string rootPath, std::string path)
	{
		std::filesystem::path fsPath(path);
		// Check if the path is absolute, if not, combine it with RootPath
		if (!fsPath.is_absolute())
		{
			fsPath = std::filesystem::path(rootPath) / fsPath;
		}

		// Normalize the path
		fsPath = fsPath.lexically_normal();
		return fsPath.string();
	}
	void Starter::RunService(const std::string& serviceEntry, int port)
	{
		std::string strServiceEntry = MakeAbsPath(m_configPath, serviceEntry);
		std::string xlangCode = ReadFileContent(strServiceEntry);
		if (xlangCode.empty())
		{
			std::cout << "Failed to read service entry file: " << strServiceEntry << std::endl;
			return;
		}
		X::ARGS args(1);
		args.push_back(port);
		X::KWARGS kwargs;
		bool bOK = X::g_pXHost->RunModuleInThread(strServiceEntry.c_str(),
			xlangCode.c_str(), (int)xlangCode.size(), args, kwargs);
		if (bOK)
		{
			LOG << "xMind Service Starting," << " http://localhost:" << port << LINE_END;
		}
	}
	bool Starter::ParseConfig(X::Value& root)
	{
		X::Dict dict(root);
		X::Value RootAgents = dict["RootAgents"];
		if (RootAgents.IsList())
		{
			X::List list(RootAgents);
			for (const auto item : *list)
			{
				X::Dict nodeItem(item);
				std::string moduleName = nodeItem["name"].ToString();
				std::string fileName = nodeItem["file"].ToString();
				fileName = MakeAbsPath(m_configPath, fileName);
				m_rootAgents.emplace(std::make_pair(moduleName, RootAgentDetail{ fileName }));
			}
		}
		X::Value webServer = dict["WebServer"];
		if (webServer.IsDict())
		{
			X::Dict webServerDict(webServer);
			X::Value ServiceEntry = webServerDict["ServiceEntry"];
			if (ServiceEntry.IsValid())
			{
				int port = 9901;
				X::Value varPort = webServerDict["Port"];
				if (varPort.IsValid())
				{
					port = varPort.ToInt();
				}
				RunService(ServiceEntry.ToString(), port);
			}
		}
		return true;
	}
	void Starter::Start(std::string& appPath)
	{
		m_appPath = appPath;
		std::filesystem::path configFolderPath = std::filesystem::path(appPath) / "Config";
		m_configPath = configFolderPath.string();
		std::filesystem::path configPath = configFolderPath / "config.yml";
		std::cout << "configPath: " << configPath << std::endl;
		X::Package yaml(xMind::MindAPISet::I().RT(), "yaml", "xlang_yaml");
		X::Value root = yaml["load"](configPath.string());
		if (root.IsObject() && root.GetObj()->GetType() == X::ObjType::Dict)
		{
			ParseConfig(root);
		}
		else
		{
			std::cout << "Failed to load config file: " << configPath << std::endl;
		}

	}

	void Starter::Stop()
	{
	}
}

