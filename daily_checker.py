#!/usr/bin/env python
#_*_coding:utf-8_*_

import email
import poplib
import datetime

import recv_mail
from recv_mail import RecvMail
import send_mail
from send_mail import SendMail

class DailyInfo:
    def __init__(self, name="", mail="", mail_subject="", mail_date="", have=False):
        self.name = name
        self.mail = mail
        self.mail_subject = mail_subject
        self.mail_date = mail_date
        self.have = have

    def set_daily_info(self, mail_subject, mail_date, have=True):
        self.mail_date = mail_date
        self.mail_subject = mail_subject
        self.have = have

    def get_row_list(self):
        return [self.name, self.mail, "已发" if self.have else "未按时发送", self.mail_date, self.mail_subject]

    def get_table_title(self):
        return ['姓名', '邮箱', '是否发送日报', '发送时间', '日报邮件标题']
#endclass

class DailySumbitInfoChecker:
    def __init__(self):
        self.dict_addr = {}
        self.matching_str = "日报"

    def init_dict_addr(self, dict_addr):
        self.dict_addr = dict_addr

    def _find_mid_index(self, find_date, recv_instanse, list_len):
        # 根据准备检查的日报日期，快速查找到指定日期的邮件位置。此处默认平均每天的邮件量在50封
        now_date = datetime.datetime.now()
        count_day = (now_date.date() - find_date.date()).days + 1

        mid_index = list_len - count_day*50
        begin_index = list_len
        end_index   = mid_index
        while 1:
            message = recv_instanse.get_one_mail(mid_index)
            mail_date = recv_instanse.get_astime_beijing(message)

            if mail_date.date() > find_date.date():
                begin_index = mid_index
                end_index   = begin_index - (100 if (begin_index-100) > 0 else 0)
                mid_index   = begin_index - int((begin_index-end_index)/2)
            elif mail_date.date() < find_date.date():
                end_index   = mid_index
                begin_index = end_index + int((list_len-begin_index)/2)
                mid_index   = begin_index - int((begin_index-end_index)/2)
            else:
                break
            continue

        return int(mid_index)
    #enddef

    def find_daily_report_mail2(self, recv_instanse, day=datetime.datetime.now().strftime("%Y-%M-%D %H:%M:%S")):
        # 根据找到的在日报日期内的邮件位置，左右查找当天的所有邮件，获取日报发送信息并更新到日报信息字典中
        list_len = recv_instanse.update_list()
        find_date = datetime.datetime.fromisoformat(day)

        mid_index = self._find_mid_index(find_date, recv_instanse, list_len)

        for index in range(0, mid_index):
            message = recv_instanse.get_one_mail(mid_index - index)

            mail_date    = recv_instanse.get_astime_beijing(message)
            mail_from    = recv_instanse.get_parsed_fromaddr(message)
            mail_subject = recv_instanse.get_decode_subject(message)

            if mail_date.date() == find_date.date():
                if mail_date.time() > find_date.time() and str(mail_from) in self.dict_addr and self.matching_str in mail_subject:
                    self.dict_addr[str(mail_from)].set_daily_info(mail_subject, mail_date, True)
            else:
                break

        for index in range(mid_index, list_len):
            message = recv_instanse.get_one_mail(index)

            mail_date    = recv_instanse.get_astime_beijing(message)
            mail_from    = recv_instanse.get_parsed_fromaddr(message)
            mail_subject = recv_instanse.get_decode_subject(message)

            if mail_date.date() == find_date.date():
                if mail_date.time() > find_date.time() and str(mail_from) in self.dict_addr and self.matching_str in mail_subject:
                    self.dict_addr[str(mail_from)].set_daily_info(mail_subject, mail_date, True)
            else:
                break

        return self.dict_addr
    #enddef
#endclass
