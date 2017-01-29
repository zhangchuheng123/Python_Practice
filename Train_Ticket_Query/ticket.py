# coding=utf-8

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
import re

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Ticket:
    def __init__(self):
        # 载入车站名和电报码的关系
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        stations = requests.get(url, verify=False)
        self.station_str = stations.text

    def query_by_name(self, datestr, departure_name, arrival_name):
        try:
            departure_code = re.findall('%s\|([^|]+)' % departure_name, self.station_str)[0]
        except IndexError as e:
            raise
        try:
            arrival_code = re.findall('%s\|([^|]+)' % arrival_name, self.station_str)[0]
        except IndexError as e:
            raise
        return self.query_by_code(datestr, str(departure_code), str(arrival_code))

    @staticmethod
    def query_by_code(datestr, departure_code, arrival_code):
        query_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' \
                    + datestr + '&leftTicketDTO.from_station=' + departure_code \
                    + '&leftTicketDTO.to_station=' + arrival_code \
                    + '&purpose_codes=ADULT'
        r = requests.get(query_url, verify=False)
        return json.loads(r.text)['data']

    @staticmethod
    def print_by_key(data, key_list):
        information_dict = {'车次': 'train_no', '始发站': 'from_station_name', '终到站': 'end_station_name',
                            '出发站': 'start_station_name', '到达站': 'to_station_name',
                            '历时': 'lishi', '出发时间': 'start_time', '到达时间': 'arrive_time',
                            '商务座': 'swz_num', '特等座': 'tz_num', '一等座': 'zy_num',
                            '二等座': 'ze_num', '高级软卧': 'gr_num', '软卧': 'rz_num',
                            '硬卧': 'yw_num', '软座': 'rz_num', '硬座': 'yz_num',
                            '无座': 'wz_num', '其他': 'qt_num'}
        acronym_list = []
        for item in key_list:
            acronym_list.append(information_dict[item])

        table = PrettyTable(key_list)
        for item in data:
            info = item['queryLeftNewDTO']
            info_list = []
            for key_item in key_list:
                info_list.append(info[information_dict[key_item]])
            table.add_row(info_list)

        return table
