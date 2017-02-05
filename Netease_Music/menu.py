# -*- coding: utf-8 -*-

import os

from ui import Ui
import curses


class Menu:
    __main_menu_items = [
        '0. Search Songs',
        '1. Login'
    ]

    __main_status_list = [
        'search',
        'login'
    ]

    __instruction = {
        'main': 'UP/DOWN: move | RIGHT: select | q: quit',
        'search_input': 'TYPE: search string | ENTER: search | q: quit',
        'search': 'UP/DOWN: move | LEFT: back to main | q: quit',
        'login_input': 'TYPE: account and password | ENTER: go | q: quit',
        'login': 'info display - LEFT: back to main | q: quit'
    }

    def __init__(self):
        self.ui = Ui()
        self.MENU_ITEMS_PER_PAGE = self.ui.NUM_MAX_RESULTS_PER_PAGE

    def start_fork(self):
        pid = os.fork()
        if pid != 0:
            self.start()

    def start(self):
        key_pos = 0
        status = 'main'
        menu_items = self.__main_menu_items
        stack = ['main']
        storage = {}

        self.ui.build_title()
        self.ui.build_instruction(self.__instruction[status])
        self.ui.build_stack(stack)
        self.ui.build_menu(menu_items, key_pos)
        self.ui.build_copyright()

        while True:
            key = self.ui.screen.getch()

            # 退出
            if key == ord('q'):
                break
            # 向下移动
            elif key == curses.KEY_DOWN:
                if key_pos is not None:
                    if key_pos + 1 < len(menu_items):
                        key_pos += 1
                        offset = self.MENU_ITEMS_PER_PAGE * (key_pos // self.MENU_ITEMS_PER_PAGE)
                        self.ui.build_menu(menu_items, key_pos, offset)
            # 向上移动
            elif key == curses.KEY_UP:
                if key_pos is not None:
                    if key_pos > 0:
                        key_pos -= 1
                        offset = self.MENU_ITEMS_PER_PAGE * (key_pos // self.MENU_ITEMS_PER_PAGE)
                        self.ui.build_menu(menu_items, key_pos, offset)
            # 向右进入
            elif key == curses.KEY_RIGHT:
                if status == 'main':
                    status = self.__main_status_list[key_pos]
                    # 从main到search
                    if status == 'search':
                        stack.append(status)
                        self.ui.build_stack(stack)
                        self.ui.build_instruction(self.__instruction['search_input'])
                        data_search = self.ui.build_search()
                        if 'error' not in data_search:
                            menu_items = data_search['menu_items']
                            storage.update(data_search['menu_info'])
                            key_pos = 0
                            self.ui.build_menu(menu_items, key_pos)
                            self.ui.build_instruction(self.__instruction[status])
                            self.ui.build_stack(stack)
                        else:
                            # problem occurs
                            status = 'main'
                    # 从main到login
                    elif status == 'login':
                        stack.append(status)
                        self.ui.build_stack(stack)
                        self.ui.build_instruction(self.__instruction['login_input'])
                        data_login = self.ui.build_login()
                        if 'error' not in data_login:
                            menu_items = data_login['menu_items']
                            storage.update(data_login['menu_info'])
                            key_pos = None
                            self.ui.build_menu(menu_items, key_pos)
                            self.ui.build_instruction(self.__instruction[status])
                            self.ui.build_stack(stack)
                        else:
                            # problem occurs
                            status = 'main'
                    else:
                        status = 'main'
            # 向左回退
            elif key == curses.KEY_LEFT:
                if (status == 'search') | (status == 'login'):
                    stack.pop()
                    status = stack[-1]
                    key_pos = 0
                    menu_items = self.__main_menu_items
                    self.ui.build_menu(menu_items, key_pos)
                    self.ui.build_instruction(self.__instruction[status])
                    self.ui.build_stack(stack)

            self.ui.build_copyright()
            self.ui.screen.refresh()

        self.ui.quit()
