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

x =10
yes = isinstance(x,int)

import xMind
import pandas as pd
import test_lib
py_ret = test_lib.hello_xMind(xMind)
xlang_ret = to_xlang(py_ret)
yes = isinstance(xlang_ret,dict)
yes = isinstance(xlang_ret,(dict,list))
xlang_ret.set("test_key","this is a key")
root = xMind.GetRootPath()
xMind.log("Root path: ",root)
@xMind.Function(Name="Start",
	Prompt="any prompt",
	EnvType ="Local"
	)
def Start():
	myName = owner.name
	xMind.log(myName, ",input a sentence to start the graph:")
	str0 = input()
	return str0

@xMind.Function()
def PassOne(input1):
	xMind.log("PassOne:",input1)
	return ["From PassOne",input1]

@xMind.Function(Name="PassTwo")
def PassTwo(input1):
	xMind.log("PassTwo:",input1)
	return ["From PassTwo",input1]


graph = xMind.Graph()
graph.addNode(Start)
graph.addNode(PassOne,"P1")
graph.addNode(PassTwo,"P2")
graph.addNode(PassOne,"P3")
graph.connect("Start","P1")
graph.connect("P1","output","P2","input")
graph.connect("P2","P3")
graph.startOnce()

print("Done")