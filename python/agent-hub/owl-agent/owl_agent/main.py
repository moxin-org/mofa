from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
# 加载环境变量
load_dotenv('.env.secret')
from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.toolkits import (
    ExcelToolkit,
    SearchToolkit,
    FileWriteToolkit,
    CodeExecutionToolkit,
)
from camel.types import ModelPlatformType, ModelType
from camel.societies import RolePlaying
from camel.logger import set_log_level

from owl.utils import run_society




def construct_society(question: str) -> RolePlaying:
    r"""Construct a society of agents based on the given question.

    Args:
        question (str): The task or question to be addressed by the society.

    Returns:
        RolePlaying: A configured society of agents ready to address the question.
    """

    # Create models for different components
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.DEEPSEEK,
            model_type=ModelType.DEEPSEEK_CHAT,
            model_config_dict={"temperature": 0},
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.DEEPSEEK,
            model_type=ModelType.DEEPSEEK_CHAT,
            model_config_dict={"temperature": 0},
        ),
    }

    # Configure toolkits
    tools = [
        *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
        SearchToolkit().search_duckduckgo,
        SearchToolkit().search_wiki,
        SearchToolkit().search_baidu,
        *ExcelToolkit().get_tools(),
        *FileWriteToolkit(output_dir="./").get_tools(),
    ]

    # Configure agent roles and parameters
    user_agent_kwargs = {"model": models["user"]}
    assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}

    # Configure task parameters
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    # Create and return the society
    society = RolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
        output_language="Chinese",
    )

    return society




@run_agent
def run(agent: MofaAgent):
    user_query = agent.receive_parameter('user_query')
    load_dotenv('.env.secret')
    society = construct_society(user_query)
    answer, chat_history, token_count = run_society(society)
    print('answer:', answer)
    print('chat_history:', chat_history)
    print('token_count:', token_count)
    agent.send_output(agent_output_name='owl_agent_result', agent_result=answer)

def main():
    agent = MofaAgent(agent_name='DeepInquire')
    run(agent=agent)

if __name__ == "__main__":
    main()
