#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/21 14:34
'''
import random, string


def random_string(num=5):
    # str = ''.join(random.sample(string.ascii_letters + string.digits, num))
    # return str
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789-_'
    for i in range(0, num):
        str += ''.join(chars[random.randint(0, len(chars) - 1)])
    return str
