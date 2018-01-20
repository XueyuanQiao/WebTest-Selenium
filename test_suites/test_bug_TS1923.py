#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/2 10:00
'''
from test_env.set_driver import init_driver,admin_login
from test_env.set_log import init_log
from test_env.set_env import test_env
from test_env.set_random import random_string
import unittest
import time

class TestTs1923(unittest.TestCase):
    '''测试全局Bug：TS-1923'''

    def setUp(self):
        self.driver = init_driver()
        self.log = init_log("Ts1923")
        self.env = test_env()

    def test_Ts1923(self):
        '''测试步骤：1.新建员工组;2.新建员工（属于新建的客服组）;3.删除新建的客服;4.删除新建的客服组;5.确认是否删除成功'''
        log = self.log
        driver = self.driver
        try:
            # 登录管理员账号
            if self.env == 0:
                url = "brazil.udesk.cn"
                log.debug("设定测试环境为\"%s\"" % url)
                admin_login(driver, url)
            else:
                url = "linapp.udeskt1.com"
                log.debug("设定测试环境为\"%s\"" % url)
                admin_login(driver, url)
                driver.implicitly_wait(5)
            driver.find_element_by_xpath("//*[@href=\"/entry/\"]")
        except:
            self.assertTrue(False, "管理员登录失败")
        log.debug("管理员登录成功")
        # 转到管理中心页面
        try:
            driver.implicitly_wait(10)
            driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/ul/li[8]").click()
            driver.implicitly_wait(5)
        except:
            self.assertTrue(False, "管理中心进入失败")
        log.debug("管理中心进入成功")
        # 进入员工组页面

        try:
            driver.find_element_by_xpath("/html/body/div[5]/div/nav/dl/dd[1]/a[2]").click()
            driver.implicitly_wait(10)

            # 点击新增员工组
            driver.find_element_by_xpath("//button[@class='btn btn-primary square-border btn-sm']").click()
        except:
            self.assertTrue(False, "员工组页面进入失败")
        log.debug("员工组页面进入成功")
        try:
            # 设置员工组名称
            group = random_string()
            driver.find_element_by_xpath("//input[@placeholder='员工组名称']").send_keys(group)
            time.sleep(1)
            driver.find_element_by_xpath("//button[@data-style='zoom-in' and text()='确定']").click()
            time.sleep(3)
        except:
            self.assertTrue(False, "员工组创建失败")
        log.debug("员工组%s创建成功" % group)
        # 进入员工列表页面
        try:
            driver.find_element_by_xpath("/html/body/div[5]/div/nav/dl/dd[1]/a[1]").click()
            time.sleep(5)

            # 点击新增员工
            driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div[2]/div[2]/div[1]/a").click()
        except:
            self.assertTrue(False, "员工列表页面进入失败")
        log.debug("员工列表页面进入成功")
        try:
            # 定义随机字符串
            agent_email = random_string()
            # 创建邮箱
            driver.find_element_by_xpath("//*[@placeholder=\"邮箱\"]").send_keys(agent_email + "@udesk.cn")
            # 创建密码
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[2]/div[2]/input[2]").send_keys("password123")
            # 创建姓名
            agent_name = random_string()
            driver.find_element_by_xpath("//*[@placeholder=\"姓名\"]").send_keys(agent_name)
            log.debug("新建员工%s" % agent_name)
            # 设置员工角色，选择下拉框第一个
            driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[8]/div[2]/div").click()
            driver.find_element_by_xpath("//*[@id=\"select2-drop\"]/ul/li[1]").click()
            # 设置员工组，选择刚才新建的
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[9]/div[2]/div/ul/li/input").click()
            try:
                a = driver.find_element_by_xpath("//div[@class='select2-result-label' and text()='%s']" % group)
                a.click()
            except:
                self.assertTrue(False, "员工组查找失败")
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[10]/div[2]/input").send_keys("1")
            try:
                # 设置员工部门
                driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[11]/div[2]/div/a").click()
                time.sleep(1)
                driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[11]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/ul").click()
                driver.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div[1]/div[2]/form/ul/li[11]/div[2]/div/div/div/div/div[3]/button[2]").click()
                time.sleep(1)
                driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div[2]/form/div/a[2]").click()
                time.sleep(1)
            except:
                self.assertTrue(False, "员工部门设置失败")
        except:
            self.assertTrue(False, "员工新建失败")
        log.debug("员工%s新建成功" % agent_name)

        # 点击员工列表栏目
        driver.find_element_by_xpath("/html/body/div[5]/div/nav/dl/dd[1]/a[1]").click()

        # 寻找创建的客服并删除
        def find_agent(s=1):
            while True:
                try:
                    b = driver.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div[1]/div[2]/div[2]/div[3]/table/tbody/tr[%d]/td[4]" % s)
                    if b.text == agent_name:
                        driver.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div[1]/div[2]/div[2]/div[3]/table/tbody/tr[%d]/td[15]/div/a[3]" % s).click()
                        log.debug("成功点击员工%s删除按钮" % agent_name)
                        time.sleep(2)
                        return True
                    else:
                        s = s + 1
                except:
                    try:
                        log.debug("当前页未找到客服%s，进入下一页寻找" % agent_name)
                        driver.implicitly_wait(10)
                        driver.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[1]/div/a[2]").click()
                        return False
                    except:
                        self.assertTrue(False, "员工%s未找到，删除失败" % agent_name)

        result = find_agent()
        while result is False:
            result = find_agent()
        # 确认删除员工时的提示
        try:
            driver.find_element_by_xpath(
                "/html/body/div[5]/div/div/div[1]/div[3]/div/div/form/div[3]/button[2]").click()
            driver.implicitly_wait(10)
        except:
            self.assertTrue(False, "员工%s删除失败" % agent_name)
        log.debug("员工%s成功删除" % agent_name)

        # 点击员工组栏目
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[5]/div/nav/dl/dd[1]/a[2]").click()
        time.sleep(1)
        # 寻找创建的员工组并删除
        s = 1
        while True:
            try:
                c = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/table/tbody/tr[%d]/td[2]" % s)
                if c.text == group:
                    driver.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div[3]/table/tbody/tr[%d]/td[6]/div/a[3]" % s).click()
                    log.debug("成功点击员工组%s删除按钮" % group)
                    time.sleep(2)
                    try:
                        driver.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div/div[4]/div/div/form/div[3]/button[2]").click()
                        log.debug("成功点击员工组删除确认按钮")
                        time.sleep(2)
                        break
                    except:
                        self.assertTrue(False, "员工组删除确认按钮点击失败")
                else:
                    s = s + 1
            except:
                self.assertTrue(False, "员工组%s删除失败" % group)

        # driver.refresh()
        # driver.switch_to.alert.accept()
        time.sleep(2)
        try:
            c.text == group
            log.debug("员工组%s仍然存在" % group)
            log.debug("员工组%s删除失败" % group)
        except:
            log.debug("员工组%s成功删除" % group)
            log.debug("TS-1923成功通过UI自动化测试！")
            return
        self.assertTrue(False, "TS-1923UI自动化测试失败！")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
