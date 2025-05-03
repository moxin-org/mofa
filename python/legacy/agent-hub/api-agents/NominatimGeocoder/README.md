# Nominatim API Integration

This project demonstrates the integration of the Nominatim API for geocoding, reverse geocoding, and OSM object lookup functionalities.

## Features
1. **Geocoding**: Convert place names into geographic coordinates.
2. **Reverse Geocoding**: Convert geographic coordinates into human-readable addresses.
3. **OSM Object Lookup**: Retrieve address details for OSM objects using their unique IDs.

## Installation
```bash
pip install requests
```

## Usage

### Geocoding (Search API)
```python
import requests

url = "https://nominatim.openstreetmap.org/search"
params = {
    'q': 'Eiffel Tower',
    'format': 'json'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if data:
        first_result = data[0]
        print(f"Coordinates: {first_result.get('lat')}, {first_result.get('lon')}")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### Reverse Geocoding (Reverse API)
```python
import requests

url = "https://nominatim.openstreetmap.org/reverse"
params = {
    'lat': '48.8588443',
    'lon': '2.2943506',
    'format': 'json'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if data:
        print(f"Address: {data.get('display_name')}")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### OSM Object Lookup (Lookup API)
```python
import requests

url = "https://nominatim.openstreetmap.org/lookup"
params = {
    'osm_ids': 'R146656,W104393803,N240109189',
    'format': 'json'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if data:
        for item in data:
            print(f"OSM Object: {item.get('osm_type')} {item.get('osm_id')}")
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

## Notes
- Include a proper `User-Agent` header in production:
  ```python
  headers = {'User-Agent': 'Your-App-Name'}
  response = requests.get(url, params=params, headers=headers)
  ```
- Respect the usage policy (max 1 request/second).