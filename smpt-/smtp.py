import smtplib

from config import password

email_sender = 'binary.nl.noreply@gmail.com'
email_getter = 'ilya@gmail.com'

smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
smtp_server.starttls()

smtp_server.login(email_sender, password)
smtp_server.sendmail(email_sender, email_getter, "Hello lol")