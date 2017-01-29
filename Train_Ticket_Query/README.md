# Description

学习python，做了一个火车票的余票查询系统。

具体使用方法如下

## 通过车站电报码来查询

```
from ticket import Ticket

datestr = '2017-02-01'
departure_station_code = 'BJP'
arrival_station_code = 'JBN'
key_list = ['车次', '始发站', '终到站', '出发站', '到达站', '历时', '出发时间', '到达时间',
            '商务座', '特等座', '一等座', '二等座', '高级软卧', '软卧',
            '硬卧', '软座', '硬座', '无座', '其他']

ticket_request = Ticket()

# 通过车站电报码查火车票
data = ticket_request.query_by_code(datestr, departure_station_code, arrival_station_code)
print(ticket_request.print_by_key(data, key_list))

```

## 通过车站名来查询
```
# coding=utf-8

from ticket import Ticket

datestr = '2017-02-01'
departure_station_name = u'北京'
arrival_station_name = u'上海'
key_list = ['车次', '始发站', '终到站', '出发站', '到达站', '历时', '出发时间', '到达时间',
            '商务座', '特等座', '一等座', '二等座', '高级软卧', '软卧',
            '硬卧', '软座', '硬座', '无座', '其他']

ticket_request = Ticket()

# 通过站名查火车票
data = ticket_request.query_by_name(datestr, departure_station_name, arrival_station_name)
print(ticket_request.print_by_key(data, key_list))

```

# 实现方法

具体的实现方法在网上一找一大把，这里不再详述。

关键点

* 通过网址``https://kyfw.12306.cn/otn/leftTicket/queryZ``可以用车站电报码查询到车票信息，返回格式为JSON
* 通过文件``https://kyfw.12306.cn/otn/resources/js/framework/station_name.js``可以找到车站名和车站电报码的对应关系
* 直接使用requests.get方法访问查询的接口会显示SSL错误，应该加上``verify=False``选项
* 使用PrettyTable来格式化输出数据，基本使用方法为``table = PrettyTable(['A','B'])``，``table.add_row['A1','B1']``