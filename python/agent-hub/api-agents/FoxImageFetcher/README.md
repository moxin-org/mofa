# Random Fox Image API Fetcher

This Python script fetches random fox images from the public API endpoint provided by `randomfox.ca`.

## Features
- Fetches a random fox image URL from the API.
- Handles HTTP response status codes to ensure successful requests.

## Usage
1. Ensure you have the `requests` library installed:
   ```bash
   pip install requests
   ```
2. Run the script:
   ```python
   import requests

   url = "https://randomfox.ca/floof"
   response = requests.get(url)

   if response.status_code == 200:
       fox_data = response.json()
       print(f"Fox image URL: {fox_data['image']}")
   else:
       print(f"Request to {url} failed with status code: {response.status_code}")
   ```

## Output
- On success, the script prints the URL of a random fox image (e.g., `images/42.jpg`).
- On failure, it prints the HTTP status code for debugging.

## Example Output
```
Fox image URL: https://randomfox.ca/images/42.jpg
```

## Notes
- The API returns JSON data with an `image` key containing the URL.
- The total number of available fox images is 124 (as indicated by "Fox Count: 124").