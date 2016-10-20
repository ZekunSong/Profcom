# -*- coding: utf-8 -*-
# 入口
from loginFrame import *
from Tkinter import *


def main():
    root = Tk()
    root.title("Profcom")
    cur_width = 400
    cur_height = 310
    scWidth, scHeight = root.maxsize()
    tempcnf = '%dx%d+%d+%d' % (cur_width, cur_height, (scWidth -
                                                       cur_width) / 2, (scHeight - cur_height) / 2)  # 是x 不是*
    root.geometry(tempcnf)
    root.resizable(width=False, height=False)  # 不可变
    app = LoginFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
