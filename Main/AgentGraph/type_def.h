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
#include "XLangCType.h"

namespace xMind
{
	typedef unsigned long long SESSION_ID;
	struct SessionIDInfo
	{
		unsigned long sid;
		unsigned short inputIndex;
		unsigned short iterationCount;
	};
	inline SESSION_ID ToSessionID(const SessionIDInfo& info)
	{
		return (static_cast<unsigned long long>(info.sid) |
			(static_cast<unsigned long long>(info.inputIndex) << 32) |
			(static_cast<unsigned long long>(info.iterationCount) << 48));
	}

	inline SessionIDInfo FromSessionID(SESSION_ID session_id)
	{
		SessionIDInfo info;
		info.sid = static_cast<unsigned long>(session_id & 0xFFFFFFFF);
		info.inputIndex = static_cast<unsigned short>((session_id >> 32) & 0xFFFF);
		info.iterationCount = static_cast<unsigned short>((session_id >> 48) & 0xFFFF);
		return info;
	}


	enum class Status
	{
		Ok,
		Fail,
		Timeout,
		Running,
		Stopped
	};
	ENUM_MAP(TrigerCondition,
		Default,
		WaitAllInputs = 1000, 
		WaitEitherInput
	);
}