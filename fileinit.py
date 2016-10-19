# -*- coding: utf-8 -*-
# 初始化文件目录和一些全局变量

import os

author = 'Neal'
author_mail = ''
version = '1.4.0'
app_name = 'Profcom'


# os.environ.get('ALLUSERSPROFILE')
all_users_profile = os.getenv('ALLUSERSPROFILE')
userProfile = os.getenv('LOCALAPPDATA')

# 创建目录
all_users_profile_profcom = all_users_profile + '\\' + app_name
if not os.path.exists(all_users_profile_profcom):
    os.makedirs(all_users_profile_profcom)
# 创建文件
logfile = all_users_profile_profcom + '\Profcom.log'
with open(logfile, "a")as f:
    pass

# 创建目录
user_profile_profcom = userProfile + '\\' + app_name
if not os.path.exists(user_profile_profcom):
    os.makedirs(user_profile_profcom)

# 创建文件
users_info_dir = user_profile_profcom + "\users"
if not os.path.exists(users_info_dir):
    os.makedirs(users_info_dir)

config_info_dir = user_profile_profcom + "\configuration"
if not os.path.exists(config_info_dir):
    os.makedirs(config_info_dir)
