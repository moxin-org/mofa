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

import requests

# Replace with your actual OpenAI API key
api_key = "Your Key"

# Define the endpoint URL
url = "https://api.openai.com/v1/chat/completions"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the data (payload) for the request
data = {
    "model": "gpt-4",  # Specify the model you want to use
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain how to use Python with REST API."}
    ],
    "temperature": 0.7
}

data = {
	"model":"gpt-4",
	"temperature":0.700000,
	"messages":[
	{
	"role":"user",
	"content":"1+1=2?"
}
]
}
# Send the POST request to the OpenAI API
response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the response
    completion = response.json()
    print(completion)
    print(completion['choices'][0]['message']['content'])
else:
    # Print the error if the request was not successful
    print(f"Error: {response.status_code}, {response.text}")
