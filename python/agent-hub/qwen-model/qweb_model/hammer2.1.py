from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download
import os
from huggingface_hub import snapshot_download

# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'
#
# snapshot_download(
#     repo_id="MadeAgents/Hammer2.1-7b",
#     local_dir="./models/hammer2.1-7b",
#     cache_dir="./hf_cache",
#     resume_download=True,
#     max_workers=20
# )

download_cmd = """./hfd.sh MadeAgents/Hammer2.1-7b \
  --tool aria2c \
  -x 8 \
  -j 5 \
  --local-dir models/hammer2.1-7b
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/qwen-model/models/hammer2.1-7b'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")

# Example conversation
messages = [
    {"role": "user", "content": "What's the weather like in New York?"},
    {"role": "assistant","content": '```\n{"name": "get_weather", "arguments": {"location": "New York, NY ", "unit": "celsius"}\n```'},
    {"role": "tool", "name": "get_weather", "content": '{"temperature": 72, "description": "Partly cloudy"}'},
    {"role": "user", "content": "Now, search for the weather in San Francisco."}
]

# Example function definition (optional)
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "description": "The unit of temperature to return"}
            },
            "required": ["location"]
        }
    },
    {
        "name": "respond",
        "description": "When you are ready to respond, use this function. This function allows the assistant to formulate and deliver appropriate replies based on the input message and the context of the conversation. Generate a concise response for simple questions, and a more detailed response for complex questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "The content of the message to respond to."}
            },
            "required": ["message"]
        }
    }
]

inputs = tokenizer.apply_chat_template(messages, tools=tools, add_generation_prompt=True, return_dict=True, return_tensors="pt")
inputs = {k: v.to(model.device) for k, v in inputs.items()}
out = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(out[0][len(inputs["input_ids"][0]):], skip_special_tokens=True))
