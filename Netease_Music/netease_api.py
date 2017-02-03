# -*- coding: utf-8 -*-

import requests
import re
import binascii
import os
import json
import base64
import time

from builtins import chr

from Crypto.Cipher import AES
from http.cookiejar import LWPCookieJar


class Constant(object):
    cookie_path = 'cookie.txt'


class NetEase(object):
    def __init__(self):
        self.modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
                        'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
                        '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
                        '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
                        '3ece0462db0a22b8e7')
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/33.0.1750.152 Safari/537.36')
        }
        self.cookies = {'appver': '1.5.2'}
        self.playlist_class_dict = {}
        self.session = requests.Session()
        self.default_timeout = 10
        self.constant = Constant()
        self.session.cookies = LWPCookieJar(self.constant.cookie_path)
        try:
            self.session.cookies.load()
            cookie = ''
            if os.path.isfile(self.constant.cookie_path):
                self.file = open(self.constant.cookie_path, 'r')
                cookie = self.file.read()
                self.file.close()
            expire_time = re.compile(r'\d{4}-\d{2}-\d{2}').findall(cookie)
            if expire_time:
                if expire_time[0] < time.strftime('%Y-%m-%d', time.localtime(time.time())):
                    os.remove(self.constant.cookie_path)
        except IOError:
            self.session.cookies.save()

    @staticmethod
    def create_secret_key(size):
        return binascii.hexlify(os.urandom(size))[:16]

    @staticmethod
    def aes_encrypt(text, sec_key):
        pad = 16 - len(text) % 16
        text += chr(pad) * pad
        encryptor = AES.new(sec_key, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    @staticmethod
    def rsa_encrypt(text, pub_key, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16),
                 int(pub_key, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def encrypted_request(self, text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(text, self.nonce),
                                    sec_key)
        enc_sec_key = self.rsa_encrypt(sec_key, self.pub_key, self.modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        return data

    def raw_http_request(self, method, action, query=None):
        if method == 'GET':
            url = action if query is None else action + '?' + query
            result = self.session.get(url,
                                      headers=self.header,
                                      timeout=self.default_timeout)
        elif method == 'POST':
            result = self.session.post(action, data=query,
                                       headers=self.header,
                                       timeout=self.default_timeout)
        elif method == 'Login_POST':
            result = self.session.post(action, data=query,
                                       headers=self.header,
                                       timeout=self.default_timeout)
            self.session.cookies.save()
        else:
            return {'error': 'raw_http_request'}

        result.encoding = 'UTF-8'
        return result.text

    def http_request(self, method, action, query=None):
        json_result = json.loads(
            self.raw_http_request(method, action, query)
        )
        return json_result

    def login(self, username, password):
        pattern = re.compile(r'^0\d{2,3}\d{7,8}$|^1[34578]\d{9}$')
        if pattern.match(username):
            return self.phone_login(username, password)
        else:
            return self.account_login(username, password)

    def phone_login(self, username, password):
        action = 'https://music.163.com/weapi/login/cellphone'
        text = {
            'phone': username,
            'password': password,
            'rememberLogin': 'true'
        }
        data = self.encrypted_request(text)
        try:
            return self.http_request('Login_POST', action, data)
        except requests.RequestException:
            return {'error': 'phone_login'}

    def account_login(self, username, password):
        action = 'https://music.163.com/weapi/login/'
        text = {
            'username': username,
            'password': password,
            'rememberLogin': 'true'
        }
        data = self.encrypted_request(text)
        try:
            return self.http_request('Login_POST', action, data)
        except requests.RequestException:
            return {'error': 'account_login'}

    def daily_signin(self, signin_type):
        # signin_type: 0 移动端 1 PC端
        action = 'http://music.163.com/weapi/point/dailyTask'
        text = {'type': signin_type}
        data = self.encrypted_request(text)
        try:
            return self.http_request('POST', action, data)
        except requests.RequestException:
            return {'error': 'daily_signin'}

    def search(self, s, stype=1, offset=0, total='true', limit=60):
        # stype: 单曲(1)，歌手(100)，专辑(10)，歌单(1000)，用户(1002)
        action = 'http://music.163.com/api/search/get'
        data = {
            's': s,
            'type': stype,
            'offset': offset,
            'total': total,
            'limit': limit
        }
        return self.http_request('POST', action, data)

    def user_playlist(self, uid, offset=0, limit=100):
        action = 'http://music.163.com/api/user/playlist/?offset={}&limit={}&uid={}'\
            .format(offset, limit, uid)
        try:
            data = self.http_request('GET', action)
            return data['playlist']
        except requests.RequestException:
            return {'error': 'user_playlist'}

    def song_detail(self, music_id):
        action = 'http://music.163.com/api/song/detail/?id={}&ids=[{}]'.format(music_id, music_id)
        try:
            data = self.http_request('GET', action)
            return data['songs']
        except requests.RequestException:
            return {'error', 'song_detail'}

    def playlist_detail(self, playlist_id):
        action = 'http://music.163.com/api/playlist/detail?id={}'.format(
            playlist_id)
        try:
            data = self.http_request('GET', action)
            return data['result']['tracks']
        except requests.RequestException:
            return {'error': 'playlist_detail'}

    @staticmethod
    def get_info(data, data_type='search_songs', info_type='single_song', id=None):
        try:
            if (data_type == 'search_songs') & (info_type == 'single_song'):
                if (data['code'] == 200) & ('songCount' in data['result']):
                    return data['result']['songs'][id]
            elif (data_type == 'single_song') & (info_type == 'music_id'):
                return data['id']
            elif (data_type == 'single_song_detail') & (info_type == 'mp3_url'):
                return data[0]['mp3Url']
            elif (data_type == 'search_users') & (info_type == 'single_user'):
                if (data['code'] == 200) & (data['result']['userprofileCount'] != 0):
                    return data['result']['userprofiles'][id]
            elif (data_type == 'single_user') & (info_type == 'user_id'):
                return data['userId']
            elif (data_type == 'user_playlist') & (info_type == 'single_playlist'):
                if len(data) != 0:
                    return data[id]
            elif (data_type == 'single_playlist') & (info_type == 'playlist_id'):
                return data['id']
            elif (data_type == 'playlist_detail') & (info_type == 'mp3_url'):
                if id is None:
                    mp3_url = [data[i]['mp3Url'] for i in range(0, len(data))]
                else:
                    mp3_url = [data[i]['mp3Url'] for i in id]
                return mp3_url
        except KeyError:
            return {'error': 'get_info_key_error'}
        except IndexError:
            return {'error': 'get_info_index_error'}
