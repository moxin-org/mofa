# EmojiHub API Integration

This Python script demonstrates how to interact with the EmojiHub API to retrieve random emojis from the "food-and-drink" category. The API provides access to a collection of emojis, allowing users to fetch random emojis, filter by categories/groups, or retrieve the entire emoji database in JSON format.

## Features
- **Random Emoji Retrieval**: Fetches a random emoji from the specified category (e.g., "food-and-drink").
- **Error Handling**: Checks the HTTP response status code to ensure successful API calls.
- **JSON Processing**: The response can be processed to extract emoji details such as name and HTML code.

## Usage
1. **Installation**: Ensure the `requests` library is installed:
   ```bash
   pip install requests
   ```

2. **Code Execution**: Run the provided Python script to fetch a random emoji from the "food-and-drink" category.
   ```python
   import requests
   url = "https://emojihub.yurace.pro/api/random/category/food-and-drink"
   response = requests.get(url)

   if response.status_code == 200:
       # Process the JSON response here to extract emoji details
       # Example: emoji_data = response.json()
       #          print(f"Name: {emoji_data['name']}, HTML Code: {emoji_data['htmlCode'][0]}")
   else:
       print(f"Request to {url} failed with status code: {response.status_code}")
   ```

## Output
- If the API call is successful (`status_code == 200`), the script will return the emoji details in JSON format.
- If the API call fails, the script will print an error message with the status code.

## Example Output
```json
{
  "name": "hamburger",
  "category": "food-and-drink",
  "group": "food-prepared",
  "htmlCode": ["🍔"],
  "unicode": ["U+1F354"]
}
```

## Notes
- Replace the `url` with other endpoints (e.g., `/api/all`) to fetch different data from the API.
- For more details on available endpoints and parameters, refer to the [EmojiHub API documentation](https://emojihub.yurace.pro/).