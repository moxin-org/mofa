# BaconMockup API Integration

This Python script demonstrates how to dynamically generate placeholder images of meat products (e.g., bacon) using the [BaconMockup API](https://baconmockup.com/). The API allows you to specify the dimensions of the placeholder image via URL parameters.

## Features
- Dynamically generates placeholder images of meat products.
- Supports custom width and height dimensions.
- Simple and lightweight integration using the `requests` library.

## Usage

### Prerequisites
- Python 3.x
- `requests` library (install via `pip install requests`)

### Code Example
```python
import requests

# Define the dimensions of the placeholder image
width = 800
height = 600

# Construct the API URL
url = f"https://baconmockup.com/{width}/{height}"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the image to a file
    with open('bacon_placeholder.jpg', 'wb') as f:
        f.write(response.content)
    print("Bacon placeholder image saved successfully")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Output
- The script saves the generated placeholder image as `bacon_placeholder.jpg` in the current directory.
- Prints a success message if the image is saved successfully or an error message if the request fails.

## Input/Output Specifications

### Input
- `width` (integer): The width of the placeholder image in pixels.
- `height` (integer): The height of the placeholder image in pixels.

### Output
- A JPEG image file (`bacon_placeholder.jpg`) with the specified dimensions.

## Error Handling
- The script checks the HTTP status code of the response and prints an error message if the request fails.

## Notes
- The API is free to use and does not require authentication.
- Ensure you have an active internet connection to make requests to the API.