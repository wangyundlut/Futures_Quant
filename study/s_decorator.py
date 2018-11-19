#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
装饰器模式
@decorator
相当于 fun = decorator(fun)
输入的为一个函数，结果为fun = wrapper，再次调用fun的时候，自动变成wrapper + 参数
返回的仍为fun传入参数的结果
wrapper 返回的是 func 返回的东西
decorator 返回的是 函数wrapper
如果decorator有输入，则最外层返回decorator
三层 一层传 decorator的输入，一层传func 一层传 *args, **kwargs
最多只能有这三层？？？！！！！！
def log(text):
    print(text)
    def decorate(fn):
        # 保存原函数的名称，不至于所有的都叫wrapper
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("this is wrapper")
            print(text)
            return fn(*args, **kwargs)
        return wrapper
    return decorate

@log(3)
def add1(a, b):
    print("2018-02-02")



"""