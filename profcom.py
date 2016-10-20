# -*- coding: utf-8 -*-
# 入口


from loginFrame import *
from Tkinter import *


def main():
    root = Tk()
    root.title("Profcom")
    curWidth = 400
    curHeight = 310
    scWidth, scHeight = root.maxsize()
    tempcnf = '%dx%d+%d+%d' % (curWidth, curHeight, (scWidth -
                                                     curWidth) / 2, (scHeight - curHeight) / 2)  # 是x 不是*
    root.geometry(tempcnf)
    root.resizable(width=False, height=False)  # 不可变
    app = LoginFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
