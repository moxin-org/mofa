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

import xlang,os,inspect

# Import xMind API from xLang
xMind_Core = xlang.importModule("xMind", thru="lrpc:99023")
root = xMind_Core.GetRootPath()
class xMind:
    # Enum for Status as part of the xMind class
    Ok = 0
    Fail = 1
    Timeout = 2
    Running = 3
    Stopped = 4

    # Internal list to hold registered nodes
    _nodes = []
    _isRunning = False

    class Node:
        def __init__(self, node_type, core_object, func):
            self.type = node_type
            self.id = core_object.ID()
            inputCount = len(core_object.inputs())
            if inputCount >0:
                self.hasInputs = True
            else:
                self.hasInputs = False
            self.core_object = core_object
            self.func = func
    @classmethod
    def RunNonInputNodes(cls):
        """
        Check all nodes where self.hasInputs is False and call their self.func without parameters.
        """
        hasNodes = False
        for node in cls._nodes:
            if not node.hasInputs:
                real_func = getattr(node.func, '_original_function', node.func)
                real_func(owner=node.core_object)
                hasNodes = True
        return hasNodes

    @staticmethod
    def Function(*args, **kwargs):
        def decorator(func):
            # Use the real function name if 'name' is not provided in kwargs
            if 'name' not in kwargs:
                kwargs['name'] = func.__name__
            module_name = func.__module__
            file_name = func.__globals__['__file__']
            # Call xMind_Core.Function and store the returned object
            moduleName ="xMind"
            nodeName = kwargs['name'];
            core_object = xMind_Core.Function(*args, **kwargs)()
            xMind_Core.AddNode(moduleName,nodeName,core_object)

            # Store the original function in the wrapper
            def wrapper(*f_args, **f_kwargs):
                xMind_Core.log(f"Calling Function: {func.__name__}")
                return func(*f_args, **f_kwargs, owner=core_object)

            # Attach the original function and the core object to the wrapper
            wrapper._original_function = func
            wrapper.coreObject = core_object  # Store the core object

            # Register the node in the list
            xMind._nodes.append(xMind.Node("Function", core_object, wrapper))
            xMind_Core.log(f"Function registered: {kwargs['name']}")
            # we return the xMindCore object to Python
            return core_object
        return decorator

    @staticmethod
    def Agent(*args, **kwargs):
        def decorator(func):
            # Use the real function name if 'name' is not provided in kwargs
            if 'name' not in kwargs:
                kwargs['name'] = func.__name__
            module_name = func.__module__
            file_name = func.__globals__['__file__']
            # Call xMind_Core.Agent and store the returned object
            moduleName ="xMind"
            nodeName = kwargs['name'];
            core_object = xMind_Core.Agent(*args, **kwargs)()
            xMind_Core.AddNode(moduleName,nodeName,core_object,"")

            # Store the original function in the wrapper
            def wrapper(*f_args, **f_kwargs):
                xMind_Core.log(f"Calling Agent: {func.__name__}")
                return func(*f_args, **f_kwargs, owner=core_object)

            # Attach the original function and the core object to the wrapper
            wrapper._original_function = func
            wrapper.coreObject = core_object  # Store the core object

            # Register the node in the list
            xMind._nodes.append(xMind.Node("Agent", core_object, wrapper))
            xMind_Core.log(f"Agent registered: {kwargs['name']}")
            # we return the xMindCore object to Python
            return core_object
        return decorator

    @staticmethod
    def Action(*args, **kwargs):
        def decorator(func):
            # Use the real function name if 'name' is not provided in kwargs
            if 'name' not in kwargs:
                kwargs['name'] = func.__name__
            module_name = func.__module__
            file_name = func.__globals__['__file__']
            # Call xMind_Core.Action and store the returned object
            moduleName ="xMind"
            nodeName = kwargs['name'];
            core_object = xMind_Core.Action(*args, **kwargs)()
            xMind_Core.AddNode(moduleName,nodeName,core_object)
            # Store the original function in the wrapper
            def wrapper(*f_args, **f_kwargs):
                xMind_Core.log(f"Calling Action: {func.__name__}")
                return func(*f_args, **f_kwargs, owner=core_object)

            # Attach the original function and the core object to the wrapper
            wrapper._original_function = func
            wrapper.coreObject = core_object  # Store the core object

            # Register the node in the list
            xMind._nodes.append(xMind.Node("Action", core_object, wrapper))
            xMind_Core.log(f"Action registered: {kwargs['name']}")
            # we return the xMindCore object to Python
            return core_object
        return decorator

    @staticmethod
    def Graph():
        """
        Create and return a new graph using xMind_Core.Graph().
        """
        graph = xMind_Core.Graph()
        xMind_Core.AddGraph(graph)
        return graph

    @classmethod
    def Stop(cls):
        cls._isRunning = False
    
    @staticmethod
    def MainLoop(pacing_time =10):
        """
        Main loop that continues as long as xMind_Core.IsRunning() returns True.
        Detects events and processes them accordingly.
        """
        xMind._isRunning = True
        xMind_Core.log("MainLoop: Starting...")

        cur_pacing_time = pacing_time
        # Get the list of node IDs
        node_ids = [node.id for node in xMind._nodes]
        sub_Id = xMind_Core.SubscribeEvents(node_ids)
        while xMind._isRunning and xMind_Core.IsRunning():
            # Detect events
            events = xMind_Core.PullEvents(sub_Id,cur_pacing_time)
            cur_pacing_time = pacing_time #keep same pacing time
            if not isinstance(events,list):
                hasNodes = xMind.RunNonInputNodes()
                if hasNodes:
                    cur_pacing_time = 0 # Call PullEvents immediately  
                continue
            # Process each event
            for event in events:
                node_id, input_pin_index, data = event
                node = next((n for n in xMind._nodes if n.id == node_id), None)

                if node:
                    real_func = getattr(node.func, '_original_function', node.func)
                    if node.type == "Function":
                        real_func(data)
                    else:
                        real_func(owner=node.core_object)
        xMind_Core.UnsubscribeEvents(sub_Id)
        xMind_Core.log("MainLoop: Stopping...")

    @staticmethod
    def log(*args, **kwargs):
        xMind_Core.log(*args, **kwargs)
    
    @staticmethod
    def importBlueprint(yamlBlueprint):
        # Check if yamlBlueprint is an absolute path
        if not os.path.isabs(yamlBlueprint):
            # Get the caller's file path
            caller_frame = inspect.stack()[1]
            caller_module = inspect.getmodule(caller_frame[0])
            caller_file_path = caller_module.__file__
            caller_dir = os.path.dirname(os.path.abspath(caller_file_path))
            yamlBlueprint = os.path.join(caller_dir, yamlBlueprint)
        
        # Load the blueprint using xMind_Core
        xMind_Core.LoadBlueprintFromFile(yamlBlueprint)

