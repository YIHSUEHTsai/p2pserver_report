#!/usr/bin/env python3
import os
import sys
import smtplib
from string import Template
import datetime

from email.utils import formataddr
from email.utils import formatdate
from email.utils import COMMASPACE
from email.header import Header
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import csv
import pandas as pd

#=================================================================================
#send_email()
#=================================================================================
def send_email(sender_name:str, sender_passwd:str, sender_addr:str, smtp_server:str, smtp_port:str,
                recipient_addr: list, subject:str ,html:str, text:str,
                fn: str='last.eml', save: bool=False):
    print ("send_email")

    sender_name = Header(sender_name, 'utf-8').encode()

    email_info = MIMEMultipart('mixed')
    email_info['Date'] = formatdate(localtime=1)
    email_info['From'] = formataddr((sender_name, sender_addr))
    email_info['To'] = COMMASPACE.join(recipient_addr)
    email_info['Subject'] = Header(subject, 'utf-8')
    email_info.preamble = 'This is a multi-part message in MIME format.'

    email_related = MIMEMultipart('related')
    email_info.attach(email_related)

    email_alternative = MIMEMultipart('alternative')
    email_related.attach(email_alternative)

    email_text = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    email_alternative.attach(email_text)

    email_html = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    email_alternative.attach(email_html)

    mail_server = smtplib.SMTP(smtp_server, smtp_port)
    mail_server.ehlo()

    try:
        mail_server.starttls()
        mail_server.ehlo()
    except smtplib.SMTPException as e:
        print(e)

    mail_server.login(sender_addr, sender_passwd)
    mail_server.send_message(email_info)
    mail_server.quit()

    if save:
        with open(fn, 'w') as f:
            f.write(email_root.as_string())

#=================================================================================
#main()
#=================================================================================
if __name__ == "__main__":
    total_bandwidth_threshold = 130002 #Mbit/s

    file = open('file_path_setting.txt', mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()

    report_path = ""
    for line in lines:
        report_path = line

    csv_file = pd.read_csv(report_path + "p2p_list.csv")

    server_bandwidth_csv = open(report_path + 'csv/all_network_bandwidth.csv', newline='')
    rows = csv.reader(server_bandwidth_csv)

    for row in rows:
        current_total_bandwidth = row[int(csv_file['group'][len(csv_file)-1][1:])]

    print (current_total_bandwidth) 
    '''
    if (total_bandwidth_threshold - int(current_total_bandwidth) <= 200000000):
        date = datetime.datetime.now()
        year = date.strftime("%Y")
        month = date.strftime("%m")

        attachments = []
        img_list = []

        date = datetime.datetime.now()
        year = date.strftime("%Y")
        month = date.strftime("%m")

        fp = open("mail_1.txt", "w")
        mail_content = "● Wyze total bandwidth is limited to 3221225472 bit/s." + '<br>' + "● Current total bandwidth is " + current_total_bandwidth + ' bit/s.<br>' + "● Please charge customer the server bandwidth fee." + '<br>'
        fp.write(mail_content)
        fp.close()

        sender_name = "TUTK P2P Server Report"
        sender_addr = "service@tutk.com"
        sender_passwd = "Jabu6729"
        smtp_server = "smtp.office365.com"
        smtp_port = "25"
        #recipient_addr = ['allop@tutk.com', 'christine_liao@tutk.com', 'sean_chu@tutk.com']
        recipient_addr = ['ethan_tsai@tutk.com']

        subject = "Wyze server exceeded the limit of bandwidth notice-(" + str(year) + "/" + str(month) + ")"

        with open("mail_1.txt" ) as f:
	        email_template = f.read()

        text = email_template.format()

        html = """
            <html>
            <head>
            <meta http-equiv="content-type" content="text/html;charset=utf-8" />
            </head>
            <body>
            <font face="verdana" size=2>{}<br/></font>
            </body>
            </html>
            """.format(text)

        send_email(sender_name, sender_passwd, sender_addr, smtp_server, smtp_port,
                recipient_addr, subject, html, text, fn='my.eml', save=False)
    '''
