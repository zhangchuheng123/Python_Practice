# Log

## 2017-01-29

* base64编码方式是一种将小段二进制文件编码为字符串的编码方式，它把3个Byte编码为四个字符，字符从64元的字符集里面得到。

## 2017-01-30

* for语句的后置用法 ``mp3_url = [data[i]['mp3Url'] for i in range(0, len(data))]``
* 电话号码的正则表达式匹配 ``'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$'``

## 2017-01-31

* 想搞清楚这几个东西：md5, SHA, AES, binascii.hexlify, 

### MD5

* arbitrary length to 128-bit 'fingerprint' or 'message digest'
* unique
* inversion infeasible (except collision)
* digital signature before being encrypted in public-key cryptosystem (i.e. RSA)
