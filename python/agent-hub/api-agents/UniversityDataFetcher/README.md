# University Search API Integration

This Python script demonstrates how to interact with the [Universities API](http://universities.hipolabs.com) to search for universities by name and country. The API returns university details in JSON format, including domains, web pages, and country information.

## Features
- **Search Universities**: Query universities by name and country.
- **JSON Response Handling**: Process the API response to extract university data.
- **Error Handling**: Check for failed requests and display the status code.

## Usage

### Prerequisites
- Python 3.x
- `requests` library (install via `pip install requests`)

### Example Code
```python
import requests

# Define the API endpoint with search parameters
url = "http://universities.hipolabs.com/search?name=middle&country=turkey"
response = requests.get(url)

if response.status_code == 200:
    # Process the JSON response
    universities = response.json()
    for university in universities:
        print(f"Name: {university['name']}")
        print(f"Country: {university['country']}")
        print(f"Web Pages: {', '.join(university['web_pages'])}")
        print("---")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Output Example
```
Name: Middle East Technical University
Country: Turkey
Web Pages: http://www.metu.edu.tr
---
Name: Middle East Technical University Northern Cyprus Campus
Country: Turkey
Web Pages: http://www.ncc.metu.edu.tr
---
```

## Error Handling
- If the request fails (e.g., due to network issues or invalid parameters), the script prints the status code for debugging.

## API Reference
For more details on the API, refer to the [Universities API documentation](http://universities.hipolabs.com).