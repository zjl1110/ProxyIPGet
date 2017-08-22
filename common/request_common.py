# -*- coding: utf-8 -*-
#__author__="ZJL"

#定义一个重试修饰器，默认重试一次，sets参数是便于将错误url和信息存入redis(或其他)
def asyncRetry(num_retries=1,sets=None):
    #用来接收函数
    def wrapper(func):
        #用来接收函数的参数,这里采用协程方式
        async def wrapper(*args,**kwargs):
            #为了方便看抛出什么错误定义一个错误变量
            last_exception =None
            #循环执行包装的函数
            for _ in range(num_retries):
                try:
                    #如果没有错误就返回包装的函数，这样跳出循环，这里需要挂起
                    return await func(*args, **kwargs)
                except Exception as e:
                    # print(e)
                    #捕捉到错误不要return，不然就不会循环了，这里不能挂起
                    # print(args[0],kwargs)
                    #这里用于将出错的url存入redis
                    # sets(args[0])
                    last_exception = e
            #如果要看抛出错误就可以抛出
            # raise last_exception
        return wrapper
    return wrapper