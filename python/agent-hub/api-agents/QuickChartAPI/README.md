# QuickChart API Integration

This project demonstrates how to use the QuickChart API to generate charts and QR codes dynamically in Python.

## Features
1. **Chart Generation**: Generate bar charts (or other types) with customizable data and dimensions.
2. **QR Code Generation**: Create QR codes with options for size, color, and error correction.

## Installation
No additional installation is required beyond the standard Python libraries:
```bash
pip install requests
```

## Usage

### Chart Generation
```python
import requests

# Example bar chart configuration
chart_config = {
    "type": "bar",
    "data": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "datasets": [{
            "label": "Users",
            "data": [50, 60, 70, 180]
        }]
    }
}

url = "https://quickchart.io/chart"
params = {
    "c": chart_config,
    "width": 500,
    "height": 300
}

response = requests.get(url, params=params)

if response.status_code == 200:
    # Save the chart image
    with open('chart.png', 'wb') as f:
        f.write(response.content)
else:
    print(f"Request failed with status code: {response.status_code}")
```

### QR Code Generation
```python
import requests

qr_data = "https://quickchart.io/documentation/"
url = "https://quickchart.io/qr"
params = {
    "text": qr_data,
    "size": 300,
    "foregroundColor": "navy",
    "backgroundColor": "white",
    "ecLevel": "H"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    # Process and save the QR code image
    with open('qrcode.png', 'wb') as f:
        f.write(response.content)
else:
    print(f"QR code request failed with status code: {response.status_code}")
```

## Output
- `chart.png`: Generated bar chart image.
- `qrcode.png`: Generated QR code image.

## Customization
- **Charts**: Modify `chart_config` to change chart type, labels, or data.
- **QR Codes**: Adjust `params` for size, colors, or error correction level.

## Error Handling
- Both snippets include basic error handling to log failed requests.

## Dependencies
- `requests`: For making HTTP requests to the QuickChart API.

## Notes
- Ensure the QuickChart API endpoints (`https://quickchart.io/chart` and `https://quickchart.io/qr`) are accessible from your environment.
- For more customization options, refer to the [QuickChart documentation](https://quickchart.io/documentation/).