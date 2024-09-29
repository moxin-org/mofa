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

#include "BaseAgent.h"

namespace xMind
{
	/**
	 * @class CompositeAgent
	 * @brief Represents a composite agent in the xMind framework.
	 *
	 * The CompositeAgent class extends the BaseAgent class to provide functionality for
	 managing a group of agents as a single entity. It includes methods for adding and
	 removing agents from the group, connecting/disconnecting agents, and enqueuing/dequeuing
	 input data.
	 */
	class CompositeAgent : public BaseAgent
	{
		std::vector<X::Value> m_agents;
		public:
			CompositeAgent()
			{
			}
			~CompositeAgent()
			{
			}
	};
}