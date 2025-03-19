# Diabetes Risk Assessment API

## Overview
This Python script sends a POST request to the Diabetes Risk Assessment API to get a diabetes risk report based on provided health parameters.

## Installation
No installation is required. Ensure you have Python 3.x installed.

## Usage
1. Replace `'你自己的AppCode'` with your actual AppCode.
2. Modify the `querys` string to include the desired health parameters.
3. Run the script.

```bash
python diabetes_risk_assessment.py
```

## Parameters
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

## Output
The script prints the diabetes risk report in JSON format.

## Example Output
```json
{
  "riskLevel": "Low",
  "recommendations": [
    "Maintain a healthy diet",
    "Exercise regularly"
  ]
}
```

## Dependencies
- `urllib3`
- `uuid`

## License
This project is licensed under the MIT License.
