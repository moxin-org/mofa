# Random Duck Image API Integration

This Python script demonstrates how to fetch a random duck image from the `random-d.uk` API and save it locally.

## Features
- Fetches a random duck image from the `https://random-d.uk/api/randomimg` endpoint.
- Saves the image to a local file (`random_duck.jpg`).
- Handles HTTP request errors gracefully.

## Usage
1. Ensure you have the `requests` library installed:
   ```bash
   pip install requests
   ```
2. Run the script:
   ```python
   python fetch_random_duck.py
   ```

## Code Explanation
```python
import requests

url = "https://random-d.uk/api/randomimg"
response = requests.get(url)

if response.status_code == 200:
    # The response content contains the image bytes
    # Example: Save the random duck image to a file
    with open('random_duck.jpg', 'wb') as f:
        f.write(response.content)
    print("Saved new duck image!")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Input/Output
- **Input**: None (the script requires no user input).
- **Output**:
  - A file named `random_duck.jpg` saved in the local directory.
  - A success message (`Saved new duck image!`) or an error message if the request fails.

## Error Handling
The script checks the HTTP status code of the response and prints an error message if the request fails (e.g., due to network issues or an invalid endpoint).

## Dependencies
- Python 3.x
- `requests` library

## Example Output
```
Saved new duck image!
```

## Notes
- The API endpoint (`https://random-d.uk/api/randomimg`) is publicly accessible and does not require authentication.
- The script is designed for simplicity and can be extended for more advanced use cases (e.g., batch downloads, image processing).