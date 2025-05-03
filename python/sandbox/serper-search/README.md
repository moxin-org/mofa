# How Sandbox Works

In Sandbox, we have created a simple dataflow for you to test your agent

The dataflow is called mofa_dataflow.yml

```yaml
nodes:
  - id: terminal-input #Add a terminal-input node to handle input and output through CLI.
    build: pip install -e ../../../node-hub/terminal-input --index-url https://mirrors.aliyun.com/pypi/simple
    path: dynamic
    outputs:
      - data
    inputs:
      agent_response: <your-agent-name>/<agent-result1-name>
      
      #in case you have multiple output, you will add more agent_response fields. 
      
  - id: <your agent name> 
    build: pip install -e ../../<your-agent-folder-in-agent-hub> --index-url https://mirrors.aliyun.com/pypi/simple
    path: <the-folder-name-where-your-python-code-can-be-found> #usually, it is a subfolder in your agent folder, in which you put in your python code. If so, just the subfoldername, no need to give full path. 

	outputs:
      - <agent-result1-name>
      #in case you have multiple output, you will claim more result names here. 
      
    inputs:
      <input1-name>: terminal-input/data #Your agent take input from terminal, there is where you claim the name of the input.
      
      #in case you have multiple input, you will claim more input names here, they always get input from "terminal-input/data"

env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
```

To test-run your code in the sandbox

At the command line

1.  `cd` to your sandbox folder
2. Setup DORA environment:
   - `dora up`
   - ``dora destroy`
   - `dora up`

4. Build the dataflow:`dora build mofa_dataflow.yml`
5. Run your dataflow:`dora start mofa_dataflow.yml`

The simple dataflow is running now, waiting for your input from terminal-input

7. open another terminal
8. run `terminal-input`
9. input the info that is needed (terminal-input/data).

You will be able to fetch your [log files](./log) and [output info](./output)