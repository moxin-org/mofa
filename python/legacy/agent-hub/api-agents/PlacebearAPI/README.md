# Placebear Image Placeholder API

## Overview
The Placebear service provides a simple API for generating placeholder images of bears with specified dimensions. This is useful for developers who need placeholder images for testing or prototyping purposes.

## Usage
To use the Placebear API, construct a URL with the desired width and height, and make a GET request to retrieve the image.

### Example Code
```python
import requests

width = 800
height = 600
url = f"https://placebear.com/g/{width}/{height}"

response = requests.get(url)

if response.status_code == 200:
    # Save the image data to a file
    with open('bear_placeholder.jpg', 'wb') as f:
        f.write(response.content)
    print("Bear image saved successfully")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Parameters
- `width`: The desired width of the placeholder image (in pixels).
- `height`: The desired height of the placeholder image (in pixels).

### Output
The API returns a bear image in JPEG format, which can be saved to a file or used directly in your application.

## Error Handling
If the request fails, the status code will be printed to help diagnose the issue.

## Dependencies
- Python `requests` library for making HTTP requests.

## Installation
To install the required dependency, run:
```bash
pip install requests
```

## License
This project uses the Placebear API, which is free to use for placeholder images.