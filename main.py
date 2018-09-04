#!/usr/bin/env python
#_*_coding:utf-8_*_

import email
import poplib
import datetime
import sys
import smtplib
from email.mime.text import MIMEText

import prettytable  #pip install prettytable

import daily_checker

if __name__ == '__main__':
    # 可通过传参方式传入要检查的指定日期信息 ‘2018-08-01 12:00:00’  日期表示检查哪天的日报，时间表示检查从几点开始以后的邮件
    date_str = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d 12:00:00")
    param_count = len(sys.argv)
    if param_count == 2:
        date_str = sys.argv[1]

    print(datetime.datetime.now())

    host     = 'pop.test.com'
    username = 'xxx@test.com'
    password = 'xxx'
    recv_instanse = RecvMail(host, username, password)

    print("Begining find daily mail info....")

    #按照以下日期，获取指定天的日报提交情况
    find_date = datetime.datetime.fromisoformat(date_str)
    day_str = "%s-%s-%s" % (find_date.date().year, find_date.date().month, find_date.date().day)

    checker    = DailySumbitInfoChecker()
    dict_daily = checker.find_daily_report_mail2(recv_instanse, date_str)

    table1 = prettytable.PrettyTable()
    table2 = prettytable.PrettyTable()
    table1.field_names = DailyInfo().get_table_title()
    table2.field_names = DailyInfo().get_table_title()

    for item in dict_daily:
        if dict_daily[item].have:
            table1.add_row(dict_daily[item].get_row_list())
        else:
            table2.add_row(dict_daily[item].get_row_list())

    content =  "\r\n\r\n【%s】日报发送情况：" % (day_str)
    content += "\r\n\r\n以下人员未按时提交日报，该上交罚款了...\r\n"
    content += table2.get_string()
    content += "\r\n\r\n给按时提交日报的给予热烈的掌声...\r\n"
    content += table1.get_string()

    print(content)

    #----------------------------------------------
    #将日报提交情况邮件通报
    to_addrs = []
    for item in dict_daily:
        to_addrs.append(dict_daily[item].mail)

    message = MIMEText(content)
    message["To"] = ",".join(to_addrs)
    message["Subject"] = day_str + "日.报.提交情况通报"

    sender = SendMail("smtp.novel-supertv.com", username, password)
    sender.send_mail(username, to_addrs, message.as_string())

    print("success.")
    print(datetime.datetime.now())


