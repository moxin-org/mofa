# NumbersAPI Integration

This project demonstrates how to interact with the NumbersAPI to retrieve interesting facts about numbers, including trivia, math-related facts, and historical events for specific dates.

## Features
- Retrieve trivia facts for specific numbers.
- Fetch mathematical properties or significance of numbers.
- Get historical events for specific dates.

## Code Examples

### Trivia Fact Retrieval
```python
import requests
url = "http://numbersapi.com/42/trivia"
response = requests.get(url)

if response.status_code == 200:
    print(f"Fact: {response.text}")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Math Fact Retrieval
```python
import requests
url = "http://numbersapi.com/5/math"
response = requests.get(url)

if response.status_code == 200:
    print(f"Math Fact: {response.text}")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Date Fact Retrieval
```python
import requests
url = "http://numbersapi.com/4/11/date"
response = requests.get(url)

if response.status_code == 200:
    print(f"On this date: {response.text}")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

## Usage
1. Ensure you have the `requests` library installed:
```bash
pip install requests
```
2. Run any of the provided code snippets to fetch facts from the NumbersAPI.

## Error Handling
The code includes basic error handling to notify if the API request fails.

## Output
- For trivia and math facts, the output is a text string containing the fact.
- For date facts, the output is a text string describing historical events on the specified date.