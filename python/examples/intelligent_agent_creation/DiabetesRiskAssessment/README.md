# Diabetes Risk Assessment API

## Overview
This Python script sends a POST request to the Diabetes Risk Assessment API to get a diabetes risk report based on provided health parameters.

## Installation
No specific installation is required. Ensure you have Python 3.x installed and the following libraries:
- `urllib3`
- `uuid`

## Usage
1. Replace `'你自己的AppCode'` with your actual AppCode.
2. Modify the `querys` string to include the desired health parameters.
3. Run the script.

### Parameters
- `age`: Age of the individual.
- `sex`: Gender of the individual (男 for male, 女 for female).
- `weight`: Weight in kilograms.
- `height`: Height in meters.
- `systolicPressure`: Systolic blood pressure.
- `diastolicPressure`: Diastolic blood pressure.
- `familyHistoryOfDiabetes`: Family history of diabetes.
- `historyOfHyperglycemia`: History of hyperglycemia.
- `intakeOfVegetablesAndFruits`: Daily intake of vegetables and fruits.
- `waist`: Waist circumference in centimeters.
- `dailyExerciseTime`: Daily exercise time in minutes.

### Example
```python
import urllib3
import uuid

host = 'https://hdl.market.alicloudapi.com'
path = '/diabetes/getReport'
method = 'POST'
appcode = '你自己的AppCode'
querys = 'age=18&sex=男&type=diabetesRisk&weight=70&height=1.85&systolicPressure=130&diastolicPressure=100&familyHistoryOfDiabetes=否,旁系亲属（爷爷/外公、奶奶/姥姥、姑、姨、叔、伯、舅、表/堂兄妹）,直系亲属（父母、兄妹、子女）&historyOfHyperglycemia=否&intakeOfVegetablesAndFruits=每天&waist=40&dailyExerciseTime=10'
url = host + path + '?' + querys
http = urllib3.PoolManager()
headers = {
    'X-Ca-Nonce': str(uuid.uuid4()),
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': 'APPCODE ' + appcode
}
post_data = '{"age":"18","sex":"男","weight":"70","height":"1.85","BMI":"25","type":"diabetesRisk","historyOfHyperglycemia":"否","intakeOfVegetablesAndFruits":"每天","waist":"40","dailyExerciseTime":"10","systolicPressure":"130","diastolicPressure":"100","familyHistoryOfDiabetes":"否"}'
response = http.request('POST', url, body=post_data, headers=headers)
content = response.data.decode('utf-8')
if (content):
    print(content)
```

## Output
The script prints the diabetes risk report received from the API.

## Contributing
Contributions are welcome! Please ensure to follow the coding standards and include appropriate documentation.
