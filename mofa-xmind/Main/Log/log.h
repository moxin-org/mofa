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

#include <iostream>
#include <fstream>
#include <sstream> 
#include <string>
#include <filesystem>
#include <regex>

#include <string>


#include "Locker.h"


namespace Cantor {
class LimitedSizeLogger 
{
public:

	bool Start(const std::string& baseFilename, std::size_t maxSize=1024*1024)
	{
		m_baseFilename = baseFilename;
		m_maxSize = maxSize;
		m_currentSize = 0; 
		m_fileIndex = 0;
		//scanExistingFiles();
		openNewFile();
		return true;
	}
	void SetMaxSize(std::size_t maxSize)
	{
		m_maxSize = maxSize;
	}
	template <typename T>
	LimitedSizeLogger& operator<<(const T& value) 
	{
		std::ostringstream oss;
		oss << value;
		std::string message = oss.str();
		log(message);
		return *this;
	}

	void log(const std::string& message) 
	{
		if (m_currentSize + message.size() > m_maxSize) 
		{
			openNewFile();
		}
		m_file << message;
		m_currentSize += message.size();
	}
	void flush() 
	{
		m_file.flush();
	}
	void close() 
	{
		if (m_file.is_open()) 
		{
			m_file.close();
		}
	}

private:
	void scanExistingFiles() 
	{
		// Using a local variable to handle regex pattern correctly
		std::string pattern = m_baseFilename + R"_(\\_(\d+)\\.log)_"; 
		// Ensuring double backslashes
		std::regex filePattern(pattern);
		std::smatch match;
		int maxIndex = -1;

		for (const auto& entry : std::filesystem::directory_iterator(std::filesystem::current_path())) {
			if (entry.is_regular_file()) {
				std::string filename = entry.path().filename().string();
				if (std::regex_match(filename, match, filePattern)) {
					int index = std::stoi(match[1].str());
					//repelace line below for std::max(maxIndex, index);
					maxIndex = maxIndex > index ? maxIndex : index;
				}
			}
		}

		if (maxIndex >= 0) {
			m_fileIndex = maxIndex;
			std::string lastFilename = m_baseFilename + "_" + std::to_string(m_fileIndex) + ".log";
			std::ifstream lastFile(lastFilename, std::ios_base::ate | std::ios_base::binary);
			m_currentSize = lastFile.tellg();
			if (m_currentSize >= m_maxSize) {
				++m_fileIndex;
				m_currentSize = 0;
			}
		}
	}

	void openNewFile() 
	{
		if (m_file.is_open()) {
			m_file.close();
		}
		std::string filename = m_baseFilename + "_" + std::to_string(m_fileIndex++) + ".log";
		m_file.open(filename, std::ios_base::out | std::ios_base::app);
		m_currentSize = 0;
	}

	std::ofstream m_file;
	std::string m_baseFilename;
	std::size_t m_maxSize;
	std::size_t m_currentSize;
	int m_fileIndex;
};

class Log
{
	Locker m_lock;
#define LOG_OUT(v)\
	if (m_toFile)\
	{\
		m_limitedSizeLogger << v;\
	}\
	if (m_toStdOut) \
	{\
		std::cout << v;\
	}

#define LOG_FLUSH()\
	if(m_toFile) m_limitedSizeLogger.flush();
public:
	Log();
	~Log();

	bool Init();
	template<typename T>
	inline Log& operator<<(const T& v)
	{
		if (m_level <= m_dumpLevel)
		{
			LOG_OUT(v);
			LOG_FLUSH();
		}
		return (Log&)*this;
	}
	inline void operator<<(Locker* l)
	{
		if (m_level <= m_dumpLevel)
		{
			LOG_OUT('\n')
		}
		l->Unlock();
	}

	inline void SetLogFileName(std::string& strFileName)
	{
		m_logFileName = strFileName;
	}
	Log& SetCurInfo(const char* fileName, const int line,const int level);
	inline Locker* LineEnd()
	{
		return &m_lock;
	}
	inline Locker* End()
	{
		return &m_lock;
	}
	inline void LineBegin()
	{
		m_lock.Lock();
	}
	inline void LineEndUnlock()
	{
		m_lock.Unlock();
	}

	inline void SetDumpLevel(int l)
	{
		m_dumpLevel = l;
	}
	inline void SetLevel(int l)
	{
		m_level = l;
	}
	inline void SetFileSizeLimit(unsigned long long size)
	{
		m_limitedSizeLogger.SetMaxSize(size);
	}
private:
	bool m_toFile = true;
	bool m_toStdOut = true;
	std::string m_logFileName;
	//std::ofstream m_file_log;
	LimitedSizeLogger m_limitedSizeLogger;

	int m_level = 0;
	int m_dumpLevel = 999999; //All level will dump out
};
extern Log log;
#define SetLogSizeLimit(l) Cantor::log.SetFileSizeLimit(l)
#define SetLogLevel(l) Cantor::log.SetDumpLevel(l)
#define LOGV(level) Cantor::log.SetCurInfo(__FILE__,__LINE__,level)
#define LOG LOGV(0)
#define LOG1 LOGV(1)
#define LOG2 LOGV(2)
#define LOG3 LOGV(3)
#define LOG4 LOGV(4)
#define LOG5 LOGV(5)
#define LOG6 LOGV(6)
#define LOG7 LOGV(7)
#define LOG8 LOGV(8)
#define LOG9 LOGV(9)
#define LINE_END Cantor::log.LineEnd()
#define LOG_END Cantor::log.End()

}