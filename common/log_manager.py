# -*- coding: utf-8 -*-
#__author__="ZJL"

# 日志管理器
# 错误分两个等级，只有尾号1会触发邮件提醒，日志文件过大也会触发邮件
# 使用尾号区分是为了用前面的数字可以记录抓取阶段表示
import logging, traceback, os
from common.email_manager import batchSendEmail
from common.setting import logfilename, errortitle


def objLogging(errorcode, errortext):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logfilename,
                        filemode='a+')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    if errorcode[-1] == "0":
        text = errortext + "\n" + traceback.format_exc()
        logging.debug(text)
    elif errorcode[-1] == "1":
        text = errortext + "\n" + traceback.format_exc()
        logging.warning(text)
        try:
            batchSendEmail(errortitle, text)
        except Exception as e:
            # print(traceback.format_exc())
            logging.warning(traceback.format_exc())
    else:
        text = errortext + "\n" + traceback.format_exc()
        logging.warning(text)

    filesize = os.path.getsize(logfilename)
    if filesize >= 3000000:
        try:
            batchSendEmail("日志文件过大", "日志文件大小大于3M，请及时处理")
        except Exception as e:
            # print(traceback.format_exc())
            logging.warning(traceback.format_exc())