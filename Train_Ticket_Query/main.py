# coding=utf-8

from ticket import Ticket

datestr = '2017-02-01'
departure_station_code = 'BJP'
departure_station_name = u'北京'
arrival_station_code = 'JBN'
arrival_station_name = u'上海'
key_list = ['车次', '始发站', '终到站', '出发站', '到达站', '历时', '出发时间', '到达时间',
            '商务座', '特等座', '一等座', '二等座', '高级软卧', '软卧',
            '硬卧', '软座', '硬座', '无座', '其他']

ticket_request = Ticket()

# 通过站名查火车票
data = ticket_request.query_by_name(datestr, departure_station_name, arrival_station_name)
print(ticket_request.print_by_key(data, key_list))

# 通过车站电报码查火车票
data = ticket_request.query_by_code(datestr, departure_station_code, arrival_station_code)
print(ticket_request.print_by_key(data, key_list))
