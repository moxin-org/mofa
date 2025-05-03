# Colormind API Integration

## Overview
This Python script integrates with the Colormind API to generate color palettes. It supports random color scheme generation or suggestions based on input colors, with support for different color models that rotate daily.

## Features
- **Color Palette Generation**: Fetch random color schemes or get suggestions based on input colors.
- **Customizable Input**: Specify input colors or use placeholders (`"N"`) for random values.
- **Error Handling**: Includes basic error handling for API request failures.

## Usage
1. **Install Required Libraries**:
   ```bash
   pip install requests
   ```

2. **Run the Script**:
   ```python
   import requests

   url = "http://colormind.io/api/"
   data = {
       "model": "default",
       "input": [[44,43,44],[90,83,82],"N","N","N"]
   }

   response = requests.post(url, json=data)

   if response.status_code == 200:
       palette = response.json()['result']
       print("Generated colors:", palette)
   else:
       print(f"Request to {url} failed with status code: {response.status_code}")
   ```

## Input/Output Specifications
- **Input**:
  - `model`: The color model to use (e.g., `"default"`).
  - `input`: A list of 5 items, where each item can be:
    - A list of 3 integers representing RGB values (e.g., `[44,43,44]`).
    - The string `"N"` to indicate a random color.

- **Output**:
  - A list of 5 RGB color values (e.g., `[[R,G,B], [R,G,B], ...]`).

## Example Output
```python
Generated colors: [[44, 43, 44], [90, 83, 82], [120, 150, 200], [200, 180, 160], [50, 60, 70]]
```

## Notes
- The API supports different color models that rotate daily. Check the [Colormind API documentation](http://colormind.io/api/) for more details.
- Ensure you have an active internet connection to use this script.