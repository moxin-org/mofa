import os
import time
import dspy
from mofa.agent_build.crewai.manage import create_agent, create_task, setup_crew
from mofa.agent_build.reasoner.reasoner import ReasonerModule, ReasonerRagModule, ReasonerWebSearchModule
from mofa.agent_build.self_refine.self_refine import SelfRefineModule, SelfRefineRagModule
from mofa.kernel.tools.tool_mapping import agent_tools
from mofa.kernel.utils.util import make_crewai_tool
from mofa.utils.envs.util import init_proxy_env, set_api_keys, init_env

from mofa.agent_build.base.llm_client import SiliconFlowClient


def run_crewai_agent(crewai_config: dict):
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


def run_dspy_agent(agent_config: dict):
    if agent_config.get('proxy_url', None) is not None:
        init_proxy_env(proxy_url=agent_config.get('proxy_url', 'http://127.0.0.1:10809'))
    if agent_config.get('envs', None) is not None: init_env(env=agent_config['envs'])
    if agent_config.get('model_api_key') != 'ollama' and "deepseek" not in agent_config.get('model_name',"openai"):
        turbo = dspy.OpenAI(model=agent_config.get('model_name'), max_tokens=agent_config.get('model_max_tokens'),
                            api_key=agent_config.get('model_api_key'), api_base=agent_config.get('model_api_url', None))
    elif agent_config.get('model_api_key') == 'ollama':
        turbo = dspy.OllamaLocal(model=agent_config.get('model_name', 'llama3'),
                                 base_url=agent_config.get('model_api_url', 'http://127.0.0.1:11434'), )
    else:
        turbo = SiliconFlowClient(
            model=agent_config.get('model_name'),
            api_key=agent_config.get('model_api_key'),
            base_url=agent_config.get('model_api_url', None),
        )

    dspy.settings.configure(lm=turbo)
    answer = ''
    if agent_config.get('agent_type') == 'reasoner':
        if agent_config.get('rag_enable') == 'True' or agent_config.get('rag_enable') == 'true' or agent_config.get('rag_enable') == True:
            os.environ["OPENAI_API_KEY"] = agent_config.get('model_api_key')
            os.environ["OPENAI_API_KEY"] = agent_config.get("rag_model_api_key")
            os.environ["OPENAI_API_BASE"] = agent_config.get("rag_model_api_url")
            reasoner = ReasonerRagModule(module_path=agent_config.get('module_path', None),
                                         model_name=agent_config.get('rag_model_name', None),
                                         files_path=agent_config.get('files_path', None),
                                         encoding=agent_config.get('encoding', 'utf-8'),
                                         chunk_size=agent_config.get('chunk_size', 256),
                                         pg_connection=agent_config.get('pg_connection', None),
                                         rag_search_num=agent_config.get('rag_search_num', 3),
                                         context=agent_config.get('context', None),
                                         temperature=agent_config.get('temperature', 0.7),
                                         objective=agent_config.get('objective', None),
                                         specifics=agent_config.get('specifics', None),
                                         actions=agent_config.get('context', None), results=agent_config.get('results', None),
                                         example=agent_config.get('example', None), answer=agent_config.get('answer', None),
                                         input_fields=agent_config.get('input_fields', None), is_upload_file=agent_config.get('is_upload_file', False),
                                         collection_name=agent_config.get('collection_name', 'my_docs'),
                                         chroma_path=agent_config.get('chroma_path', None),
                                         )
        elif agent_config.get('web_enable') == 'True' or agent_config.get('web_enable') == 'true' or agent_config.get('web_enable') == True:
            reasoner = ReasonerWebSearchModule(role=agent_config.get('role', ''), backstory=agent_config.get('backstory', ''),
                                               context=agent_config.get('context', None), objective=agent_config.get('objective', None),
                                               specifics=agent_config.get('specifics', None),
                                               actions=agent_config.get('actions', None), results=agent_config.get('results', None),
                                               example=agent_config.get('example', None), answer=agent_config.get('answer', None),
                                               temperature=agent_config.get('temperature', 0.7),
                                               input_fields=agent_config.get('input_fields', {'web_context': "Results from the internet query."}),
                                               serper_api_key = agent_config.get('serper_api_key'),
                                               search_num=agent_config.get('search_num', 10),
                                               search_engine_timeout=agent_config.get('search_engine_timeout', 5),
                                               )

        else:
            reasoner = ReasonerModule(role=agent_config.get('role', ''), backstory=agent_config.get('backstory', ''),
                                      context=agent_config.get('context', None), objective=agent_config.get('objective', None), specifics=agent_config.get('specifics', None),
                                      actions=agent_config.get('actions', None), results=agent_config.get('results', None), example=agent_config.get('example', None), answer=agent_config.get('answer', None),
                                      temperature=agent_config.get('temperature', 0.7), input_fields=agent_config.get('input_fields', None))


        answer = reasoner.forward(question=agent_config.get('task'), kwargs=agent_config.get('input_fields', {}))
    if agent_config.get('agent_type') == 'self_refine':
        if 'module_path' in agent_config and 'model_name' in agent_config:
            os.environ["OPENAI_API_KEY"] = agent_config.get('model_api_key')
            self_refine = SelfRefineRagModule(module_path=agent_config.get('module_path', None),
                                              model_name=agent_config.get('rag_model_name', None),
                                              files_path=agent_config.get('files_path', None),
                                              encoding=agent_config.get('encoding', 'utf-8'),
                                              chunk_size=agent_config.get('chunk_size', 256),
                                              pg_connection=agent_config.get('pg_connection', None),
                                              rag_search_num=agent_config.get('rag_search_num', 3),
                                              context=agent_config.get('context', None),
                                              temperature=agent_config.get('temperature', 0.7),
                                              objective=agent_config.get('objective', None),
                                              specifics=agent_config.get('specifics', None),
                                              actions=agent_config.get('context', None), results=agent_config.get('results', None),
                                              example=agent_config.get('example', None), answer=agent_config.get('answer', None),
                                              input_fields=agent_config.get('input_fields', None),
                                              is_upload_file=agent_config.get('is_upload_file', False),
                                              collection_name=agent_config.get('collection_name', 'my_docs'),
                                              )
        else:

            self_refine = SelfRefineModule(role=agent_config.get('role', ''), backstory=agent_config.get('backstory', ''),
                                           max_iterations=agent_config.get('max_iterations', 4), context=agent_config.get('context', None),
                                           temperature=agent_config.get('temperature', 0.7), )
        answer = self_refine.forward(question=agent_config.get('task'), )
    return answer

def run_dspy_or_crewai_agent(agent_config:dict):
    try:
        if 'agents' not in agent_config.keys():
            result = run_dspy_agent(agent_config=agent_config)
        else:
            result = run_crewai_agent(crewai_config=agent_config)
        return result
    except Exception as e :
        print(e)
        raise RuntimeError(str(e))

