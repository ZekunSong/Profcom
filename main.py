#-*- coding:utf-8 -*-
# 检查程序是否已运行
import os
from mtTkinter import *
import tkFont
import win32com.client
import subprocess


def check_exsit(process_name):
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery(
        'select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        return 1
    else:
        return 0


def close_window(window):
    window.destroy()

if __name__ == '__main__':
    app_process = 'Profcom.exe'
    if check_exsit(app_process) == 0:
        try:
            path = os.getcwd() + "\\" + app_process
            subprocess.Popen(path)
        except Exception, e:
            root = Tk()
            root.title("Profcom")
            curWidth = 400
            curHeight = 330
            scWidth, scHeight = root.maxsize()
            tempcnf = '%dx%d+%d+%d' % (curWidth, curHeight, (scWidth -
                                                             curWidth) / 2, (scHeight - curHeight) / 2)  # 是x 不是*
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
            lab = Label(root, text="Profcom 模块程序丢失", font=ft)
            lab.grid(row=1, column=1, columnspan=6, pady=40)
            button = Button(root, text="确定", command=lambda: close_window(
                root), height=1, width=12, fg="#FFFFFF", bg="#8C0A41")
            button.grid(row=2, column=3, rowspan=2,
                        columnspan=2, sticky=W, ipady=2)
            root.mainloop()

    else:
        root = Tk()
        root.title("Profcom")
        curWidth = 400
        curHeight = 330
        scWidth, scHeight = root.maxsize()
        tempcnf = '%dx%d+%d+%d' % (curWidth, curHeight, (scWidth -
                                                         curWidth) / 2, (scHeight - curHeight) / 2)  # 是x 不是*
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
