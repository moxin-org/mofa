from typing import List
from crewai import Agent, Task, Crew, Process


def create_agent(role: str, goal: str, backstory: str, verbose: bool=True, allow_delegation: bool=False, tools: List = None,) -> Agent:
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=verbose,
        allow_delegation=allow_delegation,
        tools=tools,
    )


def create_task(description: str, agent: Agent, expected_output: str=None,max_inter:int=None,human_input:bool=False) -> Task:
    if expected_output is None:
        expected_output = ''

    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        human_input=human_input,
        max_inter=max_inter
    )
    return task


def setup_crew(agents: List[Agent], tasks: List[Task], verbose: bool=False,process:str=None,memory:bool=False,manager_agent:str=None) -> Crew:
    if process is None:
        process = Process.sequential
    if process == 'hierarchical':
        process = Process.hierarchical
    if manager_agent is not None:
        agents = [agent for agent in agents if agent != manager_agent]
    return Crew(
        agents=agents,
        tasks=tasks,
        verbose=verbose,
        process=process,memory=memory,
        manager_agent=manager_agent
    )


def kickoff_crew(crew: Crew):
    return crew.kickoff()
