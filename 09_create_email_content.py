#!/usr/bin/env python3

# -*- coding: utf-8 -*-

'''
Simple Python 3 module for sending emails
with attachments through an SMTP server.

@author: michael hong
'''
#coding=utf-8
import locale
import datetime
import csv

import os
import smtplib
import getpass

from email.utils import formataddr
from email.utils import formatdate
from email.utils import COMMASPACE

from email.header import Header
from email import encoders

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime

import pandas as pd
import sys
now_time = datetime.datetime.now()

start2 = now_time + datetime.timedelta(days=-2)
start2_format = start2.strftime('%Y/%m/%d')
start7 = now_time + datetime.timedelta(days=-8)
start7_format = start7.strftime('%Y/%m/%d')

def send_email(sender_name: str, sender_addr: str, smtp: str, port: str,
               recipient_addr: list, subject: str, html: str, text: str,
               img_list: list=[], attachments: list=[],
               fn: str='last.eml', save: bool=False):

    passwd = ('Jabu6729')

    sender_name = Header(sender_name, 'utf-8').encode()

    msg_root = MIMEMultipart('mixed')
    msg_root['Date'] = formatdate(localtime=1)
    msg_root['From'] = formataddr((sender_name, sender_addr))
    msg_root['To'] = COMMASPACE.join(recipient_addr)
    msg_root['Subject'] = Header(subject, 'utf-8')
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    msg_related = MIMEMultipart('related')
    msg_root.attach(msg_related)

    msg_alternative = MIMEMultipart('alternative')
    msg_related.attach(msg_alternative)

    msg_text = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    msg_alternative.attach(msg_text)

    msg_html = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    msg_alternative.attach(msg_html)

    for i, img in enumerate(img_list):
        with open(img, 'rb') as fp:
            msg_image = MIMEImage(fp.read())
            msg_image.add_header('Content-ID', '<image{}>'.format(i))
            msg_related.attach(msg_image)

    for attachment in attachments:
        fname = os.path.basename(attachment)

        with open(attachment, 'rb') as f:
            msg_attach = MIMEBase('application', 'octet-stream')
            msg_attach.set_payload(f.read())
            encoders.encode_base64(msg_attach)
            msg_attach.add_header('Content-Disposition', 'attachment',
                                  filename=(Header(fname, 'utf-8').encode()))
            msg_root.attach(msg_attach)

    mail_server = smtplib.SMTP(smtp, port)
    mail_server.ehlo()

    try:
        mail_server.starttls()
        mail_server.ehlo()
    except smtplib.SMTPException as e:
        print(e)

    mail_server.login(sender_addr, passwd)
    mail_server.send_message(msg_root)
    mail_server.quit()

    if save:
        with open(fn, 'w') as f:
            f.write(msg_root.as_string())

if __name__ == '__main__':
    report_path = sys.argv[2]

    csv_file = pd.read_csv(report_path + "p2p_list.csv")
    csv_path = report_path + "csv/"

    f_g1v4 = csv_path + "all_network_bandwidth.csv"
    f_g1v5 = csv_path + "all_device_login.csv"
    o_g1_v4 = csv.reader(open(f_g1v4, 'r'))
    o_g1_v5 = csv.reader(open(f_g1v5, 'r'))



    group_number = 0
    if (len(csv_file)%3 == 0):
        group_number = len(csv_file)/3
    else:
        group_number = len(csv_file)/3 + 1

    o_all_v5 = next(o_g1_v5)
    o_all_v4 = next(o_g1_v4)
    fp = open("mail.txt", "w")
    mail_content = "Total Device Login : " + o_all_v5[int(group_number)] + " (#)" + '<br>'
    fp.write(mail_content)

    csv_file = pd.read_csv(report_path+"csv/max_bandwidth.csv")
    sum_total_max_bandwidth = 0
    for index in range(int(group_number)):
        group = "g" + str(index+1)
        for index in range(len(csv_file)):
            if (csv_file['group'][index] == group and csv_file['server'][index] == "sum"):
                sum_total_max_bandwidth = sum_total_max_bandwidth + int(csv_file['Network Bandwidth(Mbit/s)'][index])

    mail_content = "Total Average Network Bandwith : " + o_all_v4[int(group_number)] + " (Mbit/s)  ," + "Total Max Network Bandwith : "+ str(sum_total_max_bandwidth) +  " (Mbit/s) " + '<br>'
    fp.write(mail_content)


    for index in range(int(group_number)):
        group = "g" + str(index+1)
        for csv_index in range(len(csv_file)):
            if (csv_file['group'][csv_index] == group and csv_file['server'][csv_index] == "sum"):
                total_max_bandwidth = csv_file['Network Bandwidth(Mbit/s)'][csv_index]

        #print ("G" + str(index+1)+o_all_v4[int(index)])
        mail_content = "G" + str(index+1) + " Total Average Network Bandwith: " + o_all_v4[int(index)] + " (Mbit/s)  ," + "Total Max Network Bandwith:" + str(total_max_bandwidth) + " (Mbit/s) " +'<br>'
        fp.write(mail_content)
    
    fp.close()

    # Usage:
    sender_name = 'TUTK P2P Server Report'
    sender_addr = 'service@tutk.com'
    smtp = 'smtp.office365.com'
    port = '25'

    if (sys.argv[1] == "tutk"):
        print ("tutk")
        #recipient_addr = ['ethan_tsai@tutk.com']
        #recipient_addr = ['ethan_tsai@tutk.com','nick_lee@tutk.com']
        recipient_addr = ['allop@tutk.com']
    elif (sys.argv[1] == "wyze"):
        print ("wyze")
        #recipient_addr = ['allop@tutk.com','scott_yang@tutk.com','tyuan@wyze.com','sean_chu@tutk.com','leona_wu@tutk.com','inna_guo@tutk.com']
    subject = 'Wyze P2P Server Weekly Status'+ " " + "(" +start7_format + "~" + start2_format + ")"
    
    with open("mail.txt" ) as f:
	    email_template = f.read()
    
    text = email_template.format()
    
    html =  """
            <html>
            <head>
            <meta http-equiv="content-type" content="text/html;charset=utf-8" />
            </head>
            <body>
            <font face="verdana" size=2>
            """
    html = html + text +"</font>"
    
    for index in range(int(group_number)):
        html = html  + """<img src="cid:image""" + str(index) + '"' + "border=0" + "/>"

    html3 = """
             </body>
             </html>
             """
    html = html + html3

    img_list = []
    attachments = []
    for index in range(int(group_number)):
        cmd = report_path + "jpg/" + 'wyze-g' + str(index+1) + ".jpg"
        img_list.append(cmd)
        attachments.append(cmd)

    send_email(sender_name, sender_addr, smtp, port,
               recipient_addr, subject, html, text,
               img_list, attachments, fn='my.eml', save=False)
