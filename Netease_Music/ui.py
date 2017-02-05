# -*- coding: utf-8 -*-

import curses
from netease_api import NetEase
import locale


class Ui:

    COLOR_GREEN = 1
    COLOR_CYAN = 2
    COLOR_RED = 3
    COLOR_YELLOW = 4

    LINE_TITLE = 0
    LINE_INSTRUCTION = 1
    LINE_STACK = 2
    LINE_MENU_ITEMS_SEP1 = 3
    LINE_MENU_START = 4
    LINE_MENU_ITEMS_SEP2 = 14
    LINE_SEARCH = 8
    LINE_ACCOUNT = 7
    LINE_PASSWORD = 9
    LINE_COPYRIGHT = 15

    NUM_MAX_RESULTS = 100
    NUM_MAX_RESULTS_PER_PAGE = 10

    SCREEN_WIDTH = 80

    STR_SEP = '-' * SCREEN_WIDTH
    STR_INSTRUCTION =  \
        'Instruction    >>  '
    STR_STACK = \
        'You are here   >>  '
    STR_SEARCH = \
        'Search Songs:      '
    STR_LOGIN_ACCOUNT = \
        'Account/Phone:     '
    STR_LOGIN_PASSWORD = \
        'Password:          '
    STR_NOTHING = \
        'Nothing here T^T   '
    STR_PROBlEM = \
        'Something wrong T_T'
    STR_LOGIN_SUCCESS = \
        'Login succeed :)   '
    STR_SIGNIN_MOBILE = \
        'Mobile signin succeed  ♫♪♬♪♩'
    STR_SIGNIN_PC = \
        'PC signin succeed      ♬♪♫♩♬'
    STR_COPYRIGHT = \
        'Zhang Chuheng ©️ 2017'
    STR_TITLE = \
        'NetEase Music Tool'

    def __init__(self):
        self.netease = NetEase()
        # init screen
        self.screen = curses.initscr()
        # enable color
        curses.start_color()
        # do not echo bytes that user types
        curses.noecho()
        # transfer to program every time user types
        curses.cbreak()
        # process special keys
        self.screen.keypad(True)
        # setup colors
        curses.init_pair(self.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # processing non-ascii character
        locale.setlocale(locale.LC_ALL, '')

    def addstr(self, *args):
        if len(args) == 1:
            self.screen.addstr(args[0].encode('utf-8'))
        elif len(args) == 2:
            self.screen.addstr(args[0].encode('utf-8'), args[1])
        else:
            self.screen.addstr(args[0], args[1], args[2].encode('utf-8'), *args[3:])

    @staticmethod
    def quit():
        curses.endwin()

    def build_title(self):
        self.screen.move(self.LINE_TITLE, 0)
        self.screen.clrtoeol()
        self.addstr('{:^{width}}'.format(self.STR_TITLE, width=self.SCREEN_WIDTH), curses.color_pair(self.COLOR_CYAN))

    def build_instruction(self, instruction):
        self.screen.move(self.LINE_INSTRUCTION, 0)
        self.screen.clrtoeol()
        self.addstr(self.STR_INSTRUCTION)
        self.addstr(instruction)

    def build_stack(self, stack):
        self.screen.move(self.LINE_STACK, 0)
        self.screen.clrtoeol()
        self.addstr(self.STR_STACK)
        for i in range(0, len(stack)):
            self.addstr(stack[i])
            if i != len(stack) - 1:
                self. addstr(' > ', curses.color_pair(self.COLOR_YELLOW))

    def build_copyright(self):
        self.screen.move(self.LINE_COPYRIGHT, 0)
        self.screen.clrtoeol()
        self.addstr('{:^{width}}'.format(self.STR_COPYRIGHT, width=self.SCREEN_WIDTH), curses.color_pair(self.COLOR_CYAN))

    def build_menu(self, data, highlight_pos=None, offset=0):
        """

        :param data_type: 'main' / 'search'
        :param data: should be a list of str
        :param highlight_pos: highlight_position
        :param offset: where the display start from
        :return:
        """
        # clear bottom
        self.screen.move(self.LINE_MENU_ITEMS_SEP1, 0)
        self.screen.clrtobot()
        curses.noecho()

        # add seperator
        self.addstr(self.LINE_MENU_ITEMS_SEP1, 0, self.STR_SEP)

        item_num = 0
        start_num = offset
        end_num = min(start_num+self.NUM_MAX_RESULTS_PER_PAGE, len(data))

        for i in range(start_num, end_num):
            item = data[i]
            if (highlight_pos is not None) & (i == highlight_pos):
                self.addstr(self.LINE_MENU_START + item_num, 0,
                            item, curses.color_pair(self.COLOR_RED))
            else:
                self.addstr(self.LINE_MENU_START + item_num, 0, item)
            item_num += 1

        # add seperator
        self.addstr(self.LINE_MENU_ITEMS_SEP2, 0, self.STR_SEP)

    def build_search(self):
        # clear bottom
        self.screen.move(self.LINE_MENU_ITEMS_SEP1, 0)
        self.screen.clrtobot()
        curses.noecho()

        # add seperator
        self.addstr(self.LINE_MENU_ITEMS_SEP1, 0, self.STR_SEP)
        self.addstr(self.LINE_MENU_ITEMS_SEP2, 0, self.STR_SEP)

        song_name = self.get_param(self.LINE_SEARCH, self.STR_SEARCH)

        try:
            display = []
            music_id = []
            data = self.netease.search(song_name)
            if data['code'] == 200:
                if data['result']['songCount'] != 0:
                    count = min(data['result']['songCount'], self.NUM_MAX_RESULTS)
                    for i in range(0, count):
                        the_song = data['result']['songs'][i]
                        name = the_song['name'][:15]
                        artist = the_song['artists'][0]['name'][:15]
                        album = the_song['album']['name'][:15]
                        string = '{id:<2}. {name:{name_wd}}{artist:{artist_wd}}{album:{album_wd}}'.format(
                            id=i,
                            name=name,
                            name_wd=max(1, 30-self.count_chinese(name)),
                            artist=artist,
                            artist_wd=max(1, 30-self.count_chinese(artist)),
                            album=album,
                            album_wd=max(1, 30-self.count_chinese(album))
                        )
                        display.append(string)
                        music_id.append(the_song['id'])
                else:
                    display.append(self.STR_NOTHING)
            else:
                display.append(self.STR_PROBlEM)

        except Exception:
            return {'error': 'build_search'}
        return {'menu_items': display, 'menu_info': {'music_id': music_id}}

    def build_login(self):
        # clear bottom
        self.screen.move(self.LINE_MENU_ITEMS_SEP1, 0)
        self.screen.clrtobot()
        curses.noecho()

        # add seperator
        self.addstr(self.LINE_MENU_ITEMS_SEP1, 0, self.STR_SEP)
        self.addstr(self.LINE_MENU_ITEMS_SEP2, 0, self.STR_SEP)

        account = self.get_param(self.LINE_ACCOUNT, self.STR_LOGIN_ACCOUNT)
        password = self.get_param(self.LINE_PASSWORD, self.STR_LOGIN_PASSWORD, echo=False)
        password = self.netease.md5_password(password)

        display = []
        user_id = 0

        try:
            data = self.netease.login(account, password)
            if data['code'] == 200:
                display.append(self.STR_LOGIN_SUCCESS)
                user_id = data['profile']['userId']
            else:
                display.append(self.STR_PROBlEM)

            data = self.netease.daily_signin(0)
            if data['code'] == 200:
                display.append(self.STR_SIGNIN_MOBILE)

            data = self.netease.daily_signin(1)
            if data['code'] == 200:
                display.append(self.STR_SIGNIN_PC)
        except Exception:
            return {'error': 'build_login'}
        return {'menu_items': display, 'menu_info': {'user_id': user_id}}

    @staticmethod
    def count_chinese(string):
        count = 0
        for ch in string:
            if ord(ch) > 255:
                count += 1
        return count

    def get_param(self, line_number, prompt_string, echo=True):
        if echo:
            curses.echo()
        else:
            curses.noecho()
        info = ''
        while info.strip() is '':
            self.screen.move(line_number, 0)
            self.screen.clrtoeol()
            self.addstr(line_number, 0, prompt_string)
            self.screen.refresh()
            info = self.screen.getstr().decode()
        curses.noecho()
        return info
