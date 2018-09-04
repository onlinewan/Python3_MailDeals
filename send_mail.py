#!/usr/bin/env python
#_*_coding:utf-8_*_

import smtplib
import email
from email.mime.text import MIMEText

class SendMail:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.smtp_conn = smtplib.SMTP_SSL(hostname)
        self.smtp_conn.login(self.username, self.password)
    #enddef

    def __del__(self):
        try:
            self.smtp_conn.quit()
        except Exception as e:
            e
    #enddef

    def send_mail(self, from_addr, to_addrs, msg):
        self.smtp_conn.sendmail(from_addr, to_addrs, msg)
    #enddef
#endclass
