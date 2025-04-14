# Screenshotlayer API Integration

This Python script demonstrates how to use the Screenshotlayer API to capture website screenshots with customizable parameters such as viewport dimensions, full-page capture, and image format.

## Features
- **Customizable Viewport**: Specify the dimensions of the viewport (e.g., `1440x900`).
- **Full-Page Capture**: Enable full-page screenshots by setting `fullpage=1`.
- **Image Format**: Choose the output format (e.g., `PNG`).
- **Error Handling**: Basic error handling for failed API requests.

## Usage
1. Replace `'YOUR_ACCESS_KEY'` with your actual Screenshotlayer API access key.
2. Modify the `url` parameter to the target website you want to capture.
3. Adjust other parameters (`viewport`, `fullpage`, `format`) as needed.

### Example
```python
import requests

url = "http://api.screenshotlayer.com/api/capture"
params = {
    'access_key': 'YOUR_ACCESS_KEY',
    'url': 'https://example.com',
    'viewport': '1440x900',
    'fullpage': 1,
    'format': 'PNG'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    # Process the image URL from response
    # Example: image_url = response.json()['screenshot_url']
    #          print("Screenshot available at:", image_url)
    pass
else:
    print(f"Request failed with status code: {response.status_code}")
```

## Output
- On success, the API returns a JSON response containing the screenshot URL (e.g., `screenshot_url`).
- On failure, the script prints the HTTP status code for debugging.

## Notes
- Ensure you have a valid `access_key` from Screenshotlayer.
- The API may have rate limits or usage restrictions based on your subscription plan.