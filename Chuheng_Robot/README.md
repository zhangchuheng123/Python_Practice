#说明

这是一个微信公众号（订阅号）的后台程序，实现简单的问答系统、翻译和通讯录查询功能。
使用python作为后台，挂载在SAE（新浪云）上。
目前来说，微信后天的python实现有一个比较主流的包``wechat-python-sdk``，但本程序并没有使用，而是自己编写了相关的接口。

关键词：

* 微信订阅号+Python+SAE
* 微信身份验证
* 微信文字、图片、新闻信息的回复
* 图灵机器人智能问答API接入
* 有道词典API接入
* 通讯录XML文件信息获取
* 使用微信的语音识别功能，实现语音问答

具体配置可在网络上找到相关的教程，这里不详细讲，欢迎参考借鉴相关代码。

欢迎扫描下方二维码订阅公众号查看具体功能。

![](./scan_code.jpg)

#Programming Log

##2017-01-16

实现微信公众平台接口和SAE绑定

微信公众平台实现信息自动回复

##2017-01-17

搭建本地PyCharm调试环境 解决web模块无法在本地安装的问题

	原因：import web使用的package是web.py 不是web

解决了python Class中method需要增加self传入参数的问题

	method的第一个参数必须为self，调用的时候略去不写

解决了一个编码问题

	微信text类型传入的文字为Unicode编码，
	进来之后应该用encode('utf-8')变为utf-8编码，这样才能进行urlencode

解决了从PyCharm上面直接commit和push到SAE的问题

	terminal中的命令为 git push sae master:1
	在PyCharm的配置里面应该写作master  -> sae: 1

编码问题解决了一部分 但是还是不清楚 持续困扰中

解决MacOS El Captain不允许升级python six包，导致wechat_sdk安装失败的问题

	sudo -H pip2 install --ignore-installed wechat_sdk

用github page（硬）编码了通讯录，然后再服务器端抓取写好的通讯录XML文件，XML文件使用matlab输出

利用图灵机器人构建问答系统

##2017-01-18

添加了错误拦截机制，增强了程序稳定性

解决了有时候回答里面还有比如``'``这样的特殊符号的时候，会显示为html编码的问题

    web.py的render会默认进行转义，将变量名$Var写成$:Var的时候可以避免转义
    
##2017-01-19

由于微信的权限问题，实体为个人的订阅号无法获得素材管理（图片、语音等）的接口，后续更多功能的开发遇到较大的困难，今天完善了代码并且停止更新。