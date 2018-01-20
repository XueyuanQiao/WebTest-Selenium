#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/16 16:10
'''
from test_env.set_driver import init_driver,admin_login
from test_env.set_log import init_log
from test_env.set_env import test_env
import unittest
import time


class TestTS1986(unittest.TestCase):
    '''测试全局Bug：TS-1986'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("TS1986")
        self.env = test_env()

    def test_ts_1986(self):
        '''测试步骤：1.批量选中工单;2.批量更新工单状态，检查前端显示是否正确'''
        driver = self.driver
        log = self.log
        if self.env == 0:
            url = "brazil.udesk.cn"
            log.debug("设定测试环境为\"%s\"" % url)
            admin_login(driver, url)
        else:
            url = "linapp.udeskt1.com"
            log.debug("设定测试环境为\"%s\"" % url)
            admin_login(driver, url)
        try:
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[2]").click()
            time.sleep(2)
            log.debug("客服登录系统成功")
        except:
            log.debug("客服登录系统失败")
            self.assertTrue(False, "TS-1986自动化测试失败!")
        try:
            # 不同测试环境工单过滤器不同
            if self.env == 0:
                driver.find_element_by_xpath("//a[@href=\"/entry/ticket/list/305853?column=&order=\"]").click()
            else:
                driver.find_element_by_xpath("//a[@href=\"/entry/ticket/list/779?column=&order=\"]").click()
            log.debug("选择\"所有工单\"过滤器")
        except:
            log.error("未能选择到\"所有工单\"过滤器")
            self.assertTrue(False, "TS-1986自动化测试失败!")
        try:
            time.sleep(10)
            driver.find_element_by_xpath("//div[@class=' ticket-content-inner']/div[3]/ul/li/input").click()
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("//div[@class='ud-tab']/div/a").click()
            log.debug("选择\"所有工单\"第一页工单进行批量操作")
        except:
            log.error("选择\"所有工单\"第一页工单进行批量操作失败")
            self.assertTrue(False, "TS-1986自动化测试失败!")

        # 开启状态测试
        try:
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[1]/div").click()
            # 设置状态为开启
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[2]/div/ul/li[2]").click()
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
            time.sleep(10)
            log.error("设置工单状态为\"开启\"")
        except:
            log.error("设置工单状态为\"开启\"失败")
            self.assertTrue(False, "TS-1986自动化测试失败!")
        # 判断修改状态后的工单状态前端显示
        status_column = 1
        while True:
            try:
                status_element = str(driver.find_element_by_xpath(
                    "//ul[@class='ticket-float-head ui-sortable']/li[%d]/span" % status_column).get_attribute("title"))
                if status_element == "状态":
                    break
                else:
                    status_column += 1
            except:
                status_column += 1

        try:
            i = 1
            while True:
                text = driver.find_element_by_xpath(
                    "//table[@class='table table-hover']/tbody/tr[%d]/td[%d]/span" % (i, status_column)).text
                if text == "开启":
                    i += 1
                else:
                    log.error("有工单状态非 \"开启\"，为 \"%s\"" % text)
                    self.assertTrue(False, "TS-1986自动化测试失败!")
        except:
            if text != "开启":
                self.assertTrue(False, "TS-1986自动化测试失败!")
            log.debug("设置后工单状态均为开启，\"开启\"状态前端显示正确")

        # 解决中状态测试
        try:
            driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div[3]/ul/li[1]/input").click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div[2]/div[1]/a[1]").click()
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[1]/div").click()
            # 设置状态为解决中
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[2]/div/ul/li[3]").click()
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
            time.sleep(10)
            log.error("设置工单状态为\"解决中\"")
        except:
            log.error("设置工单状态为\"解决中\"失败")
            self.assertTrue(False, "TS-1986自动化测试失败!")
        # 判断修改状态后的工单状态前端显示
        try:
            i = 1
            while True:
                text = driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div[1]/div[1]/div[3]/div/table/tbody/tr[%d]/td[%d]/span" % (
                        i, status_column)).text
                if text == "解决中":
                    i += 1
                else:
                    log.error("有工单状态非 \"解决中\"，为 \"%s\"" % text)
                    self.assertTrue(False, "TS-1986自动化测试失败!")
        except:
            if text != "解决中":
                self.assertTrue(False, "TS-1986自动化测试失败!")
            log.debug("设置后工单状态均为解决中，\"解决中\"状态前端显示正确")

        # 已解决状态测试
        try:
            driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div[3]/ul/li[1]/input").click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div[2]/div[1]/a[1]").click()
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[1]/div").click()
            # 设置状态为已解决
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[2]/div/ul/li[4]").click()
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
            time.sleep(10)
            log.error("设置工单状态为\"已解决\"")
        except:
            log.error("设置工单状态为\"已解决\"失败")
            self.assertTrue(False, "TS-1986自动化测试失败!")
        # 判断修改状态后的工单状态前端显示
        try:
            i = 1
            while True:
                text = driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div[1]/div[1]/div[3]/div/table/tbody/tr[%d]/td[%d]/span" % (
                        i, status_column)).text
                if text == "已解决":
                    i += 1
                else:
                    log.error("有工单状态非 \"已解决\"，为 \"%s\"" % text)
                    self.assertTrue(False, "TS-1986自动化测试失败!")
        except:
            if text != "已解决":
                self.assertTrue(False, "TS-1986自动化测试失败!")
            log.debug("设置后工单状态均为已解决，\"已解决\"状态前端显示正确")

        # 已关闭状态测试
        try:
            driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div[3]/ul/li[1]/input").click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div[1]/div[2]/div[1]/a[1]").click()
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[1]/div").click()
            # 设置状态为已关闭
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div[1]/div[1]/div[6]/div/div/form/div[2]/div/div[1]/ul[1]/li[3]/p[2]/div/div[2]/div/ul/li[5]").click()
            time.sleep(2)
            driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
            time.sleep(10)
            log.error("设置工单状态为\"已关闭\"")
        except:
            log.error("设置工单状态为\"已关闭\"失败")
            self.assertTrue(False, "TS-1986自动化测试失败!")
        # 判断修改状态后的工单状态前端显示
        try:
            i = 1
            while True:
                text = driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div[1]/div[1]/div[3]/div/table/tbody/tr[%d]/td[%d]/span" % (
                    i, status_column)).text
                if text == "已关闭":
                    i += 1
                else:
                    log.error("有工单状态非 \"已关闭\"，为 \"%s\"" % text)
                    self.assertTrue(False, "TS-1986自动化测试失败!")
        except:
            if text != "已关闭":
                self.assertTrue(False, "TS-1986自动化测试失败!")
            log.debug("设置后工单状态均为已关闭，\"已关闭\"状态前端显示正确")
            log.debug("TS-1986自动化测试成功!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
