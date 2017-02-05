# -*- coding: utf-8 -*-

from menu import Menu


def start():
    menu_obj = Menu()
    try:
        menu_obj.start_fork()
    except OSError:
        pass

if __name__ == '__main__':
    start()
