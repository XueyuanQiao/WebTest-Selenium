#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/12/12 下午5:08
'''

import unittest
from time import sleep
from test_env.set_log import init_log
from test_env.set_driver import admin_login
from test_env.set_driver import init_driver


class TestTS2672(unittest.TestCase):
    '''测试全局BUG：TS-2672'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("TS-2672")
        self.env = 1  # 0线上环境，1测试环境

    def tearDown(self):
        self.driver.quit()

    def test_ts_2672(self):
        '''测试步骤：管理员查看客户字段，判断有无'呼叫中心工作台'字段显示'''
        driver = self.driver
        env = self.env
        log = self.log

        if env == 0:
            admin_login(driver, "brazil.udesk.cn")
            log.debug("设定测试环境为brazil.udesk.cn")
            sleep(4)
            driver.find_element_by_xpath("//div[@class='left-side-inner']/ul/li[9]/a").click()  # 9为管理中心按钮的上下位置
        elif env == 1:
            admin_login(driver, "linapp.udeskt1.com")
            log.debug("设定测试环境为linapp.udeskt1.com")
            sleep(4)
            driver.find_element_by_xpath("//div[@class='left-side-inner']/ul/li[8]/a").click()  # 8为管理中心按钮的上下位置

        sleep(3)
        log.debug("管理员登录成功")
        driver.execute_script("document.querySelector('.ud-nav').scrollTop = 3000")  # 下拉滚动条使得“管理”可以点击
        driver.find_element_by_xpath("//div[@class='wrapper']/nav/dl/dt[3]").click()  # 3为“管理”，点击后展开
        driver.find_element_by_xpath("//div[@class='wrapper']/nav/dl/dd[3]/a[7]").click()  # 7为展开后“客户字段”位置
        log.debug("点击进入'客户字段'")

        text = "呼叫中心工作台"
        try:
            real_text = str(driver.find_element_by_xpath("//span[@class='field-call-center']").text)
        except:
            self.assertTrue(False, "'呼叫中心工作台'显示验证不匹配，TS-2672自动化测试失败")

        self.assertEqual(text, real_text, "目标名称不匹配，'呼叫中心工作台'显示为%s" % real_text)

        log.debug("验证'呼叫中心工作台'显示正常，TS-2672成功通过自动化测试")
