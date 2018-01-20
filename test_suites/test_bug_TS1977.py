#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/17 15:34
'''
from test_env import *
import unittest
import time


class TestTS1977(unittest.TestCase):
    '''测试全局Bug：TS-1977'''

    def setUp(self):
        self.driver = set_driver.init_driver()
        self.log = set_log.init_log("TS1977")
        self.env = 1  # 线上环境为0，测试环境为1

    def test_ts_1977(self):
        '''测试步骤：1.客服修改邮件渠道的工单的优先级和标签;2.判断该工单的“添加满意度调查”选项是否还存在'''
        driver = self.driver
        log = self.log
        self.error = False
        if self.env == 0:
            url = "brazil.udesk.cn"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.qiao_login(driver,url)
        else:
            url = "linapp.udeskt1.com"
            log.debug("设定测试环境为\"%s\"" % url)
            set_driver.qiao_login(driver, url)
        try:
            driver.implicitly_wait(20)
            driver.find_element_by_xpath("//li[@rel='ticket.list.index']").click()
            time.sleep(2)
            log.debug("客服登录系统成功")
        except:
            log.debug("客服登录系统失败")
            self.assertTrue(False, "TS-1977自动化测试失败!")
        try:
            # 不同测试环境工单过滤器不同
            if self.env == 0:
                driver.find_element_by_xpath("//a[@href=\"/entry/ticket/list/305853?column=&order=\"]").click()
            else:
                driver.find_element_by_xpath("//a[@href=\"/entry/ticket/list/779?column=&order=\"]").click()
            log.debug("选择\"所有工单\"过滤器")
        except:
            log.error("未能选择到\"所有工单\"过滤器")
            self.assertTrue(False, "TS-1977自动化测试失败!")
        # 根据渠道排序选取到邮件渠道工单（如果有）
        try:
            time.sleep(3)
            driver.find_element_by_xpath("//span[@title=\"渠道\"]").click()
            time.sleep(3)
            way = driver.find_element_by_xpath("//div[@class='list-table-scroll scrollbar']/table/tbody/tr[1]/td[7]")
            if "邮件" in way.text:
                log.debug("成功取到邮件渠道的工单，点击进入该工单详情")
                way.click()
                time.sleep(2)
            else:
                self.assertTrue(False, "未能取到邮件渠道的工单")
        except:
            log.debug("未能取到邮件渠道的工单!")
            self.assertTrue(False, "TS-1977自动化测试失败!")

        # 判断当前邮件渠道工单的满意度评价开关是否开启
        try:
            sati_text = driver.find_element_by_xpath("//*[@id=\"commit-panel\"]/div[2]/div[2]/div[2]/label/span").text
            if sati_text == "添加满意度调查":
                log.debug("此时该工单可以添加满意度调查")
            else:
                self.assertTrue(False, "TS-1977自动化测试失败!")
        except:
            log.debug("此时该工单不可以添加满意度调查，测试中止")
            self.assertTrue(False, "TS-1977自动化测试失败!")

        # 修改该工单的状态
        try:
            state = driver.find_element_by_xpath(
                "//*[@id=\"ticket-status\"]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/span")
            # 将工单的状态在“开启”和“已关闭”间切换下
            state.click()
            state_open = driver.find_element_by_xpath("//label[@class=\"open\"]")
            state_open.click()
            log.debug("成功将工单状态置为“开启”")
            time.sleep(2)
            state.click()
            state_open = driver.find_element_by_xpath("//label[@class=\"closed\"]")
            state_open.click()
            log.debug("成功将工单状态置为“已关闭”")
            time.sleep(2)
        except:
            log.error("修改工单的状态失败！")
            self.assertTrue(False, "TS-1977自动化测试失败！")

        # 判断当前邮件渠道工单的满意度评价开关是否开启
        try:
            sati_text1 = driver.find_element_by_xpath("//*[@id=\"commit-panel\"]/div[2]/div[2]/div[2]/label/span").text
            if sati_text1 == "添加满意度调查":
                log.debug("此时该工单可以添加满意度调查")
            else:
                self.assertTrue(False, "TS-1977自动化测试失败!")
        except:
            log.error("此时该工单已没有添加满意度调查按钮 ！")
            self.error = True

        # 添加工单标签
        # try:
        #     if self.env == 1:
        #         tag = driver.find_element_by_xpath(
        #             "//*[@id=\"ticket-status\"]/div[2]/div[1]/div[6]/div/div/div[2]/div/div/ul")
        #     else:
        #         tag = driver.find_element_by_xpath(
        #             "//*[@id=\"ticket-status\"]/div[2]/div[1]/div[5]/div/div/div[2]/div/div/ul")
        #     tag.click()
        #     # # 选择一个标签
        #     # i = 1
        #     # while True:
        #     #     tag1 = driver.find_element_by_xpath("//*[@id=\"select2-drop\"]/ul/li[%s]" % str(i))
        #     #     tag1_text = driver.find_element_by_xpath("//*[@id=\"select2-drop\"]/ul/li[1]/div").text
        #     #     try:
        #     #         tag1.click()
        #     #         time.sleep(2)
        #     #         log.debug("成功为工单添加标签“%s”" % str(tag1_text))
        #     #         break
        #     #     except:
        #     #         i += 1
        #     # 新建一个标签
        #     tag_name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        #     i = 1
        #     while True:
        #         try:
        #             if self.env == 1:
        #                 tag_input = driver.find_element_by_xpath(
        #                     "//*[@id=\"ticket-status\"]/div[2]/div[1]/div[6]/div/div/div[2]/div/div/ul/li[%s]/input" % i)
        #             else:
        #                 tag_input = driver.find_element_by_xpath(
        #                     "//*[@id=\"ticket-status\"]/div[2]/div[1]/div[5]/div/div/div[2]/div/div/ul/li[%s]/input" % i)
        #             break
        #         except:
        #             i += 1
        #     tag_input.send_keys(str(tag_name))
        #     driver.find_element_by_xpath("/html/body/div[12]/ul").click()
        #     state.click()
        #     state.click()
        #     log.debug("成功为工单添加标签“%s”" % str(tag_name))
        #     time.sleep(1)
        # except:
        #     log.error("为工单添加标签失败！")
        #     self.assertTrue(False, "TS-1977自动化测试失败！")

        # 判断当前邮件渠道工单的满意度评价开关是否开启
        try:
            sati_text1 = driver.find_element_by_xpath(
                "//*[@id=\"commit-panel\"]/div[2]/div[2]/div[2]/label/span").text
            if sati_text1 == "添加满意度调查":
                log.debug("TS-1977自动化测试成功！")
            else:
                self.assertTrue(False, "TS-1977自动化测试失败!")
        except:
            log.error("此时该工单已没有添加满意度调查按钮！")
            self.assertTrue(False, "TS-1977自动化测试失败!")
        finally:
            if self.error:
                self.assertTrue(False, "TS-1977自动化测试失败!")

    def tearDown(self):
        self.driver.quit()
