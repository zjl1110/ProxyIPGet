# -*- coding: utf-8 -*-
#__author__="ZJL"

from flask import Flask
from common.ip_db_manager import Ip_DBGet
from common.redis_manager import RedisManager

rdb = RedisManager(db="4")
db_name = "proxyIP"

app = Flask(__name__)

@app.route('/getip')
def get_ipport():
    ip_port = Ip_DBGet(rdb, db_name)
    return ip_port

@app.errorhandler(403)
def page_not_found(error):
    return "403"

@app.errorhandler(404)
def page_not_found(error):
    return "404"

@app.errorhandler(410)
def page_not_found(error):
    return "403"

@app.errorhandler(500)
def page_not_found(error):
    return "500"


if __name__ == '__main__':
    app.run(debug=True,port=8111,threaded=True)