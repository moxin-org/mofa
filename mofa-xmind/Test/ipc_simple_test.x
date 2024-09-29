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

import xMind thru 'lrpc:99023'

root = xMind.GetRootPath()

def OnReady():
    print("Call from OnReady")
    
xMind.OnReady +=OnReady
xMind.Test()
def CallFromHost(info):
    print("CallFromHost:",info)
    return "Now, from client side with ret"
xTest = xMind.Test(CallFromHost)
print("Done")