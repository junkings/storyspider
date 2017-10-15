# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
from email.header import Header
# 第一个为文本内容,第二个设置文本格式,第三个编码格式
class Mail(object):
    def __init__(self):
        self.msg = MIMEText('Python邮件发送测试','plain','utf-8')
        # 显示于发件人
        self.msg['From'] = Header('小说更新提醒','utf-8')
        # 显示与收件人
        self.msg['To'] = Header('你自己','utf-8')
        # 就是标题,最醒目的
        self.subject = 'Python SMTP发送邮件小说更新'
        self.msg['Subject'] = Header(self.subject,'utf-8')
        # print self.msg
        #
        # 发送方
        self.from_addr = '876142347@qq.com'
        # 必须是自动授权码,需要发送人的授权码
        self.password = '*******'

        # qq的smtp服务器
        self.smtp_server = 'smtp.qq.com'
        # 接收方
        self.to_addr = '876142347@qq.com'

    def content(self, content):
        self.msg = MIMEText(content, 'plain', 'utf-8')
        # 显示于发件人
        self.msg['From'] = Header('小说更新提醒', 'utf-8')
        # 显示与收件人
        self.msg['To'] = Header('你自己', 'utf-8')
        # 就是标题,最醒目的
        self.subject = 'Python SMTP发送邮件小说更新'
        self.msg['Subject'] = Header(self.subject, 'utf-8')

    def send(self):
        import smtplib
        # server = smtplib.SMTP(smtp_server,25)
        # 使用了ssl模式
        server = smtplib.SMTP_SSL(self.smtp_server,465)
        # 设置为调试模式
        server.set_debuglevel(1)

        # 登陆ssl服务器
        server.login(self.from_addr,self.password)
        # 发送邮件
        server.sendmail(self.from_addr,[self.to_addr],self.msg.as_string())
        # 退出
        server.quit()

if __name__ == "__main__":
    m = Mail()
    m.send()
    import time
    time.sleep(1)
    m.content("22222222")
    m.send()
