#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/11/30 下午6:22
'''

import configparser


def test_env(case=None):
    cf = configparser.ConfigParser()
    if case:
        cf.read("config.ini", encoding='UTF-8')
    else:
        cf.read("../config.ini", encoding='UTF-8')
    env = int(cf.get("Environment", "test_env"))
    return env


def mail_env(case=None):
    cf = configparser.ConfigParser()
    if case:
        cf.read("config.ini", encoding='UTF-8')
    else:
        cf.read("../config.ini", encoding='UTF-8')
    env = int(cf.get("Environment", "mail_to"))
    return env
