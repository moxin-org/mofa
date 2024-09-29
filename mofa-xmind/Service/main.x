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

from xlang_http import http
import xMind thru 'lrpc:99023'
import json
from xlang_os import utils
# import agent_service

xMind.logV("Service Starting")
args = get_args()
if args.size()>0:
	port = args[0]
else:
	port = 9901
srv = http.Server()
srv.SupportStaticFiles = True
www_root = "webpages"
srv.StaticRoots = [www_root]
srv.StaticIndexFile = "index.html"

xMind.logV("root folder:",www_root,",pid=",pid())


session_histories ={}

# Link: http://localhost:9901/api/loadGraph?fileName=D:\Github\xMind\Schema\compositeAgent.yml
@srv.route("/api/loadGraph")
def loadGraph():
	params = req.params
	fileName = params["fileName"]
	isOK = xMind.LoadBlueprintFromFile(fileName)
	return [str(isOK,format=True), "text/json"]
# Link: http://localhost:9901/api/queryGraph
@srv.route("/api/queryGraph")
def queryGraph():
	graphJson = xMind.QueryAgentFlow()
	return [graphJson, "text/json"]


# this call will keep session history
@srv.route("/api/chat/completions")
def chat_completions():
    params = json.loads(req.body)
    resp = xMind.ChatRequest(params)
    return [str(resp,format=True), "text/json"]

@srv.route("/api/completions")
def completions():
    params = json.loads(req.body)
    resp = xMind.CompletionRequest(params)
    return [str(resp,format=True), "text/json"]


# Link: http://localhost:9901/api/rootagents
@srv.route("/api/rootagents")
def query_rootagents():
    rootAgents = xMind.GetRootAgents()
    return [str(rootAgents,format=True), "text/json"]

xMind.logV("xMind WebServer Started,port:",port)
srv.listen("::", port)
