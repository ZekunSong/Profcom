# -*- coding: utf-8 -*-
import sys
import time
if sys.platform.startswith("win32"):
    from win32api import GetLastError
    from winerror import ERROR_ALREADY_EXISTS
import tkFont
from Tkinter import *


ORG = "Neal"
APP_NAME = "Profcom"


class Singleton(object):

    def __init__(self):
        if sys.platform.startswith("win32"):
            from win32event import CreateMutex
            self.mutexName = '%s.%s' % (ORG, APP_NAME)
            self.myMutex = CreateMutex(None, False, self.mutexName)  # 创建核心对象
            self.lastErr = GetLastError()  # 检查lasterr
        else:
            # 是linux平台,可以把文件固定写在/tmp下,每次读这个文件检查pid内容，看是否有同样的pid存在
            pass

    def isAlive(self):
        if sys.platform.startswith("win32"):
            if self.lastErr == ERROR_ALREADY_EXISTS:  # 如果LastError表示已经存在，则返回，表示进程表里有同样的进程存在
                return True
            else:
                return False
        else:
            # 检查（linux）
            return False


def close_window(window):
    window.destroy()

if __name__ == '__main__':
    singleton = Singleton()
    if singleton.isAlive() == False:
        import profcom
        profcom.main()
    else:
        root = Tk()
        root.title("Profcom")
        cur_width = 400
        cur_height = 330
        scWidth, scHeight = root.maxsize()
        tempcnf = '%dx%d+%d+%d' % (cur_width, cur_height, (scWidth -
                                                           cur_width) / 2, (scHeight - cur_height) / 2)  # 是x 不是*
        root.geometry(tempcnf)
        root.resizable(width=False, height=False)  # 不可变
        try:
            root.iconbitmap('resources\\favicon.ico')
        except Exception, e:
            pass
        try:
            szu_logo = PhotoImage(file="resources\szulogin.gif")
            logo = Label(root, image=szu_logo)
            logo.image = szu_logo
            logo.grid(row=0, column=0, columnspan=8)
        except Exception, e:
            pass
        ft = tkFont.Font(family='Microsoft YaHei UI Light', size=14)
        lab = Label(root, text="Profcom 已在运行", font=ft)
        lab.grid(row=1, column=1, columnspan=6, pady=40)
        button = Button(root, text="确定", command=lambda: close_window(
            root), height=1, width=12, fg="#FFFFFF", bg="#8C0A41")
        button.grid(row=2, column=3, rowspan=2,
                    columnspan=2, sticky=W, ipady=2)
        root.mainloop()
