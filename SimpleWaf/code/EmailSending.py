import smtplib
from email.mime.text import MIMEText

#gmail = wafProject1304@gmail.com
#password = wafProject
WAF_EMAIL = "wafProject1304@gmail.com"

### password got via google, needed to generate 'app password' ###
### does not important for the prj, just need this for login ###
PASSWORD_FOR_APP = "xskr xsmy nwmh hdux"

def send_verification_mail_when_signup(destEmail:str,code:str,host_name:str):
    send_email(destEmail,"Verification Mail",
               f"Thank you for signup for our WAF.\n"
               f"Your site is: {host_name}\n"
               f"This is your signup code: {code}")
def send_attack_alert_email(destEmail:str,attack:str,host_name:str):
    host_name = host_name.replace("<","&lt;")
    msg = f"This is a msg from FireCastle WAF.\n"\
           f" we detected the attack {attack}, at your website at this address: {host_name}.\n"\
           f"Go see the log file for specific details. https://wafWeb1304.com/logFile"
    send_email(destEmail,"Attack detected!",msg)
def send_email(destEmail:str,subject:str,bodyMsg:str):
    """sends email - general func"""
    # Create the message
    msg = MIMEText(bodyMsg)

    # Set the email headers
    msg['Subject'] = subject
    msg['From'] = WAF_EMAIL
    msg['To'] = destEmail

    # SMTP server configuration for Outlook
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(WAF_EMAIL, PASSWORD_FOR_APP)
        server.sendmail(WAF_EMAIL, destEmail, msg.as_string())

if __name__ == '__main__':
    ### tests ###
    #replace to your gmail to recive the emails
    GMAIL_FOR_TESTING = "noamar1234567@gmail.com"
    send_attack_alert_email(GMAIL_FOR_TESTING, "SLOW_LORIS", "mySite.com")
    send_verification_mail_when_signup(GMAIL_FOR_TESTING, "123456", "mySite.com")