#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2018/1/12 上午10:49
'''
from test_env import *
import unittest
from time import sleep


class TestIM3262(unittest.TestCase):
    '''测试全局Bug：IM-3262'''

    def setUp(self):
        self.driver = set_driver.init_driver()
        self.log = set_log.init_log("IM-3262")
        self.env = 1  # 线上环境为0，测试环境为1

    def tearDown(self):
        self.driver.quit()

    def test_im_3262(self):
        '''测试步骤：判断对话记录是否显示条数'''
        driver = self.driver
        log = self.log
        if self.env == 0:
            url = "brazil.udesk.cn"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.admin_login(driver, url)
        else:
            url = "linapp.udeskt1.com"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.admin_login(driver, url)
        sleep(3)
        driver.find_element_by_xpath("//div[@class='left-side-inner']/ul/li[3]").click()
        sleep(2)
        log.debug("管理员登陆成功")

        # 修复小屏幕下报错，下拉滚动条使得触发器可以点击
        driver.execute_script("document.querySelector('.ud-nav').scrollTop = 3000")
        driver.find_element_by_xpath("//div[@class='wrapper']/nav/dl/dd[4]/a[4]").click()
        sleep(1)
        log.debug("对话记录进入成功")

        # 点击确定进行一次搜索
        driver.find_element_by_xpath("//a[@class='btn btn-primary btn-sm' and text()='确定']").click()
        sleep(1)
        real_text = driver.find_element_by_xpath("//div[@class='pull-left']").text
        if ("条" in real_text and "页" in real_text):
            log.debug("对话记录页数和条数都正常显示：（" + str(real_text) + "）")
            log.debug("IM3262自动化测试成功！")
        else:
            log.error("对话记录页数和条数未正常显示：（" + str(real_text) + "）")
            log.error("IM3262自动化测试失败！")
            raise Exception("对话记录页数和条数未正常显示")
