# Waifu.Pics API Integration

This project provides Python examples for interacting with the Waifu.Pics API to retrieve single or multiple image URLs based on specified categories and types.

## Features

1. **Single Image Retrieval**: Fetch a single image URL by specifying a category (e.g., "waifu", "neko") and type ("sfw" or "nsfw").
2. **Multiple Image Retrieval**: Fetch up to 30 image URLs via a POST request, with an optional exclusion list.

## API Endpoints

### 1. Get a Single Image
- **Endpoint**: `GET https://api.waifu.pics/{type}/{category}`
  - `type`: "sfw" or "nsfw"
  - `category`: Image category (e.g., "waifu", "neko")

### 2. Get Multiple Images
- **Endpoint**: `POST https://api.waifu.pics/many/{type}/{category}`
  - `type`: "sfw" or "nsfw"
  - `category`: Image category (e.g., "waifu", "neko")
  - **Payload**: Optional `exclude` list for URLs to exclude.

## Usage Examples

### Single Image Retrieval
```python
import requests

# Example: Get SFW "waifu" category image
url = "https://api.waifu.pics/sfw/waifu"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Image URL: {data['url']}")  # Extract and use the image URL
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Multiple Image Retrieval
```python
import requests

# Example: Get NSFW "neko" category images, excluding some URLs
url = "https://api.waifu.pics/many/nsfw/neko"
payload = {
    "exclude": ["https://i.waifu.pics/qUY7BBo.jpg"]  # Optional exclusion list
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(f"Image URLs: {data['files']}")  # Process the list of URLs
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

## Error Handling
- The examples include basic error handling to check the HTTP status code and print an error message if the request fails.

## Dependencies
- Python `requests` library for making HTTP requests.

## Installation
```bash
pip install requests
```

## Contribution
Feel free to contribute by submitting pull requests or opening issues for bugs and feature requests.