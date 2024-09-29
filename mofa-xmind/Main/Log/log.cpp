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

#include "log.h"
#include "port.h"
#include "utility.h"

Cantor::Log Cantor::log;

Cantor::Log::Log()
{
}

Cantor::Log::~Log()
{
	m_limitedSizeLogger.close();
}

bool Cantor::Log::Init()
{
	m_limitedSizeLogger.Start(m_logFileName); 
	return true;
}

Cantor::Log& Cantor::Log::SetCurInfo(const char* fileName,
	const int line, const int level)
{
	m_lock.Lock();
	m_level = level;
	if (m_level <= m_dumpLevel)
	{
		std::string strFileName(fileName);
		auto pos = strFileName.rfind(Path_Sep_S);
		if (pos != std::string::npos)
		{
			strFileName = strFileName.substr(pos + 1);
		}
		else
		{
			//just in case some file path use '/' as separator
			pos = strFileName.rfind('/');
			if (pos != std::string::npos)
			{
				strFileName = strFileName.substr(pos + 1);
			}
		}
		unsigned long pid = GetPID();
		unsigned long tid = GetThreadID();
		auto curTime = getCurrentTimeString();
		const int buf_Len = 1000;
		char szFilter[buf_Len];
		SPRINTF(szFilter, buf_Len,"[%d-%d-%s,%s:%d] ", pid, tid,curTime.c_str(), strFileName.c_str(), line);
		LOG_OUT(szFilter);
	}
	return *this;
}
