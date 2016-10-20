# -*- coding: utf-8 -*-

# 参考： 托盘             http://blog.csdn.net/laike9m/article/details/8763060
#       加密模块         http://www.cnblogs.com/kaituorensheng/p/4501128.html
#       限制输入         http://blog.chinaunix.net/uid-10619456-id-3466149.html

# 登录窗体


import ttk
import tkFont
import tkMessageBox
import os
import threading
import Queue
from random import Random
from prpcrypt import *
from loginLogoutUtil import *
from logger import *
from logoutFrame import *
import fileinit

from mtTkinter import *

logger = Logger(fileinit.logfile, __name__).getlogger()


class LoginFrame(Frame):
    """docstring for LoginFrame"""

    def __init__(self, master):

        Frame.__init__(self)
        self.parent = master
        self.icon_count = 0

        menubar = Menu(master)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="打开安装目录", command=self.opendir)
        filemenu.add_command(label="打开用户文件目录", command=self.open_usersfile_dir)
        filemenu.add_command(label="打开日志目录", command=self.open_log_dir)

        menubar.add_cascade(label="文件", menu=filemenu)
        menubar.add_command(label="关于", command=self.about)

        master['menu'] = menubar

        '''
        self.users_data=(
            ["100000","123456"],
            ["100001","123456"])
        '''
        # 初始化用户列表
        self.users_data = self.get_all_users()
        self.create_widgets()
        self.set_frame_configuration()
        self.handle_aoto_login()
        self.bind_all("<Return>", self.login_btn_click)

    def create_widgets(self):
        self.main_frame = Frame(self.parent)
        self.main_frame.pack()

        try:
            self.parent.iconbitmap('resources\\favicon.ico')
        except Exception, e:
            logger.error('login frame icon load failed', exc_info=True)
        try:
            szu_logo = PhotoImage(file="resources\szulogin.gif")
            self.logo = Label(self.main_frame, image=szu_logo)
            self.logo.image = szu_logo
            self.logo.grid(row=0, column=0, columnspan=8)
        except Exception, e:
            logger.error('login frame logo load failed', exc_info=True)

        ft = tkFont.Font(family='Microsoft YaHei UI', size=10)
        ift = tkFont.Font(family='Microsoft YaHei UI', size=9)
        sft = tkFont.Font(family='Microsoft YaHei UI Light',
                          size=8, underline=1)

        self.idrem = StringVar()
        self.pwrem = StringVar()
        self.label_id = Label(self.main_frame, text="卡号:", font=ft)
        self.label_id.grid(row=1, column=1, columnspan=2, sticky=E,
                           padx=(0, 5), pady=(20, 0), ipady=1)

        # 下拉输入
        ID = [user[0] for user in self.users_data]
        self.campusCardID = ttk.Combobox(
            self.main_frame, textvariable=self.idrem, values=ID, width=25, font=ift)
        self.campusCardID.bind('<<ComboboxSelected>>', self.combobox_handler)
        self.campusCardID.bind('key', self.id_keypress)
        self.campusCardID.grid(row=1, column=3, columnspan=3,
                               sticky=W, pady=(20, 0), ipady=1)

        # 删除账号信息
        self.delIDLab = Label(self.main_frame, text="删除此账号信息",
                              font=sft, fg="#2F4BA0")
        self.delIDLab.grid(row=2, column=4, columnspan=2, sticky=E)
        self.delIDLab.bind("<Button-1>", self.del_user_info)

        self.label_pw = Label(self.main_frame, text="密码:", font=ft)
        self.label_pw.grid(row=3, column=1, columnspan=2, sticky=E,
                           padx=(0, 5), pady=(0, 10), ipady=1)

        self.campusCardPW = Entry(
            self.main_frame, show="*", textvariable=self.pwrem, width=25, font=ift)
        self.campusCardPW.bind('key', self.pw_keypress)
        self.campusCardPW.grid(row=3, column=3, columnspan=3,
                               sticky=W, pady=(0, 10), ipady=1)

        self.remCheck = IntVar()
        self.remCheck.set(1)
        self.autoCheck = IntVar()
        self.rem = Checkbutton(
            self.main_frame, text="记住密码", variable=self.remCheck, command=self.remcheck_is_selected, font=ft)
        self.rem.grid(row=4, column=2, columnspan=2, sticky=E, padx=(0, 5))
        self.auto = Checkbutton(
            self.main_frame, text="自动登录", variable=self.autoCheck, command=self.autocheck_is_selected, font=ft)
        self.auto.grid(row=5, column=2, columnspan=2, sticky=E, padx=(0, 5))
        self.login_button = Button(self.main_frame, text="登录", command=self.login_btn_click,
                                   height=1, width=12, fg="#FFFFFF", bg="#8C0A41", font=ft)
        self.login_button.grid(row=4, column=4, rowspan=2,
                               columnspan=2, sticky=W, ipady=2)

        self.login_info_text = Label(self.main_frame, text="", font=ft)
        self.login_info_text.grid(row=6, column=2, columnspan=4, pady=(5, 0))

        self.after(100, self.handle_pw_show)

    def handle_aoto_login(self):
        if self.autoCheck.get() == 1:
            self.login_btn_click()

    def create_key(self, randomlength=16):
        str = ''
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            str += chars[random.randint(0, length)]
        return str

    def get_key(self, file):
        try:
            with open(file, 'r') as f:
                key_and_pw_length = 48
                key_and_pw = f.read()
                if len(key_and_pw) != key_and_pw_length:
                    key = self.create_key()
                else:
                    key = key_and_pw[0:16]
        except Exception as e:
            key = self.create_key()
            raise e
        finally:
            return key

    def about(self):
        author = "作者: " + fileinit.author + "\n"
        mail = fileinit.author_mail + "\n"
        content = "如果使用中有什么问题或者建议，欢迎给我发email\n\n"
        version = "version： " + fileinit.version
        msg = author + mail + content + version
        tkMessageBox.showinfo("关于", msg, parent=self.parent)

    def opendir(self):
        path = os.getcwd()
        os.startfile(path)

    def open_usersfile_dir(self):
        path = fileinit.users_info_dir
        os.startfile(path)

    def open_log_dir(self):
        path = fileinit.all_users_profile_profcom
        os.startfile(path)

    def progress(self):
        self.prog_bar = ttk.Progressbar(
            self.parent, orient="horizontal",
            length=400, mode="indeterminate"
        )
        self.prog_bar.pack(side=BOTTOM)

    def combobox_handler(self, event=None):
        current = self.campusCardID.current()
        self.campusCardPW.delete(0, END)
        self.campusCardPW.insert(END, self.users_data[current][1])

    def handle_pw_show(self):
        if len(self.campusCardID.get()) != 6:
            self.campusCardPW.delete(0, END)
        else:
            for user in self.users_data:
                if self.campusCardID.get() == user[0] and len(self.campusCardPW.get()) == 0:
                    self.campusCardPW.insert(END, user[1])
        self.after(100, self.handle_pw_show)

    def id_keypress(self, event=None):
        try:
            textcheck = str(self.campusCardID.get())
            textcheck = ''.join(i for i in textcheck if i in '0123456789')
            self.campusCardID.set(int(textcheck))
        except ValueError:
            self.campusCardID.set('')

    def pw_keypress(self, event=None):
        try:
            textcheck = str(self.campusCardPW.get())
            textcheck = ''.join(i for i in textcheck if i in '0123456789')
            self.pwrem.set(int(textcheck))
        except ValueError:
            self.pwrem.set('')

    def remcheck_is_selected(self):
        if self.remCheck.get() == 0:
            self.autoCheck.set(0)

    def autocheck_is_selected(self):
        if self.autoCheck.get() == 1:
            self.remCheck.set(1)

    def del_user_info(self, event=None):
        if self.users_data != () and tkMessageBox.askokcancel("删除账号信息", "删除该账号信息？", parent=self, default="cancel"):
            self.del_data()

    def del_data(self, event=None):
        campuscard_id = self.campusCardID.get()

        file = fileinit.users_info_dir + "\\" + campuscard_id
        if os.path.isfile(file):
            os.remove(file)

        # 生成新的用户列表并显示
        self.users_data = self.get_all_users()
        ID = [user[0] for user in self.users_data]
        self.campusCardID["values"] = ID
        if len(ID) > 0:
            self.idrem.set(ID[0])
        else:
            self.idrem.set("")
            self.pwrem.set("")

    def get_all_users(self):
        filenames = os.listdir(fileinit.users_info_dir)
        all_users = []
        for item in filenames:
            user = ["userID", "userPW"]
            item = os.path.join(fileinit.users_info_dir, item)
            if os.path.isfile(item):
                userID = os.path.basename(item)
                try:
                    self.key = self.get_key(item)
                    with open(item, "r") as f:
                        key_and_pw = f.read()
                        if len(key_and_pw) == 48:
                            pc = Prpcrypt(self.key)
                            PW = pc.decrypt(key_and_pw[16:48])
                        else:
                            PW = ''
                        user[0] = userID
                        user[1] = PW
                        all_users.append(user)
                except Exception, e:
                    logger.error('open userfile failed', exc_info=True)
        all_users = tuple(all_users)
        return all_users

    def set_frame_configuration(self):
        setAutocheck = 1
        # 填入ID和密码
        filenames = os.listdir(fileinit.config_info_dir)
        file = fileinit.config_info_dir + "\\lastLogin.ini"
        if os.path.isfile(file):
            try:
                f = open(file, "r")
                lastLoginID = f.read()
                # 查找密码
                filenames = os.listdir(fileinit.users_info_dir)
                file = fileinit.users_info_dir + "\\" + lastLoginID
                if os.path.isfile(file):
                    try:
                        self.key = self.get_key(file)
                        infof = open(file, "r")
                        key_and_pw = infof.read()
                        if len(key_and_pw) == 48:
                            pc = Prpcrypt(self.key)
                            PW = pc.decrypt(key_and_pw[16:48])
                        else:
                            PW = ''
                        self.idrem.set(lastLoginID)
                        self.pwrem.set(PW)
                    except Exception, e:
                        logger.error('open userfile failed', exc_info=True)
                    finally:
                        if infof:
                            infof.close()
                else:
                    setAutocheck = 0
            except Exception, e:
                logger.error('open configure file failed', exc_info=True)
            finally:
                if f:
                    f.close()
        else:
            setAutocheck = 0

        # 自动登录
        filenames = os.listdir(fileinit.config_info_dir)
        file = fileinit.config_info_dir + "\\autoLogin.ini"
        if os.path.isfile(file):
            try:
                f = open(file, "r")
                self.autoCheck.set(int(f.read()))
            except Exception, e:
                logger.error('open configure file failed', exc_info=True)
                self.autoCheck.set(0)
            finally:
                if f:
                    f.close()

        if setAutocheck == 0:
            self.autoCheck.set(0)

    def login_btn_click(self, event=None):
        campuscard_id = self.campusCardID.get()
        campuscard_pw = self.campusCardPW.get()
        self.login_info_text["text"] = ""
        if len(campuscard_id) != 6 and len(campuscard_pw) == 6:
            self.login_info_text["text"] = "卡号长度不正确!"
            self.login_info_text.configure(fg="red")
            self.campusCardID.delete(0, len(campuscard_id))
        elif len(campuscard_pw) != 6 and len(campuscard_id) == 6:
            self.login_info_text["text"] = "密码长度不正确!"
            self.login_info_text.configure(fg="red")
            self.campusCardPW.delete(0, len(campuscard_pw))
        elif len(campuscard_id) != 6 and len(campuscard_pw) != 6:
            self.login_info_text["text"] = "卡号和密码长度不正确!"
            self.login_info_text.configure(fg="red")
            self.campusCardID.delete(0, len(campuscard_id))
            self.campusCardPW.delete(0, len(campuscard_pw))
        else:
            self.login_button['state'] = 'disable'
            self.progress()
            self.prog_bar.start()
            self.prog_bar.step(20)

            self.queue = Queue.Queue()
            LoginVerify(self.queue, campuscard_id, campuscard_pw).start()
            self.after(100, lambda: self.process_queue(
                campuscard_id, campuscard_pw))

    def process_queue(self, campuscard_id, campuscard_pw):
        try:
            msg = self.queue.get(0)
            # show result of the task if needed
            response_code = msg
            if response_code == 1:
                self.prog_bar.stop()
                self.prog_bar.pack_forget()
                self.login_button['state'] = 'normal'

                # 记住最新登录用户ID
                filenames = os.listdir(fileinit.config_info_dir)
                file = fileinit.config_info_dir + "\\lastLogin.ini"
                try:
                    with open(file, "w") as f:
                        f.write(campuscard_id)
                except Exception, e:
                    logger.error('open configure file failed', exc_info=True)

                # 检查“记住密码”
                if self.remCheck.get() == 1:  # 记住密码
                    file = fileinit.users_info_dir + "\\" + campuscard_id
                    try:
                        self.key = self.get_key(file)
                        with open(file, "w") as f:
                            pc = Prpcrypt(self.key)
                            pwen = pc.encrypt(campuscard_pw)
                            f.write(self.key + pwen)
                    except Exception, e:
                        logger.error('open userfile failed', exc_info=True)

                else:  # 不记住密码
                    file = fileinit.users_info_dir + "\\" + campuscard_id
                    try:
                        with open(file, "w") as f:
                            pass
                    except Exception, e:
                        logger.error('open userfile failed', exc_info=True)

                # 检查“自动登录”
                if self.autoCheck.get() == 1:  # 勾选“自动登录”

                    filenames = os.listdir(fileinit.config_info_dir)
                    file = fileinit.config_info_dir + "\\autoLogin.ini"
                    try:
                        with open(file, "w") as f:
                            f.write("1")
                    except Exception, e:
                        logger.error(
                            'open configure file failed', exc_info=True)

                else:  # 不勾选“自动登录”
                    filenames = os.listdir(fileinit.config_info_dir)
                    file = fileinit.config_info_dir + "\\autoLogin.ini"
                    try:
                        with open(file, "w") as f:
                            f.write("0")
                    except Exception, e:
                        logger.error(
                            'open configure file failed', exc_info=True)

                # 隐藏登录页
                self.parent.withdraw()

                # 显示注销页
                # LogoutFrameThread(self,systrayThread).start()
                self.parent.logoutFrame = LogoutFrame(self)
                self.parent.logoutFrame.update()
                self.parent.logoutFrame.deiconify()
                # 显示托盘
                systrayThread = SysTrayTread(self)
                systrayThread.start()

            elif response_code == 0:
                # 登录页，页面不变化
                self.prog_bar.stop()
                self.prog_bar.pack_forget()
                self.login_button['state'] = 'normal'
                self.login_info_text["text"] = "卡号或密码错误!"
                self.login_info_text.configure(fg="red")
                self.campusCardPW.delete(0, len(campuscard_pw))
            else:
                self.prog_bar.stop()
                self.prog_bar.pack_forget()
                self.login_button['state'] = 'normal'
                self.login_info_text["text"] = "请重试或检查网络设置!"
                self.login_info_text.configure(fg="red")
        except Queue.Empty:
            self.after(100, lambda: self.process_queue(
                campuscard_id, campuscard_pw))


