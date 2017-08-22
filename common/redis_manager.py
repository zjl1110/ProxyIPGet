# -*- coding: utf-8 -*-
#__author__="ZJL"

import redis
from common.setting import redis_db,redis_host,redis_port

# redis队列管理器
class RedisManager(object):
    def __init__(self, host=redis_host, port=redis_port, db=redis_db):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.StrictRedis(connection_pool=self.pool)

        # 可以存储任意格式

    def setData(self, keyname, data):
        data = self.r.set(keyname, data)
        return data

        # 取数据

    def getData(self, keyname, coding="utf-8"):
        data = self.r.get(keyname)
        data = data.decode(coding)
        return data

        # 取数据并删除

    def getDataDel(self, keyname, coding="utf-8"):
        data = self.r.get(keyname)
        data = data.decode(coding)
        # 删除
        self.r.delete(keyname)
        return data

        # 只保存属性值,key对应多个属性

    def setValue(self, keyname, data):
        data = self.r.lpush(keyname, data)
        return data

        # 取出属性值,并删除

    def getValue(self, keyname, coding="utf-8"):
        data = self.r.brpop(keyname, 0)[1]
        data = data.decode(coding)
        return data

        # 以键值对形式保存属性名和属性值，key对应多个属性

    def setKeyValue(self, keyname, datakey, data):
        state = self.r.hset(keyname, datakey, data)
        if state == 0:
            return True
        else:
            return False

            # 取出属性值

    def getKeyValue(self, keyname, datakey, coding="utf-8"):
        data = self.r.hget(keyname, datakey)
        data = data.decode(coding)
        return data

        # 取出属性值并删除

    def getKeyValueDel(self, keyname, datakey, coding="utf-8"):
        data = self.r.hget(keyname, datakey)
        data = data.decode(coding)
        # 删除
        self.r.hdel(keyname, datakey)
        return data

        # 根据属性名删属性值

    def delAttribute(self, keyname, datakey):
        hdel = self.r.hdel(keyname, datakey)
        if hdel == 1:
            return True
        else:
            return False

            # 获得key下面所有属性名

    def getKeyAllAttribute(self, keyname):
        hkeys = self.r.hkeys(keyname)
        return hkeys

        # 获得所有key的名称

    def getKey(self):
        keys = self.r.keys()
        return keys

        # 获得同一个key还有多少

    def getLen(self, keyname):
        llen = self.r.llen(keyname)
        return llen

        # 判断key是否存在

    def getExists(self, keyname):
        exists = self.r.exists(keyname)
        return exists

        # 获得key的数量

    def getDbsize(self):
        dbsize = self.r.dbsize()
        return dbsize

        # 删除key

    def deleteKy(self, keyname):
        delete = self.r.delete(keyname)
        if delete == 1:
            return True
        else:
            return False

            # 删除当前数据库的所有数据

    def flushDB(self):
        flushdb = self.r.flushdb()
        return flushdb

        # ======集合==========

    # 添加数据，因为是集合所以有去重功能,返回添加了多少
    def setSets(self, keyname, *data):
        return self.r.sadd(keyname, *data)

        # 取出集合，返回列表

    def getSetsList(self, keyname, coding="utf-8"):
        datas = self.r.smembers(keyname)
        datas = [d.decode(coding) for d in datas]
        return datas

        # 取出集合，返回列表,最后删除

    def getSetsListDel(self, keyname, coding="utf-8"):
        datas = self.r.smembers(keyname)
        datas = [d.decode(coding) for d in datas]
        [self.r.srem(keyname, d) for d in datas]
        return datas

        # 取出集合最后一个元素

    def getSetsOne(self, keyname, coding="utf-8"):
        data = self.r.smembers(keyname)
        data = [d.decode(coding) for d in data]
        if len(data) > 0:
            return data.pop()
        else:
            return

            # 取出集合最后一个元素并删除

    def getSetsOneDel(self, keyname, coding="utf-8"):
        datas = self.r.smembers(keyname)
        datas = [d.decode(coding) for d in datas]
        if len(datas) > 0:
            data = datas.pop()
            self.r.srem(keyname, data)
            return data
        else:
            return

            # 删除集合的元素，返回删除了多少

    def setsDel(self, keyname, *data):
        return self.r.srem(keyname, data)

        # 判断元素是否存在

    def isExist(self, keyname, data):
        return self.r.sismember(keyname, data)

        # 集合长度

    def setsLen(self, keyname):
        return self.r.scard(keyname)

        # 多个集合的交集，返回列表

    def setsIntersection(self, *keyname):
        data = self.r.sinter(keyname)
        data = [d.decode("utf-8") for d in data]
        return data

        # 多个集合的并集，返回列表

    def setsAndSet(self, *keyname):
        data = self.r.sunion(keyname)
        data = [d.decode("utf-8") for d in data]
        return data


