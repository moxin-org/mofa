# Planning Agent in MoFA

## 1. Functionality
The Planning Agent is capable of breaking down complex large tasks into smaller subtasks, while annotating task dependencies and execution methods (synchronous or asynchronous).

## 2. 
1. Input a large task and obtain a list of decomposed smaller tasks.
2. Get structured task information, including task descriptions, dependencies, and execution types.

## 3. Output Format
The agent returns tasks in the following JSON structure:

```json
{
  "tasks": [
    {
      "task_id": "1",
      "description": "Install the necessary development tools (e.g., IDE, compiler)",
      "classification": "synchronous",
      "is_synchronous": true,
      "dependencies": []
    },
    // ... more tasks ...
  ]
}
```

## 4. Running the Agent
1. Install the MoFA project package.
2. Run `dora up && dora build planning_agent.yml && dora start planning_agent.yml`
3. Open another command terminal and run terminal-input. Then, input the task you want to decompose.
4. There are two types of output:
   - By default, a user-friendly output will be displayed directly in the terminal.
   - A JSON format output is also available, which can be used as input for the next node, facilitating further processing.
   You can modify the function in the `scripts/planning_agent.py` file; comments have already been provided.

## Reference
- [agentic_patterns](https://github.com/neural-maze/agentic_patterns)