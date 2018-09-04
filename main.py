#!/usr/bin/env python
#_*_coding:utf-8_*_

import datetime
import sys
import prettytable  #pip install prettytable

from email.mime.text import MIMEText

from recv_mail import RecvMail
from send_mail import SendMail
from daily_checker import DailyInfo
from daily_checker import DailySumbitInfoChecker


if __name__ == '__main__':
    # 可通过传参方式传入要检查的指定日期信息 ‘2018-08-01 12:00:00’  日期表示检查哪天的日报，时间表示检查从几点开始以后的邮件
    # 默认查询昨天的日报提交情况
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

    # 对待检查的发件人字典进行初始化，此处根据时间情况调整
    dict_addr = {}
    dict_addr["test1@test.com"] = DailyInfo("test1", "test1@test.com")
    dict_addr["test2@test.com"] = DailyInfo("test2", "test2@test.com")
    dict_addr["test3@test.com"] = DailyInfo("test3", "test3@test.com")

    checker = DailySumbitInfoChecker()
    checker.init_dict_addr(dict_addr)
    dict_daily = checker.find_daily_report_mail2(recv_instanse, date_str)

    # 格式化输出日报检查结果
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

    sender = SendMail("smtp.test.com", username, password)
    sender.send_mail(username, to_addrs, message.as_string())

    print("success.")
    print(datetime.datetime.now())


