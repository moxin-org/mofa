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
#include "value.h"
#include "singleton.h"
#include <string>
#include <unordered_map>
#include <mutex>

namespace xMind
{
	class Variable
	{
	private:
		X::Value m_value;
		std::string m_name;
		std::string m_desc;
		std::string m_scope; // use file or module name

	public:
		Variable() = default;
		Variable(const std::string& name, const std::string& desc, 
			const std::string& scope)
			: m_name(name), m_desc(desc), m_scope(scope){}

		const std::string& GetName() const { return m_name; }
		const std::string& GetScope() const { return m_scope; }
		const X::Value& GetValue() const { return m_value; }
		const std::string& GetDesc() const { return m_desc; }
		Variable& SetValue(const X::Value& value) { m_value = value; return *this; }
	};

	class VariableManager : public Singleton<VariableManager>
	{
	private:
		std::unordered_map<std::string, Variable> m_variables;
		std::mutex m_mutex;

		std::string MakeKey(const std::string& scope, const std::string& name) const
		{
			return scope + "::" + name;
		}

	public:
		void Add(const std::string& scope, const std::string& name, const std::string& desc)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			std::string key = MakeKey(scope, name);
			auto var = Variable(name, desc, scope);
			m_variables[key] = Variable(name, desc, scope);
		}
		void Add(const std::string& scope, const std::string& name, 
			const std::string& desc, const X::Value& value)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			std::string key = MakeKey(scope, name);
			m_variables[key] = Variable(name, desc, scope).SetValue(value);
		}
		void Remove(const std::string& scope, const std::string& name)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			std::string key = MakeKey(scope, name);
			m_variables.erase(key);
		}
		void Set(const std::string& scope, const std::string& name, const X::Value& value)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			std::string key = MakeKey(scope, name);
			auto it = m_variables.find(key);
			if (it != m_variables.end())
			{
				it->second.SetValue(value);
			}
		}
		X::Value Query(const std::string& scope, const std::string& name)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			std::string key = MakeKey(scope, name);
			auto it = m_variables.find(key);
			if (it != m_variables.end())
			{
				return it->second.GetValue();
			}
			return X::Value(); // Return a default value if not found
		}
		X::Value Query(const std::string& scope_name)
		{
			std::lock_guard<std::mutex> lock(m_mutex);
			auto it = m_variables.find(scope_name);
			if (it != m_variables.end())
			{
				return it->second.GetValue();
			}
			return X::Value(); // Return a default value if not found
		}
	};
}
