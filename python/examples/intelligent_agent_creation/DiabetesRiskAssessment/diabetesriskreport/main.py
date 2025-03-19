from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import urllib3
import uuid
import os

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive parameters
        params = agent.receive_parameters(['age', 'sex', 'weight', 'height', 'systolicPressure', 'diastolicPressure', 'familyHistoryOfDiabetes', 'historyOfHyperglycemia', 'intakeOfVegetablesAndFruits', 'waist', 'dailyExerciseTime'])
        
        # Prepare the request data
        bodys = {
            'age': params['age'],
            'sex': params['sex'],
            'weight': params['weight'],
            'height': params['height'],
            'systolicPressure': params['systolicPressure'],
            'diastolicPressure': params['diastolicPressure'],
            'familyHistoryOfDiabetes': params['familyHistoryOfDiabetes'],
            'historyOfHyperglycemia': params['historyOfHyperglycemia'],
            'intakeOfVegetablesAndFruits': params['intakeOfVegetablesAndFruits'],
            'waist': params['waist'],
            'dailyExerciseTime': params['dailyExerciseTime']
        }
        
        # Get appcode from environment variables
        appcode = os.getenv('APPCODE')
        if not appcode:
            raise ValueError('APPCODE environment variable is not set')
        
        # Prepare the URL and headers
        host = 'https://hdl.market.alicloudapi.com'
        path = '/diabetes/getReport'
        querys = f"age={params['age']}&sex={params['sex']}&type=diabetesRisk&weight={params['weight']}&height={params['height']}&systolicPressure={params['systolicPressure']}&diastolicPressure={params['diastolicPressure']}&familyHistoryOfDiabetes={params['familyHistoryOfDiabetes']}&historyOfHyperglycemia={params['historyOfHyperglycemia']}&intakeOfVegetablesAndFruits={params['intakeOfVegetablesAndFruits']}&waist={params['waist']}&dailyExerciseTime={params['dailyExerciseTime']}"
        url = host + path + '?' + querys
        headers = {
            'X-Ca-Nonce': str(uuid.uuid4()),
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'APPCODE ' + appcode
        }
        
        # Make the request
        http = urllib3.PoolManager()
        response = http.request('POST', url, body=str(bodys), headers=headers)
        content = response.data.decode('utf-8')
        
        # Send the output
        agent.send_output(
            agent_output_name='diabetes_risk_report',
            agent_result=content
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='DiabetesRiskAssessment')
    run(agent=agent)

if __name__ == '__main__':
    main()