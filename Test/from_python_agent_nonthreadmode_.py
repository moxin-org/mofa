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

from xMind import xMind
import time

@xMind.Agent(inputs=[{"name":"input"}],name="AgentA")
def AgentFirst(owner):
	inputData = owner.waitInput()
	if inputData[0] == xMind.Ok:
		data = inputData[2]
		xMind.log("AgentFirst LLM->: ",data)

@xMind.Action(outputs=[{"name":"output"}],name="ActionB")
def ActionFirst(owner):
	xMind.log("Wait a prompt to input to ask AgentFirst:")
	print("Input a prompt to ask AgentFirst:")
	prompt = input()
	if prompt == '!quit':
		xMind.Stop()
	else:
		xMind.log("Your Prompt:",prompt)
		owner.pushToOutput(0,prompt)


graph = xMind.Graph()
graph.addNode(ActionFirst)
graph.addNode(AgentFirst)

graph.connect("ActionB","AgentA")
graph.run()
print("Entern Mainloop")
xMind.MainLoop()

xMind.log("Done")