# Libraries
import smtplib, ssl
import pyautogui
import socket
import time
import imghdr
import os
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\fourbrick\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
from PIL import Image

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
myScreenshot.save(r'C:\Users\fourbrick\Desktop\proj\AKL\read\SS-'+a+'.png')

# the keywords matching part
img = Image.open('SS-'+a+'.png')
text = tess.image_to_string(img)
with open('sample.txt',mode ='w') as file:
    file.write(text)

fh = open('sample.txt', 'r')
count=0
word=input('input the Keyword to be matched : ')

L=fh.readlines()

for i in L:
    L2=i.split()
    L3=[x.lower() for x in L2]
    if word in L3:
        count+=1

print(count,'match found')

# the email part
if count > 0:
    sender_email = 'dhinpooja69@gmail.com'
    reciever_email = 'dhinpooja69@gmail.com'
    password = 'ThinkPad#1234567890'
    subject = 'Python!'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = reciever_email
    msg['Subject'] = subject

    email_body = 'This is a test email sent by python. Isnt that cool?'
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
        os.remove(r'C:\Users\fourbrick\Desktop\proj\AKL\read\SS-'+a+'.png')
