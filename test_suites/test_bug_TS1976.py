#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/21 10:34
'''
from test_env.set_driver import init_driver,admin_login
from test_env.set_log import init_log
from test_env.set_env import test_env
from test_env.set_random import random_string
import unittest
from time import sleep


class TestTS1976(unittest.TestCase):
    '''测试全局Bug：TS-1976'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("TS1976")
        self.env = test_env()

    def test_ts_1976(self):
        '''测试步骤：1.新建触发器，“通知-提醒目标”选择第二项;2.新建后再次进入编辑该触发器，观察“通知-提醒目标”是否仍为第二项(判断下拉框的value)'''
        driver = self.driver
        log = self.log
        # 管理员登录
        try:
            if self.env == 1:
                url = "linapp.udeskt1.com"
                log.debug("设定测试环境为\"%s\"" % url)
                admin_login(driver, url)
                driver.implicitly_wait(10)
                driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[8]").click()
                log.debug("管理员登录成功")
            else:
                url = "brazil.udesk.cn"
                log.debug("设定测试环境为\"%s\"" % url)
                admin_login(driver, url)
                driver.implicitly_wait(10)
                driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[9]").click()
                log.debug("管理员登录成功")
        except:
            log.error("管理员登录失败！")
            self.assertTrue(False, "TS-1976自动化测试失败!")
        try:
            sleep(2)
            # 下拉滚动条使得触发器可以点击
            driver.execute_script("document.querySelector('.ud-nav').scrollTop = 3000")
            # 进入触发器界面
            if self.env == 1:
                driver.find_element_by_xpath("/html/body/div[5]/div/nav/dl/dd[4]/a[5]").click()
            else:
                driver.find_element_by_xpath("/html/body/div[5]/div/nav/dl/dd[4]/a[4]").click()
            sleep(1)
            driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/div/div/a[1]").click()
            sleep(1)
            log.debug("新建触发器...")
            name = random_string()
            # 设置触发器
            sleep(2)
            driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[2]/div[1]/div/input").send_keys(name)
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div[2]/div[3]/div[2]/div/ul/li/div/select").click()
            sleep(1)
            # 发生事件
            driver.find_element_by_xpath("//option[@value='created']").click()
            sleep(1)
            driver.find_elements_by_xpath("//span[text()=\"添加新条件\"]")[0].click()
            sleep(1)
            # 满足任意条件
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div[2]/div[4]/div[2]/div/ul/li/div/select").click()
            sleep(1)
            driver.find_element_by_xpath("//option[@value='#status']").click()
            sleep(1)
            # 执行动作：通知-提醒目标
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div[2]/div[6]/div[2]/div/ul/li/div/select").click()
            sleep(1)
            driver.find_element_by_xpath("//option[@value='#tell_target']").click()
            sleep(1)
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div[2]/div[6]/div[2]/div/ul/li/div/div/div[1]/select").click()
            sleep(1)
            # 提醒通知选择第二个
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div[2]/div[6]/div[2]/div/ul/li/div/div/div[1]/select/option[2]").click()
            sleep(1)
            # 获取当前选择后下拉框的value
            before = driver.execute_script(
                "var e=document.querySelector('.ud-trigger-block .to select');return e.value")
            driver.find_element_by_xpath("//a[text()='确定']").click()
            log.debug("触发器新建成功")
        except:
            log.error("触发器新建失败")
            self.assertTrue(False, "TS-1976自动化测试失败!")
        # 重新进入该触发器
        sleep(2)
        driver.find_element_by_xpath("//span[text()='%s']/../span[4]/a[1]" % name).click()
        sleep(2)
        last = driver.execute_script("var e=document.querySelector('.ud-trigger-block .to select');return e.value")
        log.debug("重新进入该触发器，查看提醒文本是否改变")
        # 两次下拉框value值对比
        if before == last:
            log.debug("提醒文本选项与之前选择的相同")
            log.debug("TS-1976自动化测试成功!")
        else:
            log.debug("提醒文本选项与之前选择的不同")
            self.assertTrue(False, "TS-1976自动化测试失败!")

    def tearDown(self):
        self.driver.quit()
