#!/usr/bin/env python
#_*_coding:utf-8_*_

import email
import poplib
import datetime

class RecvMail:
    '邮件接收类'
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.pop_conn = poplib.POP3_SSL(host)
        self.pop_conn.user(username)
        self.pop_conn.pass_(password)
    #enddef

    def __del__(self):
        try:
            self.pop_conn.quit()
        except Exception as e:
            e
    #enddef

    def print_stat(self):
        # stat()返回邮件数量和占用空间:
        print('Messages: %s. Size: %s' % self.pop_conn.stat())
    #enddef

    def update_list(self):
        # 更新到最新邮件列表，并返回列表长度
        resp, self.mails_list, octets = self.pop_conn.list()
        return len(self.mails_list)
    #enddef

    def print_classinfo(self):
        print("Employee.__doc__:", RecvMail.__doc__)
        print("Employee.__name__:", RecvMail.__name__)
        print("Employee.__module__:", RecvMail.__module__)
        print("Employee.__bases__:", RecvMail.__bases__)
        print("Employee.__dict__:", RecvMail.__dict__)

    def get_one_mail(self, index):
        resp, lines, octets = self.pop_conn.retr(index)
        message = email.message_from_bytes(b'\r\n'.join(lines))
        #print("%05d %s\t %s\t %s" % (index, mail_date, mail_from, mail_subject))
        return message
    #enddef

    def get_decode_subject(self, message):
        # 对原始base64文本进行解码，得到文本串及文本编码
        subject = email.header.decode_header(message.get("subject"))
        mail_subject = subject[0][0]
        subcode = subject[0][1]
        if subcode is not None:
            try:
                mail_subject = mail_subject.decode(subcode if subcode.find("un") < 0 else "gb2312")
            except Exception as e:
                mail_subject = mail_subject.decode("utf-8")
        return mail_subject
    #enddef

    def get_astime_beijing(self, message):
        return email.utils.parsedate_to_datetime(message.get("date")).astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    #enddef

    def get_parsed_fromaddr(self, message):
        mail_from = message.get("from")
        mail_from = email.utils.parseaddr(mail_from)
        mail_from = mail_from[0] if len(mail_from) < 2 else mail_from[1]
        return mail_from
    #enddef
#endclass
