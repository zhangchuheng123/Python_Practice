# -*- coding: utf-8 -*-

from netease_api import NetEase
# from NEMbox.api import NetEase
import hashlib

netease = NetEase()

password = hashlib.md5(raw_password.encode('utf-8')).hexdigest()

signin_result = netease.login('zhangchuheng123@163.com', password)
print(signin_result)

signin_mobile_result = netease.daily_signin(0)

signin_pc_result = netease.daily_signin(1)

pass
