# -*- coding: utf-8 -*-

# 参考： 托盘             http://blog.csdn.net/laike9m/article/details/8763060
#       加密模块         http://www.cnblogs.com/kaituorensheng/p/4501128.html
#       限制输入         http://blog.chinaunix.net/uid-10619456-id-3466149.html

# 登录成功信息窗体


import tkMessageBox
import tkFont
import os
import threading
import Queue
import win32con
try:
    import winxpgui as win32gui
except ImportError:
    import win32gui
from host import *
from loginLogoutUtil import *
from logger import *
from loginFrame import *
import systray
import fileinit

from mtTkinter import *

logger = Logger(fileinit.logfile, __name__).getlogger()


class LogoutFrame(Toplevel):

    def __init__(self, loginFrame):
        Toplevel.__init__(self)
        self.loginFrame = loginFrame
        self.geometry("300x500-100+100")
        self.resizable(width=False, height=False)  # 不可变
        self.protocol('WM_DELETE_WINDOW', self.winclose)

        self.main_frame = Frame(self)
        self.main_frame.pack()

        try:
            self.iconbitmap('resources\\favicon.ico')
        except Exception, e:
            logger.error('logout frame icon load failed', exc_info=True)

        logoutMenubar = Menu(self)

        filemenu = Menu(logoutMenubar, tearoff=0)
        filemenu.add_command(label="打开安装目录", command=self.opendir)
        filemenu.add_command(label="打开用户文件目录", command=self.open_usersfile_dir)
        filemenu.add_command(label="打开日志目录", command=self.open_log_dir)

        logoutMenubar.add_cascade(label="文件", menu=filemenu)
        logoutMenubar.add_command(label="关于", command=self.about)
        self['menu'] = logoutMenubar

        try:
            szu_logo = PhotoImage(file="resources\szulogout.gif")
            self.logo = Label(self.main_frame, image=szu_logo)
            self.logo.image = szu_logo
            self.logo.grid(row=0, column=0, columnspan=8)
        except Exception, e:
            logger.error('logout frame logo load failed', exc_info=True)

        # 获取ID
        campuscard_id = self.loginFrame.campusCardID.get()
        myhost = Host()
        hostaddr = myhost.gethost()

        ft = tkFont.Font(family='Microsoft YaHei UI Light', size=10)
        self.success_info_text = Label(self.main_frame, text="", font=ft)
        self.success_info_text.grid(row=1, column=2, columnspan=4, pady=(25, 10))
        self.address_show_text = Label(self.main_frame, text="", font=ft)
        self.address_show_text.grid(row=2, column=1, columnspan=6, pady=10)
        self.logout_button = Button(self.main_frame, text="注销", font=ft, command=self.logout_btn_click,
                                    height=1, width=12, fg="#FFFFFF", bg="#8C0A41")
        self.logout_button.grid(row=3, column=3, rowspan=2,
                                columnspan=2, sticky=W, pady=20, ipady=2)
        self.success_info_text["text"] = campuscard_id + " 登录成功！"
        self.success_info_text.configure(fg="black")
        if hostaddr == -1:
            self.address_show_text["text"] = "内网IP地址获取失败"
        else:
            self.address_show_text["text"] = "内网IP地址：" + str(hostaddr)

    def progress(self):
        self.prog_bar = ttk.Progressbar(
            self, orient="horizontal",
            length=300, mode="indeterminate"
        )
        self.prog_bar.pack(side=BOTTOM)

    def logout_btn_click(self):
        if self.state() != 'normal':
            self.update()
            self.deiconify()
        self.logout_button['state'] = 'disable'
        self.progress()
        self.prog_bar.start()
        self.prog_bar.step(10)

        self.queue = Queue.Queue()
        LogoutTry(self.queue).start()
        self.after(100, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            responseCode = msg
            if responseCode == 1:

                if self.state() != 'normal':
                    self.update()
                    self.deiconify()
                self.prog_bar.stop()
                self.prog_bar.pack_forget()
                self.logout_button['state'] = 'normal'
                # 隐藏注销页
                self.withdraw()
                # 给托盘进程发出destroy消息
                handle = win32gui.FindWindow(
                    None, self.loginFrame.window_class)
                win32gui.PostMessage(handle, win32con.WM_DESTROY, 0, 0)
                win32gui.PostMessage(handle, win32con.WM_NCDESTROY, 0, 0)
                # 生成新的用户列表
                self.loginFrame.userData = self.loginFrame.get_all_users()
                ID = [user[0] for user in self.loginFrame.userData]
                self.loginFrame.campusCardID["values"] = ID
                self.loginFrame.set_frame_configuration()
                # 如果登陆前没有勾选“记住密码”
                if self.loginFrame.remCheck.get() == 0:
                    s2 = self.loginFrame.campusCardPW.get()
                    self.loginFrame.campusCardPW.delete(0, len(s2))
                self.loginFrame.login_info_text["text"] = ""
                # 显示登录页
                self.loginFrame.parent.update()
                self.loginFrame.parent.deiconify()

            elif responseCode == -1:
                self.prog_bar.stop()
                self.prog_bar.pack_forget()
                self.logout_button['state'] = 'normal'
                tkMessageBox.showinfo("注销", "注销失败                   \n\n\n", parent=self)
        except Queue.Empty:
            self.after(100, self.process_queue)

    def about(self):
        author = "作者: " + fileinit.author + "\n"
        mail = fileinit.author_mail + "\n"
        content = "如果使用中有什么问题或者建议，欢迎给我发email\n\n"
        version = "version： " + fileinit.version
        msg = author + mail + content + version
        tkMessageBox.showinfo("关于", msg, parent=self)

    def opendir(self):
        path = os.getcwd()
        os.startfile(path)

    def open_usersfile_dir(self):
        path = fileinit.users_info_dir
        os.startfile(path)

    def open_log_dir(self):
        path = fileinit.all_users_profile_profcom
        os.startfile(path)

    def quit_systray(self):
        # 托盘退出
        self.systray_queue = Queue.Queue()
        LogoutTry(self.systray_queue).start()
        self.after(100, self.process_systray_queue)

    def process_systray_queue(self):
        try:
            msg = self.systray_queue.get(0)
            responseCode = msg
            if responseCode == 1:
                self.loginFrame.parent.quit()
            elif responseCode == -1:
                tkMessageBox.showinfo("退出", "注销失败，已退出            \n\n\n", parent=self)
                self.loginFrame.parent.quit()
        except Queue.Empty:
            self.after(100, self.process_systray_queue)

    def winclose(self):
        self.withdraw()


class LogoutTry(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        logout_util = LoginLogoutUtil()
        result = logout_util.logout()
        self.queue.put(result)
