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

#include "Callable.h"

namespace xMind
{
	class Function :public Callable
	{
		BEGIN_PACKAGE(Function)
			ADD_BASE(Callable);
		END_PACKAGE
		virtual bool ReceiveData(SESSION_ID sessionId, int inputIndex, X::Value& data) override
		{
			//when receive data, call the real function
			//and push the result to the next node
			//only support one input data
			if (m_implObject.IsObject())
			{
				X::ARGS params(1);
				params.push_back(data);
				X::KWARGS kwParams;
				auto* pXPack = Function::APISET().GetProxy(this);
				X::Value varOwner = X::Value(pXPack);
				kwParams.Add("owner", varOwner);
				X::Value retData = m_implObject.ObjCall(params, kwParams);
				PushToOutput(sessionId,0, retData);
			}
			else
			{
				PushEvent(inputIndex,data);
			}
			return true;
		}
		inline bool Create()
		{
			return true;
		}
		inline virtual bool Run() override
		{
			return true;
		}
		inline virtual void Stop() override
		{
		}
		virtual X::Value Clone() override
		{
			Function* pFuncObj = new Function();
			pFuncObj->Copy(this);
			auto* pXPack = Function::APISET().GetProxy(pFuncObj);
			X::Value retValue = X::Value(pXPack);
			return retValue;
		}
		public:
		Function()
		{
			m_inputs.push_back(Pin{ "input" });
			m_outputs.push_back(Pin{ "output" });
		}

	};
}