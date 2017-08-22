免费代理IP服务的简单实现

Python爬虫去各大免费代理ip网站抓取代理ip并做校验入库(redis)，然后对库里的ip不停做校验，最后用flask做成api接口

目录结构：

ProxyIPGet

    |----app

        |----flaskrun.py(flask程序)

        |----static(没用上)

        |----templates(没用上)

    |----checkout_script.py(用来不停校验库里的ip是否有效)

    |----common(公用模块)

        |----__init__.py

        |----email_manager.py(发邮件模块，没用上)

        |----html_manager.py(html模块，没用上)

        |----ip_db_manager.py(存，取ip)

        |----log_manager.py(日志模块，没用上)

        |----redis_manager.py(Redis模块)

        |----request_common.py(请求模块)

        |----request_manager(请求模块)

        |----setting.py(设置模块)

        |----url_manager.py(url模块，没用上)

    |----run.py(抓取校验ip并入库)


分别执行run.py(爬虫服务)，checkout_script.py(ip校验服务)，app/flaskrun.py(flask服务)

需要python3.5以上(使用了async/await新语法)，需要redis
用到了redis，aiohttp，flask库

app下flask服务，可以换成其它web框架实现

