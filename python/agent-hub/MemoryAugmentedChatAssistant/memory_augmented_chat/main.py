# Dependencies: pip install mem0ai openai
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
from mem0 import Memory
import os

@run_agent
def run(agent: MofaAgent):
    try:
        # All nodes call this input for stateless operation
        user_input = agent.receive_parameter('user_input')
        user_id = agent.receive_parameter('user_id') if 'user_id' in agent.input_ports else 'default_user'

        # Type enforcement
        message = str(user_input)
        user_id = str(user_id) if user_id else 'default_user'

        # Retrieve relevant memories
        memory = Memory()
        relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
        memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories.get('results', []))

        # Generate system prompt
        system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        openai_client = OpenAI()
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        if not hasattr(response, 'choices') or not response.choices:
            raise RuntimeError("OpenAI API did not return any response choices.")
        assistant_response = response.choices[0].message.content

        # Save the conversation to Memory
        messages.append({"role": "assistant", "content": assistant_response})
        memory.add(messages, user_id=user_id)

        # Output the assistant's response
        agent.send_output(
            agent_output_name='assistant_response',
            agent_result=str(assistant_response)
        )
    except Exception as e:
        # Error containment: return error as output, do not raise
        agent.send_output(
            agent_output_name='assistant_response',
            agent_result=f"Error: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='MemoryAugmentedChatAssistant')
    run(agent=agent)

if __name__ == '__main__':
    main()
