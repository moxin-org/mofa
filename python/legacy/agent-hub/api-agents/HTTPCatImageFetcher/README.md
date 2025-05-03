# HTTP Cat Image Fetcher

A simple Python utility to fetch HTTP status code-themed cat images from the `https://http.cat` service.

## Features
- Fetches cat images associated with HTTP status codes.
- Saves the image locally with a filename corresponding to the status code.
- Handles failed requests gracefully with error messages.

## Installation
No additional installation is required beyond the standard Python libraries. However, ensure you have the `requests` library installed:
```bash
pip install requests
```

## Usage
1. Import the function in your Python script:
```python
from http_cat_fetcher import get_http_cat
```
2. Call the function with the desired HTTP status code:
```python
get_http_cat(404)  # Fetches the cat image for HTTP 404
```

## Example
```python
import requests

def get_http_cat(status_code):
    url = f"https://http.cat/{status_code}.jpg"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the cat image for the requested HTTP status code
        with open(f'http_{status_code}.jpg', 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Request failed for status {status_code}: {response.status_code}")
        return False

# Example usage: Get image for HTTP 404
get_http_cat(404)
```

## Output
- On success, the function saves the cat image locally as `http_[status_code].jpg` and returns `True`.
- On failure, it prints an error message and returns `False`.

## Notes
- The service supports standard HTTP status codes (e.g., 200, 404, 500).
- Ensure you have write permissions in the directory where the script is executed.