# ExchangeRate-API

## Description
This package provides exchange rates for USD using the ExchangeRate-API.

## Installation
```bash
pip install ExchangeRate-API
```

## Usage
```python
from exchangerate_api import ExchangeRateAPI

api = ExchangeRateAPI(api_key='your_api_key')
rates = api.get_exchange_rates()
print(rates)
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
