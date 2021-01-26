import smtplib, ssl
from email.mime.text import MIMEText

def bot_message(user, password, recipient):
    sent_from = user 
    to = recipient

    message = "Yo dis STONK BOT 🤖 Hope I make tendies :p"

    msg = MIMEText(message,  _charset='UTF-8')
    msg['Subject'] = 'STONK BOT 🤖'
    msg['From'] = sent_from
    msg['To'] = to

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:


            server.login(user, password)
            server.sendmail(sent_from, to, msg.as_string())
            print("mail successfully sent")
    except:
        print('Something went wrong...')

def send (user, password, recipient, text_message):
    sent_from = user
    to = recipient
    
    msg = MIMEText(text_message,  _charset='UTF-8')
    msg['Subject'] = 'STONK BOT 🤖'
    msg['From'] = sent_from
    msg['To'] = to

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:


            server.login(user, password)
            server.sendmail(sent_from, to, msg.as_string())
            print("mail successfully sent")
    except:
        print('Something went wrong...')