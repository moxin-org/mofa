import os

from dotenv import load_dotenv

from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv(dotenv_path='.env.secret')
sender_email = os.getenv('SEND_EMAIL')
app_password = os.getenv('SEND_EMAIL_PASSWORD')

receiver_email = os.getenv('RECEIVER_EMAIL')

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
data = 'Hello'
message["Subject"] = data
message.attach(MIMEText(data, "plain"))
server = smtplib.SMTP(os.getenv('SMTP_SERVER', "smtp.gmail.com"), 587)
server.starttls()
server.login(sender_email, app_password)
server.sendmail(sender_email, receiver_email, message.as_string())
server.quit()
