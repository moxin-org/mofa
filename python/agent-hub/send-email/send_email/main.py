import os
from mofa.agent_build.base.base_agent import MofaAgent
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    agent = MofaAgent(agent_name='send-email-agent')
    while True:

        # 设置发件人邮箱地址和密码
        sender_email = os.getenv('EMAIL')
        app_password = os.getenv('PASSWORD')

        # 设置收件人邮箱地址
        receiver_email = os.getenv('RECEIVER_EMAIL')

        # 创建邮件内容
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Python SMTP Test1"
        message.attach(MIMEText(agent.receive_parameter('email_data'), "plain"))
        server = smtplib.SMTP(os.getenv('SMTP_SERVER',"smtp.gmail.com"), 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        agent.send_output(agent_output_name='send_email_result',agent_result="Email sent successfully!")
if __name__ == "__main__":
    main()
