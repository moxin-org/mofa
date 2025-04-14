# Urban Dictionary API Integration

This Python script fetches definitions and examples for a given word from the Urban Dictionary API. It processes the JSON response to display the first three definitions and their examples.

## Features
- Fetches definitions and examples for a specified word.
- Displays the first three definitions and their examples.
- Handles HTTP request errors gracefully.

## Usage
1. Replace the `word` variable with the desired word or phrase.
2. Run the script to fetch and display the definitions.

### Example Output
```
Definition: A term used to describe something that is typical or representative.
Example: "This is just an example of how things work here."
```

## Code Explanation
- **Imports**: The `requests` library is used to make HTTP requests.
- **URL Construction**: The API endpoint is constructed using the provided word.
- **Response Handling**: The script checks the HTTP status code and processes the JSON response if successful.
- **Output**: The first three definitions and examples are printed to the console.

## Error Handling
- If the request fails, the script prints the status code and the failed URL.

## Requirements
- Python 3.x
- `requests` library (install via `pip install requests`)

## Example
```python
import requests

word = "example"  # Replace with desired word
url = f"https://api.urbandictionary.com/v0/define?term={word}"
response = requests.get(url)

if response.status_code == 200:
    # Process the JSON response here to extract definitions
    data = response.json()
    for definition in data.get('list', [])[:3]:  # Show first 3 definitions
        print(f"Definition: {definition.get('definition')}")
        print(f"Example: {definition.get('example')}\n")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```