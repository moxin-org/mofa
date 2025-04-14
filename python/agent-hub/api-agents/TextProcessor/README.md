# Exude API Client

A Python client for interacting with the Exude API, which provides text processing capabilities including stopping word filtering, stemming, and swear word detection.

## Features
- **Text Processing**: Filter stopping words and stem words using the Porter algorithm.
- **File Processing**: Upload text files for bulk processing.
- **Swear Word Detection**: Identify and flag inappropriate language in text.

## Installation
No additional installation is required beyond the `requests` library, which is typically included in Python environments.

```bash
pip install requests
```

## Usage

### Text Processing
Filter stopping and stemmed words from a given text.

```python
import requests

url = "https://exude.herokuapp.com/api/exude"
text_data = {
    "data": "This is a sample text containing stopping words and connections connecting"
}

response = requests.post(url, data=text_data)

if response.status_code == 200:
    processed_data = response.json()
    print(processed_data.get('filtered_data'))
else:
    print(f"Request to {url} failed with status code: {response.status_code}")
```

### File Processing
Process a text file to filter stopping and stemmed words.

```python
import requests

url = "https://exude.herokuapp.com/api/exude-file"
files = {'file': open('document.txt', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    file_results = response.json()
    print(file_results.get('filtered_content'))
else:
    print(f"File processing failed with status code: {response.status_code}")
```

### Swear Word Detection
Detect swear words in a given text.

```python
import requests

url = "https://exude.herokuapp.com/api/exude-swear"
payload = {
    "data": "This text contains inappropriate language"
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    detection_results = response.json()
    print(detection_results.get('swear_words'))
else:
    print(f"Swear detection request failed with status code: {response.status_code}")
```

## Output Examples
- **Text Processing**: `sample text contain connect`
- **File Processing**: Filtered content of the uploaded file.
- **Swear Word Detection**: List of detected swear words.

## Testing
A Postman collection is available for testing the API endpoints. Refer to the [Exude API documentation](https://exude.herokuapp.com) for more details.

## Contribution
Contributions are welcome! Please submit a pull request or open an issue for any improvements or bug fixes.