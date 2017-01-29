# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Zhang Chuheng
Email: zhangchuheng123@live.com
Date: 2015-12-27
Description:
	This script is for search for locations containing some keyword in a specified city.
	All the results are written to output.txt.
	Baidu Map API is used here.
	Since it can only return 400 results per query, the possible region of interested city is divided 
	into grids, and each of the lattice points are detected and query for results if the point belongs
	to the interested city.
"""

import urllib
import chardet
import xml.etree.ElementTree as ET
import math

# These paramenters can be costumized,
# where as you should put your own Baidu Map API private key here.
# The key is provided for free at http://developer.baidu.com/map/index.php?title=首页
page_size = 20
city = '北京市'
query = '便利店'
private_key = '>>>>you should put your own key here<<<<'

# Two type of Baidu Map Web API are used: Place API and Geocoding API
search_baseurl = 'http://api.map.baidu.com/place/v2/search'
search_values = {"ak":private_key,"outputs":"xml","query":query,\
    "page_size":str(page_size),"scope":"1"}
geo_baseurl = 'http://api.map.baidu.com/geocoder/v2/'
geo_values = {"ak":private_key,"outputs":"xml"}

# The following coordinate is Baidu Map Coordinate which is the outter frame of the city
# You can fetch these coordinate at http://api.map.baidu.com/lbsapi/getpoint/
lat1 = 39.496607
lng1 = 115.278009
lat2 = 41.241387
lng2 = 117.559274

lattice_num = 100

delta_lat = (lat2 - lat1) / lattice_num
delta_lng = (lng2 - lng1) / lattice_num

# set up the output file
with open('output.txt', 'w', encoding='utf-8') as f:
	f.write('This is the Begining of the output file: \n')

for lat in range(lattice_num):
	for lng in range(lattice_num):
		# generate new lattice point and test whether it belongs to the interested city
		geo_values['location'] = '%f,%f' % (lat1 + ((lat+0.5)*delta_lat),lng1 + ((lng+0.5)*delta_lng))
		data = urllib.parse.urlencode(geo_values) 
		url = geo_baseurl + '?' + data
		response = urllib.request.urlopen(url)
		info_bytes = response.read()
		info_type = chardet.detect(info_bytes)
		info_str = info_bytes.decode(info_type['encoding'])
		try:
			info_tree = ET.fromstring(info_str)
		except Exception as e:
			print(info_str)
			print('Warning: ', e.strerror, e.errno)
		print(info_tree.find('result').find('addressComponent').find('city').text, lat, lng)
		if info_tree.find('result').find('addressComponent').find('city').text == city:
			# The query if returned page by page, and this is why the iteration is used here
			for i in range(20):
				bounds = '%f,%f,%f,%f' % (lat1 + (lat*delta_lat), lng1 + (lng*delta_lng), lat1 + ((lat+1)*delta_lat), lng1 + ((lng+1)*delta_lng))
				search_values['bounds'] = bounds
				search_values['page_num'] = '%d' % i
				data = urllib.parse.urlencode(search_values) 
				data = data.replace('%2C',',')
				url = search_baseurl + '?' + data
				response = urllib.request.urlopen(url)
				info_bytes = response.read()
				info_type = chardet.detect(info_bytes)
				info_str = info_bytes.decode(info_type['encoding'])
				try:
					info_tree = ET.fromstring(info_str)
				except Exception as e:
					print(info_str)
					print('Warning: ', e.strerror, e.errno)
				if (info_tree[0].text == '0') and (info_tree[1].text == 'ok'):
					tot = int(info_tree[2].text)
					if (i >= math.ceil(tot / page_size)):
						break
				else:
					# In the returning XML file, status == 0 and message == 'ok' if there's nothing wrong.
					print('Ooooooops! There seems something wrong!')
				if (i == 19):
					# If the number of returning results is exceeding the upper limit of 400, you'd better 
					# increase the lattice number to ensure there are no more than 400 results in each of 
					# the individual grid cell.
					print("Warning: You'd better increase 'lattice_num'.")
				with open('output.txt', 'a', encoding='utf-8') as f:
					f.write(info_str)