class LoginVerify(threading.Thread):

    def __init__(self, queue, campuscard_id, campuscard_pw):
        threading.Thread.__init__(self)
        self.queue = queue
        self.campuscard_id = campuscard_id
        self.campuscard_pw = campuscard_pw

    def run(self):
        login_util = LoginLogoutUtil()
        result = login_util.login(self.campuscard_id, self.campuscard_pw)
        self.queue.put(result)


class SysTrayTread(threading.Thread):

    def __init__(self, loginFrame):
        super(SysTrayTread, self).__init__()
        self.loginFrame = loginFrame
        self.logoutFrame = loginFrame.parent.logoutFrame

    def run(self):
        def quit():  # 如果要把类作为参数,直接传名字就好了,不用加模块名
            # if tkMessageBox.askokcancel("退出程序", "退出?",default="cancel"):       不能显示对话框且自动返回false，所以去掉
            # 发出注销请求
            try:
                self.logoutFrame.quit_systray()
            except Exception, e:
                logger.error('connection error', exc_info=True)

        def show(SysTrayIcon):
            SysTrayIcon.show_window()

        def logout(SysTrayIcon):
            SysTrayIcon.logout()

        self.loginFrame.icon_count = self.loginFrame.icon_count + 1
        self.loginFrame.window_class = 'ProfCOMIcon' + \
            str(self.loginFrame.icon_count)
        icon = 'resources\\favicon.ico'
        hover_text = u'Profcom'  # 鼠标移动到tray上,显示的文字
        menu_options = ((u'打开主面板', None, show),  # systray里面会自动加上退出的选项
                        (u'注销', None, logout),
                        )
        # 传入on_quit函数,如果点了菜单中默认的退出选项,则先执行on_quit,再执行默认的托盘退出过程
        systray.SysTrayIcon(icon, self.logoutFrame, hover_text, menu_options, on_quit=quit,
                            default_menu_index=0, window_class_name=self.loginFrame.window_class)
