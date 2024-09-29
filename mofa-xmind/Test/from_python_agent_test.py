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

import xlang
import time
xMind = xlang.importModule("xMind",thru="lrpc:99023")
root = xMind.GetRootPath()
print(root)

xMind_Running =3
xMind_Ok = 0
owner = None

@xMind.Agent(inputs=[{"name":"input"}],name="AgentA")
def AgentFirst():
	xMind.log("AgentFirst: Start")
	while owner.isRunning() == xMind_Running:
		inputData = owner.waitInput()
		if inputData[0] == xMind_Ok:
			data = inputData[2]
			xMind.log("AgentFirst LLM->: ",data)
	xMind.log("AgentFirst: Stop")

@xMind.Action(outputs=[{"name":"output"}],name="ActionB")
def ActionFirst():
	xMind.log("ActionFirst: Start")
	while owner.isRunning() == xMind_Running:
		xMind.log("Input a prompt to ask AgentFirst:")
		prompt = input()
		if prompt == '!quit':
			owner.graph.stop()
			break
		else:
			owner.pushToOutput(0,prompt)
	xMind.log("ActionFirst: Stop")


graph = xMind.Graph()
graph.addNode(ActionFirst)
graph.addNode(AgentFirst)

graph.connect("ActionB","AgentA")
graph.run()


def main_event_loop():
	print("Starting the non-blocking loop...")
	while True:
		time.sleep(0.1) 

# graph.waitToStop()
# input()
main_event_loop()
xMind.log("Done")