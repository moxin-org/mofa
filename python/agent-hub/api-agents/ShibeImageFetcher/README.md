# Shiba Inu Image Fetcher

This Python script fetches random Shiba Inu (shibe) images from the `shibe.online` API.

## Features
- Fetches a specified number of Shiba Inu image URLs.
- Handles HTTP response status codes for error checking.
- Outputs the first image URL from the fetched list.

## Usage
1. Ensure you have the `requests` library installed:
   ```bash
   pip install requests
   ```
2. Run the script:
   ```python
   python shibe_fetcher.py
   ```

## Code Explanation
- The script sends a GET request to the `shibe.online` API endpoint (`http://shibe.online/api/shibes?count=10`).
- If the request is successful (status code 200), it processes the JSON response to extract image URLs.
- The first image URL is printed for demonstration purposes.
- If the request fails, the script prints the error status code.

## Example Output
```
First shibe image URL: https://shibe.online/shibes/1.jpg
```

## Error Handling
- The script checks the HTTP status code and prints an error message if the request fails.

## Dependencies
- `requests` library for making HTTP requests.

## API Reference
- Endpoint: `http://shibe.online/api/shibes`
- Parameters:
  - `count`: Number of shibe images to fetch (default: 1).

## Privacy Policy
For more information, refer to the [Privacy Policy](http://shibe.online/privacy).