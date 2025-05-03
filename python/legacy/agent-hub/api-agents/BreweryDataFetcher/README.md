# Open Brewery DB API Integration

## Overview
This Python script demonstrates how to interact with the Open Brewery DB API, a public REST API that provides data about breweries, cideries, and brewpubs. The script fetches brewery data from the API and processes the JSON response.

## Features
- **API Endpoint**: Fetches data from `https://api.openbrewerydb.org/v1/breweries`.
- **Response Handling**: Checks the HTTP status code and processes the JSON response if successful.
- **Error Handling**: Logs an error message if the request fails.

## Usage
1. Ensure you have the `requests` library installed:
   ```bash
   pip install requests
   ```
2. Run the script:
   ```python
   import requests
   url = "https://api.openbrewerydb.org/v1/breweries"
   response = requests.get(url)

   if response.status_code == 200:
       # Process the JSON response here to extract brewery data
       # Example: breweries = response.json()
       #          for brewery in breweries:
       #              print(brewery.get('name'))
       pass
   else:
       print(f"Request to {url} failed with status code: {response.status_code}")
   ```

## Input/Output
- **Input**: None (the script makes a GET request to the API endpoint).
- **Output**: JSON data containing brewery information (if the request is successful).

## Error Handling
- The script checks the HTTP status code and prints an error message if the request fails.

## Example Output
```json
[
  {
    "id": "1",
    "name": "Brewery 1",
    "brewery_type": "micro",
    "street": "123 Main St",
    "city": "Portland",
    "state": "Oregon",
    "postal_code": "97201",
    "country": "United States",
    "phone": "503-555-1234",
    "website_url": "http://www.brewery1.com"
  },
  {
    "id": "2",
    "name": "Brewery 2",
    "brewery_type": "regional",
    "street": "456 Oak Ave",
    "city": "Denver",
    "state": "Colorado",
    "postal_code": "80202",
    "country": "United States",
    "phone": "303-555-5678",
    "website_url": "http://www.brewery2.com"
  }
]
```

## Dependencies
- Python 3.x
- `requests` library

## License
This script is provided under the MIT License. The Open Brewery DB API is a public API, and its usage is subject to its own terms and conditions.