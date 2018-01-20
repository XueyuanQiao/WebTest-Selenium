# coding=utf-8
'''
@author: Qiaoxueyuan
@time: 2017/8/2 10:00
'''
import HTMLTestReportCN
import unittest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formataddr
import time
import email.encoders
import smtplib
import paramiko


# 定义发送邮件函数
def send_mail(message, all=0, fail=0, error=0):
    env = 3  # 0为发送给全体研发，1为发送给自己，2为发送测试组
    from_addr = "*************"
    password = "***********"
    if env == 0:
        to_addr = "g_rd@udesk.cn"
    elif env == 1:
        to_addr = "lixuegang@udesk.cn"
    elif env == 2:
        to_addr = ["qiaoxueyuan@udesk.cn", "lixuegang@udesk.cn"]
    else:
        to_addr = "qiaoxueyuan@udesk.cn"
    smtp_server = "smtpcloud.sohu.com"
    msg = MIMEMultipart()
    msg['From'] = formataddr(["UI自动化测试报告", "no-reply@autotest.udesk.cn"])
    msg['Subject'] = Header('UI自动化测试报告', 'utf-8').encode()
    if env == 2:
        for i in range(len(to_addr)):
            msg['To'] = formataddr([to_addr[i], to_addr[i]])
    else:
        msg['To'] = formataddr([to_addr, to_addr])

    totalnum = int(all)
    failnum = int(fail)
    errornum = int(error)
    passnum = totalnum - failnum - errornum
    html = """\
    <html><body><h3 style="font-size:20px">----- UI自动化测试完成 -----</h3>
    <table width="30%%" border="1" cellspacing="0">
    <tr>
        <td>总计</td>
        <td>通过</td>
        <td>失败</td>
        <td>错误</td>
        <td>通过率</td>
    </tr>
    <tr>
        <td>%d</td>
        <td>%d</td>
        <td>%d</td>
        <td>%d</td>
        <td>%.2f%%</td>
    </tr>
    </table>
    <p>报告详情请点击： <a href="http://autotest.udeskt1.com/%s">自动化测试报告</a>...附件预览会有乱码，请下载查看</p> 
    </body></html>
          """ % (totalnum, passnum, failnum, errornum, float(passnum) / float(
        totalnum) * 100, message)

    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # 添加附件:
    with open('.' + '/test_report/' + message, 'rb') as f:
        # 设置附件的MIME和文件名:
        mime = MIMEBase('text', 'html', filename=message.replace("自动化测试报告.html", '-auto-test-report.html'))
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment',
                        filename=message.replace("自动化测试报告.html", '-auto-test-report.html'))
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        email.encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    # 发送邮件
    if env == 2:
        server.sendmail(from_addr, [to_addr[0], to_addr[1]], msg.as_string())
    else:
        server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


# 定义上传报告函数
def upload_report(local, file):
    private_key = paramiko.RSAKey.from_private_key_file('D:\id_rsa.txt')  # 私钥
    ssh = paramiko.SSHClient()
    # ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # t1
    ssh.connect("***********", port=22, username='webuser', pkey=private_key)
    sftp = ssh.open_sftp()
    sftp.put(local, '/srv/www/autotest/' + file)
    ssh.close()

    # t1b
    ssh.connect("***********", port=22, username='webuser', pkey=private_key)
    sftp = ssh.open_sftp()
    sftp.put(local, '/srv/www/autotest/' + file)
    ssh.close()


# 设置报告文件保存路径
report_path = '.' + '/test_report/'

# 获取系统当前时间
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

# 设置报告名称格式
HtmlFile = report_path + now + "自动化测试报告.html"
fp = open(HtmlFile, "wb")
to_mail = HtmlFile.replace(report_path, '')

# 构建suite
suite_path = '.' + '/test_suites/'
suite = unittest.TestLoader().discover(suite_path)

if __name__ == '__main__':
    i = 0
    if i == 0:
        runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title="UI自动化测试报告", environment="http://brazil.udesk.cn",
                                                 tester="乔雪源,李雪刚",
                                                 description="用例执行情况")
    else:
        runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title="UI自动化测试报告", environment="http://linapp.udeskt1.com",
                                                 tester="乔雪源,李雪刚",
                                                 description="用例执行情况")
    # 执行用例
    test_result = runner.run(suite)

    # 执行情况统计
    all_case = test_result.testsRun
    fail_case = len(test_result.failures)
    error_case = len(test_result.errors)

    fp.close()

    # 上传报告至服务器
    upload_report(HtmlFile, to_mail)

    # 发送邮件
    time.sleep(20)
    send_mail(to_mail, all_case, fail_case, error_case)
