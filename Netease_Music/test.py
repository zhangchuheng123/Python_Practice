# -*- coding: utf-8 -*-

from netease_api import NetEase
# from NEMbox.api import NetEase

netease = NetEase()

result = netease.search('zhangchuheng123', stype=1002)
uid = netease.get_info(netease.get_info(result, 'search_users', 'single_user', id=0),
                       'single_user', 'user_id')
print(uid)
playlist = netease.user_playlist(uid)

pid = netease.get_info(netease.get_info(playlist, 'user_playlist', 'single_playlist', id=0),
                       'single_playlist', 'playlist_id')

playlist_detail = netease.playlist_detail(pid)

mp3_urls = netease.get_info(playlist_detail, 'playlist_detail', 'mp3_url')

pass
