import os

from dotenv import load_dotenv

from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@run_agent
def run(agent:MofaAgent):
    load_dotenv(dotenv_path='.env.secret')
    sender_email = os.getenv('EMAIL')
    app_password = os.getenv('PASSWORD')

    receiver_email = os.getenv('RECEIVER_EMAIL')

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    data = agent.receive_parameter('email_data')
    message["Subject"] = data
    message.attach(MIMEText(data, "plain"))
    server = smtplib.SMTP(os.getenv('SMTP_SERVER', "smtp.gmail.com"), 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    agent.send_output(agent_output_name='send_email_result', agent_result="Email sent successfully!")

def main():
    agent = MofaAgent(agent_name='send-email-agent')
    run(agent)
if __name__ == "__main__":
    main()
