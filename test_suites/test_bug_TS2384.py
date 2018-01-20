#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/11/10 上午10:44
'''

from test_env.set_driver import init_driver,admin_login
from test_env.set_log import init_log
from test_env.set_env import test_env
import unittest
from time import sleep


class TestTS2384(unittest.TestCase):
    '''测试全局BUG：TS-2384'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("TS-2384")
        self.env = test_env()
        self.js_code = "><script>alert('test -> TS-2384')</script><"

    def test_ts_2384(self):
        driver = self.driver
        log = self.log
        if self.env == 0:
            admin_login(driver, "brazil.udesk.cn")
            log.debug("设定测试环境为brazil.udesk.cn")
        else:
            admin_login(driver, "linapp.udeskt1.com")
            log.debug("设定测试环境为linapp.udeskt1.com")
        o = 0
        while o < 10:
            try:
                driver.find_element_by_xpath("//li[@rel='ticket.list.index']").click()
                break
            except:
                o += 1
                sleep(1)
        if o == 10:
            raise Exception("管理员登陆失败")
        log.debug("管理员登陆成功")
        sleep(2)
        try:
            if self.env == 0:
                driver.find_element_by_xpath("//a[@href=\"/entry/ticket/list/305853?column=&order=\"]").click()
            else:
                driver.find_element_by_xpath("//a[@href=\"/entry/ticket/list/779?column=&order=\"]").click()
        except:
            raise Exception("未能进入'所有工单'")
        log.debug("选取'所有工单'过滤器")
        i = 0
        while i < 10:
            try:
                driver.find_element_by_class_name("subject").click()
                break
            except:
                sleep(1)
                i += 1
        if i == 10:
            raise Exception("未能进入工单编辑页面")

        j = 0
        while j < 10:
            try:
                driver.find_element_by_xpath("//a[text()='编辑']").click()
                break
            except:
                sleep(1)
                i += 1
        if j == 10:
            raise Exception("未能点击编辑按钮")
        log.debug("选择第一个工单编辑")
        try:
            driver.find_element_by_xpath("//div[@class='panel-body ']/ul/li[1]/input").clear()
            driver.find_element_by_xpath("//div[@class='panel-body ']/ul/li[1]/input").send_keys(self.js_code)
        except:
            raise Exception("未能编辑该工单主题")
        try:
            driver.find_element_by_xpath("//a[text()='保存']").click()
        except:
            raise Exception("未能编辑该工单主题")
        log.debug("将该工单主题编辑改为js代码:'%s'并保存" % self.js_code)
        sleep(3)
        try:
            title = driver.find_element_by_xpath("//span[@class='ticket-desc-title']")
        except:
            raise Exception("未能取到工单主题")
        if title.text == "主题：" + self.js_code:
            raise Exception("主题并未对js代码进行过滤，测试失败")
        else:
            log.debug("主题已被过滤，过滤后的主题为'%s'" % str(title.text)[3:])
        log.debug("TS-2384成功通过自动化测试")

    def tearDown(self):
        sleep(5)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
