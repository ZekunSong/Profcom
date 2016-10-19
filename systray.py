# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Module     : SysTrayIcon.py
# Synopsis   : Windows System tray icon.
# Programmer : Simon Brunning - simon@brunningonline.net
# Date       : 11 April 2005
# Notes      : Based on (i.e. ripped off from) Mark Hammond's
#              win32gui_taskbar.py and win32gui_menu.py demos from PyWin32
# 参考：   http://blog.csdn.net/laike9m/article/details/8763060
#         http://www.brunningonline.net/simon/blog/archives/SysTrayIcon.py.html
# 托盘
import os
import win32api
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui


class SysTrayIcon(object):
    '''TODO'''
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    FIRST_ID = 1023

    def __init__(self,
                 icon,
                 gui,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,):

        self.icon = icon
        self.gui = gui  # 增加了这个参数,是产生托盘的GUI类的实例,参见后面代码
        self.hover_text = hover_text
        self.on_quit = on_quit

        # 生成菜单
        # 改了选项的文字，把'quit'替换成自己想用的代表'退出'的文字
        menu_options = menu_options + ((u'退出', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,  # 注册窗体消息，传递给相同名字的窗体
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify, }
        # Register the Window class.
        window_class = win32gui.WNDCLASS()  # 生成窗口结构对象
        self.hinst = window_class.hInstance = win32gui.GetModuleHandle(
            None)  # 实例化
        window_class.lpszClassName = self.window_class_name  # 窗口类名
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW         # 窗口类型
        window_class.hCursor = win32gui.LoadCursor(
            0, win32con.IDC_ARROW)  # 窗口鼠标光标
        window_class.hbrBackground = win32con.COLOR_WINDOW  # 窗口背景色
        # could also specify a wndproc.   #定义窗口处理函数
        window_class.lpfnWndProc = message_map
        self.classAtom = win32gui.RegisterClass(window_class)  # 注册窗口类
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom,  # 生成窗口   类名
                                          self.window_class_name,  # 窗口title
                                          style,  # 类型
                                          0,  # x
                                          0,  # y
                                          win32con.CW_USEDEFAULT,  # 宽度
                                          win32con.CW_USEDEFAULT,  # 高度
                                          0,  # 父窗口
                                          0,  # 菜单
                                          self.hinst,  # 句柄实例
                                          None)  # 必须为None，未知项
        win32gui.UpdateWindow(self.hwnd)  # 更新窗口
        self.notify_id = None
        self.refresh_icon()

        win32gui.PumpMessages()  # 消息循环直到窗口退出

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add(
                    (self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                print 'Unknown item', option_text, option_icon, option_action
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        # Try and find a custom icon
        self.hinst = win32gui.GetModuleHandle(None)  # 获取句柄
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(self.hinst,  # 载入图像  #句柄
                                       self.icon,  # icon
                                       win32con.IMAGE_ICON,  # 类型
                                       0,  # cxDesired 参数，控制像素
                                       0,  # cyDesired
                                       icon_flags)  # 载入图像大小
        else:
            # print "Can't find icon file - using default."
            # 没有找到图标，使用默认图标
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY  # 修改状态去的图标
        else:
            message = win32gui.NIM_ADD  # 添加图标到状态区
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)  # 添加、移除或改变任务栏图标

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd, msg, wparam, lparam):
        #if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def destroy_window(self):
        win32gui.DestroyWindow(self.hwnd)  # 销毁窗口
        win32gui.UnregisterClass(self.classAtom, self.hinst)  # 注销

    def show_window(self):
        if self.gui.state() != 'normal':
            self.gui.update()
            self.gui.deiconify()

    def logout(self):
        self.show_window()
        # 注销登录，引用LogoutFrame的方法
        self.gui.logout_btn_click()

    def notify(self, hwnd, msg, wparam, lparam):
        '''
        这个函数定义了在托盘图标上双击/左击/右击时会发生的事情,双击时想恢复主窗口,修改双击时的默认操作
        '''
        if lparam == win32con.WM_LBUTTONDBLCLK:
            #self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
            self.show_window()  # 双击显示主面板
        elif lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        return True

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        #win32gui.SetMenuDefaultItem(menu, 1000, 0)

        pos = win32gui.GetCursorPos()
        # See
        # http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(
            0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x,
                            ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]
        if menu_action == self.QUIT:  # 当点击'退出'选项时就执行下面的代码
            win32gui.DestroyWindow(self.hwnd)
            self.on_quit()  # on_quit函数是外面传进来的,参见后面的代码
        else:
            menu_action(self)


def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, basestring)
