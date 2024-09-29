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
#include "xlang.h"
#include "xhost.h"

namespace xMind
{
	class PropScope :
		public X::XCustomScope
	{
		X::KWARGS* kwParams;
		std::vector<std::string> Keys;
	public:
		PropScope(X::KWARGS* kw):kwParams(kw)
		{
		}
		inline virtual int AddOrGet(const char* name, bool bGetOnly) override
		{
			std::string strName(name);
			Keys.push_back(strName);
			return  (int)Keys.size()-1;
		}
		inline virtual bool Get(int idx, X::Value& v, void* lValue = nullptr) override
		{
			return false;
		}
		inline virtual bool Set(int idx, X::Value& v) override
		{
			kwParams->Add(Keys[idx].c_str(), v,true);
			return true;
		}
	};
}