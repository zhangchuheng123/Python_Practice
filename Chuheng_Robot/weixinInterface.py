#! python2
# -*- coding: utf-8 -*-
import hashlib
import web
import time
import os
import urllib
import json
from lxml import etree


class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "chuhengrobot"
        # 字典序排序
        verification_list = [token, timestamp, nonce]
        verification_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, verification_list)
        hashcode = sha1.hexdigest()
        # sha1加密算法

        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):        
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        msg_type = xml.find("MsgType").text
        from_user = xml.find("FromUserName").text
        to_user = xml.find("ToUserName").text

        # 功能列表
        function_str = u"【翻译+文本】\n【交叉+姓名】\n【智能问答】\n【语音问答】\n【图片原样返回】\n【张楚珩的个人主页】"

        # 处理不同类型的消息, 转变为content变量提供下一步使用
        if msg_type == 'text':
            content = xml.find("Content").text  # input类型为unicode
        elif msg_type == 'voice':
            content = xml.find("Recognition").text  # input类型为unicode
            print(content)
        elif msg_type == 'event':
            event = xml.find('Event').text
            if event == 'subscribe':
                content = u'保留：subscribe'
            elif event == 'unsubscribe':
                content = u'保留：unsubscribe'
        elif msg_type == 'image':
            media_id = xml.find("MediaId").text
            response_all = {'kind': 'image', 'media_id': media_id}
            content = u'保留：跳过'
        else:
            content = u"保留：不支持的消息类型"

        # 处理文字信息
        if (content == u"helf") | (content == u"帮助"):
            response_all = {'kind': 'text', 'content': u"目前的功能有：\n" + function_str}
        elif content == u"保留：不支持的消息类型":
            response_all = {'kind': 'text', 'content': u"目前暂时不支持这种消息类型呀，现在支持文字和语音"}
        elif content == u'保留：subscribe':
            response_all = {'kind': 'text', 'content': u"欢迎和我聊天！目前的功能有：" + function_str +
                            u"\n 回复相应的文字即可使用功能"}
        elif content == u'保留：unsubscribe':
            response_all = {'kind': 'text', 'content': u"居然不理我了，拜拜！"}
        elif content[0:2] == u"翻译":
            response_all = self.youdao(content[2:])
        elif content[0:2] == u"交叉":
            response_all = self.phone_book(content[2:])
        elif (content == u"张楚珩") | (content == u"个人主页") | (content == u"张楚珩的个人主页"):
            response_all = {'kind': 'news', 'title': u'张楚珩的个人主页',
                            'description': u'这是我的个人主页，欢迎参观。请点击下方的"访问原网页"进行访问',
                            'picurl': u'http://sealzhang.tk/assets/images/2016-11-26-homepage.jpg',
                            'url': u'http://sealzhang.tk'}
        elif content != u'保留：跳过':
            response_all = self.answer_questions(content, from_user)

        # 根据response_all回复信息
        if response_all['kind'] == 'text':
            return self.render.reply_text(from_user, to_user, int(time.time()), response_all['content'])
        elif response_all['kind'] == 'link':
            return self.render.reply_text(from_user, to_user, int(time.time()),
                                          response_all['content'] + u'\n' + response_all['url'])
        elif response_all['kind'] == 'image':
            return self.render.reply_image(from_user, to_user, int(time.time()), response_all['media_id'])
        elif response_all['kind'] == 'news':
            return self.render.reply_news(from_user, to_user, int(time.time()), response_all['title'],
                                          response_all['description'], response_all['picurl'],
                                          response_all['url'])

    def youdao(self, input_text):
        # 利用有道API提供翻译和查词服务
        query = {'keyfrom': 'chuhengrobot',
                 'key': '990176764',
                 'type': 'data',
                 'doctype': 'xml',
                 'version': '1.1',
                 'q': input_text.encode('utf-8')}
        url = 'http://fanyi.youdao.com/openapi.do?' + urllib.urlencode(query)
        response = urllib.urlopen(url)
        xml_response = response.read()  # xml_response is utf-8
        xml = etree.fromstring(xml_response)  # the input needs to be utf-8

        code = xml.xpath('errorCode')
        if code[0].text == u'20':
            response_all = {'kind': 'text', 'content': u'你讲的太多了，我记不下来'}
            return response_all
        elif code[0].text == u'30':
            response_all = {'kind': 'text', 'content': u'这个翻译太难了，我不会'}
            return response_all
        elif code[0].text == u'40':
            response_all = {'kind': 'text', 'content': u'你讲的这种语言我不懂'}
            return response_all
        elif code[0].text == u'50':
            response_all = {'kind': 'text', 'content': u'翻译的钥匙找不到啦'}
            return response_all
        elif code[0].text == u'60':
            response_all = {'kind': 'text', 'content': u'无词典结果'}
            return response_all
        elif code[0].text != u'0':
            response_all = {'kind': 'text', 'content': u'这货发生了未知错误'}
            return response_all

        explain_content = u''
        explain = xml.xpath('translation/paragraph')
        if len(explain) == 0:
            explain = xml.xpath('basic/explains/ex')
        if len(explain) == 0:
            explain = xml.xpath('web/explain/value/ex')

        if len(explain) == 1:
            explain_content = explain[0].text
        elif len(explain) > 1:
            counter = 1
            for item in explain:
                explain_content = explain_content + unicode(counter) + u'. ' + item.text + u'\n'
                counter += 1

        response_all = {'kind': 'text', 'content': explain_content}
        return response_all

    def phone_book(self, name_text):
        # 利用自己挂在的XML返回通讯录查询信息
        name_text = name_text.strip()
        url = 'http://sealzhang.tk/WebAPI/jiaochayan16_basic_info.xml'
        response = urllib.urlopen(url)
        xml_response = response.read()
        xml = etree.fromstring(xml_response)
        output_content = name_text + u"的信息如下:\n"
        flag = 0

        nodes = xml.xpath(u".//*[@Name='" + name_text + u"']/Phone")
        if len(nodes) != 0:
            output_content = output_content + u"手机号码：" + nodes[0].text + u"\n"
            flag = 1
        nodes = xml.xpath(u".//*[@Name='" + name_text + u"']/Email")
        if len(nodes) != 0:
            output_content = output_content + u"电子邮箱：" + nodes[0].text + u"\n"
            flag = 1
        nodes = xml.xpath(u".//*[@Name='" + name_text + u"']/QQ")
        if len(nodes) != 0:
            output_content = output_content + u"QQ号码：" + nodes[0].text + u"\n"
            flag = 1
        nodes = xml.xpath(u".//*[@Name='" + name_text + u"']/Birthday")
        if len(nodes) != 0:
            output_content = output_content + u"出生日期：" + nodes[0].text + u"\n"
            flag = 1
        if flag == 1:
            response_all = {'kind': 'text', 'content': output_content}
        else:
            response_all = {'kind': 'text', 'content': u"你要查询的同学不存在，请检查一下名字是否写错了哦"}
        return response_all

    def answer_questions(self, question_text, from_user):
        # 利用图灵机器人进行智能问答回复
        url = 'http://www.tuling123.com/openapi/api'
        input_data = {
            "key": "c8ca0a3f0c344d0385f15d7d094c38af",
            "info": question_text.encode('utf-8'),
            "userid": from_user.encode('utf-8')
        }
        post_data = urllib.urlencode(input_data)
        response = urllib.urlopen(url + u'?' + post_data)
        parsed_json = json.loads(response.read())
        if parsed_json['code'] == 100000:
            response_all = {'kind': 'text', 'content': parsed_json['text']}
        elif parsed_json['code'] == 200000:
            response_all = {'kind': 'link', 'content': parsed_json['text'], 'url': parsed_json['url']}
        elif (parsed_json['code'] == 302000) | (parsed_json['code'] == 308000):
            response_all = {'kind': 'text', 'content': parsed_json['text']}
        elif (parsed_json['code'] == 40001) | (parsed_json['code'] == 40002) | (parsed_json['code'] == 40004) | (parsed_json['code'] == 40007):
            response_all = {'kind': 'text',
                            'content': u'这货有点蠢，出bug了 错误代码：' + unicode(parsed_json['code']) + \
                                       u'调试信息：' + parsed_json['text'] + \
                                       u'你的问题：' + unicode(parsed_json['code'])+question_text}
        else:
            response_all = {'kind': 'text', 'content': u'这货太懒了，没有反应，也没有留下什么调试信息，T_T'}

        return response_all

