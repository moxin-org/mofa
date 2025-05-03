# Stack Exchange API Integration

This project demonstrates interaction with the Stack Exchange API v2.3 to retrieve questions, user profiles, and perform advanced searches. The API supports various endpoints to fetch or modify content programmatically.

## Features

1. **Fetch Recent Questions**: Retrieve the most recent questions from Stack Overflow.
2. **Get User Profiles**: Fetch user details by their IDs, including reputation and activity stats.
3. **Advanced Search**: Perform complex searches for questions based on criteria like tags, titles, and dates.

## Installation

No additional installation is required beyond the standard Python libraries:
```bash
pip install requests
```

## Usage

### Fetch Recent Questions
```python
import requests

url = "https://api.stackexchange.com/2.3/questions"
params = {
    "site": "stackoverflow",
    "order": "desc",
    "sort": "activity",
    "pagesize": 5
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        print(item['title'])
else:
    print(f"Request failed with status code: {response.status_code}")
```

### Get User Profiles
```python
import requests

user_id = "12345"
url = f"https://api.stackexchange.com/2.3/users/{user_id}"
params = {
    "site": "stackoverflow",
    "filter": "!9_bDDxJY5"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data['items'][0]['display_name'])
else:
    print(f"Request failed with status code: {response.status_code}")
```

### Advanced Search
```python
import requests

url = "https://api.stackexchange.com/2.3/search/advanced"
params = {
    "site": "stackoverflow",
    "q": "Python",
    "accepted": "true",
    "pagesize": 3
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        print(item['link'])
else:
    print(f"Request failed with status code: {response.status_code}")
```

## Output Examples

### Recent Questions
- Example question title 1
- Example question title 2

### User Profile
- Display Name: John Doe

### Advanced Search Results
- [Link to question 1](https://stackoverflow.com/q/12345)
- [Link to question 2](https://stackoverflow.com/q/67890)

## Contribution

Feel free to contribute by submitting pull requests or opening issues for improvements or additional features.