#
# Copyright (C) 2024 The XLang Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# <END>

import xMind

@xMind.Agent(inputs=[{"name":"input"}])
def AgentFirst():
	inputData = owner.waitInput()
	if inputData[0] == xMind.Ok:
		data = inputData[2]
		xMind.log("AgentFirst LLM->: ",data)

@xMind.Action(outputs=[{"name":"output"}])
def ActionFirst():
	xMind.log("Input a prompt to ask AgentFirst:")
	prompt = input()
	if prompt == '!quit':
		owner.graph.stop()
		break
	else:
		owner.pushToOutput(0,prompt)

graph = xMind.Graph()
graph.addNode(ActionFirst)
graph.addNode(AgentFirst)

graph.connect("ActionFirst","AgentFirst")
graph.run()

graph.waitToStop()
xMind.log("Done")
