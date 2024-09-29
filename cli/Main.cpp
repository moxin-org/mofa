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

#include <signal.h>
#include <vector>
#include <string>
#include <cstring>
#include "xload.h"
#include "xlang.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <filesystem>

#ifdef __linux__
#include <unistd.h>
#elif __APPLE__
#include <mach-o/dyld.h>
#elif _WIN32
#include <windows.h>
#endif

#if (WIN32)
#define Path_Sep_S "\\"
#define Path_Sep '\\'
#else
#include <string.h> //for memcpy
#define Path_Sep_S "/"
#define Path_Sep '/'
#endif


struct ParamConfig
{
	std::string appPath;
	std::string appName;
	X::Config config;
	bool runLocalScript = false;
	bool print_usage = false;//-help |-? |-h
};

X::XLoad g_xLoad;
void signal_callback_handler(int signum) 
{
	X::AppEventCode code = g_xLoad.HandleAppEvent(signum);
	if (code == X::AppEventCode::Exit)
	{
		exit(signum);
	}
	signal(SIGINT, signal_callback_handler);
}


void PrintUsage()
{
	std::cout << 
	 "xmcli [-dbg] -run script_file_name" << std::endl;
	std::cout << "xmcli -help | -? | -h for help" << std::endl;
}

std::string getExecutableFilePath()
{
	std::string exe_path;
#ifdef __linux__
	std::filesystem::path fs_exe_path = std::filesystem::canonical("/proc/self/exe");
	exe_path = fs_exe_path.string();
#elif __APPLE__
	char path[1024];
	uint32_t size = sizeof(path);
	if (_NSGetExecutablePath(path, &size) == 0) {
		std::filesystem::path fs_exe_path = std::filesystem::canonical(path);
		exe_path = fs_exe_path.string();
	}
#elif _WIN32
	char buffer[MAX_PATH];
	DWORD length = GetModuleFileName(nullptr, buffer, MAX_PATH);
	if (length > 0) {
		exe_path = buffer;
	}
#endif
	return exe_path;
}


bool ParseCommandLine(std::vector<std::string>& params, ParamConfig& paramCfg)
{
	std::string progName = params[0];
	std::filesystem::path fsPath(progName);
	// Check if the path is absolute, if not, combine it with RootPath
	if (!fsPath.is_absolute())
	{
		progName = getExecutableFilePath();
	}
	auto pos = progName.rfind(Path_Sep);
	if (pos != progName.npos)
	{
		std::string strAppPath = progName.substr(0, pos);
		paramCfg.config.appPath = new char[strAppPath.length() + 1];
		memcpy((char*)paramCfg.config.appPath, strAppPath.data(), strAppPath.length() + 1);
	}
	paramCfg.config.appFullName = new char[progName.length() + 1];
	memcpy((char*)paramCfg.config.appFullName, progName.data(), progName.length() + 1);

	return true;
}
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

int main(int argc, char* argv[])
{
	std::vector<std::string> params(argv, argv+argc);
	ParamConfig paramConfig;
	ParseCommandLine(params, paramConfig);
	paramConfig.config.enterEventLoop = false;

	signal(SIGINT, signal_callback_handler);
	int retCode = g_xLoad.Load(&paramConfig.config);
	if (retCode != 0)
	{
		return retCode;
	}
	g_xLoad.Run();
	if (paramConfig.runLocalScript)
	{
		std::string fileName = paramConfig.config.fileName;
		std::filesystem::path fsFileName(fileName);
		if (!fsFileName.is_absolute())
		{
			std::filesystem::path fsFilePath(paramConfig.appPath);
			fsFilePath /= fsFileName;
			fileName = fsFilePath.string();
		}
		std::string script_content = ReadFileContent(fileName);	
		if (!script_content.empty())
		{
			X::Value retVal;
			X::ARGS args((int)params.size());
			for (auto& p : params)
			{
				args.push_back(p);
			}
			X::g_pXHost->RunCodeWithParam(fileName.c_str(),
				script_content.c_str(),
				(int)script_content.size(), args, retVal);
		}
		return 0;
	}
	//::MessageBox(nullptr, "XLang Engine Loaded", "XLang", MB_OK);
	//Run Script
	static std::string script_files[] =
	{
		"Scripts/cli.x"
	};
	std::string fileRootFolder = paramConfig.config.appPath;
	for (int i = 0; i < sizeof(script_files) / sizeof(std::string); i++)
	{
		auto& script_file = script_files[i];
		std::filesystem::path fsFileName(fileRootFolder);
		fsFileName /= script_file;
		std::string filePath = fsFileName.string();
		std::string script_content = ReadFileContent(filePath);
		if (!script_content.empty())
		{
			X::Value retVal;
			X::ARGS args((int)params.size());
			for (auto& p : params)
			{
				args.push_back(p);
			}
			X::g_pXHost->RunCodeWithParam(script_file.c_str(), 
				script_content.c_str(),
				(int)script_content.size(), args,retVal);
		}
	}

	g_xLoad.Unload();
	return 0;
}
