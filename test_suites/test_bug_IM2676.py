#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/16 10:43
'''
from test_env import *
import unittest
import time


class TestIM2676(unittest.TestCase):
    '''测试全局Bug：IM-2676'''

    def setUp(self):
        self.driver = set_driver.init_driver()
        self.log = set_log.init_log("IM2676")
        self.env = 0  # 线上环境为0，测试环境为1

    def test_im_2676(self):
        '''测试步骤：1.客服登录进入IM对话页面，此时滚动条为最下面;2.客服切换到呼叫中心栏目再切换回来，判断滚动条是否还在最下面'''
        driver = self.driver
        log = self.log
        if self.env == 1:
            url = "linapp.udeskt1.com"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.qiao_login(driver, url)
        else:
            url = "brazil.udesk.cn"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.qiao_login(driver, url)
        try:
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[4]").click()
            time.sleep(2)
            log.debug("客服登录系统成功")
        except:
            log.debug("客服登录系统失败")
            self.assertTrue(False, "IM-2676自动化测试失败!")
        try:
            driver.find_element_by_xpath("//*[@id=\"im-chats\"]/div[4]/ul/li").click()
            time.sleep(3)
            log.debug("进入IM对话成功")
        except:
            log.debug("客服进入IM对话失败")
            self.assertTrue(False, "IM-2676自动化测试失败!")
        log.debug("执行js通过会话框属性判断IM对话页面的滚动条是否为最下面")
        try:
            driver.implicitly_wait(10)
            scrollHeight0 = driver.execute_script(
                "var e =document.getElementById(\"msg-panel\").children[1];return e.scrollHeight")
            log.debug("此时对话框的scrollHeight值为%s" % str(scrollHeight0))
            scrollTop0 = driver.execute_script(
                "var e =document.getElementById(\"msg-panel\").children[1];return e.scrollTop")
            log.debug("此时对话框的scrollTop值为%s" % str(scrollTop0))
            clientHeight0 = driver.execute_script(
                "var e =document.getElementById(\"msg-panel\").children[1];return e.clientHeight")
            log.debug("此时对话框的clientHeight值为%s" % str(clientHeight0))
        except:
            log.error("执行js命令失败")
        if scrollHeight0 == scrollTop0 + clientHeight0:
            log.debug("scrollHeight值等于scrollTop与clientHeight之和，说明此时滚动条位于最下方")
        try:
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[3]").click()
            time.sleep(3)
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[4]").click()
            time.sleep(3)
            log.debug("进入呼叫中心页面，再切换回IM会话页面成功")
        except:
            log.debug("进入呼叫中心页面，再切换回IM会话页面失败")
            self.assertTrue(False, "IM-2676自动化测试失败!")
        js = "var e=document.getElementById(\"msg-panel\").children[1];return e.scrollHeight === e.scrollTop + e.clientHeight"
        log.debug("执行js通过会话框属性判断IM对话页面的滚动条是否为最下面")
        try:
            scrollHeight = driver.execute_script(
                "var e =document.getElementById(\"msg-panel\").children[1];return e.scrollHeight")
            log.debug("此时对话框的scrollHeight值为%s" % str(scrollHeight))
            scrollTop = driver.execute_script(
                "var e =document.getElementById(\"msg-panel\").children[1];return e.scrollTop")
            log.debug("此时对话框的scrollTop值为%s" % str(scrollTop))
            clientHeight = driver.execute_script(
                "var e =document.getElementById(\"msg-panel\").children[1];return e.clientHeight")
            log.debug("此时对话框的clientHeight值为%s" % str(clientHeight))
        except:
            log.error("执行js命令失败")
            self.assertTrue(False, "IM-2676自动化测试失败!")
        try:
            scrollHeight == scrollTop + clientHeight
        except:
            log.error("js返回结果错误")
            self.assertTrue(False, "IM-2676自动化测试失败!")
        if scrollHeight == scrollTop + clientHeight:
            log.debug("scrollHeight值等于scrollTop与clientHeight之和，说明此时滚动条位于最下方")
            log.debug("IM-2676自动化测试通过!")
            return
        else:
            log.debug("scrollHeight值不等于scrollTop与clientHeight之和，说明此时滚动条不是最下方")
            log.debug("IM-2676自动化测试未通过!")
            self.assertTrue(False, "IM-2676自动化测试失败!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
