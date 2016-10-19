# -*- coding: utf-8 -*-
# 登录注销
import re
import requests
from logger import *
import fileinit

logger = Logger(fileinit.logfile, __name__).getlogger()


class LoginLogoutUtil():

    def __init__(self):
        # url设置
        self.loginurl = 'http://172.30.255.2/a30.htm'
        self.logouturl = 'http://172.30.255.2/F.htm'
        self.connTestUrl = 'http://www.szu.edu.cn/szu.asp'
        # 用headers把程序伪装成浏览器
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}

    def getresponse(self, form_data):
        # 发出请请求，若请求返回响应，异常返回-1
        try:
            s = requests.session()
            response = s.get(self.connTestUrl, headers=self.header, timeout=20)
            response = s.post(self.loginurl, data=form_data,
                              headers=self.header, timeout=20)
            content = response.content
            # 短时间重复提交登录，服务器返回“error5”
            rreg = r'error5'
            retryre = re.compile(rreg)
            retryflag = re.findall(retryre, content)
            while len(retryflag) > 0:
                # 先注销再请求登录
                response = s.get(
                    self.logouturl, headers=self.header, timeout=20)
                response = s.post(self.loginurl, data=form_data,
                                  headers=self.header, timeout=20)
                content = response.content
                rreg = r'error5'
                retryre = re.compile(rreg)
                retryflag = re.findall(retryre, content)
            return content
        except Exception, e:
            logger.error('login failed', exc_info=True)
            return -1

    def login(self, id, password):
        # 登录成功返回1 ，密码错误返回0，异常返回-1

        # 登录需要提交的表单
        form_data = {'DDDDD': 'XXXXXX',  # 填入校园卡号
                     'upass': 'XXXXXX',  # 填入校园卡密码
                     '0MKKey': '%B5%C7%A1%A1%C2%BC'
                     }
        form_data['upass'] = password  # 将密码填入表单
        form_data['DDDDD'] = str(id)  # 将用户名填入表单
        result = self.getresponse(form_data)  # 登录，获取返回的 response 结果
        if result == -1:
            return -1
        reg = r'UID'
        successre = re.compile(reg)
        flag = re.findall(successre, result)
        num = len(flag)
        if num >= 1:
            return 1
        else:
            return 0

    def logout(self):
        try:
            s = requests.session()
            response = s.get(self.logouturl, headers=self.header, timeout=20)
            return 1
        except Exception, e:
            logger.error('logout failed', exc_info=True)
            return -1
