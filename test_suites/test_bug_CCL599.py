#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/11/9 下午4:37
'''

from test_env.set_log import init_log
from test_env.set_driver import init_driver
from test_env.set_env import test_env
import unittest
import time


class TestCCL599(unittest.TestCase):
    '''测试全局BUG：CCL-599'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("CCL599")
        self.env = test_env()

    def test_ccl_599(self):
        '''测试步骤：用具有编辑、查看组内客户，不具有编辑全部客户的客服查看客户详情看是否正常'''
        driver = self.driver
        log = self.log

        if self.env == 0:
            driver.get("http://brazil.udesk.cn/hc")
            log.debug("设定测试环境为http://brazil.udesk.cn/hc")
        else:
            driver.get("http://linapp.udeskt1.com/hc")
            log.debug("设定测试环境为http://linapp.udeskt1.com/hc")

        driver.find_element_by_class_name("login").click()
        driver.find_element_by_id("user_email").send_keys("CCL599@udesk.cn")
        driver.find_element_by_id("user_password").send_keys("*****")
        driver.find_element_by_xpath("//input[@name='commit']").click()
        time.sleep(5)

        driver.find_element_by_xpath("//li[@rel='crm.customer.list.index']").click()
        time.sleep(5)
        log.debug("客服登陆成功")

        customers = driver.find_elements_by_xpath("//tr[@class='cursor-pointer']/td[2]")
        customers[1].click()
        time.sleep(5)
        log.debug("点击某客户查看客户详情")

        try:
            driver.find_element_by_class_name("customer-name")
            log.debug("该客户的客户详情正常显示，CCL-599成功通过自动化测试")
        except:
            log.debug("该客户的客户详情不能正常显示，CCL-599自动化测试失败")
            raise Exception("CCL-599自动化测试失败")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
