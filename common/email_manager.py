# -*- coding: utf-8 -*-
#__author__="ZJL"

import smtplib
import email.mime.multipart
import email.mime.text
from common.setting import toEmail, emailName, emailPassword, smtp_connect


class EmailTloost:
    def __init__(self, toemail, totilte, totext):
        self.toemail = toemail
        self.emailname = emailName
        self.emailpassword = emailPassword
        self.smtp_connect = smtp_connect

        self.msg = email.mime.multipart.MIMEMultipart()
        self.msg['from'] = self.emailname
        self.msg['to'] = self.toemail
        self.msg['subject'] = totilte
        self.content = totext
        self.txt = email.mime.text.MIMEText(self.content)
        self.msg.attach(self.txt)

        # smtp = smtplib

    def sendEmail(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.smtp_connect, '25')
        smtp.login(self.emailname, self.emailpassword)
        smtp.sendmail(self.emailname, self.toemail, str(self.msg))
        smtp.quit()


def batchSendEmail(totilte, totext):
    for toemail in toEmail:
        e = EmailTloost(toemail, totilte, totext)
        e.sendEmail()

        # batchSendEmail("xxx","hahahah")