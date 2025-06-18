# MemoryAugmentedChatAssistant for dora-rs (mofa agent compliant)
# Dependencies: openai, mem0, pyyaml, python-dotenv
# Ensure you have /configs/agent.yml and .env.secret with correct keys

import os
import yaml
from openai import OpenAI
from mem0 import Memory
from dotenv import load_dotenv
from mofa.agent_build.base.base_agent import MofaAgent, run_agent

def load_yaml_config():
    config_path = os.path.join(os.path.dirname(__file__), 'configs', 'agent.yml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration file: {e}")

@run_agent
def run(agent: MofaAgent):
    # Enforce agent input API (single string input)
    try:
        user_message = agent.receive_parameter('user_input')
        if not isinstance(user_message, str):
            raise ValueError('Input "user_input" must be a string.')
    except Exception as e:
        agent.send_output('assistant_response', {'error': f'Input error: {e}'})
        return

    # Load environment and config safely
    try:
        load_dotenv('.env.secret')
        openai_api_key = os.getenv('OPENAI_API_KEY')
        mem0_api_key = os.getenv('MEM0_API_KEY')

        if not openai_api_key:
            raise EnvironmentError('OPENAI_API_KEY not found in environment.')
        if not mem0_api_key:
            raise EnvironmentError('MEM0_API_KEY not found in environment.')
    except Exception as e:
        agent.send_output('assistant_response', {'error': f'Environment error: {e}'})
        return

    # Load YAML agent config
    try:
        config = load_yaml_config()
        openai_model = config.get('openai', {}).get('model', 'gpt-4o-mini')
        openai_temperature = float(config.get('openai', {}).get('temperature', 0.7))
        memory_limit = int(config.get('memory', {}).get('limit', 3))
        user_id_default = config.get('memory', {}).get('user_id_default', 'default_user')
    except Exception as e:
        agent.send_output('assistant_response', {'error': f'Config error: {e}'})
        return

    # Use user_id_default unless one is provided via optional dataflow (advance: not required in this spec)
    user_id = user_id_default

    # Initialize external clients
    try:
        openai_client = OpenAI(api_key=openai_api_key)
        memory = Memory(api_key=mem0_api_key)
    except Exception as e:
        agent.send_output('assistant_response', {'error': f'API client initialization error: {e}'})
        return

    # Retrieve relevant memories
    try:
        relevant_memories = memory.search(query=user_message, user_id=user_id, limit=memory_limit)
        mem_results = relevant_memories.get('results', [])
        if not isinstance(mem_results, list):
            raise ValueError('mem0 search returned non-list results.')
        memories_str = "\n".join(f"- {str(entry.get('memory', ''))}" for entry in mem_results) if mem_results else "(No previous memories found.)"
    except Exception as e:
        agent.send_output('assistant_response', {'error': f'Memory retrieval error: {e}'})
        return

    # Construct LLM prompt with system prompt
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # LLM call
    try:
        response = openai_client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=openai_temperature
        )
        ai_content = response.choices[0].message.content.strip()
    except Exception as e:
        agent.send_output('assistant_response', {'error': f'LLM API error: {e}'})
        return

    # Store conversation in memory
    try:
        messages.append({"role": "assistant", "content": ai_content})
        memory.add(messages, user_id=user_id)
    except Exception as e:
        # Memory storage error should not prevent output of result
        agent.send_output('assistant_response', {'warning': f'Response generated, but memory saving failed: {e}', 'response': ai_content})
        return

    # Output
    agent.send_output(
        agent_output_name='assistant_response',
        agent_result=ai_content
    )

def main():
    agent = MofaAgent(agent_name='MemoryAugmentedChatAssistant')
    run(agent=agent)

if __name__ == '__main__':
    main()
