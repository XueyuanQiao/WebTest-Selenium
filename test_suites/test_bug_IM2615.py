#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/9 16:31
'''
from test_env import *
import unittest
import time


class TestIm2615(unittest.TestCase):
    '''测试全局Bug：IM-2615,同时检测超长名称客户新建（最多支持255个字符）:ICDT-212星巴克每次登录的时候都会创建新的客户，昵称是随机生成的字符串225个字符 '''

    def setUp(self):
        self.driver = set_driver.init_driver()
        self.log = set_log.init_log("Im2615")
        self.env = 0  # 线上环境为0，测试环境为1

    def test_Im_2615(self):
        '''测试步骤：1.新建长名称客户（测试中为255个字符）;2.客户详情中查看客户名称是否被省略'''
        driver = self.driver
        log = self.log
        if self.env == 1:
            url = "linapp.udeskt1.com"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.admin_login(driver, url)

        else:
            url = "brazil.udesk.cn"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.admin_login(driver, url)
        try:
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[5]").click()
            log.debug("管理员登录成功")
            driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div[1]/div/a[2]").click()
            log.debug("点击新增客户按钮")
            customer_name = set_random.random_string(255)
            driver.find_element_by_xpath("//*[@placeholder=\"客户名称\"]").send_keys(customer_name)
            driver.find_element_by_xpath("//button[@type='submit']") .click()
            time.sleep(5)
            check_name = str(driver.find_element_by_class_name("customer-name").text)
            log.debug("新增255字符姓名客户,名称为\"%s\"" % customer_name)
            try:
                if check_name == customer_name:
                    log.debug("客户详情中客户名称显示为\"%s\"，与新建时一致" % check_name)
                    log.debug("IM-2615成功通过自动化测试!")
                    return
                else:
                    log.debug("客户详情中客户名称显示为\"%s\"，与新建时不一致" % check_name)
                    self.assertTrue(False, "IM-2615自动化测试失败!")
            except Exception as e:
                log.error(e)
                self.assertTrue(False, "IM-2615自动化测试失败!")
        except Exception as e:
            log.error(e)
            self.assertTrue(False, "IM-2615自动化测试失败!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
