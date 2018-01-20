#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/12/16 下午3:51
'''

import unittest
from time import sleep
from test_env.set_log import init_log
from test_env.set_driver import admin_login
from test_env.set_driver import init_driver


class TestTS2656(unittest.TestCase):
    '''测试全局BUG：Ts-2656'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("Ts-2656")
        self.env = 0  # 0线上环境，1测试环境

    def tearDown(self):
        self.driver.quit()

    def test_ts_2656(self):
        '''测试步骤：管理员修改邮件模板内容保存，判定修改是否生效'''
        driver = self.driver
        log = self.log
        env = self.env
        change_text = "测试修改邮件模板"

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

        sleep(2)
        log.debug("管理员登录成功")
        driver.find_element_by_xpath("//div[@class='wrapper']/nav/dl/dd[2]/a[1]").click()  # 1为渠道管理“邮箱”位置
        sleep(4)
        log.debug("'邮箱设置'进入成功")

        old_text = driver.find_element_by_id("email-template").text  # 备份原模板内容
        log.debug("成功获取到此时邮件模板的内容")
        driver.find_element_by_id("email-template").clear()  # 清除模板内容
        driver.find_element_by_id("email-template").send_keys(change_text)  # 填入设定好的内容

        def save_button(driver):
            saves = driver.find_elements_by_xpath("//button[text()='保存']")
            length = len(saves)
            saves[length - 1].click()  # 保存修改后的模板
            sleep(1)

        save_button(driver)
        log.debug("将邮件模板内容替换为定义好的文字")


        # 切换到其他页面在切换回来
        driver.find_element_by_xpath("//div[@class='wrapper']/nav/dl/dd[2]/a[2]").click()
        sleep(2)
        driver.find_element_by_xpath("//div[@class='wrapper']/nav/dl/dd[2]/a[1]").click()
        sleep(2)
        log.debug("切换到其他页面在切换回来,重新获取模板内容")

        new_text = str(driver.find_element_by_id("email-template").text).replace(" ","")  # 重新获取邮件模板内容

        if new_text == change_text:
            log.debug("邮件模板内容已修改为定义好的文字")
            log.debug("Ts-2656成功通过自动化测试")

            driver.find_element_by_id("email-template").clear()  # 清除模板内容
            driver.find_element_by_id("email-template").send_keys(old_text)  # 将模板内容还原为修改前内容
            save_button(driver)  # 保存修改后的模板
            log.debug("已将模板内容还原为修改前的内容")

        else:
            log.debug("邮件模板内容不是刚才修改的定义好的文字，而是：")
            log.debug("%s" % new_text)

            driver.find_element_by_id("email-template").clear()  # 清除模板内容
            driver.find_element_by_id("email-template").send_keys(old_text)  # 将模板内容还原为修改前内容
            save_button(driver)  # 保存修改后的模板
            log.debug("已将模板内容还原为修改前的内容")

            raise Exception("Ts-2656自动化测试失败")
