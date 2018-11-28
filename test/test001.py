# -*- coding: utf-8 -*-
# @author: chenhuachao
# @time: 2018/11/28


import time
def logs(*params):
    print(*params)
    def timer(func):
        def deco(*args):
            start = time.time()
            func(args)
            stop = time.time()
            print(stop-start)
        return deco
    return timer

@logs("aaaa")
def test(parameter): #8
    time.sleep(2)
    print("test is running!")


test('a')
