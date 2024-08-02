import os
import dspy

from mae.apps.crewai.manage import create_agent, create_task, setup_crew
from mae.apps.reasoner.reasoner import ReasonerModule, ReasonerRagModule, ReasonerWebSearchModule

from mae.apps.self_refine.self_refine import SelfRefineModule, SelfRefineRagModule
from mae.kernel.tools.tool_mapping import agent_tools
from mae.kernel.utils.util import make_crewai_tool
from mae.utils.envs.util import init_proxy_env, set_api_keys, init_env


def run_crewai_agent(crewai_config: dict):
    print(crewai_config)
    if crewai_config.get('envs', None) is not None:
        for env_name, env_value in crewai_config['envs'].items():
            os.environ[env_name] = env_value
    model_config, agents_config, tasks_config, other_config = crewai_config.get('model'), crewai_config.get(
        'agents'), crewai_config.get('tasks'), crewai_config.get('other')
    proxy_url = other_config.get('proxy_url', None)
    if proxy_url is not None:
        init_proxy_env(is_proxy=True, proxy_url=proxy_url)
    set_api_keys(**model_config)
    agents = {}
    for agent_config in crewai_config['agents']:
        tool_names = agent_config.get('tools', None)
        tools = agent_tools(tool_names=tool_names)
        all_tools = []
        for func in tools:
            try:
                all_tools.append(make_crewai_tool(func))
            except Exception as e:
                print(e)
                all_tools.append(func)
        agent = create_agent(
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=agent_config['backstory'],
            verbose=agent_config['verbose'],
            allow_delegation=agent_config['allow_delegation'],

            tools=all_tools,
        )
        agents[agent_config['name']] = agent

    tasks = []
    for task_config in crewai_config['tasks']:
        task = create_task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=agents.get(task_config.get('agent')),
            max_inter=task_config['max_inter'],
            human_input=task_config.get('human_input', False),
        )
        tasks.append(task)

    crew = setup_crew(
        agents=list(agents.values()),
        tasks=tasks,
        memory=crewai_config.get('crewai_config').get('memory', False),
        process=crewai_config.get('crewai_config').get('process', None),
        manager_agent=agents.get(crewai_config.get('crewai_config').get('manager_agent', None))
    )
    result = crew.kickoff()
    return result


def run_dspy_agent(inputs: dict):
    if inputs.get('proxy_url', None) is not None:
        init_proxy_env(proxy_url=inputs.get('proxy_url', 'http://127.0.0.1:10809'))
    if inputs.get('envs', None) is not None: init_env(env=inputs['envs'])
    if inputs.get('model_api_key') !='ollama':
        turbo = dspy.OpenAI(model=inputs.get('model_name'), max_tokens=inputs.get('model_max_tokens'),
                            api_key=inputs.get('model_api_key'), api_base=inputs.get('model_api_url', None))
    else:
        turbo = dspy.OllamaLocal(model=inputs.get('model_name','llama3'),
                            base_url=inputs.get('model_api_url', 'http://127.0.0.1:11434'),)
    dspy.settings.configure(lm=turbo)
    answer = ''
    if inputs.get('agent_type') == 'reasoner':
        if 'module_path' in inputs and 'model_name' in inputs:
            os.environ["OPENAI_API_KEY"] = inputs.get('model_api_key')
            reasoner = ReasonerRagModule(module_path=inputs.get('module_path', None),
                                         model_name=inputs.get('rag_model_name', None),
                                         files_path=inputs.get('files_path', None),
                                         encoding=inputs.get('encoding', 'utf-8'),
                                         chunk_size=inputs.get('chunk_size', 256),
                                         pg_connection=inputs.get('pg_connection', None),
                                         rag_search_num=inputs.get('rag_search_num', 3),
                                         context=inputs.get('context', None),
                                         temperature=inputs.get('temperature', 0.7),
                                         objective=inputs.get('objective', None),
                                         specifics=inputs.get('specifics', None),
                                         actions=inputs.get('context', None), results=inputs.get('results', None),
                                         example=inputs.get('example', None), answer=inputs.get('answer', None),
                                         input_fields=inputs.get('input_fields', None),is_upload_file=inputs.get('is_upload_file',False),
                                         collection_name=inputs.get('collection_name', 'my_docs'),
                                         )
        elif 'serper_api_key' in inputs:
            reasoner = ReasonerWebSearchModule(role=inputs.get('role', ''), backstory=inputs.get('backstory', ''),
                                      context=inputs.get('context', None), objective=inputs.get('objective', None),
                                      specifics=inputs.get('specifics', None),
                                      actions=inputs.get('actions', None), results=inputs.get('results', None),
                                      example=inputs.get('example', None), answer=inputs.get('answer', None),
                                      temperature=inputs.get('temperature', 0.7),
                                      input_fields=inputs.get('input_fields', {'web_context':"Results from the internet query."}),
                                      serper_api_key = inputs.get('serper_api_key'),
                                      search_num=inputs.get('search_num', 10),
                                      search_engine_timeout=inputs.get('search_engine_timeout', 5),
                                      )

        else:
            reasoner = ReasonerModule(role=inputs.get('role', ''), backstory=inputs.get('backstory', ''),
                                      context=inputs.get('context', None),objective=inputs.get('objective',None),specifics=inputs.get('specifics',None),
                                      actions=inputs.get('actions', None),results=inputs.get('results',None),example=inputs.get('example',None),answer=inputs.get('answer',None),
                                      temperature=inputs.get('temperature', 0.7), input_fields=inputs.get('input_fields',None))


        answer = reasoner.forward(question=inputs.get('task'),kwargs=inputs.get('input_fields',{}))
    if inputs.get('agent_type') == 'self_refine':
        if 'module_path' in inputs and 'model_name' in inputs:
            os.environ["OPENAI_API_KEY"] = inputs.get('model_api_key')
            self_refine = SelfRefineRagModule(module_path=inputs.get('module_path', None),
                                         model_name=inputs.get('rag_model_name', None),
                                         files_path=inputs.get('files_path', None),
                                         encoding=inputs.get('encoding', 'utf-8'),
                                         chunk_size=inputs.get('chunk_size', 256),
                                         pg_connection=inputs.get('pg_connection', None),
                                         rag_search_num=inputs.get('rag_search_num', 3),
                                         context=inputs.get('context', None),
                                         temperature=inputs.get('temperature', 0.7),
                                         objective=inputs.get('objective', None),
                                         specifics=inputs.get('specifics', None),
                                         actions=inputs.get('context', None), results=inputs.get('results', None),
                                         example=inputs.get('example', None), answer=inputs.get('answer', None),
                                         input_fields=inputs.get('input_fields', None),
                                         is_upload_file=inputs.get('is_upload_file', False),
                                         collection_name=inputs.get('collection_name', 'my_docs'),
                                         )
        else:

            self_refine = SelfRefineModule(role=inputs.get('role', ''), backstory=inputs.get('backstory', ''),
                                        max_iterations=inputs.get('max_iterations', 4),context=inputs.get('context',None),
                                             temperature=inputs.get('temperature',0.7),)
        answer = self_refine.forward(question=inputs.get('task'),)
    return answer

