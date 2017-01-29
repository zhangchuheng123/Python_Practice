# -*- coding: utf-8 -*-

from weixinInterface import WeixinInterface

# content = u'小狗的图片'
# user_id = u'张楚珩'
#
# instance = WeixinInterface()
# output_all = instance.answer_questions(content, user_id)
# print(output_all['kind'])
# print(output_all['content'])

# content = u'交叉 啧啧啧'
#
# instance = WeixinInterface()
# if content[0:2] == u"交叉":
#     output_all = instance.phone_book(content[2:])
# print(output_all['kind'])
# print(output_all['content'])

content = u'翻译 爱斯基摩犬长得还不错'

instance = WeixinInterface()
if content[0:2] == u"翻译":
    output_all = instance.youdao(content[2:])
print(output_all['kind'])
print(output_all['content'])
