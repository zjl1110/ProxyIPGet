# -*- coding: utf-8 -*-
#__author__="ZJL"

import random


# 将有效IP存到reids
def Ip_DBSave(rm, db_name, ip_port, ip_time):
    try:
        ip_times = rm.getKeyAllAttribute(db_name)
        if len(ip_times)<14:
            rm.setKeyValue(db_name,ip_time,ip_port)
        else:
            ip_times.sort(reverse=True)
            rm.delAttribute(db_name, ip_times[-1])
            rm.setKeyValue(db_name, ip_time, ip_port)
    except Exception as e:
        return e,"Ip_DB"


# 随机获取IP
def Ip_DBGet(rm, db_name):
    try:
        ip_times = rm.getKeyAllAttribute(db_name)
        ip_len = len(ip_times)
        ip_prot = rm.getKeyValue(db_name,ip_times[random.randint(0,ip_len-1)])
        return ip_prot
    except Exception as e:
        return e,"Ip_DBGet"

# 获取所有IP
def Ip_DBGetAll(rm, db_name):
    ip_prots={}
    try:
        ip_times = rm.getKeyAllAttribute(db_name)
        for ip_time in ip_times:
            ip = rm.getKeyValue(db_name, ip_time)
            ip_prots[ip] = ip_time
        # ips = [rm.getKeyValue(db_name, ip_time) for ip_time in ip_times]
        return ip_prots
    except Exception as e:
        return e,"Ip_DBGetAll"


