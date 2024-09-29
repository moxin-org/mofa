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
#include "BufferedProcessor.h"
namespace xMind
{
    class BaseAction : public BufferedProcessor
    {
        BEGIN_PACKAGE(BaseAction)
            ADD_BASE(BufferedProcessor);
        END_PACKAGE
        
        inline virtual X::Value GetOwner() override
        {
            auto* pXPack = BaseAction::APISET().GetProxy(this);
            return X::Value(pXPack);
        }
    public:
        BaseAction()
        {
        }

        virtual ~BaseAction()
        {
        }
        virtual X::Value Clone() override
        {
            BaseAction* pAction = new BaseAction();
            pAction->Copy(this);
            auto* pXPack = BaseAction::APISET().GetProxy(pAction);
            X::Value retValue = X::Value(pXPack);
            return retValue;
        }
    };
}

