from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkcalendar as tkcalendar
from PIL import Image, ImageTk, ImageFont, ImageDraw
# import urllib.request
# import ssl
# import threading
# import sys
# import wmi
# import re
import time
import datetime
import os
import math
from Database import MySQL
from Database import Filezilla

MIN_WIDTH = 853
MIN_HEIGHT = 480
# [bg, fg, selector, actBg, actFg, bg2, fg2, selector2, actBg2, actFg2, fontColor2]
CP = [['#ECEFF1', '#171010', '#EEEEEE', "#D89216", None,
       '#90A4AE', '#DA0037', '#EEEEEE', '#CFD8DC', 'black',
       '#6E85B2', 'black', None, '#B0BEC5', 'black'],
      ['#2B2B2B', '#EEEEEE', '#5C527F', "#423F3E", None,
       '#261C2C', '#FFD369', '#5C527F', '#5C527F', '#EEEEEE',
       '#6E85B2', 'black', None, '#5C527F', 'black']]

"""
Old
    ['#E1D89F', '#171010', '#EEEEEE', "#D89216", None,
       '#EEB76B', '#DA0037', '#EEEEEE', '#E1D89F', 'black',
       '#6E85B2', 'black', None, '#5C527F', 'black']
"""

BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
server_setting = ["localhost", None, None, None, 'pnradmin', 'pnradmin']
db = None
fl = None
TEMP_FOLDER = 'temp'
DRIVER_FOLDER = 'driver'
PLT_NUM_FOLDER = 'plate_number'
PRIVILEGE = ''
CURR_USER = ''

"""
    Search Tag: Database Connection
"""


class SentsGui(Tk):
    class LoginCanvas(Canvas):
        class Setting(Toplevel):
            def __init__(self, root):
                super().__init__(root)
                filename = 'logo_light_mode.png'
                try:
                    filename = os.path.join(BASE_PATH, filename)
                except Exception as e:
                    print('Error:', e)
                self.icon = PhotoImage(file=filename)
                self.iconphoto(False, self.icon)

                title = "Server Setting "
                width = 514  # round(self.root.winfo_width() / 2)
                height = 440  # round(self.root.winfo_height() / 1.2) # 530
                # print(width, height)
                x = round(root.winfo_width() / 2 - width / 2) + root.winfo_x()
                y = round(root.winfo_height() / 2 - height / 2) + root.winfo_y()
                gap = 50
                entry_length = 20

                self.title(title)
                self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
                # self.attributes('-topmost', True)
                self.grab_set()
                # self.grab_release()  # After Finish Setting
                self.resizable(False, False)

                self.main_canvas = Canvas(self, highlightthickness=0, bg=CP[root.theme][5], width=width, height=height)
                self.main_canvas.place(x=0, y=0)
                self.main_canvas.update()

                self.server_frame = Frame(self.main_canvas, bg=CP[root.theme][5])
                font_setting = "Calibri " + str(18) + " bold"  # round(root.font_size * 1)
                self.server_label = Label(self.main_canvas, font=font_setting, text="Server Setting",
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.server_label.place(x=0, y=0)
                self.server_label.update()

                font_setting = "Calibri " + str(12)  # round(root.font_size * 0.95)
                self.host_label = Label(self.server_frame, font=font_setting, text="IP Address\t: ",
                                        bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.user_sql_label = Label(self.server_frame, font=font_setting, text="User SQL\t\t: ",
                                            bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.pass_sql_label = Label(self.server_frame, font=font_setting, text="Pass. SQL\t\t: ",
                                            bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.user_fl_label = Label(self.server_frame, font=font_setting, text="User FL\t\t: ",
                                           bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.pass_fl_label = Label(self.server_frame, font=font_setting, text="Pass. FL\t\t: ",
                                           bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.server_label.place(x=0, y=0)
                self.host_label.place(x=0, y=0)
                self.user_sql_label.place(x=0, y=0)
                self.pass_sql_label.place(x=0, y=0)
                self.user_fl_label.place(x=0, y=0)
                self.pass_fl_label.place(x=0, y=0)
                self.server_label.update()
                self.host_label.update()
                self.user_sql_label.update()
                self.pass_sql_label.update()
                self.user_fl_label.update()
                self.pass_fl_label.update()
                self.server_label.place(x=self.main_canvas.winfo_width() / 2 - self.server_label.winfo_width() / 2,
                                        y=self.main_canvas.winfo_width() / 12)
                self.server_label.update()
                y_coord = 0
                self.host_label.place(x=0, y=y_coord)
                y_coord = y_coord + gap
                self.user_sql_label.place(x=0, y=y_coord)
                y_coord = y_coord + gap
                self.pass_sql_label.place(x=0, y=y_coord)
                y_coord = y_coord + gap
                self.user_fl_label.place(x=0, y=y_coord)
                y_coord = y_coord + gap
                self.pass_fl_label.place(x=0, y=y_coord)
                self.host_label.update()
                self.user_sql_label.update()
                self.pass_sql_label.update()
                self.user_fl_label.update()
                self.pass_fl_label.update()

                self.host_str = StringVar()
                self.user_sql_str = StringVar()
                self.pass_sql_str = StringVar()
                self.user_fl_str = StringVar()
                self.pass_fl_str = StringVar()

                with open('setting.txt', 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.find("host=") == 0:
                            server_setting[0] = line.split('=')[1].replace("\n", "")
                            self.host_str.set(server_setting[0])
                            if server_setting[0] == "":
                                server_setting[0] = None
                        elif line.find("user_sql=") == 0:
                            server_setting[2] = line.split('=')[1].replace("\n", "")
                            self.user_sql_str.set(server_setting[2])
                            if server_setting[2] == "":
                                server_setting[2] = None
                        elif line.find("pass_sql=") == 0:
                            server_setting[3] = line.split('=')[1].replace("\n", "")
                            self.pass_sql_str.set(server_setting[3])
                            if server_setting[3] == "":
                                server_setting[3] = None
                        elif line.find("user_fl=") == 0:
                            server_setting[4] = line.split('=')[1].replace("\n", "")
                            self.user_fl_str.set(server_setting[4])
                            if server_setting[4] == "":
                                server_setting[4] = None
                        elif line.find("pass_fl=") == 0:
                            server_setting[5] = line.split('=')[1].replace("\n", "")
                            self.pass_fl_str.set(server_setting[5])
                            if server_setting[5] == "":
                                server_setting[5] = None

                font_setting = "Calibri " + str(12)  # round(math.pow(root.font_size, 0.87))
                ttk.Style().configure('pad.TEntry', padding='2 1 2 1')
                self.host_entry = ttk.Entry(self.server_frame, width=entry_length, textvariable=self.host_str,
                                            font=font_setting, style='pad.TEntry')
                self.user_sql_entry = ttk.Entry(self.server_frame, width=entry_length, textvariable=self.user_sql_str,
                                                font=font_setting, style='pad.TEntry')
                self.pass_sql_entry = ttk.Entry(self.server_frame, width=entry_length, textvariable=self.pass_sql_str,
                                                font=font_setting, style='pad.TEntry')
                self.user_fl_entry = ttk.Entry(self.server_frame, width=entry_length, textvariable=self.user_fl_str,
                                               font=font_setting, style='pad.TEntry')
                self.pass_fl_entry = ttk.Entry(self.server_frame, width=entry_length, textvariable=self.pass_fl_str,
                                               font=font_setting, style='pad.TEntry')
                self.host_entry.place(x=0, y=0)
                self.user_sql_entry.place(x=0, y=0)
                self.pass_sql_entry.place(x=0, y=0)
                self.user_fl_entry.place(x=0, y=0)
                self.pass_fl_entry.place(x=0, y=0)
                self.host_entry.update()
                self.user_sql_entry.update()
                self.pass_sql_entry.update()
                self.user_fl_entry.update()
                self.pass_fl_entry.update()
                y_coord = 0
                self.host_entry.place(x=self.host_label.winfo_width(),
                                      y=y_coord +
                                        (self.host_label.winfo_height() / 2 - self.host_entry.winfo_height() / 2))
                y_coord = y_coord + gap
                self.user_sql_entry.place(x=self.user_sql_label.winfo_width(),
                                          y=y_coord +
                                            (
                                                    self.user_sql_label.winfo_height() / 2 - self.user_sql_entry.winfo_height() / 2))
                y_coord = y_coord + gap
                self.pass_sql_entry.place(x=self.pass_sql_label.winfo_width(),
                                          y=y_coord +
                                            (
                                                    self.pass_sql_label.winfo_height() / 2 - self.pass_sql_entry.winfo_height() / 2))
                y_coord = y_coord + gap
                self.user_fl_entry.place(x=self.user_fl_label.winfo_width(),
                                         y=y_coord +
                                           (
                                                   self.user_fl_label.winfo_height() / 2 - self.user_fl_entry.winfo_height() / 2))
                y_coord = y_coord + gap
                self.pass_fl_entry.place(x=self.pass_fl_label.winfo_width(),
                                         y=y_coord +
                                           (
                                                   self.pass_fl_label.winfo_height() / 2 - self.pass_fl_entry.winfo_height() / 2))
                self.host_entry.update()
                self.user_sql_entry.update()
                self.pass_sql_entry.update()
                self.user_fl_entry.update()
                self.pass_fl_entry.update()

                font_setting = "Calibri " + str(10)  # round(root.font_size * 0.65)
                self.host_def_btn = Button(self.server_frame, font=font_setting, text="Default", padx=2,
                                           bg=CP[root.theme][10], fg=CP[root.theme][11],
                                           activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                           command=lambda a=1, b=root: self.btn_event(a, b))
                self.user_sql_def_btn = Button(self.server_frame, font=font_setting, text="Default", padx=2,
                                               bg=CP[root.theme][10], fg=CP[root.theme][11],
                                               activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                               command=lambda a=3, b=root: self.btn_event(a, b))
                self.pass_sql_def_btn = Button(self.server_frame, font=font_setting, text="Default", padx=2,
                                               bg=CP[root.theme][10], fg=CP[root.theme][11],
                                               activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                               command=lambda a=4, b=root: self.btn_event(a, b))
                self.user_fl_def_btn = Button(self.server_frame, font=font_setting, text="Default", padx=2,
                                              bg=CP[root.theme][10], fg=CP[root.theme][11],
                                              activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                              command=lambda a=5, b=root: self.btn_event(a, b))
                self.pass_fl_def_btn = Button(self.server_frame, font=font_setting, text="Default", padx=2,
                                              bg=CP[root.theme][10], fg=CP[root.theme][11],
                                              activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                              command=lambda a=6, b=root: self.btn_event(a, b))
                self.host_def_btn.place(x=0, y=0)
                self.user_sql_def_btn.place(x=0, y=0)
                self.pass_sql_def_btn.place(x=0, y=0)
                self.user_fl_def_btn.place(x=0, y=0)
                self.pass_fl_def_btn.place(x=0, y=0)
                self.host_def_btn.update()
                self.user_sql_def_btn.update()
                self.pass_sql_def_btn.update()
                self.user_fl_def_btn.update()
                self.pass_fl_def_btn.update()
                y_coord = 0
                self.host_def_btn.place(x=self.host_label.winfo_width() + self.host_entry.winfo_width() + 10,
                                        y=y_coord +
                                          (self.host_label.winfo_height() / 2 - self.host_def_btn.winfo_height() / 2))
                y_coord = y_coord + gap
                self.user_sql_def_btn.place(
                    x=self.user_sql_label.winfo_width() + self.user_sql_entry.winfo_width() + 10,
                    y=y_coord +
                      (
                              self.host_label.winfo_height() / 2 - self.user_sql_def_btn.winfo_height() / 2))
                y_coord = y_coord + gap
                self.pass_sql_def_btn.place(
                    x=self.pass_sql_label.winfo_width() + self.pass_sql_entry.winfo_width() + 10,
                    y=y_coord +
                      (
                              self.host_label.winfo_height() / 2 - self.pass_sql_def_btn.winfo_height() / 2))
                y_coord = y_coord + gap
                self.user_fl_def_btn.place(
                    x=self.user_fl_label.winfo_width() + self.user_fl_entry.winfo_width() + 10,
                    y=y_coord +
                      (
                              self.host_label.winfo_height() / 2 - self.user_fl_def_btn.winfo_height() / 2))
                y_coord = y_coord + gap
                self.pass_fl_def_btn.place(
                    x=self.pass_fl_label.winfo_width() + self.pass_fl_entry.winfo_width() + 10,
                    y=y_coord +
                      (
                              self.host_label.winfo_height() / 2 - self.pass_fl_def_btn.winfo_height() / 2))
                # y_coord = y_coord + gap * 1.1
                self.host_def_btn.update()
                self.user_sql_def_btn.update()
                self.pass_sql_def_btn.update()
                self.user_fl_def_btn.update()
                self.pass_fl_def_btn.update()

                font_setting = "Calibri " + str(10)  # round(root.font_size * 0.65)
                self.stats_lbl = Label(self.server_frame, font=font_setting, text="Failed to Connect",
                                       bg=CP[root.theme][5], fg=CP[root.theme][5])
                self.stats_lbl.place(x=width, y=height)
                self.stats_lbl.update()
                y_coord = y_coord + self.pass_sql_label.winfo_height() + 3
                self.stats_lbl.place(x=10, y=y_coord)
                self.stats_lbl.update()
                y_coord = y_coord + self.stats_lbl.winfo_height() + 10

                self.server_frame.configure(width=self.host_label.winfo_width() + self.host_entry.winfo_width() + 10 +
                                                  self.host_def_btn.winfo_width(),
                                            height=y_coord)
                self.server_frame.place(x=width, y=height)
                self.server_frame.update()

                self.ok_btn = Button(self.server_frame, font=font_setting, text="Ok", width=8,
                                     bg=CP[root.theme][10], fg=CP[root.theme][11],
                                     activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                     command=lambda a=7, b=root: self.btn_event(a, b))
                self.conn_btn = Button(self.server_frame, font=font_setting, text="Test", width=8,
                                       bg=CP[root.theme][10], fg=CP[root.theme][11],
                                       activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                       command=lambda a=8, b=root: self.btn_event(a, b))
                self.cancel_btn = Button(self.server_frame, font=font_setting, text="Cancel", width=8,
                                         bg=CP[root.theme][10], fg=CP[root.theme][11],
                                         activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                         command=lambda a=9, b=root: self.btn_event(a, b))
                self.ok_btn.place(x=width, y=height)
                self.conn_btn.place(x=width, y=height)
                self.cancel_btn.place(x=width, y=height)
                self.ok_btn.update()
                self.conn_btn.update()
                self.cancel_btn.update()
                self.ok_btn.place(x=self.server_frame.winfo_width() / 2 - self.ok_btn.winfo_width() - 15 -
                                    self.conn_btn.winfo_width() / 2,
                                  y=y_coord)
                self.conn_btn.place(x=self.server_frame.winfo_width() / 2 - self.conn_btn.winfo_width() / 2,
                                    y=y_coord)
                self.cancel_btn.place(x=self.server_frame.winfo_width() / 2 + 15 + self.conn_btn.winfo_width() / 2,
                                      y=y_coord)
                self.ok_btn.update()
                self.conn_btn.update()
                self.cancel_btn.update()

                self.server_frame.configure(width=self.server_frame.winfo_width() + 1,
                                            height=self.server_frame.winfo_height() + self.ok_btn.winfo_height())
                self.server_frame.update()
                self.server_frame.place(x=self.main_canvas.winfo_width() / 2 - self.server_frame.winfo_width() / 2,
                                        y=self.main_canvas.winfo_height() / 2 - self.server_frame.winfo_height() / 2.5)
                self.server_frame.update()

            def btn_event(self, type, root):
                # type = 2 is originally for port, got taken out
                if type == 1:
                    self.host_str.set("localhost")
                elif type == 3:
                    self.user_sql_str.set("")
                elif type == 4:
                    self.pass_sql_str.set("")
                elif type == 5:
                    self.user_fl_str.set("pnradmin")
                elif type == 6:
                    self.pass_fl_str.set("pnradmin")
                elif type == 7:
                    # Ok Stuff
                    server_setting[0] = self.host_str.get()
                    server_setting[2] = self.user_sql_str.get()
                    server_setting[3] = self.pass_sql_str.get()
                    server_setting[4] = self.user_fl_str.get()
                    server_setting[5] = self.pass_fl_str.get()

                    f = open('setting.txt', 'r')
                    lines = f.readlines()
                    f.close()

                    f = open('setting.txt', 'w')
                    for line in lines:
                        if line.find("host=") == 0:
                            line = "host=" + server_setting[0] + "\n"
                            f.write(line)
                        elif line.find("user_sql=") == 0:
                            line = "user_sql=" + server_setting[2] + "\n"
                            f.write(line)
                        elif line.find("pass_sql=") == 0:
                            line = "pass_sql=" + server_setting[3] + "\n"
                            f.write(line)
                        elif line.find("user_fl=") == 0:
                            line = "user_fl=" + server_setting[4] + "\n"
                            f.write(line)
                        elif line.find("pass_fl=") == 0:
                            line = "pass_fl=" + server_setting[5] + "\n"
                            f.write(line)
                        else:
                            f.write(line)
                    f.close()

                    for i in range(0, len(server_setting)):
                        if server_setting[i] == "":
                            server_setting[i] = None
                    # print(server_setting)

                    self.destroy()
                elif type == 8:
                    if db.update_connection(host=self.host_str.get(), user=self.user_sql_str.get(),
                                            password=self.pass_sql_str.get()) and \
                            fl.update_connection(host=self.host_str.get(), user=self.user_fl_str.get(),
                                                 password=self.pass_fl_str.get()):
                        self.stats_lbl.configure(text="Successfully Connect", fg=CP[root.theme][6])
                    else:
                        self.stats_lbl.configure(text="Failed to Connect", fg=CP[root.theme][6])
                    self.after(3000, lambda a=root: self.status_fade(a))
                elif type == 9:
                    self.destroy()

            def status_fade(self, root):
                self.stats_lbl.configure(fg=CP[root.theme][5])

        def __init__(self, root, theme, screen_width, screen_height, width, height, font_size,
                     canvas_index):
            super().__init__(width=screen_width, height=screen_height, bg=CP[theme][0], highlightthickness=0)
            self.canvas_index = canvas_index
            self.root = root
            self.place(x=width, y=height)
            self.server_setting = None

            filename = './logo_dark_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
            except Exception as e:
                print('Error:', e)
            self.ori_logo = Image.open(filename)
            logo_height = round(25 / 100 * height)
            logo_width = round(logo_height * self.ori_logo.width / self.ori_logo.height)

            self.resized_logo = self.ori_logo.resize((logo_width, logo_height),
                                                     Image.ANTIALIAS)
            self.logo_tk = ImageTk.PhotoImage(self.resized_logo)
            self.login_logo_label = Label(self, image=self.logo_tk, border=0, bg=CP[theme][0])
            self.login_logo_label.place(x=width, y=height)
            self.login_logo_label.update()
            self.login_logo_label.place(x=width / 2 - self.login_logo_label.winfo_width() / 2,
                                        y=3 / 11 * height - self.login_logo_label.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 1.45)) + " bold"
            self.login_title_text = Label(self, text="UTeM Security Entrance System", bg=CP[theme][0],
                                          fg=CP[theme][1],
                                          font=font_setting)
            self.login_title_text.place(x=width, y=height)
            self.login_title_text.update()
            self.login_title_text.place(x=width / 2 - self.login_title_text.winfo_width() / 2,
                                        y=height / 2 - self.login_title_text.winfo_height() / 2)

            self.login_user_frame = Frame(self, bg=CP[theme][0])
            self.login_user_frame.place(x=self.winfo_width(), y=self.winfo_height())

            y_coord = 0
            font_setting = "Calibri " + str(round(font_size * 1))
            self.login_user_text = Label(self.login_user_frame, text="Staff ID\t : ", bg=CP[theme][0], fg=CP[theme][1],
                                         font=font_setting)
            self.login_user_text.place(x=0, y=0)
            self.login_user_text.update()

            self.login_pass_text = Label(self.login_user_frame, text="Password\t : ", bg=CP[theme][0], fg=CP[theme][1],
                                         font=font_setting)
            self.login_pass_text.place(x=0, y=self.login_user_text.winfo_height() * 1.5)
            self.login_pass_text.update()

            y_coord = round(0.05 * self.login_user_text.winfo_height())
            font_setting = "Calibri " + str(round(font_size * 0.85))
            self.login_user_strvar = StringVar()
            self.login_user_field = ttk.Entry(self.login_user_frame, width=20, textvariable=self.login_user_strvar,
                                              font=font_setting)
            self.login_user_field.place(x=self.login_user_text.winfo_width(), y=y_coord)

            self.login_pass_strvar = StringVar()
            y_coord += self.login_user_text.winfo_height() * 1.5
            self.login_pass_field = ttk.Entry(self.login_user_frame, width=20, textvariable=self.login_pass_strvar,
                                              font=font_setting, show='*')
            self.login_pass_field.place(x=self.login_pass_text.winfo_width(), y=y_coord)
            self.login_user_field.update()
            self.login_pass_field.update()

            y_coord += self.login_pass_text.winfo_height()
            font_setting = "Calibri " + str(round(font_size * 0.7))
            self.message_lbl = Label(self.login_user_frame, text="", font=font_setting,
                                     bg=CP[theme][0], fg=CP[theme][6])
            self.message_lbl.place(x=self.login_pass_text.winfo_width(), y=y_coord)
            self.message_lbl.update()

            y_coord += round(self.message_lbl.winfo_height() * 1.5)
            font_setting = "Calibri " + str(round(font_size * 0.75)) + " bold"
            self.login_btn = Button(self.login_user_frame, bg=CP[theme][5], fg=CP[theme][1],
                                    activebackground=CP[theme][8], activeforeground=CP[theme][9], border=1,
                                    text="Login", font=font_setting, padx=10, pady=1,
                                    command=lambda a=1: self.button_event(a))
            self.login_btn.place(x=self.login_user_frame.winfo_width(), y=y_coord)
            self.login_btn.update()
            self.login_user_frame.config(width=self.login_user_text.winfo_width() + self.login_user_field.winfo_width(),
                                         height=self.login_user_text.winfo_height())
            self.login_user_frame.update()
            self.login_btn.place(x=round(self.login_user_frame.winfo_width() / 2 - self.login_btn.winfo_width() / 2),
                                 y=y_coord)

            self.login_user_frame.config(height=y_coord + self.login_btn.winfo_height())
            self.login_user_frame.update()
            self.login_user_frame.place(x=width / 2 - self.login_user_frame.winfo_width() / 2,
                                        y=height * 3 / 4 - self.login_user_frame.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 0.7)) + " bold"
            self.setting_btn = Button(self, bg=CP[theme][5], fg=CP[theme][1],
                                      activebackground=CP[theme][8], activeforeground=CP[theme][9], border=1,
                                      text="Setting", font=font_setting, padx=5, pady=3,
                                      command=lambda a=2: self.button_event(a))
            self.setting_btn.place(x=self.login_user_frame.winfo_width(), y=self.login_user_frame.winfo_height())
            self.setting_btn.update()
            self.setting_btn.place(x=root.winfo_width() - (root.margin_width / 2 + self.setting_btn.winfo_width() / 2),
                                   y=root.margin_height / 2 - self.setting_btn.winfo_height() / 2)

            self.update()
            if self.canvas_index != 0:
                self.place_forget()
            else:
                self.place(x=0, y=0)

        def button_event(self, type):
            global PRIVILEGE, CURR_USER
            if type == 1:
                """
                # Input
                    self.login_user_strvar.get()
                    self.login_pass_strvar.get()
                """

                msg = ''
                if self.login_user_strvar.get() and self.login_pass_strvar.get():
                    # Database Connection
                    match_account = False

                    match_account, msg = db.login_user(self.login_user_strvar.get(), self.login_pass_strvar.get())

                    """
                    Output
                        match_account
                        msg
                    """

                    # Login Frame
                    if match_account:
                        self.canvas_index = 1
                        self.root.set_canvas_index(self.canvas_index)
                        self.place_forget()
                        self.root.set_canvas()

                        if self.login_user_strvar.get().lower() == 'root':
                            PRIVILEGE = 'root'
                        else:
                            PRIVILEGE = 'admin'
                        print("Login as", PRIVILEGE)
                        CURR_USER = self.login_user_strvar.get()
                    else:
                        self.message_lbl.configure(text=msg)
                        self.message_lbl.after(3000, lambda: message_fade())
                        print(msg)

                    # Temporary Login
                    # self.canvas_index = 1
                    # self.root.set_canvas_index(self.canvas_index)
                    # self.place_forget()
                    # self.root.set_canvas()
                    self.login_user_strvar.set("")
                    self.login_pass_strvar.set("")
                    self.login_user_field.focus_set()
                else:
                    msg = "All Field Must be Filled"
                    self.message_lbl.configure(text=msg)
                    self.message_lbl.after(3000, lambda: message_fade())
                    print(msg)
            elif type == 2:
                self.setting = self.Setting(self.root)

            def message_fade():
                self.message_lbl.configure(text='')

        def update_res(self, root):
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size

            self.place(x=0, y=0)
            # self.configure(width=width, height=height)
            logo_height = round(25 / 100 * height)
            logo_width = round(logo_height * self.ori_logo.width / self.ori_logo.height)
            self.resized_logo = self.ori_logo.resize((logo_width, logo_height),
                                                     Image.ANTIALIAS)
            self.logo_tk = ImageTk.PhotoImage(self.resized_logo)
            self.login_logo_label.configure(image=self.logo_tk)
            self.login_logo_label.place(x=width, y=height)
            self.login_logo_label.update()
            self.login_logo_label.place(x=width / 2 - self.login_logo_label.winfo_width() / 2,
                                        y=3 / 11 * height - self.login_logo_label.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 1.45)) + " bold"
            self.login_title_text.configure(font=font_setting)
            self.login_title_text.update()
            self.login_title_text.place(x=width / 2 - self.login_title_text.winfo_width() / 2,
                                        y=height / 2 - self.login_title_text.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 1))
            self.login_user_text.configure(font=font_setting)
            self.login_user_text.place(x=0, y=0)
            self.login_user_text.update()

            self.login_pass_text.configure(font=font_setting)
            self.login_pass_text.place(x=0, y=self.login_user_text.winfo_height() * 1.5)
            self.login_pass_text.update()

            y_coord = round(0.05 * self.login_user_text.winfo_height())
            font_setting = "Calibri " + str(round(font_size * 0.85))
            self.login_user_field.configure(font=font_setting)
            self.login_user_field.place(x=self.login_user_text.winfo_width(), y=y_coord)

            y_coord += self.login_user_text.winfo_height() * 1.5
            self.login_pass_field.configure(font=font_setting)
            self.login_pass_field.place(x=self.login_pass_text.winfo_width(), y=y_coord)
            self.login_user_field.update()
            self.login_pass_field.update()

            y_coord += self.login_pass_text.winfo_height()
            font_setting = "Calibri " + str(round(font_size * 0.7))
            self.message_lbl.configure(font=font_setting)
            self.message_lbl.place(x=self.login_pass_text.winfo_width(), y=y_coord)
            self.message_lbl.update()

            y_coord += round(self.message_lbl.winfo_height() * 1.5)
            font_setting = "Calibri " + str(round(font_size * 0.75)) + " bold"
            self.login_btn.configure(font=font_setting)
            self.login_btn.place(x=self.login_user_frame.winfo_width(),
                                 y=self.login_user_frame.winfo_height())
            self.login_btn.update()
            self.login_user_frame.config(width=self.login_user_text.winfo_width() + self.login_user_field.winfo_width(),
                                         height=self.login_user_text.winfo_height() * 2.5 +
                                                self.login_pass_text.winfo_height())
            self.login_user_frame.update()
            self.login_btn.place(x=round(self.login_user_frame.winfo_width() / 2 - self.login_btn.winfo_width() / 2),
                                 y=y_coord)

            self.login_user_frame.config(height=y_coord + self.login_btn.winfo_height())
            self.login_user_frame.update()
            self.login_user_frame.place(x=width / 2 - self.login_user_frame.winfo_width() / 2,
                                        y=height * 3 / 4 - self.login_user_frame.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 0.7)) + " bold"
            self.setting_btn.configure(font=font_setting)
            self.setting_btn.place(x=root.winfo_width() - (root.margin_width / 2 + self.setting_btn.winfo_width() / 2),
                                   y=root.margin_height / 2 - self.setting_btn.winfo_height() / 2)

            self.update()

        def change_theme(self, theme):
            filename = ''
            if theme == 1:
                filename = './logo_dark_mode.png'
                try:
                    filename = os.path.join(BASE_PATH, filename)
                except Exception as e:
                    print('Error:', e)
                self.ori_logo = Image.open(filename)
            else:
                filename = './logo_light_mode.png'
                try:
                    filename = os.path.join(BASE_PATH, filename)
                except Exception as e:
                    print('Error:', e)
                self.ori_logo = Image.open(filename)
            logo_height = round(25 / 100 * self.root.winfo_height())
            logo_width = round(logo_height * self.ori_logo.width / self.ori_logo.height)
            self.resized_logo = self.ori_logo.resize((logo_width, logo_height),
                                                     Image.ANTIALIAS)
            self.logo_tk = ImageTk.PhotoImage(self.resized_logo)

            self.configure(bg=CP[theme][0])
            self.login_logo_label.configure(image=self.logo_tk, bg=CP[theme][0])
            self.login_title_text.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.login_user_frame.configure(bg=CP[theme][0])
            self.login_user_text.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.login_pass_text.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.message_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.login_btn.configure(bg=CP[theme][5], fg=CP[theme][1],
                                     activebackground=CP[theme][8], activeforeground=CP[theme][9])
            self.setting_btn.configure(bg=CP[theme][5], fg=CP[theme][1],
                                       activebackground=CP[theme][8], activeforeground=CP[theme][9])
            self.update()

    class Notification(Toplevel):
        def __init__(self, root, title, desc, size=0.85):
            super().__init__(root)
            filename = 'logo_light_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
            except Exception as e:
                print('Error:', e)
            self.icon = PhotoImage(file=filename)
            self.iconphoto(False, self.icon)

            width = 320  # round(self.root.winfo_width() / 2)
            height = 180  # round(self.root.winfo_height() / 1.2) # 530
            # print(width, height)
            x = round(root.winfo_width() / 2 - width / 2) + root.winfo_x()
            y = round(root.winfo_height() / 2 - height / 2) + root.winfo_y()
            gap = 50
            entry_length = 20

            self.title(title)
            self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            # self.attributes('-topmost', True)
            self.grab_set()
            # self.grab_release()  # After Finish Setting
            self.resizable(False, False)

            self.main_canvas = Canvas(self, highlightthickness=0, bg=CP[root.theme][5], width=width, height=height)
            self.main_canvas.place(x=0, y=0)
            self.main_canvas.update()

            self.noti_frame = Frame(self.main_canvas, bg=CP[root.theme][5])
            font_setting = "Calibri " + str(round(18 * size))  # round(root.font_size * size)
            self.noti_label = Label(self.main_canvas, font=font_setting, text=desc,
                                    bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.noti_label.place(x=0, y=0)
            self.noti_label.update()
            self.noti_label.place(x=width / 2 - self.noti_label.winfo_width() / 2,
                                  y=height / 4)  # self.noti_label.winfo_height()/2

            font_setting = "Calibri " + str(10)  # round(root.font_size * 0.65)
            self.ok_btn = Button(self.main_canvas, font=font_setting, text="Ok", width=8,
                                 bg=CP[root.theme][10], fg=CP[root.theme][11],
                                 activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                 command=lambda a=1: self.btn_event(a))
            self.ok_btn.place(x=width, y=height)
            self.ok_btn.update()
            self.ok_btn.place(x=width / 2 - self.ok_btn.winfo_width() / 2,
                              y=3 * height / 4 - self.ok_btn.winfo_height())
            self.ok_btn.update()

        def btn_event(self, type):
            # type = 2 is originally for port, got taken out
            if type == 1:
                self.destroy()

    class MainCanvas(Canvas):
        def __init__(self, root, theme, screen_width, screen_height, width, height, main_layout, font_size,
                     margin_width, margin_height, canvas_index):
            super().__init__(width=screen_width, height=screen_height, bg=CP[theme][0], highlightthickness=0)
            self.canvas_index = canvas_index
            self.root = root

            # Need Comment out later
            self.place(x=width, y=height)

            self.layout_btn = Frame(self, bg=CP[theme][5])

            font_setting = "Calibri " + str(round(font_size * 0.73))
            self.view_driver_btn = Button(self.layout_btn, text="View Driver", font=font_setting, padx=10, pady=1,
                                          bg=CP[theme][5], fg=CP[theme][1],
                                          activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                          state=DISABLED, command=lambda a=1: self.button_event(a))
            self.reg_driver_btn = Button(self.layout_btn, text="Add Driver", font=font_setting, padx=10, pady=1,
                                         bg=CP[theme][5], fg=CP[theme][1],
                                         activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                         command=lambda a=2: self.button_event(a))
            self.view_admin_btn = Button(self.layout_btn, text="View Admin", font=font_setting, padx=10, pady=1,
                                         bg=CP[theme][5], fg=CP[theme][1],
                                         activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                         command=lambda a=3: self.button_event(a))
            self.reg_admin_btn = Button(self.layout_btn, text="Add Admin", font=font_setting, padx=10, pady=1,
                                        bg=CP[theme][5], fg=CP[theme][1],
                                        activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                        command=lambda a=4: self.button_event(a))
            self.prof_btn = Button(self.layout_btn, text="Profile", font=font_setting, padx=10, pady=1,
                                   bg=CP[theme][5], fg=CP[theme][1],
                                   activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                   command=lambda a=5: self.button_event(a))
            self.logout_btn = Button(self, text="Logout", font=font_setting, padx=10, pady=1,
                                     bg=CP[theme][5], fg=CP[theme][1],
                                     activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                     command=lambda a=0: self.button_event(a))

            self.layout_btn.place(x=width, y=height)
            self.view_driver_btn.place(x=0, y=0)
            self.reg_driver_btn.place(x=0, y=0)
            self.view_admin_btn.place(x=0, y=0)
            self.reg_admin_btn.place(x=0, y=0)
            self.logout_btn.place(x=0, y=0)
            self.prof_btn.place(x=0, y=0)
            """
            self.view_driver_btn.place(x=width, y=height)
            self.reg_driver_btn.place(x=width, y=height)
            self.view_admin_btn.place(x=width, y=height)
            self.reg_admin_btn.place(x=width, y=height)
            self.logout_btn.place(x=width, y=height)
            self.prof_btn.place(x=width, y=height)
            """

            self.layout_btn.update()
            self.view_driver_btn.update()
            self.reg_driver_btn.update()
            self.view_admin_btn.update()
            self.reg_admin_btn.update()
            self.logout_btn.update()
            self.prof_btn.update()

            self.layout_btn.configure(width=self.view_driver_btn.winfo_width() + self.reg_driver_btn.winfo_width() +
                                            self.view_admin_btn.winfo_width() + self.reg_admin_btn.winfo_width() +
                                            self.prof_btn.winfo_width(),
                                      height=self.view_driver_btn.winfo_height())
            self.view_driver_btn.place(x=0, y=0)
            temp = self.view_driver_btn.winfo_width()
            self.reg_driver_btn.place(x=temp, y=0)
            temp = temp + self.reg_driver_btn.winfo_width()
            self.view_admin_btn.place(x=temp, y=0)
            temp = temp + self.view_admin_btn.winfo_width()
            self.reg_admin_btn.place(x=temp, y=0)
            temp = temp + self.reg_admin_btn.winfo_width()
            self.prof_btn.place(x=temp, y=0)
            self.logout_btn.place(x=width - (margin_width / 2 + self.logout_btn.winfo_width() / 2),
                                  y=margin_height / 2 - self.logout_btn.winfo_height() / 2)
            self.layout_btn.place(x=width / 2 - self.layout_btn.winfo_width() / 2,
                                  y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            """
            self.view_driver_btn.place(x=width / 2 - self.reg_driver_btn.winfo_width() -
                                         self.view_driver_btn.winfo_width(),
                                       y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.reg_driver_btn.place(x=width / 2 - self.reg_driver_btn.winfo_width(),
                                      y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.reg_admin_btn.place(x=width / 2,
                                     y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.prof_btn.place(x=width / 2 + self.reg_admin_btn.winfo_width(),
                                y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.logout_btn.place(x=width - margin_width,
                                  y=margin_height / 2 - self.logout_btn.winfo_height() / 2)
            """

            self.view_driver = SentsGui.ViewDriver(root, self, theme, main_layout, font_size,
                                                   margin_width, margin_height, canvas_index)
            self.add_driver = SentsGui.AddDriver(root, self, theme, main_layout, font_size,
                                                 margin_width, margin_height, canvas_index)
            self.view_admin = SentsGui.ViewAdmin(root, self, theme, main_layout, font_size,
                                                 margin_width, margin_height, canvas_index)
            self.add_admin = SentsGui.AddAdmin(root, self, theme, main_layout, font_size,
                                               margin_width, margin_height, canvas_index)
            self.prof_admin = SentsGui.ProfileAdmin(root, self, theme, main_layout, font_size,
                                                    margin_width, margin_height, canvas_index)

            self.update()
            if self.canvas_index != 1:
                self.place_forget()
            else:
                self.place(x=0, y=0)

        def button_event(self, canvas_index):
            # ViewDriver
            self.canvas_index = canvas_index
            self.root.set_canvas_index(self.canvas_index)
            self.place_forget()
            self.root.set_canvas()

            if canvas_index == 0:
                self.view_driver.search_str.set("")
                self.view_driver.driver_list.clear()
                self.view_admin.admin_list.clear()
                self.view_admin.search_str.set("")
                self.view_admin.num_pg_label.place_forget()
                self.view_admin.prev_label.place_forget()
                self.view_admin.next_label.place_forget()
                self.view_driver.num_pg_label.place_forget()
                self.view_driver.prev_label.place_forget()
                self.view_driver.next_label.place_forget()
                # self.add_driver.clear(main_layout, font_size)
                # self.add_admin.clear(main_layout)
                # self.prof_admin.clear()

                # self.view_driver_btn.configure(state=DISABLED)
                # self.reg_driver_btn.configure(state=NORMAL)
                # self.view_admin_btn.configure(state=NORMAL)
                # self.reg_admin_btn.configure(state=NORMAL)
                # self.prof_btn.configure(state=NORMAL)
                # self.view_driver.place(x=margin_width, y=margin_height)
                # self.add_driver.place_forget()
                # self.view_admin.place_forget()
                # self.view_admin.search_frame.place_forget()
                # self.add_admin.place_forget()
                # self.prof_admin.place_forget()
                # self.view_driver.update_res(root)

        def update_res(self, root):
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size
            margin_width = root.margin_width
            margin_height = root.margin_height
            main_layout = root.main_layout
            canvas_index = root.canvas_index

            self.place(x=0, y=0)
            self.canvas_index = canvas_index
            font_setting = "Calibri " + str(round(font_size * 0.73))
            self.view_driver_btn.configure(font=font_setting)
            self.reg_driver_btn.configure(font=font_setting)
            self.view_admin_btn.configure(font=font_setting)
            self.reg_admin_btn.configure(font=font_setting)
            self.prof_btn.configure(font=font_setting)
            self.logout_btn.configure(font=font_setting)

            if self.canvas_index == 0:
                self.view_driver.search_str.set("")
                self.view_driver.driver_list.clear()
                self.view_admin.admin_list.clear()
                self.view_admin.search_str.set("")
                self.view_admin.num_pg_label.place_forget()
                self.view_admin.prev_label.place_forget()
                self.view_admin.next_label.place_forget()
                self.view_driver.num_pg_label.place_forget()
                self.view_driver.prev_label.place_forget()
                self.view_driver.next_label.place_forget()
                self.add_driver.clear(main_layout, font_size)
                self.add_admin.clear(main_layout)
                self.prof_admin.clear()

                self.view_driver_btn.configure(state=DISABLED)
                self.reg_driver_btn.configure(state=NORMAL)
                self.view_admin_btn.configure(state=NORMAL)
                self.reg_admin_btn.configure(state=NORMAL)
                self.prof_btn.configure(state=NORMAL)
                self.view_driver.place(x=margin_width, y=margin_height)
                self.add_driver.place_forget()
                self.view_admin.place_forget()
                self.view_admin.search_frame.place_forget()
                self.add_admin.place_forget()
                self.prof_admin.place_forget()
                self.view_driver.update_res(root)
            elif self.canvas_index == 1:
                self.view_admin.admin_list.clear()
                self.view_admin.search_str.set("")
                self.view_admin.num_pg_label.place_forget()
                self.view_admin.prev_label.place_forget()
                self.view_admin.next_label.place_forget()

                self.view_driver_btn.configure(state=DISABLED)
                self.reg_driver_btn.configure(state=NORMAL)
                self.view_admin_btn.configure(state=NORMAL)
                self.reg_admin_btn.configure(state=NORMAL)
                self.prof_btn.configure(state=NORMAL)
                self.view_driver.place(x=margin_width, y=margin_height)
                self.add_driver.place_forget()
                self.view_admin.place_forget()
                self.view_admin.search_frame.place_forget()
                self.add_admin.place_forget()
                self.prof_admin.place_forget()
                self.view_driver.update_res(root)
            elif self.canvas_index == 2:
                self.view_driver.search_str.set("")
                self.view_driver.driver_list.clear()
                self.view_admin.admin_list.clear()
                self.view_admin.search_str.set("")
                self.view_driver.num_pg_label.place_forget()
                self.view_driver.prev_label.place_forget()
                self.view_driver.next_label.place_forget()
                self.view_admin.num_pg_label.place_forget()
                self.view_admin.prev_label.place_forget()
                self.view_admin.next_label.place_forget()
                self.add_driver.clear(main_layout, font_size)

                self.view_driver_btn.configure(state=NORMAL)
                self.reg_driver_btn.configure(state=DISABLED)
                self.view_admin_btn.configure(state=NORMAL)
                self.reg_admin_btn.configure(state=NORMAL)
                self.prof_btn.configure(state=NORMAL)
                self.view_driver.place_forget()
                self.view_driver.search_frame.place_forget()
                self.add_driver.place(x=margin_width, y=margin_height)
                self.view_admin.place_forget()
                self.view_admin.search_frame.place_forget()
                self.add_admin.place_forget()
                self.prof_admin.place_forget()
                self.add_driver.update_res(root)
            elif self.canvas_index == 3:
                self.view_driver.search_str.set("")
                self.view_driver.driver_list.clear()
                self.view_driver.num_pg_label.place_forget()
                self.view_driver.prev_label.place_forget()
                self.view_driver.next_label.place_forget()

                self.view_driver_btn.configure(state=NORMAL)
                self.reg_driver_btn.configure(state=NORMAL)
                self.view_admin_btn.configure(state=DISABLED)
                self.reg_admin_btn.configure(state=NORMAL)
                self.prof_btn.configure(state=NORMAL)
                self.view_driver.place_forget()
                self.view_driver.search_frame.place_forget()
                self.add_driver.place_forget()
                self.view_admin.place(x=margin_width, y=margin_height)
                self.add_admin.place_forget()
                self.prof_admin.place_forget()
                self.view_admin.update_res(root)
            elif self.canvas_index == 4:
                self.view_driver.search_str.set("")
                self.view_driver.driver_list.clear()
                self.view_admin.admin_list.clear()
                self.view_admin.search_str.set("")
                self.view_driver.num_pg_label.place_forget()
                self.view_driver.prev_label.place_forget()
                self.view_driver.next_label.place_forget()
                self.view_admin.num_pg_label.place_forget()
                self.view_admin.prev_label.place_forget()
                self.view_admin.next_label.place_forget()
                self.add_admin.clear(main_layout)

                self.view_driver_btn.configure(state=NORMAL)
                self.reg_driver_btn.configure(state=NORMAL)
                self.view_admin_btn.configure(state=NORMAL)
                self.reg_admin_btn.configure(state=DISABLED)
                self.prof_btn.configure(state=NORMAL)
                self.view_driver.place_forget()
                self.view_driver.search_frame.place_forget()
                self.add_driver.place_forget()
                self.view_admin.place_forget()
                self.view_admin.search_frame.place_forget()
                self.add_admin.place(x=margin_width, y=margin_height)
                self.prof_admin.place_forget()
                self.add_admin.update_res(root)
            elif self.canvas_index == 5:
                self.view_driver.search_str.set("")
                self.view_driver.driver_list.clear()
                self.view_admin.admin_list.clear()
                self.view_admin.search_str.set("")
                self.view_driver.num_pg_label.place_forget()
                self.view_driver.prev_label.place_forget()
                self.view_driver.next_label.place_forget()
                self.view_admin.num_pg_label.place_forget()
                self.view_admin.prev_label.place_forget()
                self.view_admin.next_label.place_forget()
                self.prof_admin.clear()

                self.view_driver_btn.configure(state=NORMAL)
                self.reg_driver_btn.configure(state=NORMAL)
                self.view_admin_btn.configure(state=NORMAL)
                self.reg_admin_btn.configure(state=NORMAL)
                self.prof_btn.configure(state=DISABLED)
                self.view_driver.place_forget()
                self.view_driver.search_frame.place_forget()
                self.add_driver.place_forget()
                self.view_admin.place_forget()
                self.view_admin.search_frame.place_forget()
                self.add_admin.place_forget()
                self.prof_admin.place(x=margin_width, y=margin_height)
                self.prof_admin.update_res(root)

            self.view_driver_btn.update()
            self.reg_driver_btn.update()
            self.view_admin_btn.update()
            self.reg_admin_btn.update()
            self.prof_btn.update()
            self.logout_btn.update()

            self.layout_btn.configure(width=self.view_driver_btn.winfo_width() + self.reg_driver_btn.winfo_width() +
                                            self.view_admin_btn.winfo_width() + self.reg_admin_btn.winfo_width() +
                                            self.prof_btn.winfo_width(),
                                      height=self.view_driver_btn.winfo_height())
            self.layout_btn.update()

            self.view_driver_btn.place(x=0, y=0)
            temp = self.view_driver_btn.winfo_width()
            self.reg_driver_btn.place(x=temp, y=0)
            temp = temp + self.reg_driver_btn.winfo_width()
            self.view_admin_btn.place(x=temp, y=0)
            temp = temp + self.view_admin_btn.winfo_width()
            self.reg_admin_btn.place(x=temp, y=0)
            temp = temp + self.reg_admin_btn.winfo_width()
            self.prof_btn.place(x=temp, y=0)
            self.logout_btn.place(x=width - (margin_width / 2 + self.logout_btn.winfo_width() / 2),
                                  y=margin_height / 2 - self.logout_btn.winfo_height() / 2)
            self.layout_btn.place(x=width / 2 - self.layout_btn.winfo_width() / 2,
                                  y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            """
            self.view_driver_btn.place(x=width / 2 - self.reg_driver_btn.winfo_width() -
                                         self.view_driver_btn.winfo_width(),
                                       y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.reg_driver_btn.place(x=width / 2 - self.reg_driver_btn.winfo_width(),
                                      y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.reg_admin_btn.place(x=width / 2,
                                     y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.prof_btn.place(x=width / 2 + self.reg_admin_btn.winfo_width(),
                                y=margin_height / 2 - self.view_driver_btn.winfo_height() / 2)
            self.logout_btn.place(x=width - margin_width,
                                  y=margin_height / 2 - self.logout_btn.winfo_height() / 2)
            """

        # Change Theme for MainCanvas
        def change_theme(self, theme):
            self.configure(bg=CP[theme][0])
            self.view_driver_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                           activeforeground=CP[theme][9])
            self.reg_driver_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                          activeforeground=CP[theme][9])
            self.view_admin_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                          activeforeground=CP[theme][9])
            self.reg_admin_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                         activeforeground=CP[theme][9])
            self.prof_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                    activeforeground=CP[theme][9])
            self.logout_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                      activeforeground=CP[theme][9])

            self.view_driver.change_theme(theme)
            self.add_driver.change_theme(theme)
            self.view_admin.change_theme(theme)
            self.add_admin.change_theme(theme)
            self.prof_admin.change_theme(theme)

    class ViewDriver(Frame):
        def __init__(self, root, canvas, theme, main_layout, font_size, margin_width, margin_height, canvas_index):
            self.mar_search = 0.92
            self.root = root
            self.borderwidth = 1
            self.prof_per_frame = 3
            super().__init__(master=canvas, width=main_layout[0], height=round(self.mar_search * main_layout[1]),
                             bg=CP[theme][0], highlightthickness=0)
            self.place(x=margin_width, y=margin_height + round(0.05 * main_layout[1]))

            """
            self.scroll_view = Scrollbar(self, bg=CP[theme][1], orient="vertical")
            self.scroll_view.pack(side=RIGHT, fill=Y)
            # self.scroll_view.place(x=0, y=0)
            """

            self.view_canvas = Canvas(self, width=main_layout[0], height=round(self.mar_search * main_layout[1]),
                                      bg=CP[theme][1], highlightthickness=0)
            self.view_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            # self.view_canvas.configure(yscrollcommand=self.scroll_view.set)
            # self.scroll_view.configure(command=self.view_canvas.yview)

            self.driver_list = []
            self.sub_frame = []
            self.page_index = 0
            self.canvas_item = []
            self.frame_item = []

            font_setting = "Calibri " + str(round(math.pow(font_size, 1)))
            self.num_pg_label = Label(root, text="1 / 1", font=font_setting, bg=CP[theme][0], fg=CP[theme][1])
            font_setting = "Calibri " + str(round(math.pow(font_size, 1.1))) + " bold"
            self.prev_label = Label(root, text="<", font=font_setting, bg=CP[theme][0], fg=CP[theme][1], padx=10)
            self.next_label = Label(root, text=">", font=font_setting, bg=CP[theme][0], fg=CP[theme][1], padx=10)
            self.num_pg_label.place(x=root.winfo_width(), y=root.winfo_height())
            self.prev_label.place(x=root.winfo_width(), y=root.winfo_height())
            self.next_label.place(x=root.winfo_width(), y=root.winfo_height())
            self.prev_label.bind("<ButtonPress-1>", func=lambda event, a=1, b=theme: self.on_press(event, a, b))
            self.prev_label.bind("<ButtonRelease-1>", func=lambda event, a=1, b=root: self.on_release(event, a, b))
            self.next_label.bind("<ButtonPress-1>", func=lambda event, a=2, b=theme: self.on_press(event, a, b))
            self.next_label.bind("<ButtonRelease-1>", func=lambda event, a=2, b=root: self.on_release(event, a, b))
            self.num_pg_label.update()
            self.prev_label.update()
            self.next_label.update()

            self.num_pg_label.place_forget()
            self.prev_label.place_forget()
            self.next_label.place_forget()

            self.place(x=root.winfo_width(), y=root.winfo_height())
            # self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))
            # self.view_canvas.bind('<Configure>', self.onFrameConfigure)

            self.search_frame = Frame(canvas, width=main_layout[0], height=round(0.08 * main_layout[1]),
                                      bg=CP[theme][0], highlightthickness=0)
            self.search_frame.place(x=margin_width, y=margin_height)

            self.search_str = StringVar()
            self.search_by_str = StringVar()
            self.search_filter_str = StringVar()
            # self.search_sort_str = StringVar()

            font_setting = "Calibri " + str(round(math.pow(font_size, 0.89)))
            # print(font_size, font_size * 0.75)
            pe = str(round(self.winfo_width() / 412))  # 412
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            coord_x = margin_width / 10
            self.search_entry = ttk.Entry(self.search_frame, width=30, textvariable=self.search_str,
                                          font=font_setting, style='pad.TEntry')
            self.search_entry.place(x=coord_x, y=0)
            self.search_entry.update()

            # Default Search By Name
            coord_x = coord_x + self.search_entry.winfo_width() + math.sqrt(margin_width)
            self.search_by_cbox = ttk.Combobox(self.search_frame, width=20, font=font_setting,
                                               textvariable=self.search_by_str, style='pad.TCombobox')
            self.search_by_cbox['values'] = ['Search By...', 'Name', 'Plate Number', 'Student/Staff/Officer ID',
                                             'Car Brand', 'Car Model']
            self.search_by_cbox['state'] = 'readonly'  # disabled or readonly
            self.search_by_cbox.current(0)
            self.search_by_cbox.place(x=coord_x, y=0)
            self.search_by_cbox.update()

            # Default Filter By All
            coord_x = coord_x + self.search_by_cbox.winfo_width() + math.sqrt(margin_width)
            self.search_filter_cbox = ttk.Combobox(self.search_frame, width=10, font=font_setting,
                                                   textvariable=self.search_filter_str, style='pad.TCombobox')
            self.search_filter_cbox['values'] = ['Filter By...', 'All', 'Student', 'Staff', 'Officer']
            self.search_filter_cbox['state'] = 'readonly'  # disabled or readonly
            self.search_filter_cbox.current(0)
            self.search_filter_cbox.place(x=coord_x, y=0)
            self.search_filter_cbox.update()

            # Default Sort By Name Asc.
            # coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(margin_width)
            # self.search_sort_cbox = ttk.Combobox(self.search_frame, width=22, font=font_setting,
            #                                      textvariable=self.search_sort_str, style='pad.TCombobox')
            # self.search_sort_cbox['values'] = ['Sort By...', 'Name Asc.', 'Name Desc.',
            #                                    'Plt. Num. Asc.', 'Plt. Num. Desc.',
            #                                    'Matric No./Staff ID Asc.', 'Matric No./Staff ID Desc.']
            # self.search_sort_cbox['state'] = 'readonly'  # disabled or readonly
            # self.search_sort_cbox.current(0)
            # self.search_sort_cbox.place(x=coord_x, y=0)
            # self.search_sort_cbox.update()

            coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(
                margin_width)  # self.search_sort_cbox.winfo_width() +
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.85)))
            self.search_btn = Button(self.search_frame, bg=CP[theme][5], fg=CP[theme][1],
                                     activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                     text="Search", font=font_setting, padx=10, pady=1,
                                     command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                                     self.search_driver(a, b))
            self.search_btn.place(x=coord_x + self.search_btn.winfo_width() / 2, y=0)
            self.search_btn.update()
            self.place_forget()

        def update_res(self, root):
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size
            margin_width = root.margin_width
            margin_height = root.margin_height
            main_layout = root.main_layout
            canvas_index = root.canvas_index

            self.configure(width=main_layout[0], height=round(self.mar_search * main_layout[1]))
            self.view_canvas.configure(width=main_layout[0], height=round(self.mar_search * main_layout[1]))
            if self.driver_list:
                self.place(x=margin_width, y=margin_height + round((1 - self.mar_search) * main_layout[1]))

                font_setting = "Calibri " + str(round(math.pow(font_size, 1)))
                self.num_pg_label.configure(font=font_setting)
                font_setting = "Calibri " + str(round(math.pow(font_size, 1.1))) + " bold"
                self.prev_label.configure(font=font_setting)
                self.next_label.configure(font=font_setting)
                self.num_pg_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.prev_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.next_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.num_pg_label.update()
                self.prev_label.update()
                self.next_label.update()

                self.view_canvas.update()
                y_coord = 0
                GAP = round(0.25 / 100 * root.winfo_width())
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                frame_item_ind = (self.page_index - 1) * self.prof_per_frame
                division = math.ceil(len(self.frame_item) / self.prof_per_frame)
                remainder = len(self.frame_item) % self.prof_per_frame
                path_driver = os.path.join(TEMP_FOLDER, DRIVER_FOLDER)
                last_page = False
                # print("PG IND: ", self.page_index, "\tDIV", division)
                if self.page_index == division:
                    last_page = True
                else:
                    last_page = False

                # for file in os.listdir('./temp/driver'):
                #     os.remove(file)

                for i, frame in enumerate(self.sub_frame[self.page_index - 1]):
                    frame.configure(width=self.view_canvas.winfo_width(), height=frame_height)
                    self.view_canvas.coords(self.canvas_item[i], (0, y_coord))
                    y_coord = y_coord + frame_height

                    if not last_page or (last_page and i < remainder) or remainder == 0:
                        # print(frame_item_ind + i, i, last_page)
                        font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                        self.frame_item[frame_item_ind + i][2].configure(font=font_setting)

                        font_setting = "Calibri " + str(round(root.font_size * 0.65))
                        self.frame_item[frame_item_ind + i][3].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][4].configure(font=font_setting)

                        self.frame_item[frame_item_ind + i][2].update()
                        self.frame_item[frame_item_ind + i][3].update()
                        self.frame_item[frame_item_ind + i][4].update()

                        coord = [round(20 / 100 * self.view_canvas.winfo_width()), round(5 / 100 * frame_height)]
                        self.frame_item[frame_item_ind + i][2].place(x=coord[0], y=coord[1])
                        coord[1] = coord[1] + self.frame_item[frame_item_ind + i][2].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][3].place(x=coord[0], y=coord[1])
                        y_coord_lbl = coord[1] + self.frame_item[frame_item_ind + i][3].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][4].place(x=coord[0], y=y_coord_lbl)

                        coord[0] = coord[0] + round(20 / 100 * self.view_canvas.winfo_width())
                        y_coord_lbl = coord[1]

                        add_index = 0
                        if self.frame_item[frame_item_ind + i][0] == 'student':
                            self.frame_item[frame_item_ind + i][5].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][6].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][7].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][5].update()
                            self.frame_item[frame_item_ind + i][6].update()
                            self.frame_item[frame_item_ind + i][7].update()
                            self.frame_item[frame_item_ind + i][5].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][5].winfo_height() + GAP
                            self.frame_item[frame_item_ind + i][6].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][6].winfo_height() + GAP
                            self.frame_item[frame_item_ind + i][7].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][7].winfo_height() + GAP
                            add_index = 7
                        elif self.frame_item[frame_item_ind + i][0] == 'staff':
                            self.frame_item[frame_item_ind + i][5].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][5].update()
                            self.frame_item[frame_item_ind + i][5].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][5].winfo_height() + GAP
                            add_index = 5
                        elif self.frame_item[frame_item_ind + i][0] == 'officer':
                            self.frame_item[frame_item_ind + i][5].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][5].update()
                            self.frame_item[frame_item_ind + i][5].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][5].winfo_height() + GAP
                            add_index = 5

                        self.frame_item[frame_item_ind + i][add_index + 1].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][add_index + 2].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][add_index + 3].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][add_index + 4].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][add_index + 5].configure(font=font_setting)

                        self.frame_item[frame_item_ind + i][add_index + 1].update()
                        self.frame_item[frame_item_ind + i][add_index + 2].update()
                        self.frame_item[frame_item_ind + i][add_index + 3].update()
                        self.frame_item[frame_item_ind + i][add_index + 4].update()
                        self.frame_item[frame_item_ind + i][add_index + 5].update()

                        self.frame_item[frame_item_ind + i][add_index + 1].place(x=coord[0], y=y_coord_lbl)
                        coord[0] = coord[0] + round(28 / 100 * self.view_canvas.winfo_width())
                        y_coord_lbl = coord[1]
                        self.frame_item[frame_item_ind + i][add_index + 2].place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][
                            add_index + 2].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][add_index + 3].place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][
                            add_index + 3].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][add_index + 4].place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + self.frame_item[frame_item_ind + i][
                            add_index + 4].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][add_index + 5].place(x=coord[0], y=y_coord_lbl)

                        no_img_driver = Image.new('RGB', (frame_height - self.borderwidth * 2,
                                                          frame_height - self.borderwidth * 2), color='#171010')
                        no_img_driver_text = "No Driver\nImage Available"
                        no_img_driver_font = ImageFont.truetype("calibri.ttf", round(root.font_size * 1.1))
                        draw = ImageDraw.Draw(no_img_driver)
                        w, h = draw.textsize(no_img_driver_text, font=no_img_driver_font)
                        draw.text((round((no_img_driver.width / 2 - w / 2)),
                                   round(no_img_driver.height / 2 - h / 2)),
                                  no_img_driver_text, "#EEEEEE", font=no_img_driver_font, align=CENTER)

                        if self.frame_item[frame_item_ind + i][0] == 'student':
                            if self.frame_item[frame_item_ind + i][15]:
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[frame_item_ind + i][16]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[frame_item_ind + i][13] = ImageTk.PhotoImage(img_resized_driver)
                            else:
                                self.frame_item[frame_item_ind + i][13] = ImageTk.PhotoImage(no_img_driver)
                            self.frame_item[frame_item_ind + i][14].configure(
                                image=self.frame_item[frame_item_ind + i][13],
                                width=frame_height - self.borderwidth * 2, height=frame_height - self.borderwidth * 2)
                            self.frame_item[frame_item_ind + i][14].place(x=0, y=0)
                            self.frame_item[frame_item_ind + i][14].update()
                        elif self.frame_item[frame_item_ind + i][0] == 'staff':
                            if self.frame_item[frame_item_ind + i][13]:
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[frame_item_ind + i][14]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[frame_item_ind + i][11] = ImageTk.PhotoImage(img_resized_driver)
                            else:
                                self.frame_item[frame_item_ind + i][11] = ImageTk.PhotoImage(no_img_driver)
                            # self.frame_item[frame_item_ind + i][11] = ImageTk.PhotoImage(no_img_driver)
                            self.frame_item[frame_item_ind + i][12].configure(
                                image=self.frame_item[frame_item_ind + i][11],
                                width=frame_height - self.borderwidth * 2, height=frame_height - self.borderwidth * 2)
                            self.frame_item[frame_item_ind + i][12].place(x=0, y=0)
                            self.frame_item[frame_item_ind + i][12].update()
                        elif self.frame_item[frame_item_ind + i][0] == 'officer':
                            if self.frame_item[frame_item_ind + i][13]:
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[frame_item_ind + i][14]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[frame_item_ind + i][11] = ImageTk.PhotoImage(img_resized_driver)
                            else:
                                self.frame_item[frame_item_ind + i][11] = ImageTk.PhotoImage(no_img_driver)
                            # self.frame_item[frame_item_ind + i][11] = ImageTk.PhotoImage(no_img_driver)
                            self.frame_item[frame_item_ind + i][12].configure(
                                image=self.frame_item[frame_item_ind + i][11],
                                width=frame_height - self.borderwidth * 2, height=frame_height - self.borderwidth * 2)
                            self.frame_item[frame_item_ind + i][12].place(x=0, y=0)
                            self.frame_item[frame_item_ind + i][12].update()

                        font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                        self.frame_item[frame_item_ind + i][add_index + 10].configure(font=font_setting,
                                                                                      width=round(
                                                                                          0.01 * frame.winfo_width()))
                        self.frame_item[frame_item_ind + i][add_index + 11].configure(font=font_setting,
                                                                                      width=round(
                                                                                          0.01 * frame.winfo_width()))
                        # command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                        #                                              self.search_driver(a, b)
                        self.frame_item[frame_item_ind + i][add_index + 10].update()
                        self.frame_item[frame_item_ind + i][add_index + 11].update()
                        self.frame_item[frame_item_ind + i][add_index + 10].place(
                            x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                add_index + 10].winfo_width() - self.borderwidth * 2,
                            y=self.borderwidth)
                        self.frame_item[frame_item_ind + i][add_index + 11].place(
                            x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                add_index + 11].winfo_width() - self.borderwidth * 2,
                            y=round(self.frame_item[frame_item_ind + i][
                                        add_index + 11].winfo_height() * 1.1) + self.borderwidth)

                remainder = (frame_height - (self.borderwidth * 2)) * self.prof_per_frame - \
                            self.view_canvas.winfo_height()
                remainder = remainder + (self.borderwidth * 2 * self.prof_per_frame)
                self.view_canvas.configure(width=main_layout[0],
                                           height=round(self.mar_search * main_layout[1]) + remainder)

                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() - (
                                                margin_height - self.num_pg_label.winfo_height() / 2))
                if self.page_index >= len(self.sub_frame) and len(self.sub_frame) > 1:
                    self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                            self.prev_label.winfo_width() * 1.5,
                                          y=(root.winfo_height() - margin_height) +
                                            (margin_height / 2 - self.next_label.winfo_height() / 2))
                elif self.page_index > len(self.sub_frame) and len(self.sub_frame) <= 1:
                    self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                            self.prev_label.winfo_width() * 1.5,
                                          y=(root.winfo_height() - margin_height) +
                                            (margin_height / 2 - self.next_label.winfo_height() / 2))

                if self.page_index < len(self.sub_frame):
                    self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                            self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                          y=(root.winfo_height() - margin_height) +
                                            (margin_height / 2 - self.next_label.winfo_height() / 2))

            else:
                self.place(x=width, y=height)
                self.num_pg_label.place_forget()
                self.prev_label.place_forget()
                self.next_label.place_forget()

            self.search_frame.configure(width=main_layout[0], height=round(0.08 * main_layout[1]))
            self.search_frame.place(x=margin_width, y=margin_height)

            font_setting = "Calibri " + str(round(math.pow(font_size, 0.89)))
            pe = str(round(self.winfo_width() / 412))  # 412
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            coord_x = margin_width / 10
            self.search_entry.configure(font=font_setting, style='pad.TEntry')
            self.search_entry.place(x=coord_x, y=0)
            self.search_entry.update()

            # Default Search By Name
            coord_x = coord_x + self.search_entry.winfo_width() + math.sqrt(margin_width)
            self.search_by_cbox.configure(font=font_setting, style='pad.TCombobox')
            self.search_by_cbox.place(x=coord_x, y=0)
            self.search_by_cbox.update()

            # Default Filter By All
            coord_x = coord_x + self.search_by_cbox.winfo_width() + math.sqrt(margin_width)
            self.search_filter_cbox.configure(font=font_setting, style='pad.TCombobox')
            self.search_filter_cbox.place(x=coord_x, y=0)
            self.search_filter_cbox.update()

            # Default Sort By Name Asc.
            # coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(margin_width)
            # self.search_sort_cbox.configure(font=font_setting, style='pad.TCombobox')
            # self.search_sort_cbox.place(x=coord_x, y=0)
            # self.search_sort_cbox.update()

            coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(
                margin_width)  # self.search_sort_cbox.winfo_width() +
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.85)))
            self.search_btn.configure(font=font_setting,
                                      command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                                      self.search_driver(a, b))
            self.search_btn.place(x=coord_x, y=0)
            self.search_btn.update()

            font_setting = "Calibri " + str(round(math.pow(font_size, 0.89)))
            self.search_by_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
                                        format(self.search_by_cbox, font_setting))
            self.search_filter_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
                                            format(self.search_filter_cbox, font_setting))
            # self.search_sort_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
            #                               format(self.search_sort_cbox, font_setting))

            """
            # Need to Adjust back After Search
            for frame in self.sub_frame:
                frame.configure(width=main_layout[0])
            
            self.view_canvas.bind_all("<MouseWheel>",
                                      lambda event, a=self, b=[margin_width, margin_height, self.mar_search],
                                      : self.root._on_mousewheel(event, a, b))
            """

            if not self.driver_list:
                self.place_forget()
            self.update()

        def search_driver(self, margin, root):
            main_layout = root.main_layout
            theme = root.theme
            self.driver_list = []
            print("Search Driver")
            # Test
            """
            if self.search_str.get() == "test":
                self.driver_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            
            Input
                self.search_str
                self.search_by_str
                self.search_sort_str (Unused)
                self.search_filter_str
            """

            search_by = ""
            if self.search_by_str.get() == self.search_by_cbox['value'][1]:
                search_by = "name"
            elif self.search_by_str.get() == self.search_by_cbox['value'][2]:
                search_by = "plate"
            elif self.search_by_str.get() == self.search_by_cbox['value'][3]:
                search_by = "id"
            elif self.search_by_str.get() == self.search_by_cbox['value'][4]:
                search_by = "brand"
            elif self.search_by_str.get() == self.search_by_cbox['value'][5]:
                search_by = "model"
            else:
                search_by = "name"

            search_filter = ""
            if self.search_filter_str.get() == self.search_filter_cbox['value'][0]:
                search_filter = 'all'
            else:
                search_filter = self.search_filter_str.get().lower()

            # Database Connection
            search_input = self.search_str.get()

            # print("Test = " + search_input)
            # db.select_user(search_input)
            # db.select_car_owner(search_input)
            self.driver_list = db.search_driver(search_input, search_by, search_filter)
            # self.driver_list
            print("Result,")
            for each in self.driver_list:
                print('\t', each)
            # print(user_from_db)

            """
            Output
                List of Driver (2D Array)
                [
                [Name, Matric/staff id, car plate, vehicle type... so on], 
                [Name, Matric/staff id, car plate, vehicle type... so on],
                [Name, Matric/staff id, car plate, vehicle type... so on],
                ... so on
                ]
            """

            # Result Search
            # print(self.driver_list)
            if self.driver_list:
                self.page_index = 1
                self.place(x=margin[0], y=margin[1] + round((1 - margin[2]) * self.winfo_height()))
                y_coord = 0
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                # print(self.view_canvas.winfo_height(), frame_height)
                temp_sub_frame = []
                self.canvas_item = []
                self.sub_frame = []
                self.frame_item = []
                GAP = round(0.25 / 100 * root.winfo_width())
                self.view_canvas.delete('all')

                path_driver = os.path.join(TEMP_FOLDER, DRIVER_FOLDER)
                for file in os.listdir(path_driver):
                    os.remove(os.path.join(path_driver, file))

                for i, driver in enumerate(self.driver_list):
                    # print("\t", driver)
                    each_sub_frame = Frame(self.view_canvas, width=self.view_canvas.winfo_width(), height=frame_height,
                                           bg=CP[theme][5], highlightthickness=self.borderwidth)
                    # Start Label Fragment HERE
                    # data = (role, id, name, year, hostel, vaccineStat, rankOfficer, plateNum, vehType, vehBrand, vehModel, roadTax)

                    font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                    name = Label(each_sub_frame, text="Name\t: " + driver[2].upper(), font=font_setting,
                                 bg=CP[root.theme][5],
                                 fg=CP[root.theme][1])

                    font_setting = "Calibri " + str(round(root.font_size * 0.65))
                    role = Label(each_sub_frame, text="Role\t: " + driver[0].upper(), font=font_setting,
                                 bg=CP[root.theme][5],
                                 fg=CP[root.theme][1])
                    driver_id = Label(each_sub_frame, text="ID\t: " + driver[1].upper(), font=font_setting,
                                      bg=CP[root.theme][5], fg=CP[root.theme][1])
                    year = None
                    hostel = None
                    vac_stat = None
                    rank = None

                    role.place(x=self.view_canvas.winfo_width(), y=frame_height)
                    driver_id.place(x=self.view_canvas.winfo_width(), y=frame_height)
                    name.place(x=self.view_canvas.winfo_width(), y=frame_height)
                    role.update()
                    driver_id.update()
                    name.update()

                    coord = [round(20 / 100 * self.view_canvas.winfo_width()), round(5 / 100 * frame_height)]
                    name.place(x=coord[0], y=coord[1])
                    coord[1] = coord[1] + name.winfo_height() + GAP
                    role.place(x=coord[0], y=coord[1])
                    y_coord_lbl = coord[1] + role.winfo_height() + GAP
                    driver_id.place(x=coord[0], y=y_coord_lbl)

                    coord[0] = coord[0] + round(20 / 100 * self.view_canvas.winfo_width())
                    y_coord_lbl = coord[1]

                    if driver[0] == 'student':
                        driver_id.configure(text="Matric ID\t: " + driver[1].upper())
                        year = Label(each_sub_frame, text="Year\t\t: " + str(driver[3]), font=font_setting,
                                     bg=CP[root.theme][5],
                                     fg=CP[root.theme][1])
                        hostel = Label(each_sub_frame, text="Hostel\t\t: " + driver[4], font=font_setting,
                                       bg=CP[root.theme][5],
                                       fg=CP[root.theme][1])
                        vac_stat = Label(each_sub_frame, text="Vaccine Status\t: " + driver[5], font=font_setting,
                                         bg=CP[root.theme][5],
                                         fg=CP[root.theme][1])
                        year.place(x=0, y=0)
                        hostel.place(x=0, y=0)
                        vac_stat.place(x=0, y=0)
                        year.update()
                        hostel.update()
                        vac_stat.update()
                        year.place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + year.winfo_height() + GAP
                        hostel.place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + hostel.winfo_height() + GAP
                        vac_stat.place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + vac_stat.winfo_height() + GAP
                    elif driver[0] == 'staff':
                        driver_id.configure(text="Staff ID\t: " + driver[1].upper())
                        vac_stat = Label(each_sub_frame, text="Vaccine Status\t: " + driver[5], font=font_setting,
                                         bg=CP[root.theme][5],
                                         fg=CP[root.theme][1])
                        vac_stat.place(x=coord[0], y=0)
                        vac_stat.update()
                        vac_stat.place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + vac_stat.winfo_height() + GAP
                    elif driver[0] == 'officer':
                        driver_id.configure(text="Officer ID\t: " + driver[1].upper())
                        rank = Label(each_sub_frame, text="Rank\t\t: " + driver[6], font=font_setting,
                                     bg=CP[root.theme][5],
                                     fg=CP[root.theme][1])
                        rank.place(x=coord[0], y=0)
                        rank.update()
                        rank.place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + rank.winfo_height() + GAP

                    plate_num = Label(each_sub_frame, text="Plate Number\t: " + driver[7].upper(), font=font_setting,
                                      bg=CP[root.theme][5],
                                      fg=CP[root.theme][1])
                    veh_type = Label(each_sub_frame, text="Vehicle Type\t: " + driver[8], font=font_setting,
                                     bg=CP[root.theme][5],
                                     fg=CP[root.theme][1])
                    veh_brand = Label(each_sub_frame, text="Vehicle Brand\t: " + driver[9].upper(), font=font_setting,
                                      bg=CP[root.theme][5],
                                      fg=CP[root.theme][1])
                    veh_model = Label(each_sub_frame, text="Vehicle Brand\t: " + driver[10].upper(), font=font_setting,
                                      bg=CP[root.theme][5],
                                      fg=CP[root.theme][1])
                    road_tax = Label(each_sub_frame,
                                     text="Road Tax\t\t: " + datetime.datetime.strftime(driver[11], '%d/%m/%Y'),
                                     font=font_setting, bg=CP[root.theme][5], fg=CP[root.theme][1])

                    plate_num.place(x=0, y=0)
                    veh_type.place(x=0, y=0)
                    veh_brand.place(x=0, y=0)
                    veh_model.place(x=0, y=0)
                    road_tax.place(x=0, y=0)
                    plate_num.update()
                    veh_type.update()
                    veh_brand.update()
                    veh_model.update()
                    road_tax.update()

                    plate_num.place(x=coord[0], y=y_coord_lbl)
                    coord[0] = coord[0] + round(28 / 100 * self.view_canvas.winfo_width())
                    y_coord_lbl = coord[1]
                    veh_type.place(x=coord[0], y=y_coord_lbl)
                    y_coord_lbl = y_coord_lbl + veh_type.winfo_height() + GAP
                    veh_brand.place(x=coord[0], y=y_coord_lbl)
                    y_coord_lbl = y_coord_lbl + veh_brand.winfo_height() + GAP
                    veh_model.place(x=coord[0], y=y_coord_lbl)
                    y_coord_lbl = y_coord_lbl + veh_model.winfo_height() + GAP
                    road_tax.place(x=coord[0], y=y_coord_lbl)

                    no_img_driver = Image.new('RGB', (frame_height - self.borderwidth * 2,
                                                      frame_height - self.borderwidth * 2), color='#171010')
                    no_img_driver_text = "No Driver\nImage Available"
                    no_img_driver_font = ImageFont.truetype("calibri.ttf", round(root.font_size * 1.1))
                    draw = ImageDraw.Draw(no_img_driver)
                    w, h = draw.textsize(no_img_driver_text, font=no_img_driver_font)
                    draw.text((round((no_img_driver.width / 2 - w / 2)),
                               round(no_img_driver.height / 2 - h / 2)),
                              no_img_driver_text, "#EEEEEE", font=no_img_driver_font, align=CENTER)
                    driver_img_tk = ImageTk.PhotoImage(no_img_driver)
                    driver_img_label = Label(each_sub_frame, bg=CP[theme][2], bd=0,
                                             width=frame_height - self.borderwidth * 2,
                                             height=frame_height - self.borderwidth * 2)

                    dw_result = False
                    driver_img = ''
                    if i < self.prof_per_frame:
                        canvas_item = self.view_canvas.create_window((0, y_coord), window=each_sub_frame, anchor=NW)
                        self.canvas_item.append(canvas_item)
                        dw_result, driver_img = fl.dw_from_server(path_driver, driver[1].upper(), 1)
                        if dw_result:
                            img_driver = Image.open(os.path.join(path_driver, driver_img))
                            img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                    frame_height - self.borderwidth * 2),
                                                                   Image.ANTIALIAS)
                            if driver[0] == 'student':
                                driver_img_tk = ImageTk.PhotoImage(img_resized_driver)
                                driver_img_label.configure(image=driver_img_tk)
                                driver_img_label.place(x=0, y=0)
                                driver_img_label.update()
                            elif driver[0] == 'staff':
                                driver_img_tk = ImageTk.PhotoImage(img_resized_driver)
                                driver_img_label.configure(image=driver_img_tk)
                                driver_img_label.place(x=0, y=0)
                                driver_img_label.update()
                            elif driver[0] == 'officer':
                                driver_img_tk = ImageTk.PhotoImage(img_resized_driver)
                                driver_img_label.configure(image=driver_img_tk)
                                driver_img_label.place(x=0, y=0)
                                driver_img_label.update()
                    y_coord = y_coord + frame_height

                    font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                    edit_btn = Button(each_sub_frame, bg=CP[theme][10], fg=CP[theme][11],
                                      activebackground=CP[theme][13], activeforeground=CP[theme][14],
                                      text="Edit", font=font_setting,
                                      width=round(0.01 * each_sub_frame.winfo_width()), pady=1)
                    remove_btn = Button(each_sub_frame, bg=CP[theme][10], fg=CP[theme][11],
                                        activebackground=CP[theme][13], activeforeground=CP[theme][14],
                                        text="Remove", font=font_setting,
                                        width=round(0.01 * each_sub_frame.winfo_width()), pady=1)
                    # command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                    #                                              self.search_driver(a, b)
                    edit_btn.place(x=0, y=0)
                    remove_btn.place(x=0, y=0)
                    edit_btn.update()
                    remove_btn.update()
                    edit_btn.place(x=each_sub_frame.winfo_width() - edit_btn.winfo_width() - self.borderwidth * 2,
                                   y=self.borderwidth)
                    remove_btn.place(x=each_sub_frame.winfo_width() - remove_btn.winfo_width() - self.borderwidth * 2,
                                     y=round(edit_btn.winfo_height() * 1.1) + self.borderwidth)

                    if driver[0] == 'student':
                        self.frame_item.append(
                            [driver[0], driver[1].upper(), name, role, driver_id, year, hostel, vac_stat, plate_num,
                             veh_type, veh_brand, veh_model, road_tax,
                             driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn])
                        self.frame_item[len(self.frame_item) - 1][14].configure(
                            image=self.frame_item[len(self.frame_item) - 1][13])
                        self.frame_item[len(self.frame_item) - 1][14].place(x=0, y=0)
                        self.frame_item[len(self.frame_item) - 1][14].update()

                        self.frame_item[len(self.frame_item) - 1][17].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.edit_driver_menu(a, b)
                        )
                        self.frame_item[len(self.frame_item) - 1][18].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.rem_driver(a, b)
                        )
                    elif driver[0] == 'staff':
                        self.frame_item.append(
                            [driver[0], driver[1].upper(), name, role, driver_id, vac_stat, plate_num, veh_type,
                             veh_brand, veh_model, road_tax,
                             driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn])
                        self.frame_item[len(self.frame_item) - 1][12].configure(
                            image=self.frame_item[len(self.frame_item) - 1][11])
                        self.frame_item[len(self.frame_item) - 1][12].place(x=0, y=0)
                        self.frame_item[len(self.frame_item) - 1][12].update()

                        self.frame_item[len(self.frame_item) - 1][15].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.edit_driver_menu(a, b)
                        )
                        self.frame_item[len(self.frame_item) - 1][16].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.rem_driver(a, b)
                        )
                    elif driver[0] == 'officer':
                        self.frame_item.append(
                            [driver[0], driver[1].upper(), name, role, driver_id, rank, plate_num, veh_type, veh_brand,
                             veh_model, road_tax,
                             driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn])
                        self.frame_item[len(self.frame_item) - 1][12].configure(
                            image=self.frame_item[len(self.frame_item) - 1][11])
                        self.frame_item[len(self.frame_item) - 1][12].place(x=0, y=0)
                        self.frame_item[len(self.frame_item) - 1][12].update()

                        self.frame_item[len(self.frame_item) - 1][15].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.edit_driver_menu(a, b)
                        )
                        self.frame_item[len(self.frame_item) - 1][16].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.rem_driver(a, b)
                        )

                    if i % self.prof_per_frame < self.prof_per_frame - 1:
                        temp_sub_frame.append(each_sub_frame)
                        if i == len(self.driver_list) - 1:
                            remainder = self.prof_per_frame - (i % self.prof_per_frame)

                            for j in range(0, remainder):
                                each_sub_frame = Frame(self.view_canvas, width=self.view_canvas.winfo_width(),
                                                       height=frame_height,
                                                       bg=CP[theme][5], highlightthickness=self.borderwidth)
                                temp_sub_frame.append(each_sub_frame)

                                canvas_item = self.view_canvas.create_window((0, y_coord), window=each_sub_frame,
                                                                             anchor=NW)
                                self.canvas_item.append(canvas_item)
                                y_coord = y_coord + frame_height
                            self.sub_frame.append(temp_sub_frame)
                    else:
                        temp_sub_frame.append(each_sub_frame)
                        self.sub_frame.append(temp_sub_frame)
                        temp_sub_frame = []

                self.configure(width=main_layout[0], height=round(margin[2] * main_layout[1]))
                self.place(x=margin[0], y=margin[1] + round((1 - margin[2]) * main_layout[1]))

                remainder = self.view_canvas.winfo_height() - (frame_height - (self.borderwidth * 2)) * \
                            self.prof_per_frame
                remainder = remainder - (self.borderwidth * 2 * self.prof_per_frame)

                self.view_canvas.configure(width=main_layout[0], height=self.view_canvas.winfo_height() - remainder)
                self.view_canvas.update()
                self.search_frame.configure(width=main_layout[0], height=round(0.08 * main_layout[1]))
                self.search_frame.place(x=margin[0], y=margin[1])
                # self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))

                font_setting = "Calibri " + str(round(math.pow(root.font_size, 1)))
                self.num_pg_label.configure(font=font_setting, text=("1 / " + str(len(self.sub_frame))))
                font_setting = "Calibri " + str(round(math.pow(root.font_size, 1.1))) + " bold"
                self.prev_label.configure(font=font_setting)
                self.next_label.configure(font=font_setting)
                self.num_pg_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.prev_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.next_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.num_pg_label.update()
                self.prev_label.update()
                self.next_label.update()

                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() - (
                                                margin[1] - self.num_pg_label.winfo_height() / 2))
                """self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                        self.prev_label.winfo_width() * 1.5,
                                      y=(root.winfo_height() - margin[1]) +
                                        (margin[1] / 2 - self.next_label.winfo_height() / 2))"""
                if len(self.sub_frame) > 1:
                    self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                            self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                          y=(root.winfo_height() - margin[1]) +
                                            (margin[1] / 2 - self.next_label.winfo_height() / 2))
            else:
                self.place_forget()
                self.num_pg_label.place_forget()
                self.prev_label.place_forget()
                self.next_label.place_forget()
                print("Empty Search Result")

        def onFrameConfigure(self, event):
            self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))

        def on_press(self, event, type, theme):
            if type == 1:
                self.prev_label.configure(bg=CP[theme][3])
            elif type == 2:
                self.next_label.configure(bg=CP[theme][3])

        def on_release(self, event, type, root):
            if type == 1:
                self.prev_label.configure(bg=CP[root.theme][0])
                self.page_index = self.page_index - 1

                self.view_canvas.update()
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                y_coord = 0
                self.view_canvas.delete('all')
                self.canvas_item = []
                for frame in self.sub_frame[self.page_index - 1]:
                    frame.configure(width=self.view_canvas.winfo_width(), height=frame_height)
                    canvas_item = self.view_canvas.create_window((0, y_coord), window=frame, anchor=NW)
                    self.canvas_item.append(canvas_item)
                    y_coord = y_coord + frame_height

                self.num_pg_label.configure(text=(str(self.page_index) + " / " + str(len(self.sub_frame))))
                self.num_pg_label.update()
                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() -
                                          (root.margin_height - self.num_pg_label.winfo_height() / 2))

                self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                        self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                      y=(root.winfo_height() - root.margin_height) +
                                        (root.margin_height / 2 - self.next_label.winfo_height() / 2))

                if self.page_index > 1:
                    self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                            self.prev_label.winfo_width() * 1.5,
                                          y=(root.winfo_height() - root.margin_height) +
                                            (root.margin_height / 2 - self.next_label.winfo_height() / 2))
                else:
                    self.prev_label.place_forget()
            elif type == 2:
                self.next_label.configure(bg=CP[root.theme][0])
                self.page_index = self.page_index + 1

                self.view_canvas.update()
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                y_coord = 0
                self.view_canvas.delete('all')
                self.canvas_item = []
                for frame in self.sub_frame[self.page_index - 1]:
                    frame.configure(width=self.view_canvas.winfo_width(), height=frame_height)
                    canvas_item = self.view_canvas.create_window((0, y_coord), window=frame, anchor=NW)
                    self.canvas_item.append(canvas_item)
                    y_coord = y_coord + frame_height

                self.num_pg_label.configure(text=(str(self.page_index) + " / " + str(len(self.sub_frame))))
                self.num_pg_label.update()
                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() -
                                          (root.margin_height - self.num_pg_label.winfo_height() / 2))

                self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                        self.prev_label.winfo_width() * 1.5,
                                      y=(root.winfo_height() - root.margin_height) +
                                        (root.margin_height / 2 - self.next_label.winfo_height() / 2))

                if self.page_index < len(self.sub_frame):
                    self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                            self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                          y=(root.winfo_height() - root.margin_height) +
                                            (root.margin_height / 2 - self.next_label.winfo_height() / 2))
                else:
                    self.next_label.place_forget()

            if 1 <= type <= 2:
                GAP = round(0.25 / 100 * root.winfo_width())
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                frame_item_ind = (self.page_index - 1) * self.prof_per_frame
                division = math.ceil(len(self.frame_item) / self.prof_per_frame)
                remainder = len(self.frame_item) % self.prof_per_frame
                last_page = False
                # print("PG IND: ", self.page_index, "\tDIV", division)
                if self.page_index == division:
                    last_page = True
                else:
                    last_page = False

                path_driver = os.path.join(TEMP_FOLDER, DRIVER_FOLDER)
                for file in os.listdir(path_driver):
                    os.remove(os.path.join(path_driver, file))

                path_driver = os.path.join(TEMP_FOLDER, DRIVER_FOLDER)
                index = (self.page_index - 1) * self.prof_per_frame
                for i, frame in enumerate(self.sub_frame[self.page_index - 1]):
                    if not last_page or (last_page and i < remainder) or remainder == 0:
                        # print(index + i, i, last_page)
                        font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                        self.frame_item[index + i][2].configure(font=font_setting)

                        font_setting = "Calibri " + str(round(root.font_size * 0.65))
                        self.frame_item[index + i][3].configure(font=font_setting)
                        self.frame_item[index + i][4].configure(font=font_setting)

                        self.frame_item[index + i][2].update()
                        self.frame_item[index + i][3].update()
                        self.frame_item[index + i][4].update()

                        coord = [round(20 / 100 * self.view_canvas.winfo_width()), round(5 / 100 * frame_height)]
                        self.frame_item[index + i][2].place(x=coord[0], y=coord[1])
                        coord[1] = coord[1] + self.frame_item[index + i][2].winfo_height() + GAP
                        self.frame_item[index + i][3].place(x=coord[0], y=coord[1])
                        y_coord_lbl = coord[1] + self.frame_item[index + i][3].winfo_height() + GAP
                        self.frame_item[index + i][4].place(x=coord[0], y=y_coord_lbl)

                        coord[0] = coord[0] + round(20 / 100 * self.view_canvas.winfo_width())
                        y_coord_lbl = coord[1]

                        add_index = 0
                        if self.frame_item[index + i][0] == 'student':
                            self.frame_item[index + i][5].configure(font=font_setting)
                            self.frame_item[index + i][6].configure(font=font_setting)
                            self.frame_item[index + i][7].configure(font=font_setting)
                            self.frame_item[index + i][5].update()
                            self.frame_item[index + i][6].update()
                            self.frame_item[index + i][7].update()
                            self.frame_item[index + i][5].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[index + i][5].winfo_height() + GAP
                            self.frame_item[index + i][6].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[index + i][6].winfo_height() + GAP
                            self.frame_item[index + i][7].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[index + i][7].winfo_height() + GAP
                            add_index = 7
                        elif self.frame_item[index + i][0] == 'staff':
                            self.frame_item[index + i][5].configure(font=font_setting)
                            self.frame_item[index + i][5].update()
                            self.frame_item[index + i][5].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[index + i][5].winfo_height() + GAP
                            add_index = 5
                        elif self.frame_item[index + i][0] == 'officer':
                            self.frame_item[index + i][5].configure(font=font_setting)
                            self.frame_item[index + i][5].update()
                            self.frame_item[index + i][5].place(x=coord[0], y=y_coord_lbl)
                            y_coord_lbl = y_coord_lbl + self.frame_item[index + i][5].winfo_height() + GAP
                            add_index = 5

                        self.frame_item[index + i][add_index + 1].configure(font=font_setting)
                        self.frame_item[index + i][add_index + 2].configure(font=font_setting)
                        self.frame_item[index + i][add_index + 3].configure(font=font_setting)
                        self.frame_item[index + i][add_index + 4].configure(font=font_setting)
                        self.frame_item[index + i][add_index + 5].configure(font=font_setting)

                        self.frame_item[index + i][add_index + 1].update()
                        self.frame_item[index + i][add_index + 2].update()
                        self.frame_item[index + i][add_index + 3].update()
                        self.frame_item[index + i][add_index + 4].update()
                        self.frame_item[index + i][add_index + 5].update()

                        self.frame_item[index + i][add_index + 1].place(x=coord[0], y=y_coord_lbl)
                        coord[0] = coord[0] + round(28 / 100 * self.view_canvas.winfo_width())
                        y_coord_lbl = coord[1]
                        self.frame_item[index + i][add_index + 2].place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + self.frame_item[index + i][
                            add_index + 2].winfo_height() + GAP
                        self.frame_item[index + i][add_index + 3].place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + self.frame_item[index + i][
                            add_index + 3].winfo_height() + GAP
                        self.frame_item[index + i][add_index + 4].place(x=coord[0], y=y_coord_lbl)
                        y_coord_lbl = y_coord_lbl + self.frame_item[index + i][
                            add_index + 4].winfo_height() + GAP
                        self.frame_item[index + i][add_index + 5].place(x=coord[0], y=y_coord_lbl)

                        dw_result, driver_img = fl.dw_from_server(path_driver, self.frame_item[index + i][1], 1)
                        if dw_result:
                            # img_driver = Image.open(os.path.join(path_driver, driver_img))
                            # img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                            #                                         frame_height - self.borderwidth * 2),
                            #                                        Image.ANTIALIAS)
                            print("Index: ", index + i)
                            print(self.frame_item[index + i])
                            if self.frame_item[index + i][0] == 'student':
                                self.frame_item[index + i][15] = dw_result
                                self.frame_item[index + i][16] = driver_img
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[index + i][16]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[index + i][13] = ImageTk.PhotoImage(img_resized_driver)
                                self.frame_item[index + i][14].configure(
                                    image=self.frame_item[index + i][13],
                                    width=frame_height - self.borderwidth * 2,
                                    height=frame_height - self.borderwidth * 2)
                                self.frame_item[index + i][14].place(x=0, y=0)
                                self.frame_item[index + i][14].update()
                            elif self.frame_item[index + i][0] == 'staff':
                                self.frame_item[index + i][13] = dw_result
                                self.frame_item[index + i][14] = driver_img
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[index + i][14]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(img_resized_driver)
                                # self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                                self.frame_item[index + i][12].configure(
                                    image=self.frame_item[index + i][11],
                                    width=frame_height - self.borderwidth * 2,
                                    height=frame_height - self.borderwidth * 2)
                                self.frame_item[index + i][12].place(x=0, y=0)
                                self.frame_item[index + i][12].update()
                            elif self.frame_item[index + i][0] == 'officer':
                                self.frame_item[index + i][13] = dw_result
                                self.frame_item[index + i][14] = driver_img
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[index + i][14]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(img_resized_driver)
                                # self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                                self.frame_item[index + i][12].configure(
                                    image=self.frame_item[index + i][11],
                                    width=frame_height - self.borderwidth * 2,
                                    height=frame_height - self.borderwidth * 2)
                                self.frame_item[index + i][12].place(x=0, y=0)
                                self.frame_item[index + i][12].update()
                        else:
                            no_img_driver = Image.new('RGB', (frame_height - self.borderwidth * 2,
                                                              frame_height - self.borderwidth * 2), color='#171010')
                            no_img_driver_text = "No Driver\nImage Available"
                            no_img_driver_font = ImageFont.truetype("calibri.ttf", round(root.font_size * 1.1))
                            draw = ImageDraw.Draw(no_img_driver)
                            w, h = draw.textsize(no_img_driver_text, font=no_img_driver_font)
                            draw.text((round((no_img_driver.width / 2 - w / 2)),
                                       round(no_img_driver.height / 2 - h / 2)),
                                      no_img_driver_text, "#EEEEEE", font=no_img_driver_font, align=CENTER)

                            if self.frame_item[index + i][0] == 'student':
                                self.frame_item[index + i][13] = ImageTk.PhotoImage(no_img_driver)
                                self.frame_item[index + i][14].configure(
                                    image=self.frame_item[index + i][13],
                                    width=frame_height - self.borderwidth * 2,
                                    height=frame_height - self.borderwidth * 2)
                                self.frame_item[index + i][14].place(x=0, y=0)
                                self.frame_item[index + i][14].update()
                            elif self.frame_item[index + i][0] == 'staff':
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                                self.frame_item[index + i][12].configure(
                                    image=self.frame_item[index + i][11],
                                    width=frame_height - self.borderwidth * 2,
                                    height=frame_height - self.borderwidth * 2)
                                self.frame_item[index + i][12].place(x=0, y=0)
                                self.frame_item[index + i][12].update()
                            elif self.frame_item[index + i][0] == 'officer':
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                                self.frame_item[index + i][12].configure(
                                    image=self.frame_item[index + i][11],
                                    width=frame_height - self.borderwidth * 2,
                                    height=frame_height - self.borderwidth * 2)
                                self.frame_item[index + i][12].place(x=0, y=0)
                                self.frame_item[index + i][12].update()

                        if self.frame_item[index + i][0] == 'student':
                            if self.frame_item[index + i][15]:
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[index + i][16]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[index + i][13] = ImageTk.PhotoImage(img_resized_driver)
                            else:
                                self.frame_item[index + i][13] = ImageTk.PhotoImage(no_img_driver)
                            self.frame_item[index + i][14].configure(
                                image=self.frame_item[index + i][13],
                                width=frame_height - self.borderwidth * 2, height=frame_height - self.borderwidth * 2)
                            self.frame_item[index + i][14].place(x=0, y=0)
                            self.frame_item[index + i][14].update()
                        elif self.frame_item[index + i][0] == 'staff':
                            if self.frame_item[index + i][13]:
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[index + i][14]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(img_resized_driver)
                            else:
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                            # self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                            self.frame_item[index + i][12].configure(
                                image=self.frame_item[index + i][11],
                                width=frame_height - self.borderwidth * 2, height=frame_height - self.borderwidth * 2)
                            self.frame_item[index + i][12].place(x=0, y=0)
                            self.frame_item[index + i][12].update()
                        elif self.frame_item[index + i][0] == 'officer':
                            if self.frame_item[index + i][13]:
                                img_driver = Image.open(
                                    os.path.join(path_driver, self.frame_item[index + i][14]))
                                img_resized_driver = img_driver.resize((frame_height - self.borderwidth * 2,
                                                                        frame_height - self.borderwidth * 2),
                                                                       Image.ANTIALIAS)
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(img_resized_driver)
                            else:
                                self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                            # self.frame_item[index + i][11] = ImageTk.PhotoImage(no_img_driver)
                            self.frame_item[index + i][12].configure(
                                image=self.frame_item[index + i][11],
                                width=frame_height - self.borderwidth * 2, height=frame_height - self.borderwidth * 2)
                            self.frame_item[index + i][12].place(x=0, y=0)
                            self.frame_item[index + i][12].update()

                        font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                        self.frame_item[frame_item_ind + i][add_index + 10].configure(font=font_setting,
                                                                                      width=round(
                                                                                          0.01 * frame.winfo_width()))
                        self.frame_item[frame_item_ind + i][add_index + 11].configure(font=font_setting,
                                                                                      width=round(
                                                                                          0.01 * frame.winfo_width()))
                        # command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                        #                                              self.search_driver(a, b)
                        self.frame_item[frame_item_ind + i][add_index + 10].update()
                        self.frame_item[frame_item_ind + i][add_index + 11].update()
                        self.frame_item[frame_item_ind + i][add_index + 10].place(
                            x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                add_index + 10].winfo_width() - self.borderwidth * 2,
                            y=self.borderwidth)
                        self.frame_item[frame_item_ind + i][add_index + 11].place(
                            x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                add_index + 11].winfo_width() - self.borderwidth * 2,
                            y=round(self.frame_item[frame_item_ind + i][
                                        add_index + 11].winfo_height() * 1.1) + self.borderwidth)

        def rem_driver(self, root, data):
            confirm = Toplevel(root)
            filename = 'logo_light_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
            except Exception as e:
                print('Error:', e)
            self.icon = PhotoImage(file=filename)
            confirm.iconphoto(False, self.icon)

            width = 320
            height = 180
            x = round(root.winfo_width() / 2 - width / 2) + root.winfo_x()
            y = round(root.winfo_height() / 2 - height / 2) + root.winfo_y()
            gap = 50
            entry_length = 20

            confirm.title('Confirmation')
            confirm.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            # self.attributes('-topmost', True)
            confirm.grab_set()
            # self.grab_release()  # After Finish Setting
            confirm.resizable(False, False)

            confirm_main_canvas = Canvas(confirm, highlightthickness=0, bg=CP[root.theme][5],
                                         width=width, height=height)
            confirm_main_canvas.place(x=0, y=0)
            confirm_main_canvas.update()

            confirm_frame = Frame(confirm_main_canvas, bg=CP[root.theme][5])
            font_setting = "Calibri " + str(15)  # round(root.font_size * 0.85)
            confirm_label = Label(confirm_main_canvas, font=font_setting, text='Confirm to Remove?',
                                  bg=CP[root.theme][5], fg=CP[root.theme][1])
            confirm_label.place(x=0, y=0)
            confirm_label.update()
            confirm_label.place(x=width / 2 - confirm_label.winfo_width() / 2,
                                y=height / 4)

            font_setting = "Calibri " + str(10)  # round(root.font_size * 0.65)
            confirm_ok_btn = Button(confirm_main_canvas, font=font_setting, text="Confirm", width=8,
                                    bg=CP[root.theme][10], fg=CP[root.theme][11],
                                    activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                    command=lambda a=root, b=confirm, c=2, d=data: btn_event(a, b, c, d))
            confirm_ok_btn.place(x=width, y=height)
            confirm_ok_btn.update()
            confirm_ok_btn.place(x=width / 2 - confirm_ok_btn.winfo_width() - 10,
                                 y=3 * height / 4 - confirm_ok_btn.winfo_height())
            confirm_ok_btn.update()

            confirm_cancel_btn = Button(confirm_main_canvas, font=font_setting, text="Cancel", width=8,
                                        bg=CP[root.theme][10], fg=CP[root.theme][11],
                                        activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                        command=lambda a=root, b=confirm, c=1, d=data: btn_event(a, b, c, d))
            confirm_cancel_btn.place(x=width, y=height)
            confirm_cancel_btn.update()
            confirm_cancel_btn.place(x=width / 2 + 10,
                                     y=3 * height / 4 - confirm_cancel_btn.winfo_height())
            confirm_cancel_btn.update()

            def btn_event(root, confirm, type, data):
                # type = 2 is originally for port, got taken out
                if type == 1:
                    confirm.destroy()
                elif type == 2:
                    label_data = []
                    if data[0] == 'student':
                        label_data = ['student', 'studentID', data[4].cget("text").split(': ')[1],
                                      data[8].cget("text").split(': ')[1]]
                    elif data[0] == 'staff':
                        label_data = ['staff', 'staffID', data[4].cget("text").split(': ')[1],
                                      data[6].cget("text").split(': ')[1]]
                    elif data[0] == 'officer':
                        label_data = ['officer', 'officerID', data[4].cget("text").split(': ')[1],
                                      data[6].cget("text").split(': ')[1]]

                    stats, msg = fl.rem_from_server(label_data[2])
                    stats, msg = db.remove_driver(label_data)
                    confirm.destroy()

                    title = ''
                    desc = msg
                    if stats:
                        title = 'Success!'
                    else:
                        title = 'Failed...'
                    SentsGui.Notification(root, title, desc)

                    # Update Search List
                    self.search_driver([root.margin_width, root.margin_height, self.mar_search], root)

        def edit_driver_menu(self, root, data):
            edit = Toplevel(root)
            filename = 'logo_light_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
            except Exception as e:
                print('Error:', e)
            self.icon = PhotoImage(file=filename)
            edit.iconphoto(False, self.icon)

            width = round(45 / 100 * self.winfo_screenwidth())  # round(67 / 100 * self.winfo_screenwidth())
            height = round(50 / 100 * self.winfo_screenheight())  # round(67 / 100 * self.winfo_screenheight())
            x = round(root.winfo_width() / 2 - width / 2) + root.winfo_x()
            y = round(root.winfo_height() / 2 - height / 2) + root.winfo_y()

            gap = 40
            entry_length = 60

            # edit.title('Edit ' + data[0])
            edit.title('Edit Driver')
            edit.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            edit.grab_set()
            edit.resizable(False, False)

            edit_main_canvas = Canvas(edit, highlightthickness=0, bg=CP[root.theme][5],
                                      width=width, height=height)
            edit_main_canvas.place(x=0, y=0)
            edit_main_canvas.update()

            # self.FONTSIZE_RATIO = 30.87
            font_size = round(self.winfo_screenwidth() / 100)
            margin = [round(0.15 * edit.winfo_width()), round(0.08 * edit.winfo_height())]

            # LAYOUT
            y_coord = 0
            edit_frame = Frame(edit_main_canvas, bg=CP[root.theme][5],
                               width=width - 2 * margin[0], height=height - 2 * margin[1])
            edit_frame.place(x=width, y=height)
            edit_frame.update()

            font_setting = "Calibri " + str(round(font_size * 1))  # round(root.font_size * 0.85) or 15
            edit_label = Label(edit_frame, font=font_setting, text='Edit Driver',
                               bg=CP[root.theme][5], fg=CP[root.theme][1])
            edit_label.place(x=0, y=0)
            edit_label.update()
            y_coord = edit_frame.winfo_height() / 32
            edit_label.place(x=edit_frame.winfo_width() / 2 - edit_label.winfo_width() / 2,
                             y=y_coord)

            edit_type_str = StringVar()
            # pe = str(round(width / 412))
            font_setting = "Calibri " + str(round(font_size * 0.75))
            # ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            self.edit_type_cbox = ttk.Combobox(edit_frame, width=round(entry_length - 2), font=font_setting,
                                               textvariable=edit_type_str, style='pad.TCombobox')

            if data[0] == 'student':
                self.edit_type_cbox['values'] = [
                    'Select...', 'Name', 'Year', 'Hostel', 'Vaccination Status', 'Plate Number', 'Vehicle Type',
                    'Vehicle Brand', 'Vehicle Model', 'Road Tax'
                ]
            elif data[0] == 'staff':
                self.edit_type_cbox['values'] = [
                    'Select...', 'Name', 'Vaccination Status', 'Plate Number', 'Vehicle Type',
                    'Vehicle Brand', 'Vehicle Model', 'Road Tax'
                ]
            elif data[0] == 'officer':
                self.edit_type_cbox['values'] = [
                    'Select...', 'Name', 'Rank', 'Plate Number', 'Vehicle Type',
                    'Vehicle Brand', 'Vehicle Model', 'Road Tax'
                ]
            self.edit_type_cbox['state'] = 'readonly'  # disabled or readonly
            self.edit_type_cbox.current(0)
            y_coord = y_coord + gap * 2
            self.edit_type_cbox.place(x=0, y=y_coord)
            # edit_type_cbox.bind("<<ComboboxSelected>>", lambda event, a=data: edit_type_event(event, a))
            self.edit_type_cbox.after(500, lambda: set_current())

            font_setting = "Calibri " + str(round(font_size * 0.85))
            current_val_label = Label(edit_frame, font=font_setting, text='',
                                      bg=CP[root.theme][5], fg=CP[root.theme][1])
            # current_val_label.place(x=0, y=0)
            # current_val_label.update()
            # y_coord = y_coord + gap + edit_type_cbox.winfo_height()
            # current_val_label.place(x=round(margin[0] / 8), y=y_coord)

            edit_value_label = Label(edit_frame, font=font_setting, text='Value:',
                                     bg=CP[root.theme][5], fg=CP[root.theme][1])
            # edit_value_label.place(x=0, y=0)
            # edit_value_label.update()
            # y_coord = y_coord + round(gap / 2) + current_val_label.winfo_height()
            # edit_value_label.place(x=0, y=y_coord)

            self.edit_value_str = StringVar()
            font_setting = "Calibri " + str(round(font_size * 0.75))
            # ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            edit_value_entry = ttk.Entry(edit_frame, width=round(entry_length), textvariable=self.edit_value_str,
                                         font=font_setting, style='pad.TEntry')
            # edit_value_entry.place(x=0, y=0)
            # edit_value_entry.update()
            # y_coord = y_coord + edit_value_label.winfo_height()
            # edit_value_entry.place(x=0, y=y_coord)

            self.edit_value_cbox = ttk.Combobox(edit_frame, width=round(entry_length - 2), font=font_setting,
                                                textvariable=self.edit_value_str, style='pad.TCombobox')
            self.edit_value_cbox['state'] = 'readonly'
            # edit_value_cbox['values'] = ['Select...']
            # edit_value_cbox.current(0)
            # y_coord = y_coord + edit_value_label.winfo_height()
            # edit_value_cbox.place(x=0, y=y_coord)

            # pc = str(round(self.winfo_width() / 118))
            # ttk.Style().configure('pad.DateEntry', padding=(pc + ' 0 ' + pc + ' 0'))
            edit_value_date = tkcalendar.DateEntry(edit_frame, width=10, selectmode='day', style='pad.DateEntry',
                                                   textvariable=self.edit_value_str, date_pattern='dd/mm/yyyy',
                                                   state='readonly', font=font_setting)

            # BUTTONS
            button_coord = [edit.winfo_width() - margin[0], edit.winfo_height() - margin[1]]
            font_setting = "Calibri " + str(round(font_size * 0.65))  # round(root.font_size * 0.65) or 10
            edit_apply_btn = Button(edit_main_canvas, font=font_setting, text="Apply", width=8,
                                    bg=CP[root.theme][10], fg=CP[root.theme][11],
                                    activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                    command=lambda a=root, b=edit, c=1, d=data: btn_event(a, b, c, d)
                                    )  # command=lambda a=root, b=edit, c=1, d=data: btn_event(a, b, c, d)
            edit_apply_btn.place(x=width, y=height)
            edit_apply_btn.update()
            button_coord[0] = button_coord[0] - edit_apply_btn.winfo_width()
            edit_apply_btn.place(x=button_coord[0],
                                 y=button_coord[1] - edit_apply_btn.winfo_height())
            edit_apply_btn.update()

            edit_cancel_btn = Button(edit_main_canvas, font=font_setting, text="Cancel", width=8,
                                     bg=CP[root.theme][10], fg=CP[root.theme][11],
                                     activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                     command=lambda a=root, b=edit, c=2, d=data: btn_event(a, b, c, d)
                                     )  # command=lambda a=root, b=edit, c=2, d=data: btn_event(a, b, c, d)
            edit_cancel_btn.place(x=width, y=height)
            edit_cancel_btn.update()
            button_coord[0] = button_coord[0] - edit_cancel_btn.winfo_width() - 15
            edit_cancel_btn.place(x=button_coord[0],
                                  y=button_coord[1] - edit_cancel_btn.winfo_height())
            edit_cancel_btn.update()

            edit_ok_btn = Button(edit_main_canvas, font=font_setting, text="Ok", width=8,
                                 bg=CP[root.theme][10], fg=CP[root.theme][11],
                                 activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                 command=lambda a=root, b=edit, c=3, d=data: btn_event(a, b, c, d)
                                 )  # command=lambda a=root, b=edit, c=3, d=data: btn_event(a, b, c, d)
            edit_ok_btn.place(x=width, y=height)
            edit_ok_btn.update()
            button_coord[0] = button_coord[0] - edit_ok_btn.winfo_width() - 15
            edit_ok_btn.place(x=button_coord[0],
                              y=button_coord[1] - edit_ok_btn.winfo_height())
            edit_ok_btn.update()

            # Final Refresh (for clean display)
            self.edit_type_cbox.bind("<<ComboboxSelected>>", lambda event, a=data, b=current_val_label,
                                                                    c=edit_value_label,
                                                                    d=edit_value_entry,
                                                                    e=y_coord: edit_type_event(event, a, b, c, d, e)
                                     # h=[edit_apply_btn, edit_ok_btn]
                                     )
            edit_frame.place(x=margin[0], y=margin[1])

            def btn_event(root, edit, c, data):
                value = self.edit_value_str.get()
                if self.edit_type_cbox.get() == 'Name' or self.edit_type_cbox.get() == 'Plate Number' or \
                        self.edit_type_cbox.get() == 'Vehicle Brand' or self.edit_type_cbox.get() == 'Vehicle Model':
                    value = self.edit_value_str.get().upper()
                elif self.edit_type_cbox.get() == 'Road Tax':
                    print(value)
                    value = datetime.datetime.strptime(self.edit_value_str.get(), '%d/%m/%Y').strftime('%Y-%m-%d')

                if c == 1:
                    print('Apply Changes')
                    if self.edit_value_str.get() != '' and self.edit_value_str.get() != 'Select...' and \
                            self.edit_type_cbox.get() != self.edit_type_cbox['values'][0]:
                        stats, msg = db.edit_driver(data[4].cget('text').split(': ')[1], data[0],
                                                    self.edit_type_cbox.get(), value)
                        title = ''
                        if stats:
                            title = 'Success!'
                        else:
                            title = "Failed..."

                        SentsGui.Notification(root, title, msg)
                elif c == 2:
                    print('Close')
                    # print('Type:', edit_type_cbox.get())
                    edit.destroy()
                    self.search_driver([root.margin_width, root.margin_height, self.mar_search], root)
                elif c == 3:
                    print('Apply and Close')
                    if self.edit_value_str.get() != '' and self.edit_value_str.get() != 'Select...' and \
                            self.edit_type_cbox.get() != self.edit_type_cbox['values'][0]:
                        stats, msg = db.edit_driver(data[4].cget('text').split(': ')[1], data[0],
                                                    self.edit_type_cbox.get(), value)
                        title = ''
                        if stats:
                            title = 'Success!'
                        else:
                            title = "Failed..."

                        SentsGui.Notification(root, title, msg)
                        self.search_driver([root.margin_width, root.margin_height, self.mar_search], root)

                    edit.destroy()

            def edit_type_event(event, data, current_val_label, edit_value_label, edit_value_entry, y_coord):
                index = 0
                self.edit_value_str.set('')
                cbox_list = {
                    'Year': ['Select...', '1', '2', '3', '4', '5'],
                    'Hostel': ['Select...', 'Inside UTeM', 'Outside UTeM'],
                    'Vaccination Status': ['Select...', 'Unvaccinated', 'Partially vaccinated', 'Fully vaccinated'],
                    'Rank': ['Select...', 'Sub-Inspektor', 'Sarjan Mejar', 'Sarjan', 'Koperal', 'Lans Koperal',
                             'Konstabel'],
                    'Vehicle Type': ['Select...', 'Car', 'Bike']
                }

                """
                Pram for Data Structure:
                    Student:
                        [driver[0], driver[1].upper(), name, role, driver_id, year, hostel, vac_stat, plate_num,
                                     veh_type, veh_brand, veh_model, road_tax,
                                     driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn]
                    Staff:
                        [driver[0], driver[1].upper(), name, role, driver_id, vac_stat, plate_num, veh_type,
                                     veh_brand, veh_model, road_tax,
                                     driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn]
                    Officer:
                        [driver[0], driver[1].upper(), name, role, driver_id, rank, plate_num, veh_type, veh_brand,
                                     veh_model, road_tax,
                                     driver_img_tk, driver_img_label, dw_result, driver_img, edit_btn, remove_btn]
                """

                if data[0] == 'student':
                    # edit_type_cbox['values'] = [
                    #     'Select...', 'Name', 'Year', 'Hostel', 'Vaccination Status', 'Plate Number', 'Vehicle Type',
                    #     'Vehicle Brand', 'Vehicle Model', 'Road Tax'
                    # ]
                    name_to_index = {
                        'Name': 2,
                        'Year': 5,
                        'Hostel': 6,
                        'Vaccination Status': 7,
                        'Plate Number': 8,
                        'Vehicle Type': 9,
                        'Vehicle Brand': 10,
                        'Vehicle Model': 11,
                        'Road Tax': 12
                    }
                    index = name_to_index[self.edit_type_cbox.get()]
                elif data[0] == 'staff':
                    # edit_type_cbox['values'] = [
                    #     'Select...', 'Name', 'Vaccination Status', 'Plate Number', 'Vehicle Type',
                    #     'Vehicle Brand', 'Vehicle Model', 'Road Tax'
                    # ]
                    name_to_index = {
                        'Name': 2,
                        'Vaccination Status': 5,
                        'Plate Number': 6,
                        'Vehicle Type': 7,
                        'Vehicle Brand': 8,
                        'Vehicle Model': 9,
                        'Road Tax': 10
                    }
                    index = name_to_index[self.edit_type_cbox.get()]
                elif data[0] == 'officer':
                    # edit_type_cbox['values'] = [
                    #     'Select...', 'Name', 'Rank', 'Plate Number', 'Vehicle Type',
                    #     'Vehicle Brand', 'Vehicle Model', 'Road Tax'
                    # ]
                    name_to_index = {
                        'Name': 2,
                        'Rank': 5,
                        'Plate Number': 6,
                        'Vehicle Type': 7,
                        'Vehicle Brand': 8,
                        'Vehicle Model': 9,
                        'Road Tax': 10
                    }
                    index = name_to_index[self.edit_type_cbox.get()]

                curr_val_str = self.edit_type_cbox.get() + ': ' + data[index].cget('text').split(': ')[1]

                current_val_label.configure(text=curr_val_str)
                y_coord = y_coord + gap + self.edit_type_cbox.winfo_height()
                current_val_label.place(x=round(margin[0] / 8), y=y_coord)

                edit_value_label.place(x=0, y=0)
                edit_value_label.update()
                y_coord_2 = y_coord + round(gap / 2) + current_val_label.winfo_height()
                edit_value_label.place(x=0, y=y_coord_2)

                if self.edit_type_cbox.get() == 'Name' or self.edit_type_cbox.get() == 'Plate Number' or \
                        self.edit_type_cbox.get() == 'Vehicle Brand' or self.edit_type_cbox.get() == 'Vehicle Model':
                    self.edit_value_str.set(self.edit_value_str.get().upper())
                    edit_value_entry.place(x=0, y=0)
                    edit_value_entry.update()
                    y_coord_2 = y_coord_2 + edit_value_label.winfo_height()
                    edit_value_entry.place(x=0, y=y_coord_2)
                    self.edit_value_cbox.place_forget()
                    edit_value_date.place_forget()
                elif self.edit_type_cbox.get() == 'Year' or self.edit_type_cbox.get() == 'Hostel' or \
                        self.edit_type_cbox.get() == 'Vaccination Status' or \
                        self.edit_type_cbox.get() == 'Vehicle Type' or self.edit_type_cbox.get() == 'Rank':
                    self.edit_value_cbox['values'] = cbox_list[self.edit_type_cbox.get()]
                    self.edit_value_cbox.current(0)
                    y_coord_2 = y_coord_2 + edit_value_label.winfo_height()
                    self.edit_value_cbox.place(x=0, y=y_coord_2)
                    edit_value_entry.place_forget()
                    edit_value_date.place_forget()
                elif self.edit_type_cbox.get() == 'Road Tax':
                    y_coord_2 = y_coord_2 + edit_value_label.winfo_height()
                    edit_value_date.set_date(datetime.date.today())
                    edit_value_date.place(x=0, y=y_coord_2)
                    edit_value_entry.place_forget()
                    self.edit_value_cbox.place_forget()

                # button[0].configure(command=lambda a=root, b=edit, c=1, d=data, e=edit_type_cbox.get(),
                #                                    f=edit_value_str.get().lower(): btn_event(a, b, c, d, e, f))
                # button[1].configure(command=lambda a=root, b=edit, c=3, d=data, e=edit_type_cbox.get(),
                #                                    f=edit_value_str.get().lower(): btn_event(a, b, c, d, e, f))

            def set_current():
                self.edit_type_cbox.current(0)

        # Change Theme for ViewDriver
        def change_theme(self, theme):
            self.configure(bg=CP[theme][0])
            self.view_canvas.configure(bg=CP[theme][1])
            self.prev_label.bind("<ButtonPress-1>", func=lambda event, a=1, b=theme: self.on_press(event, a, b))
            self.next_label.bind("<ButtonPress-1>", func=lambda event, a=2, b=theme: self.on_press(event, a, b))

            for page in range(1, len(self.sub_frame) + 1):
                frame_item_ind = (page - 1) * self.prof_per_frame
                division = math.ceil(len(self.frame_item) / self.prof_per_frame)
                remainder = len(self.frame_item) % self.prof_per_frame
                last_page = False
                # print("PG IND: ", self.page_index, "\tDIV", division)
                if page == division:
                    last_page = True
                else:
                    last_page = False

                for i, frame in enumerate(self.sub_frame[page - 1]):
                    # print(self.frame_item[frame_item_ind])
                    frame.configure(bg=CP[theme][5])

                    if not last_page or (last_page and i < remainder) or remainder == 0:
                        self.frame_item[frame_item_ind + i][2].configure(bg=CP[theme][5], fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][3].configure(bg=CP[theme][5], fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][4].configure(bg=CP[theme][5], fg=CP[theme][1])

                        add_index = 0
                        if self.frame_item[frame_item_ind + i][0] == 'student':
                            self.frame_item[frame_item_ind + i][5].configure(bg=CP[theme][5], fg=CP[theme][1])
                            self.frame_item[frame_item_ind + i][6].configure(bg=CP[theme][5], fg=CP[theme][1])
                            self.frame_item[frame_item_ind + i][7].configure(bg=CP[theme][5], fg=CP[theme][1])
                            add_index = 7
                        elif self.frame_item[frame_item_ind + i][0] == 'staff':
                            self.frame_item[frame_item_ind + i][5].configure(bg=CP[theme][5], fg=CP[theme][1])
                            add_index = 5
                        elif self.frame_item[frame_item_ind + i][0] == 'officer':
                            self.frame_item[frame_item_ind + i][5].configure(bg=CP[theme][5], fg=CP[theme][1])
                            add_index = 5

                        self.frame_item[frame_item_ind + i][add_index + 1].configure(bg=CP[theme][5],
                                                                                     fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][add_index + 2].configure(bg=CP[theme][5],
                                                                                     fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][add_index + 3].configure(bg=CP[theme][5],
                                                                                     fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][add_index + 4].configure(bg=CP[theme][5],
                                                                                     fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][add_index + 5].configure(bg=CP[theme][5],
                                                                                     fg=CP[theme][1])

                        self.frame_item[frame_item_ind + i][add_index + 10].configure(bg=CP[theme][10],
                                                                                      fg=CP[theme][11],
                                                                                      activebackground=CP[theme][13],
                                                                                      activeforeground=CP[theme][14])
                        self.frame_item[frame_item_ind + i][add_index + 11].configure(bg=CP[theme][10],
                                                                                      fg=CP[theme][11],
                                                                                      activebackground=CP[theme][13],
                                                                                      activeforeground=CP[theme][14])

            self.num_pg_label.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.prev_label.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.next_label.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.search_frame.configure(bg=CP[theme][0])
            self.search_btn.configure(bg=CP[theme][5], fg=CP[theme][1], activebackground=CP[theme][8],
                                      activeforeground=CP[theme][9])

    class AddDriver(Frame):
        def __init__(self, root, canvas, theme, main_layout, font_size, margin_width, margin_height, canvas_index):
            super().__init__(master=canvas, width=main_layout[0], height=main_layout[1], bg=CP[theme][0],
                             highlightthickness=0)
            self.place(x=root.winfo_width(), y=root.winfo_height())
            self.update()

            self.plate_img_path = None
            self.driver_img_path = None
            percent = 37
            no_img_driver = Image.new('RGB', (round(percent / 100 * main_layout[1]),
                                              round(percent / 100 * main_layout[1])), color='#171010')
            no_img_plate = Image.new('RGB', (round(percent / 100 * main_layout[1]),
                                             round(percent / 100 * main_layout[1])), color='#171010')
            no_img_driver_text = "No Driver\nImage Uploaded"
            no_img_driver_font = ImageFont.truetype("calibri.ttf", round(font_size * 1.1))
            draw = ImageDraw.Draw(no_img_driver)
            w, h = draw.textsize(no_img_driver_text, font=no_img_driver_font)
            draw.text((round((no_img_driver.width / 2 - w / 2)),
                       round(no_img_driver.height / 2 - h / 2)),
                      no_img_driver_text, "#EEEEEE", font=no_img_driver_font, align=CENTER)
            self.driver_img_tk = ImageTk.PhotoImage(no_img_driver)

            no_img_plate_text = "No Plate Number\nImage Uploaded"
            no_img_plate_font = ImageFont.truetype("calibri.ttf", round(font_size * 1.1))
            draw = ImageDraw.Draw(no_img_plate)
            w, h = draw.textsize(no_img_plate_text, font=no_img_plate_font)
            draw.text((round((no_img_driver.width / 2 - w / 2)),
                       round(no_img_driver.height / 2 - h / 2)),
                      no_img_plate_text, "#EEEEEE", font=no_img_plate_font, align=CENTER)
            self.plate_img_tk = ImageTk.PhotoImage(no_img_plate)

            self.driver_img_label = Label(self, image=self.driver_img_tk, bg=CP[theme][2])
            self.plate_img_label = Label(self, image=self.plate_img_tk, bg=CP[theme][2])

            self.driver_img_label.place(x=0, y=0)
            self.plate_img_label.place(x=0, y=self.winfo_height() / 2)
            self.driver_img_label.update()
            self.plate_img_label.update()

            font_setting = "Calibri " + str(round(font_size * 0.6))
            self.upload_driver_btn = Button(self, text="Upload Image", padx=5, pady=1, font=font_setting,
                                            bg=CP[theme][5], fg=CP[theme][1],
                                            activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                            command=lambda a=0, b=main_layout: self.open_filedialogue(a, b))
            self.upload_plate_btn = Button(self, text="Upload Image", padx=5, pady=1, font=font_setting,
                                           bg=CP[theme][5], fg=CP[theme][1],
                                           activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                           command=lambda a=1, b=main_layout: self.open_filedialogue(a, b))
            self.upload_driver_btn.place(x=canvas.winfo_width(), y=canvas.winfo_height())
            self.upload_plate_btn.place(x=canvas.winfo_width(), y=canvas.winfo_height())
            self.upload_driver_btn.update()
            self.upload_plate_btn.update()
            self.upload_driver_btn.place(x=self.driver_img_label.winfo_width() / 2 -
                                           self.upload_driver_btn.winfo_width() / 2,
                                         y=percent / 100 * main_layout[1] + self.upload_driver_btn.winfo_width() / 6)
            self.upload_plate_btn.place(
                x=self.driver_img_label.winfo_width() / 2 - self.upload_plate_btn.winfo_width() / 2,
                y=(percent + 50) / 100 * main_layout[1] + self.upload_plate_btn.winfo_width() / 6)
            self.upload_driver_btn.update()
            self.upload_plate_btn.update()

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.driver_name_lbl = Label(self, text="Driver Name: ", font=font_setting,
                                         bg=CP[theme][0], fg=CP[theme][1])
            self.driver_role_lbl = Label(self, text="Driver Role: ", font=font_setting,
                                         bg=CP[theme][0], fg=CP[theme][1])
            # Matric Num, Staff ID, Officer ID
            self.driver_id_lbl = Label(self, text="", font=font_setting,
                                       bg=CP[theme][0], fg=CP[theme][1])
            # Other data
            self.driver_year_lbl = Label(self, text="Year: ", font=font_setting,
                                         bg=CP[theme][0], fg=CP[theme][1])
            self.driver_hostel_lbl = Label(self, text="Hostel: ", font=font_setting,
                                           bg=CP[theme][0], fg=CP[theme][1])
            self.driver_rank_lbl = Label(self, text="Rank: ", font=font_setting,
                                         bg=CP[theme][0], fg=CP[theme][1])
            self.driver_vaccine_lbl = Label(self, text="Vaccination Status: ", font=font_setting,
                                            bg=CP[theme][0], fg=CP[theme][1])

            self.veh_type_lbl = Label(self, text="Vehicle Type: ", font=font_setting,
                                      bg=CP[theme][0], fg=CP[theme][1])
            self.veh_plate_lbl = Label(self, text="Vehicle Plate Number: ", font=font_setting,
                                       bg=CP[theme][0], fg=CP[theme][1])
            self.veh_brand_lbl = Label(self, text="Vehicle Brand: ", font=font_setting,
                                       bg=CP[theme][0], fg=CP[theme][1])
            self.veh_model_lbl = Label(self, text="Vehicle Model: ", font=font_setting,
                                       bg=CP[theme][0], fg=CP[theme][1])
            self.veh_roadtax_lbl = Label(self, text="Road Tax Expire Date: ", font=font_setting,
                                         bg=CP[theme][0], fg=CP[theme][1])

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            self.driver_name_str = StringVar()
            self.driver_role_str = StringVar()
            self.driver_id_str = StringVar()
            self.driver_year_str = StringVar()
            self.driver_hostel_str = StringVar()
            self.driver_rank_str = StringVar()
            self.driver_vaccine_str = StringVar()
            self.veh_type_str = StringVar()
            self.veh_plate_str = StringVar()
            self.veh_brand_str = StringVar()
            self.veh_model_str = StringVar()
            self.veh_roadtax_str = StringVar()

            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            entry_length = 75
            self.driver_name_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.driver_name_str,
                                               font=font_setting, style='pad.TEntry')
            entry_length = 30
            # self.driver_role_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.driver_role_str,
            #                                    font=font_setting)
            self.driver_id_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.driver_id_str,
                                             font=font_setting, style='pad.TEntry')
            # self.driver_year_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.driver_year_str,
            #                                    font=font_setting, style='pad.TEntry')
            # self.veh_type_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.veh_type_str,
            #                                 font=font_setting)
            self.veh_plate_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.veh_plate_str,
                                             font=font_setting, style='pad.TEntry')
            self.veh_brand_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.veh_brand_str,
                                             font=font_setting, style='pad.TEntry')
            self.veh_model_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.veh_model_str,
                                             font=font_setting, style='pad.TEntry')
            """
            self.veh_roadtax_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.veh_roadtax_str,
                                               font=font_setting, state='readonly')
            """
            pc = str(round(self.winfo_width() / 118))
            ttk.Style().configure('pad.DateEntry', padding=(pc + ' 0 ' + pc + ' 0'))
            self.veh_roadtax_entry = tkcalendar.DateEntry(self, width=10, selectmode='day', style='pad.DateEntry',
                                                          textvariable=self.veh_roadtax_str, date_pattern='dd/mm/yyyy',
                                                          state='readonly', font=font_setting)
            self.driver_role_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                                 textvariable=self.driver_role_str, style='pad.TCombobox')
            self.driver_role_cbox['values'] = ['Select...', 'Student', 'Staff', 'Officer']
            self.driver_role_cbox['state'] = 'readonly'  # disabled or readonly
            self.driver_role_cbox.current(0)
            self.driver_role_cbox.bind("<<ComboboxSelected>>",
                                       lambda event, a=main_layout: self.driver_role_event(event, a))
            self.driver_role_prev = self.driver_role_cbox.get()

            self.veh_type_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                              textvariable=self.veh_type_str, style='pad.TCombobox')
            self.veh_type_cbox['values'] = ['Select...', 'Car', 'Bike']
            self.veh_type_cbox['state'] = 'readonly'  # disabled or readonly
            self.veh_type_cbox.current(0)

            self.driver_year_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                                 textvariable=self.driver_year_str, style='pad.TCombobox')
            self.driver_year_cbox['values'] = ['Select...', '1', '2', '3', '4', '5']
            self.driver_year_cbox['state'] = 'readonly'  # disabled or readonly
            self.driver_year_cbox.current(0)

            self.driver_hostel_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                                   textvariable=self.driver_hostel_str, style='pad.TCombobox')
            self.driver_hostel_cbox['values'] = ['Select...', 'Inside UTeM', 'Outside UTeM']
            self.driver_hostel_cbox['state'] = 'readonly'  # disabled or readonly
            self.driver_hostel_cbox.current(0)

            self.driver_rank_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                                 textvariable=self.driver_rank_str, style='pad.TCombobox')
            self.driver_rank_cbox['values'] = ['Select...', 'Sub-Inspektor', 'Sarjan Mejar', 'Sarjan', 'Koperal',
                                               'Lans Koperal', 'Konstabel']
            self.driver_rank_cbox['state'] = 'readonly'  # disabled or readonly
            self.driver_rank_cbox.current(0)

            self.driver_vaccine_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                                    textvariable=self.driver_vaccine_str, style='pad.TCombobox')
            self.driver_vaccine_cbox['values'] = ['Select...', 'Unvaccinated', 'Partially vaccinated',
                                                  'Fully vaccinated']
            self.driver_vaccine_cbox['state'] = 'readonly'  # disabled or readonly
            self.driver_vaccine_cbox.current(0)

            self.driver_name_entry.place(x=root.winfo_width(), y=root.winfo_width())
            self.driver_name_entry.update()

            coord = [main_layout[0] / 4 + self.driver_name_entry.winfo_width() / 16,
                     main_layout[1] / 26]

            gap_label_entry = round(main_layout[1] / 19)
            gap_cat = round(main_layout[1] / 7.8)
            self.driver_name_lbl.place(x=coord[0], y=coord[1])
            self.driver_name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.driver_role_lbl.place(x=coord[0], y=coord[1])
            self.driver_role_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)

            x_2 = coord[0] + 3 / 5 * self.driver_name_entry.winfo_width()
            if self.driver_role_cbox.get() == self.driver_role_cbox['values'][1]:
                # print("student")
                self.driver_id_lbl.configure(text="Matric No.: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place(x=x_2, y=coord[1])
                self.driver_year_cbox.place(x=x_2, y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.driver_hostel_lbl.place(x=coord[0], y=coord[1])
                self.driver_hostel_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.driver_vaccine_lbl.place(x=x_2, y=coord[1])
                self.driver_vaccine_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()
            elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][2]:
                # print("staff")
                self.driver_id_lbl.configure(text="Staff ID: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_vaccine_lbl.place(x=x_2, y=coord[1])
                self.driver_vaccine_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()
            elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][3]:
                # print("officer")
                self.driver_id_lbl.configure(text="Officer ID: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_rank_lbl.place(x=x_2, y=coord[1])
                self.driver_rank_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_vaccine_lbl.place_forget()
                self.driver_vaccine_cbox.place_forget()
            else:  # None
                self.driver_id_lbl.place_forget()
                self.driver_id_entry.place_forget()
                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_vaccine_lbl.place_forget()
                self.driver_vaccine_cbox.place_forget()
                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()

            if self.driver_role_cbox.get() != self.driver_role_cbox['values'][0]:
                coord[1] = coord[1] + gap_cat
                temp_coord = coord[1]
                self.veh_type_lbl.place(x=coord[0], y=coord[1])
                self.veh_type_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_brand_lbl.place(x=coord[0], y=coord[1])
                self.veh_brand_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_model_lbl.place(x=coord[0], y=coord[1])
                self.veh_model_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = temp_coord
                coord[0] = coord[0] + 3 / 5 * self.driver_name_entry.winfo_width()
                self.veh_plate_lbl.place(x=coord[0], y=coord[1])
                self.veh_plate_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_roadtax_lbl.place(x=coord[0], y=coord[1])
                self.veh_roadtax_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            else:
                self.veh_type_lbl.place_forget()
                self.veh_type_cbox.place_forget()
                self.veh_plate_lbl.place_forget()
                self.veh_plate_entry.place_forget()
                self.veh_brand_lbl.place_forget()
                self.veh_brand_entry.place_forget()
                self.veh_model_lbl.place_forget()
                self.veh_model_entry.place_forget()
                self.veh_roadtax_lbl.place_forget()
                self.veh_roadtax_entry.place_forget()

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.add_btn = Button(self, text="Save", font=font_setting, padx=15, pady=1,
                                  bg=CP[theme][5], fg=CP[theme][1],
                                  command=lambda a=root: self.save_driver(a))
            self.add_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.add_btn.update()
            self.add_btn.place(x=main_layout[0] - self.add_btn.winfo_width(),
                               y=main_layout[1] - self.add_btn.winfo_height())

            self.clear_btn = Button(self, text="Clear", font=font_setting, padx=15, pady=1,
                                    bg=CP[theme][5], fg=CP[theme][1],
                                    command=lambda a=main_layout, b=font_size: self.clear(a, b))
            self.clear_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.clear_btn.update()
            self.clear_btn.place(x=main_layout[0] - self.clear_btn.winfo_width() - self.add_btn.winfo_width() * 1.5,
                                 y=main_layout[1] - self.clear_btn.winfo_height())

            self.place_forget()

        def update_res(self, root):
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size
            margin_width = root.margin_width
            margin_height = root.margin_height
            main_layout = root.main_layout
            canvas_index = root.canvas_index

            self.configure(width=main_layout[0], height=main_layout[1])
            self.update()

            percent = 37
            if self.driver_img_path:
                img = Image.open(self.driver_img_path)
                percent = 37
                resized_img = img.resize((round(percent / 100 * main_layout[1]), round(percent / 100 * main_layout[1])),
                                         Image.ANTIALIAS)
                self.driver_img_tk = ImageTk.PhotoImage(resized_img)
            else:
                no_img_driver = Image.new('RGB', (round(percent / 100 * main_layout[1]),
                                                  round(percent / 100 * main_layout[1])), color='#171010')
                no_img_driver_text = "No Driver\nImage Uploaded"
                no_img_driver_font = ImageFont.truetype("calibri.ttf", round(font_size * 1.1))
                draw = ImageDraw.Draw(no_img_driver)
                w, h = draw.textsize(no_img_driver_text, font=no_img_driver_font)
                draw.text((round((no_img_driver.width / 2 - w / 2)),
                           round(no_img_driver.height / 2 - h / 2)),
                          no_img_driver_text, "#EEEEEE", font=no_img_driver_font, align=CENTER)
                self.driver_img_tk = ImageTk.PhotoImage(no_img_driver)

            if self.plate_img_path:
                img = Image.open(self.plate_img_path)
                percent = 37
                resized_img = img.resize((round(percent / 100 * main_layout[1]), round(percent / 100 * main_layout[1])),
                                         Image.ANTIALIAS)
                self.plate_img_tk = ImageTk.PhotoImage(resized_img)
            else:
                no_img_plate = Image.new('RGB', (round(percent / 100 * main_layout[1]),
                                                 round(percent / 100 * main_layout[1])), color='#171010')
                no_img_plate_text = "No Plate Number\nImage Uploaded"
                no_img_plate_font = ImageFont.truetype("calibri.ttf", round(font_size * 1.1))
                draw = ImageDraw.Draw(no_img_plate)
                w, h = draw.textsize(no_img_plate_text, font=no_img_plate_font)
                draw.text((round((no_img_plate.width / 2 - w / 2)),
                           round(no_img_plate.height / 2 - h / 2)),
                          no_img_plate_text, "#EEEEEE", font=no_img_plate_font, align=CENTER)
                self.plate_img_tk = ImageTk.PhotoImage(no_img_plate)

            self.driver_img_label.configure(image=self.driver_img_tk)
            self.plate_img_label.configure(image=self.plate_img_tk)

            self.driver_img_label.place(x=0, y=0)
            self.plate_img_label.place(x=0, y=self.winfo_height() / 2)
            self.driver_img_label.update()
            self.plate_img_label.update()

            font_setting = "Calibri " + str(round(font_size * 0.6))
            self.upload_driver_btn.configure(font=font_setting,
                                             command=lambda a=0, b=main_layout: self.open_filedialogue(a, b))
            self.upload_plate_btn.configure(font=font_setting,
                                            command=lambda a=1, b=main_layout: self.open_filedialogue(a, b))
            self.upload_driver_btn.place(x=width, y=height)
            self.upload_plate_btn.place(x=width, y=height)
            self.upload_driver_btn.update()
            self.upload_plate_btn.update()
            self.upload_driver_btn.place(x=self.driver_img_label.winfo_width() / 2 -
                                           self.upload_driver_btn.winfo_width() / 2,
                                         y=percent / 100 * main_layout[1] + self.upload_driver_btn.winfo_width() / 6)
            self.upload_plate_btn.place(
                x=self.driver_img_label.winfo_width() / 2 - self.upload_plate_btn.winfo_width() / 2,
                y=(percent + 50) / 100 * main_layout[1] + self.upload_plate_btn.winfo_width() / 6)
            self.upload_driver_btn.update()
            self.upload_plate_btn.update()

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.driver_name_lbl.configure(font=font_setting)
            self.driver_role_lbl.configure(font=font_setting)
            self.driver_id_lbl.configure(font=font_setting)
            self.driver_year_lbl.configure(font=font_setting)
            self.driver_hostel_lbl.configure(font=font_setting)
            self.driver_rank_lbl.configure(font=font_setting)
            self.driver_vaccine_lbl.configure(font=font_setting)
            self.veh_type_lbl.configure(font=font_setting)
            self.veh_plate_lbl.configure(font=font_setting)
            self.veh_brand_lbl.configure(font=font_setting)
            self.veh_model_lbl.configure(font=font_setting)
            self.veh_roadtax_lbl.configure(font=font_setting)

            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            entry_length = 75
            self.driver_name_entry.configure(width=round(entry_length), font=font_setting, style='pad.TEntry')
            entry_length = 30
            self.driver_role_cbox.configure(width=round(entry_length - 2), font=font_setting, style='pad.TCombobox')
            self.driver_id_entry.configure(width=round(entry_length), font=font_setting, style='pad.TEntry')
            self.driver_year_cbox.configure(width=round(entry_length - 2), font=font_setting, style='pad.TCombobox')
            self.driver_hostel_cbox.configure(width=round(entry_length - 2), font=font_setting, style='pad.TCombobox')
            self.driver_rank_cbox.configure(width=round(entry_length - 2), font=font_setting, style='pad.TCombobox')
            self.driver_vaccine_cbox.configure(width=round(entry_length - 2), font=font_setting, style='pad.TCombobox')
            self.veh_type_cbox.configure(width=round(entry_length - 2), font=font_setting, style='pad.TCombobox')
            self.veh_plate_entry.configure(width=round(entry_length), font=font_setting, style='pad.TEntry')
            self.veh_brand_entry.configure(width=round(entry_length), font=font_setting, style='pad.TEntry')
            self.veh_model_entry.configure(width=round(entry_length), font=font_setting, style='pad.TEntry')
            pc = str(round(self.winfo_width() / 118))
            ttk.Style().configure('pad.DateEntry', padding=(pc + ' 0 ' + pc + ' 0'))
            self.veh_roadtax_entry.configure(width=10, font=font_setting, style='pad.DateEntry')

            font_cbox = "Calibri " + str(round(font_size * 0.7))
            # self.option_add('*TCombobox*Listbox.font', font_cbox)
            self.driver_role_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
                                          format(self.driver_role_cbox, font_cbox))
            self.veh_type_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
                                       format(self.veh_type_cbox, font_cbox))

            self.update()
            coord = [main_layout[0] / 4 + self.driver_name_entry.winfo_width() / 16,
                     main_layout[1] / 26]
            gap_label_entry = round(main_layout[1] / 19)
            gap_cat = round(main_layout[1] / 7.8)
            self.driver_name_lbl.place(x=coord[0], y=coord[1])
            self.driver_name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.driver_role_lbl.place(x=coord[0], y=coord[1])
            self.driver_role_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)

            x_2 = coord[0] + 3 / 5 * self.driver_name_entry.winfo_width()
            if self.driver_role_cbox.get() == self.driver_role_cbox['values'][1]:
                # print("student")
                self.driver_id_lbl.configure(text="Matric No.: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place(x=x_2, y=coord[1])
                self.driver_year_cbox.place(x=x_2, y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.driver_hostel_lbl.place(x=coord[0], y=coord[1])
                self.driver_hostel_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.driver_vaccine_lbl.place(x=x_2, y=coord[1])
                self.driver_vaccine_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()
            elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][2]:
                # print("staff")
                self.driver_id_lbl.configure(text="Staff ID: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_vaccine_lbl.place(x=x_2, y=coord[1])
                self.driver_vaccine_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()
            elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][3]:
                # print("officer")
                self.driver_id_lbl.configure(text="Officer ID: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_rank_lbl.place(x=x_2, y=coord[1])
                self.driver_rank_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_vaccine_lbl.place_forget()
                self.driver_vaccine_cbox.place_forget()
            else:  # None
                self.driver_id_lbl.place_forget()
                self.driver_id_entry.place_forget()
                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_vaccine_lbl.place_forget()
                self.driver_vaccine_cbox.place_forget()
                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()

            if self.driver_role_cbox.get() != self.driver_role_cbox['values'][0]:
                coord[1] = coord[1] + gap_cat
                temp_coord = coord[1]
                self.veh_type_lbl.place(x=coord[0], y=coord[1])
                self.veh_type_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_brand_lbl.place(x=coord[0], y=coord[1])
                self.veh_brand_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_model_lbl.place(x=coord[0], y=coord[1])
                self.veh_model_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = temp_coord
                coord[0] = coord[0] + 3 / 5 * self.driver_name_entry.winfo_width()
                self.veh_plate_lbl.place(x=coord[0], y=coord[1])
                self.veh_plate_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_roadtax_lbl.place(x=coord[0], y=coord[1])
                self.veh_roadtax_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            else:
                self.veh_type_lbl.place_forget()
                self.veh_type_cbox.place_forget()
                self.veh_plate_lbl.place_forget()
                self.veh_plate_entry.place_forget()
                self.veh_brand_lbl.place_forget()
                self.veh_brand_entry.place_forget()
                self.veh_model_lbl.place_forget()
                self.veh_model_entry.place_forget()
                self.veh_roadtax_lbl.place_forget()
                self.veh_roadtax_entry.place_forget()

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.add_btn.configure(font=font_setting)
            self.add_btn.place(x=width, y=height)
            self.add_btn.update()
            self.add_btn.place(x=main_layout[0] - self.add_btn.winfo_width(),
                               y=main_layout[1] - self.add_btn.winfo_height())

            self.clear_btn.configure(font=font_setting, command=lambda a=main_layout, b=font_size: self.clear(a, b))
            self.clear_btn.place(x=width, y=height)
            self.clear_btn.update()
            self.clear_btn.place(x=main_layout[0] - self.clear_btn.winfo_width() - self.add_btn.winfo_width() * 1.5,
                                 y=main_layout[1] - self.clear_btn.winfo_height())
            self.driver_role_cbox.bind("<<ComboboxSelected>>",
                                       lambda event, a=main_layout: self.driver_role_event(event, a))

            self.update()

        def open_filedialogue(self, type, main_layout):
            """
            path = filedialog.askopenfilename(title="Select Image", filetypes=(("PNG", "*.png"),
                                                                               ("JPEG", "*.jpg; *.jpeg; *.jpe; "
                                                                                        "*.jfif; *.exif"),
                                                                                ("all files", "*.*")))
            """
            path = filedialog.askopenfilename(title="Select Image",
                                              filetypes=[("Image File", "*.png; *.jpg; *.jpeg; *.jpe; *.jfif; *.exif")])
            if path:
                img = Image.open(path)
                percent = 37
                resized_img = img.resize((round(percent / 100 * main_layout[1]), round(percent / 100 * main_layout[1])),
                                         Image.ANTIALIAS)
                if type == 0:
                    self.driver_img_path = path
                    self.driver_img_tk = ImageTk.PhotoImage(resized_img)
                    self.driver_img_label.configure(image=self.driver_img_tk)
                    self.driver_img_label.place(x=0, y=0)
                elif type == 1:
                    self.plate_img_path = path
                    self.plate_img_tk = ImageTk.PhotoImage(resized_img)
                    self.plate_img_label.configure(image=self.plate_img_tk)
                    self.plate_img_label.place(x=0, y=self.winfo_height() / 2)

        def clear(self, main_layout, font_size):
            self.veh_roadtax_entry.set_date(datetime.date.today())
            self.driver_name_str.set("")
            self.driver_role_cbox.current(0)
            self.driver_id_str.set("")
            self.driver_year_cbox.current(0)
            self.driver_hostel_cbox.current(0)
            self.driver_rank_cbox.current(0)
            self.driver_vaccine_cbox.current(0)
            self.veh_type_cbox.current(0)
            self.veh_plate_str.set("")
            self.veh_brand_str.set("")
            self.veh_model_str.set("")
            self.veh_roadtax_entry.set_date(datetime.date.today())

            self.driver_img_path = None
            self.plate_img_path = None

            percent = 37
            no_img_driver = Image.new('RGB', (round(percent / 100 * main_layout[1]),
                                              round(percent / 100 * main_layout[1])), color='#171010')
            no_img_driver_text = "No Driver\nImage Uploaded"
            no_img_driver_font = ImageFont.truetype("calibri.ttf", round(font_size * 1.1))
            draw = ImageDraw.Draw(no_img_driver)
            w, h = draw.textsize(no_img_driver_text, font=no_img_driver_font)
            draw.text((round((no_img_driver.width / 2 - w / 2)),
                       round(no_img_driver.height / 2 - h / 2)),
                      no_img_driver_text, "#EEEEEE", font=no_img_driver_font, align=CENTER)
            self.driver_img_tk = ImageTk.PhotoImage(no_img_driver)

            no_img_plate = Image.new('RGB', (round(percent / 100 * main_layout[1]),
                                             round(percent / 100 * main_layout[1])), color='#171010')
            no_img_plate_text = "No Plate Number\nImage Uploaded"
            no_img_plate_font = ImageFont.truetype("calibri.ttf", round(font_size * 1.1))
            draw = ImageDraw.Draw(no_img_plate)
            w, h = draw.textsize(no_img_plate_text, font=no_img_plate_font)
            draw.text((round((no_img_plate.width / 2 - w / 2)),
                       round(no_img_plate.height / 2 - h / 2)),
                      no_img_plate_text, "#EEEEEE", font=no_img_plate_font, align=CENTER)
            self.plate_img_tk = ImageTk.PhotoImage(no_img_plate)

            self.driver_img_label.configure(image=self.driver_img_tk)
            self.plate_img_label.configure(image=self.plate_img_tk)
            self.driver_img_label.update()
            self.plate_img_label.update()

            self.driver_role_event(None, main_layout)

        def save_driver(self, root):
            """
            # Input
                self.driver_name_str = StringVar()
                self.driver_role_str = StringVar()
                self.driver_id_str = StringVar()
                self.driver_year_str = StringVar()
                self.driver_hostel_str = StringVar()
                self.driver_rank_str = StringVar()
                self.driver_vaccine_str = StringVar()
                self.veh_type_str = StringVar()
                self.veh_plate_str = StringVar()
                self.veh_brand_str = StringVar()
                self.veh_model_str = StringVar()
                self.veh_roadtax_str = StringVar()
                self.plate_img_path
                self.driver_img_path
            """
            # Database Connection
            if self.driver_name_str.get() and self.driver_role_cbox.get() != self.driver_role_cbox['values'][0] and \
                    self.driver_id_str.get() and self.veh_type_cbox.get() != self.veh_type_cbox['values'][0] and \
                    self.veh_plate_str.get() and self.veh_brand_str.get() and \
                    self.veh_model_str.get() and self.veh_roadtax_str.get() and \
                    self.plate_img_path and self.driver_img_path:
                title = "Failed..."
                desc = "Unknown Reason"
                split_driver = self.driver_img_path.split('/')
                split_plate_num = self.plate_img_path.split('/')

                path_driver = ""
                path_plate_num = ""
                for i, each_split in enumerate(split_driver):
                    if i < len(split_driver) - 1:
                        path_driver += each_split + '/'

                for i, each_split in enumerate(split_plate_num):
                    if i < len(split_plate_num) - 1:
                        path_plate_num += each_split + '/'

                file_driver = split_driver[len(split_driver) - 1]
                file_plate_num = split_plate_num[len(split_plate_num) - 1]
                # print(path_driver)
                # print(file_driver)
                # print(path_plate_num)
                # print(file_plate_num)

                if self.driver_role_cbox.get() == self.driver_role_cbox['values'][1] and \
                        self.driver_year_cbox.get() != self.driver_year_cbox['values'][0] and \
                        self.driver_hostel_cbox.get() != self.driver_hostel_cbox['values'][0] and \
                        self.driver_vaccine_cbox.get() != self.driver_vaccine_cbox['values'][0]:
                    # Student
                    print("Save Student")
                    title, desc = db.insert_student(self.driver_id_str.get(), self.driver_name_str.get(),
                                                    self.driver_year_str.get(), self.driver_hostel_str.get(),
                                                    self.driver_vaccine_str.get(), self.veh_plate_str.get(),
                                                    self.veh_type_str.get(), self.veh_brand_str.get(),
                                                    self.veh_model_str.get(), self.veh_roadtax_str.get())
                    if title == 'Success!':
                        if not fl.up_to_server(path_driver, file_driver, self.driver_id_str.get(), 1) or \
                                not fl.up_to_server(path_plate_num, file_plate_num, self.driver_id_str.get(), 2):
                            title = "Failed..."
                            desc = "Failed to Upload Image"
                elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][2] and \
                        self.driver_vaccine_cbox.get() != self.driver_vaccine_cbox['values'][0]:
                    # Staff
                    print("Save Staff")
                    title, desc = db.insert_staff(self.driver_id_str.get(), self.driver_name_str.get(),
                                                  self.driver_vaccine_str.get(), self.veh_plate_str.get(),
                                                  self.veh_type_str.get(), self.veh_brand_str.get(),
                                                  self.veh_model_str.get(), self.veh_roadtax_str.get())
                    if title == 'Success!':
                        if not fl.up_to_server(path_driver, file_driver, self.driver_id_str.get(), 1) or \
                                not fl.up_to_server(path_plate_num, file_plate_num, self.driver_id_str.get(), 2):
                            title = "Failed..."
                            desc = "Failed to Upload Image"
                elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][3] and \
                        self.driver_rank_cbox.get() != self.driver_rank_cbox['values'][0]:
                    # Officer
                    print("Save Officer")
                    print(self.driver_rank_str.get())
                    title, desc = db.insert_officer(self.driver_id_str.get(), self.driver_name_str.get(),
                                                    rank=self.driver_rank_str.get(),
                                                    plate_num=self.veh_plate_str.get(),
                                                    veh_type=self.veh_type_str.get(),
                                                    veh_brand=self.veh_brand_str.get(),
                                                    veh_model=self.veh_model_str.get(),
                                                    road_tax=self.veh_roadtax_str.get())
                    if title == 'Success!':
                        if not fl.up_to_server(path_driver, file_driver, self.driver_id_str.get(), 1) or \
                                not fl.up_to_server(path_plate_num, file_plate_num, self.driver_id_str.get(), 2):
                            title = "Failed..."
                            desc = "Failed to Upload Image"
                else:
                    print("All Field Must be Filled 2")
                    desc = "All Field Must be Filled"

                SentsGui.Notification(root, title, desc)
            else:
                print("All Field Must be Filled")
                SentsGui.Notification(root, "Failed!", "All Field Must be Filled")

        def driver_role_event(self, event, main_layout):
            similar = None
            if self.driver_role_prev == self.driver_role_cbox.get():
                similar = True
            else:
                similar = False
                self.driver_role_prev = self.driver_role_cbox.get()

            self.update()
            coord = [main_layout[0] / 4 + self.driver_name_entry.winfo_width() / 16,
                     main_layout[1] / 26]
            gap_label_entry = round(main_layout[1] / 19)
            gap_cat = round(main_layout[1] / 7.8)
            self.driver_name_lbl.place(x=coord[0], y=coord[1])
            self.driver_name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.driver_role_lbl.place(x=coord[0], y=coord[1])
            self.driver_role_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)

            x_2 = coord[0] + 3 / 5 * self.driver_name_entry.winfo_width()
            if self.driver_role_cbox.get() == self.driver_role_cbox['values'][1]:
                print("student")
                self.driver_id_lbl.configure(text="Matric No.: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place(x=x_2, y=coord[1])
                self.driver_year_cbox.place(x=x_2, y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.driver_hostel_lbl.place(x=coord[0], y=coord[1])
                self.driver_hostel_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.driver_vaccine_lbl.place(x=x_2, y=coord[1])
                self.driver_vaccine_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()
            elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][2]:
                print("staff")
                self.driver_id_lbl.configure(text="Staff ID: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_vaccine_lbl.place(x=x_2, y=coord[1])
                self.driver_vaccine_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()
            elif self.driver_role_cbox.get() == self.driver_role_cbox['values'][3]:
                print("officer")
                self.driver_id_lbl.configure(text="Officer ID: ")
                coord[1] = coord[1] + gap_cat
                self.driver_id_lbl.place(x=coord[0], y=coord[1])
                self.driver_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)

                self.driver_rank_lbl.place(x=x_2, y=coord[1])
                self.driver_rank_cbox.place(x=x_2, y=coord[1] + gap_label_entry)

                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_vaccine_lbl.place_forget()
                self.driver_vaccine_cbox.place_forget()
            else:  # None
                self.driver_id_lbl.place_forget()
                self.driver_id_entry.place_forget()
                self.driver_year_lbl.place_forget()
                self.driver_year_cbox.place_forget()
                self.driver_hostel_lbl.place_forget()
                self.driver_hostel_cbox.place_forget()
                self.driver_vaccine_lbl.place_forget()
                self.driver_vaccine_cbox.place_forget()
                self.driver_rank_lbl.place_forget()
                self.driver_rank_cbox.place_forget()

            if self.driver_role_cbox.get() != self.driver_role_cbox['values'][0]:
                coord[1] = coord[1] + gap_cat
                temp_coord = coord[1]
                self.veh_type_lbl.place(x=coord[0], y=coord[1])
                self.veh_type_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_brand_lbl.place(x=coord[0], y=coord[1])
                self.veh_brand_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_model_lbl.place(x=coord[0], y=coord[1])
                self.veh_model_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = temp_coord
                coord[0] = coord[0] + 3 / 5 * self.driver_name_entry.winfo_width()
                self.veh_plate_lbl.place(x=coord[0], y=coord[1])
                self.veh_plate_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                coord[1] = coord[1] + gap_cat
                self.veh_roadtax_lbl.place(x=coord[0], y=coord[1])
                self.veh_roadtax_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            else:
                self.veh_type_lbl.place_forget()
                self.veh_type_cbox.place_forget()
                self.veh_plate_lbl.place_forget()
                self.veh_plate_entry.place_forget()
                self.veh_brand_lbl.place_forget()
                self.veh_brand_entry.place_forget()
                self.veh_model_lbl.place_forget()
                self.veh_model_entry.place_forget()
                self.veh_roadtax_lbl.place_forget()
                self.veh_roadtax_entry.place_forget()

            # Reseting Part
            if not similar:
                self.driver_id_str.set('')
                self.driver_year_cbox.current(0)
                self.driver_hostel_cbox.current(0)
                self.driver_rank_cbox.current(0)
                self.driver_vaccine_cbox.current(0)
                self.veh_plate_str.set('')
                self.veh_type_cbox.current(0)
                self.veh_brand_str.set('')
                self.veh_model_str.set('')
                self.veh_roadtax_entry.set_date(datetime.date.today())

        # Change Theme for AddDriver
        def change_theme(self, theme):
            self.configure(bg=CP[theme][0])

            self.driver_img_label.configure(bg=CP[theme][2])
            self.plate_img_label.configure(bg=CP[theme][2])

            self.upload_driver_btn.configure(bg=CP[theme][5], fg=CP[theme][1],
                                             activebackground=CP[theme][8], activeforeground=CP[theme][9])
            self.upload_plate_btn.configure(bg=CP[theme][5], fg=CP[theme][1],
                                            activebackground=CP[theme][8], activeforeground=CP[theme][9])
            self.driver_name_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.driver_role_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.driver_id_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.driver_year_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.driver_hostel_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.driver_rank_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.driver_vaccine_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.veh_type_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.veh_plate_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.veh_brand_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.veh_model_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.veh_roadtax_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.add_btn.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.clear_btn.configure(bg=CP[theme][5], fg=CP[theme][1])

    class ViewAdmin(Frame):
        def __init__(self, root, canvas, theme, main_layout, font_size, margin_width, margin_height, canvas_index):
            self.mar_search = 0.92
            self.root = root
            self.borderwidth = 1
            self.prof_per_frame = 3
            super().__init__(master=canvas, width=main_layout[0], height=round(self.mar_search * main_layout[1]),
                             bg=CP[theme][0], highlightthickness=0)
            self.place(x=margin_width, y=margin_height + round(0.05 * main_layout[1]))

            """
            self.scroll_view = Scrollbar(self, bg=CP[theme][1], orient="vertical")
            self.scroll_view.pack(side=RIGHT, fill=Y)
            # self.scroll_view.place(x=0, y=0)
            """

            self.view_canvas = Canvas(self, width=main_layout[0], height=round(self.mar_search * main_layout[1]),
                                      bg=CP[theme][1], highlightthickness=0)
            self.view_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            # self.view_canvas.configure(yscrollcommand=self.scroll_view.set)
            # self.scroll_view.configure(command=self.view_canvas.yview)

            self.admin_list = []
            self.sub_frame = []
            self.canvas_item = []
            self.page_index = 0
            self.frame_item = []

            font_setting = "Calibri " + str(round(math.pow(font_size, 1)))
            self.num_pg_label = Label(root, text="1 / 1", font=font_setting, bg=CP[theme][0], fg=CP[theme][1])
            font_setting = "Calibri " + str(round(math.pow(font_size, 1.1))) + " bold"
            self.prev_label = Label(root, text="<", font=font_setting, bg=CP[theme][0], fg=CP[theme][1], padx=10)
            self.next_label = Label(root, text=">", font=font_setting, bg=CP[theme][0], fg=CP[theme][1], padx=10)
            self.num_pg_label.place(x=root.winfo_width(), y=root.winfo_height())
            self.prev_label.place(x=root.winfo_width(), y=root.winfo_height())
            self.next_label.place(x=root.winfo_width(), y=root.winfo_height())
            self.prev_label.bind("<ButtonPress-1>", func=lambda event, a=1, b=theme: self.on_press(event, a, b))
            self.prev_label.bind("<ButtonRelease-1>", func=lambda event, a=1, b=root: self.on_release(event, a, b))
            self.next_label.bind("<ButtonPress-1>", func=lambda event, a=2, b=theme: self.on_press(event, a, b))
            self.next_label.bind("<ButtonRelease-1>", func=lambda event, a=2, b=root: self.on_release(event, a, b))
            self.num_pg_label.update()
            self.prev_label.update()
            self.next_label.update()

            self.num_pg_label.place_forget()
            self.prev_label.place_forget()
            self.next_label.place_forget()

            self.place(x=root.winfo_width(), y=root.winfo_height())
            # self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))
            # self.view_canvas.bind('<Configure>', self.onFrameConfigure)

            self.search_frame = Frame(canvas, width=main_layout[0], height=round(0.08 * main_layout[1]),
                                      bg=CP[theme][0], highlightthickness=0)
            self.search_frame.place(x=margin_width, y=margin_height)

            self.search_str = StringVar()
            self.search_by_str = StringVar()
            self.search_filter_str = StringVar()
            # self.search_sort_str = StringVar()

            font_setting = "Calibri " + str(round(math.pow(font_size, 0.89)))
            # print(font_size, font_size * 0.75)
            pe = str(round(self.winfo_width() / 412))  # 412
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            coord_x = margin_width / 10
            self.search_entry = ttk.Entry(self.search_frame, width=30, textvariable=self.search_str,
                                          font=font_setting, style='pad.TEntry')
            self.search_entry.place(x=coord_x, y=0)
            self.search_entry.update()

            # Default Search By Name
            coord_x = coord_x + self.search_entry.winfo_width() + math.sqrt(margin_width)
            self.search_by_cbox = ttk.Combobox(self.search_frame, width=20, font=font_setting,
                                               textvariable=self.search_by_str, style='pad.TCombobox')
            self.search_by_cbox['values'] = ['Search By...', 'Name', 'Staff ID']
            self.search_by_cbox['state'] = 'readonly'  # disabled or readonly
            self.search_by_cbox.current(0)
            self.search_by_cbox.place(x=coord_x, y=0)
            self.search_by_cbox.update()

            # Default Filter By All
            coord_x = coord_x + self.search_by_cbox.winfo_width() + math.sqrt(margin_width)
            self.search_filter_cbox = ttk.Combobox(self.search_frame, width=10, font=font_setting,
                                                   textvariable=self.search_filter_str, style='pad.TCombobox')
            self.search_filter_cbox['values'] = ['Filter By...', 'All', 'Admin', 'Security']
            self.search_filter_cbox['state'] = 'readonly'  # disabled or readonly
            self.search_filter_cbox.current(0)
            self.search_filter_cbox.place(x=coord_x, y=0)
            self.search_filter_cbox.update()

            # Default Sort By Name Asc.
            # coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(margin_width)
            # self.search_sort_cbox = ttk.Combobox(self.search_frame, width=22, font=font_setting,
            #                                      textvariable=self.search_sort_str, style='pad.TCombobox')
            # self.search_sort_cbox['values'] = ['Sort By...', 'Name Asc.', 'Name Desc.',
            #                                    'Staff ID Asc.', 'Staff ID Desc.']
            # self.search_sort_cbox['state'] = 'readonly'  # disabled or readonly
            # self.search_sort_cbox.current(0)
            # self.search_sort_cbox.place(x=coord_x, y=0)
            # self.search_sort_cbox.update()

            coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(margin_width)
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.85)))
            self.search_btn = Button(self.search_frame, bg=CP[theme][5], fg=CP[theme][1],
                                     activebackground=CP[theme][8], activeforeground=CP[theme][9],
                                     text="Search", font=font_setting, padx=10, pady=1,
                                     command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                                     self.search_admin(a, b))
            self.search_btn.place(x=coord_x + self.search_btn.winfo_width() / 2, y=0)
            self.search_btn.update()

            self.place_forget()
            self.num_pg_label.place_forget()
            self.prev_label.place_forget()
            self.next_label.place_forget()

        def update_res(self, root):
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size
            margin_width = root.margin_width
            margin_height = root.margin_height
            main_layout = root.main_layout
            canvas_index = root.canvas_index

            self.configure(width=main_layout[0], height=round(self.mar_search * main_layout[1]))
            self.view_canvas.configure(width=main_layout[0], height=round(self.mar_search * main_layout[1]))
            if self.admin_list:
                self.place(x=margin_width, y=margin_height + round((1 - self.mar_search) * main_layout[1]))

                font_setting = "Calibri " + str(round(math.pow(font_size, 1)))
                self.num_pg_label.configure(font=font_setting)
                font_setting = "Calibri " + str(round(math.pow(font_size, 1.1))) + " bold"
                self.prev_label.configure(font=font_setting)
                self.next_label.configure(font=font_setting)
                self.num_pg_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.prev_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.next_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.num_pg_label.update()
                self.prev_label.update()
                self.next_label.update()

                self.view_canvas.update()
                y_coord = 0
                GAP = round(0.25 / 100 * root.winfo_width())
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                frame_item_ind = (self.page_index - 1) * self.prof_per_frame
                division = math.ceil(len(self.frame_item) / self.prof_per_frame)
                remainder = len(self.frame_item) % self.prof_per_frame
                last_page = False
                # print("PG IND: ", self.page_index, "\tDIV", division)
                if self.page_index == division:
                    last_page = True
                else:
                    last_page = False
                for i, frame in enumerate(self.sub_frame[self.page_index - 1]):
                    frame.configure(width=self.view_canvas.winfo_width(), height=frame_height)
                    self.view_canvas.coords(self.canvas_item[i], (0, y_coord))
                    y_coord = y_coord + frame_height

                    if not last_page or (last_page and i < remainder) or remainder == 0:
                        print(self.frame_item[frame_item_ind + i])
                        font_setting = "Calibri " + str(round(root.font_size * 0.8))
                        self.frame_item[frame_item_ind + i][0].configure(font=font_setting)

                        font_setting = "Calibri " + str(round(root.font_size * 0.8))
                        self.frame_item[frame_item_ind + i][1].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][2].configure(font=font_setting)

                        self.frame_item[frame_item_ind + i][0].place(x=self.view_canvas.winfo_width(), y=frame_height)
                        self.frame_item[frame_item_ind + i][1].place(x=self.view_canvas.winfo_width(), y=frame_height)
                        self.frame_item[frame_item_ind + i][2].place(x=self.view_canvas.winfo_width(), y=frame_height)
                        self.frame_item[frame_item_ind + i][0].update()
                        self.frame_item[frame_item_ind + i][1].update()
                        self.frame_item[frame_item_ind + i][2].update()

                        coord = [round(20 / 100 * self.view_canvas.winfo_width()), round(18 / 100 * frame_height)]
                        self.frame_item[frame_item_ind + i][0].place(x=coord[0], y=coord[1])
                        coord[1] = coord[1] + self.frame_item[frame_item_ind + i][0].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][1].place(x=coord[0], y=coord[1])
                        y_coord_lbl = coord[1] + self.frame_item[frame_item_ind + i][1].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][2].place(x=coord[0], y=y_coord_lbl)

                        if self.frame_item[frame_item_ind + i][3]:
                            font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                            self.frame_item[frame_item_ind + i][3].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][3].update()
                            self.frame_item[frame_item_ind + i][3].place(
                                x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                    3].winfo_width() - self.borderwidth * 2, y=self.borderwidth)

                        if self.frame_item[frame_item_ind + i][4]:
                            font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                            self.frame_item[frame_item_ind + i][4].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][4].update()
                            self.frame_item[frame_item_ind + i][4].place(
                                x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                    4].winfo_width() - self.borderwidth * 2,
                                y=self.frame_item[frame_item_ind + i][3].winfo_height() * 1.1)

                remainder = (frame_height - (self.borderwidth * 2)) * self.prof_per_frame - \
                            self.view_canvas.winfo_height()
                remainder = remainder + (self.borderwidth * 2 * self.prof_per_frame)
                self.view_canvas.configure(width=main_layout[0],
                                           height=round(self.mar_search * main_layout[1]) + remainder)

                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() - (
                                                margin_height - self.num_pg_label.winfo_height() / 2))
                if self.page_index >= len(self.sub_frame) and len(self.sub_frame) > 1:
                    self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                            self.prev_label.winfo_width() * 1.5,
                                          y=(root.winfo_height() - margin_height) +
                                            (margin_height / 2 - self.next_label.winfo_height() / 2))
                elif self.page_index > len(self.sub_frame) and len(self.sub_frame) <= 1:
                    self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                            self.prev_label.winfo_width() * 1.5,
                                          y=(root.winfo_height() - margin_height) +
                                            (margin_height / 2 - self.next_label.winfo_height() / 2))

                if self.page_index < len(self.sub_frame):
                    self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                            self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                          y=(root.winfo_height() - margin_height) +
                                            (margin_height / 2 - self.next_label.winfo_height() / 2))
            else:
                self.place(x=width, y=height)
                self.num_pg_label.place_forget()
                self.prev_label.place_forget()
                self.next_label.place_forget()

            self.search_frame.configure(width=main_layout[0], height=round(0.08 * main_layout[1]))
            self.search_frame.place(x=margin_width, y=margin_height)

            font_setting = "Calibri " + str(round(math.pow(font_size, 0.89)))
            pe = str(round(self.winfo_width() / 412))  # 412
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            coord_x = margin_width / 10
            self.search_entry.configure(font=font_setting, style='pad.TEntry')
            self.search_entry.place(x=coord_x, y=0)
            self.search_entry.update()

            # Default Search By Name
            coord_x = coord_x + self.search_entry.winfo_width() + math.sqrt(margin_width)
            self.search_by_cbox.configure(font=font_setting, style='pad.TCombobox')
            self.search_by_cbox.place(x=coord_x, y=0)
            self.search_by_cbox.update()

            # Default Filter By All
            coord_x = coord_x + self.search_by_cbox.winfo_width() + math.sqrt(margin_width)
            self.search_filter_cbox.configure(font=font_setting, style='pad.TCombobox')
            self.search_filter_cbox.place(x=coord_x, y=0)
            self.search_filter_cbox.update()

            # Default Sort By Name Asc.
            # coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(margin_width)
            # self.search_sort_cbox.configure(font=font_setting, style='pad.TCombobox')
            # self.search_sort_cbox.place(x=coord_x, y=0)
            # self.search_sort_cbox.update()

            coord_x = coord_x + self.search_filter_cbox.winfo_width() + math.sqrt(margin_width)
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.85)))
            self.search_btn.configure(font=font_setting,
                                      command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                                      self.search_admin(a, b))
            self.search_btn.place(x=coord_x, y=0)
            self.search_btn.update()

            font_setting = "Calibri " + str(round(math.pow(font_size, 0.89)))
            self.search_by_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
                                        format(self.search_by_cbox, font_setting))
            self.search_filter_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
                                            format(self.search_filter_cbox, font_setting))
            # self.search_sort_cbox.tk.eval('[ttk::combobox::PopdownWindow {}].f.l configure -font "{}"'.
            #                               format(self.search_sort_cbox, font_setting))

            # Need to Adjust back After Search
            """
            for frame in self.sub_frame[self.page_index - 1]:
                frame.configure(width=main_layout[0])

            if self.admin_list:
                self.view_canvas.bind_all("<MouseWheel>",
                                          lambda event, a=self, b=[margin_width, margin_height, self.mar_search],
                                          : self.root._on_mousewheel(event, a, b))
            else:
                self.view_canvas.bind_all("<MouseWheel>", self.root._on_mousewheel_pass)
                """

            if not self.admin_list:
                self.place_forget()
                self.num_pg_label.place_forget()
                self.prev_label.place_forget()
                self.next_label.place_forget()
            self.update()

        def search_admin(self, margin, root):
            global CURR_USER
            main_layout = root.main_layout
            theme = root.theme
            self.admin_list.clear()
            print("Search Admin")
            # Test
            """
            if self.search_str.get() == "test":
                self.admin_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            """
            """
            Input
                self.search_str
                self.search_by_str
                self.search_sort_str (Unused)
                self.search_filter_str
            """

            search_by = ""
            if self.search_by_str.get() == self.search_by_cbox['value'][1]:
                search_by = "name"
            elif self.search_by_str.get() == self.search_by_cbox['value'][2]:
                search_by = "id"
            else:
                search_by = "name"

            search_filter = ""
            if self.search_filter_str.get() == self.search_filter_cbox['value'][0]:
                search_filter = 'all'
            else:
                search_filter = self.search_filter_str.get().lower()

            # Database Connection
            self.admin_list = db.search_admin(self.search_str.get(), search_by, search_filter)

            """
            Output
                List of Admin (2D Array)
                [
                [Name, staff id, car plate... so on], 
                [Name, staff id, car plate... so on],
                [Name, staff id, car plate... so on],
                ... so on
                ]
            """

            # Result Search
            if self.admin_list:
                self.page_index = 1
                self.place(x=margin[0], y=margin[1] + round((1 - margin[2]) * self.winfo_height()))
                y_coord = 0
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                # print(self.view_canvas.winfo_height(), frame_height)
                temp_sub_frame = []
                self.canvas_item = []
                self.sub_frame = []
                self.frame_item = []
                GAP = round(0.25 / 100 * root.winfo_width())
                self.view_canvas.delete('all')
                for i, admin in enumerate(self.admin_list):
                    print("\t", admin)
                    each_sub_frame = Frame(self.view_canvas, width=main_layout[0], height=frame_height, bg=CP[theme][5],
                                           highlightthickness=self.borderwidth)

                    # data = (role, staffID, name)
                    font_setting = "Calibri " + str(round(root.font_size * 0.8))
                    name = Label(each_sub_frame, text="Name\t: " + admin[2].upper(), font=font_setting,
                                 bg=CP[root.theme][5],
                                 fg=CP[root.theme][1])

                    font_setting = "Calibri " + str(round(root.font_size * 0.8))
                    role = Label(each_sub_frame, text="Role\t: " + admin[0].upper(), font=font_setting,
                                 bg=CP[root.theme][5],
                                 fg=CP[root.theme][1])
                    admin_id = Label(each_sub_frame, text="ID\t: " + admin[1].upper(), font=font_setting,
                                     bg=CP[root.theme][5],
                                     fg=CP[root.theme][1])

                    if admin[0] == 'staff':
                        admin_id.configure(text="Staff ID\t: " + admin[1].upper())
                    elif admin[0] == 'officer':
                        admin_id.configure(text="Officer ID\t: " + admin[1].upper())

                    role.place(x=self.view_canvas.winfo_width(), y=frame_height)
                    admin_id.place(x=self.view_canvas.winfo_width(), y=frame_height)
                    name.place(x=self.view_canvas.winfo_width(), y=frame_height)
                    role.update()
                    admin_id.update()
                    name.update()

                    coord = [round(20 / 100 * self.view_canvas.winfo_width()), round(18 / 100 * frame_height)]
                    name.place(x=coord[0], y=coord[1])
                    coord[1] = coord[1] + name.winfo_height() + GAP
                    role.place(x=coord[0], y=coord[1])
                    y_coord_lbl = coord[1] + role.winfo_height() + GAP
                    admin_id.place(x=coord[0], y=y_coord_lbl)

                    # if admin[0] == 'staff':
                    #     self.frame_item.append([admin[0], name, role, admin_id])
                    # elif admin[0] == 'officer':
                    #     self.frame_item.append([admin[0], name, role, admin_id])

                    # coord[0] = coord[0] + round(20 / 100 * self.view_canvas.winfo_width())
                    # y_coord_lbl = coord[1]

                    # canvas_item = self.view_canvas.create_window((0, y_coord), window=each_sub_frame, anchor=NW)
                    # self.canvas_item.append(canvas_item)
                    # y_coord = y_coord + frame_height
                    # self.sub_frame.append(each_sub_frame)

                    if i < self.prof_per_frame:
                        canvas_item = self.view_canvas.create_window((0, y_coord), window=each_sub_frame, anchor=NW)
                        self.canvas_item.append(canvas_item)
                    y_coord = y_coord + frame_height

                    each_sub_frame.update()
                    if CURR_USER == 'root' or (CURR_USER != 'root' and admin[0] == 'officer'):
                        font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                        edit_btn = Button(each_sub_frame, bg=CP[theme][10], fg=CP[theme][11],
                                          activebackground=CP[theme][13], activeforeground=CP[theme][14],
                                          text="Edit", font=font_setting,
                                          width=round(0.01 * main_layout[0]), pady=1)
                        remove_btn = Button(each_sub_frame, bg=CP[theme][10], fg=CP[theme][11],
                                            activebackground=CP[theme][13], activeforeground=CP[theme][14],
                                            text="Remove", font=font_setting,
                                            width=round(0.01 * main_layout[0]), pady=1)
                        # command=lambda a=[margin_width, margin_height, self.mar_search], b=root:
                        #                                              self.search_driver(a, b)
                        edit_btn.place(x=0, y=0)
                        remove_btn.place(x=0, y=0)
                        edit_btn.update()
                        remove_btn.update()
                        edit_btn.place(x=each_sub_frame.winfo_width() - edit_btn.winfo_width() - self.borderwidth * 2,
                                       y=self.borderwidth)
                        remove_btn.place(
                            x=each_sub_frame.winfo_width() - remove_btn.winfo_width() - self.borderwidth * 2,
                            y=round(edit_btn.winfo_height() * 1.1) + self.borderwidth)

                    if admin[0] == 'staff':
                        if CURR_USER == 'root':
                            self.frame_item.append([role, admin_id, name, edit_btn, remove_btn])
                            self.frame_item[len(self.frame_item) - 1][3].configure(
                                command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                                self.edit_admin_menu(a, b)
                            )
                            self.frame_item[len(self.frame_item) - 1][4].configure(
                                command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                                self.rem_admin(a, b)
                            )
                        else:
                            self.frame_item.append([role, admin_id, name, None, None])

                    elif admin[0] == 'officer':
                        self.frame_item.append([role, admin_id, name, edit_btn, remove_btn])
                        self.frame_item[len(self.frame_item) - 1][3].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.edit_admin_menu(a, b)
                        )
                        self.frame_item[len(self.frame_item) - 1][4].configure(
                            command=lambda a=root, b=self.frame_item[len(self.frame_item) - 1]:
                            self.rem_admin(a, b)
                        )

                    if i % self.prof_per_frame < self.prof_per_frame - 1:
                        temp_sub_frame.append(each_sub_frame)
                        if i == len(self.admin_list) - 1:
                            remainder = self.prof_per_frame - (i % self.prof_per_frame)

                            for j in range(0, remainder):
                                each_sub_frame = Frame(self.view_canvas, width=self.view_canvas.winfo_width(),
                                                       height=frame_height,
                                                       bg=CP[theme][5], highlightthickness=self.borderwidth)
                                temp_sub_frame.append(each_sub_frame)

                                canvas_item = self.view_canvas.create_window((0, y_coord), window=each_sub_frame,
                                                                             anchor=NW)
                                self.canvas_item.append(canvas_item)
                                y_coord = y_coord + frame_height
                            self.sub_frame.append(temp_sub_frame)
                    else:
                        temp_sub_frame.append(each_sub_frame)
                        self.sub_frame.append(temp_sub_frame)
                        temp_sub_frame = []

                self.configure(width=main_layout[0], height=round(margin[2] * main_layout[1]))
                self.place(x=margin[0], y=margin[1] + round((1 - margin[2]) * main_layout[1]))

                remainder = self.view_canvas.winfo_height() - (frame_height - (self.borderwidth * 2)) * \
                            self.prof_per_frame
                remainder = remainder - (self.borderwidth * 2 * self.prof_per_frame)

                self.view_canvas.configure(width=main_layout[0], height=self.view_canvas.winfo_height() - remainder)
                self.view_canvas.update()
                self.search_frame.configure(width=main_layout[0], height=round(0.08 * main_layout[1]))
                self.search_frame.place(x=margin[0], y=margin[1])
                # self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))

                font_setting = "Calibri " + str(round(math.pow(root.font_size, 1)))
                self.num_pg_label.configure(font=font_setting, text=("1 / " + str(len(self.sub_frame))))
                font_setting = "Calibri " + str(round(math.pow(root.font_size, 1.1))) + " bold"
                self.prev_label.configure(font=font_setting)
                self.next_label.configure(font=font_setting)
                self.num_pg_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.prev_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.next_label.place(x=root.winfo_width(), y=root.winfo_height())
                self.num_pg_label.update()
                self.prev_label.update()
                self.next_label.update()

                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() - (
                                                margin[1] - self.num_pg_label.winfo_height() / 2))
                """self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                        self.prev_label.winfo_width() * 1.5,
                                      y=(root.winfo_height() - margin[1]) +
                                        (margin[1] / 2 - self.next_label.winfo_height() / 2))"""
                if len(self.sub_frame) > 1:
                    self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                            self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                          y=(root.winfo_height() - margin[1]) +
                                            (margin[1] / 2 - self.next_label.winfo_height() / 2))
            else:
                self.place_forget()
                # self.view_canvas.bind_all("<MouseWheel>", self.root._on_mousewheel_pass)
                self.num_pg_label.place_forget()
                self.prev_label.place_forget()
                self.next_label.place_forget()
                print("Empty Search Result")

        # def onFrameConfigure(self, event):
        #     self.view_canvas.configure(scrollregion=self.view_canvas.bbox("all"))

        def rem_admin(self, root, data):
            confirm = Toplevel(root)
            filename = 'logo_light_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
            except Exception as e:
                print('Error:', e)
            self.icon = PhotoImage(file=filename)
            confirm.iconphoto(False, self.icon)

            width = 320
            height = 180
            x = round(root.winfo_width() / 2 - width / 2) + root.winfo_x()
            y = round(root.winfo_height() / 2 - height / 2) + root.winfo_y()
            gap = 50
            entry_length = 20

            confirm.title('Confirmation')
            confirm.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            # self.attributes('-topmost', True)
            confirm.grab_set()
            # self.grab_release()  # After Finish Setting
            confirm.resizable(False, False)

            confirm_main_canvas = Canvas(confirm, highlightthickness=0, bg=CP[root.theme][5],
                                         width=width, height=height)
            confirm_main_canvas.place(x=0, y=0)
            confirm_main_canvas.update()

            confirm_frame = Frame(confirm_main_canvas, bg=CP[root.theme][5])
            font_setting = "Calibri " + str(15)  # round(root.font_size * 0.85)
            confirm_label = Label(confirm_main_canvas, font=font_setting, text='Confirm to Remove?',
                                  bg=CP[root.theme][5], fg=CP[root.theme][1])
            confirm_label.place(x=0, y=0)
            confirm_label.update()
            confirm_label.place(x=width / 2 - confirm_label.winfo_width() / 2,
                                y=height / 4)

            font_setting = "Calibri " + str(10)  # round(root.font_size * 0.65)
            confirm_ok_btn = Button(confirm_main_canvas, font=font_setting, text="Confirm", width=8,
                                    bg=CP[root.theme][10], fg=CP[root.theme][11],
                                    activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                    command=lambda a=root, b=confirm, c=2, d=data: btn_event(a, b, c, d))
            confirm_ok_btn.place(x=width, y=height)
            confirm_ok_btn.update()
            confirm_ok_btn.place(x=width / 2 - confirm_ok_btn.winfo_width() - 10,
                                 y=3 * height / 4 - confirm_ok_btn.winfo_height())
            confirm_ok_btn.update()

            confirm_cancel_btn = Button(confirm_main_canvas, font=font_setting, text="Cancel", width=8,
                                        bg=CP[root.theme][10], fg=CP[root.theme][11],
                                        activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                        command=lambda a=root, b=confirm, c=1, d=data: btn_event(a, b, c, d))
            confirm_cancel_btn.place(x=width, y=height)
            confirm_cancel_btn.update()
            confirm_cancel_btn.place(x=width / 2 + 10,
                                     y=3 * height / 4 - confirm_cancel_btn.winfo_height())
            confirm_cancel_btn.update()

            def btn_event(root, confirm, type, data):
                # type = 2 is originally for port, got taken out
                # print(data)
                # print(data[0].cget('text').split(': ')[1].lower())
                if type == 1:
                    confirm.destroy()
                elif type == 2:
                    label_data = []
                    if data[0].cget('text').split(': ')[1].lower() == 'staff':
                        label_data = ['admin', 'staffID', data[1].cget('text').split(': ')[1].upper(),
                                      data[2].cget('text').split(': ')[1].upper()]
                    elif data[0].cget('text').split(': ')[1].lower() == 'officer':
                        label_data = ['officer', 'officerID', data[1].cget('text').split(': ')[1].upper(),
                                      data[2].cget('text').split(': ')[1].upper()]

                    # print(label_data)
                    stats, msg = db.remove_admin(label_data)
                    confirm.destroy()

                    title = ''
                    desc = msg
                    if stats:
                        title = 'Success!'
                    else:
                        title = 'Failed...'
                    SentsGui.Notification(root, title, desc)

                    # Update Search List
                    self.search_admin([root.margin_width, root.margin_height, self.mar_search], root)

        def edit_admin_menu(self, root, data):
            edit = Toplevel(root)
            filename = 'logo_light_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
            except Exception as e:
                print('Error:', e)
            self.icon = PhotoImage(file=filename)
            edit.iconphoto(False, self.icon)

            width = round(45 / 100 * self.winfo_screenwidth())
            height = round(50 / 100 * self.winfo_screenheight())
            x = round(root.winfo_width() / 2 - width / 2) + root.winfo_x()
            y = round(root.winfo_height() / 2 - height / 2) + root.winfo_y()
            gap = 50
            entry_length = 20

            edit.title('Edit Admin')
            edit.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            # self.attributes('-topmost', True)
            edit.grab_set()
            # self.grab_release()  # After Finish Setting
            edit.resizable(False, False)

            edit_main_canvas = Canvas(edit, highlightthickness=0, bg=CP[root.theme][5],
                                      width=width, height=height)
            edit_main_canvas.place(x=0, y=0)
            edit_main_canvas.update()

            font_size = round(self.winfo_screenwidth() / 100)
            margin = [round(0.1 * edit.winfo_width()), round(0.08 * edit.winfo_height())]

            edit_frame = Frame(edit_main_canvas, bg=CP[root.theme][5], width=width - margin[0] * 2,
                               height=height - margin[1] * 2)
            edit_frame.place(x=width, y=height)
            edit_frame.update()

            font_setting = "Calibri " + str(round(font_size * 1.3))
            title_lbl = Label(edit_frame, text="Edit Admin ", font=font_setting,
                              bg=CP[root.theme][5], fg=CP[root.theme][1])
            title_lbl.place(x=width, y=height)
            title_lbl.update()

            font_setting = "Calibri " + str(round(font_size * 0.85))
            name_lbl = Label(edit_frame, text="Name: ", font=font_setting,
                             bg=CP[root.theme][5], fg=CP[root.theme][1])
            # self.username_lbl = Label(self, text="User Name: ", font=font_setting,
            #                           bg=CP[theme][0], fg=CP[theme][1])
            pass_res_lbl = Label(edit_frame, text="Password", font=font_setting,
                                 bg=CP[root.theme][5], fg=CP[root.theme][1])

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            self.name_str = StringVar()
            # self.username_str = StringVar()

            entry_length = 65
            name_entry = ttk.Entry(edit_frame, width=round(entry_length), textvariable=self.name_str,
                                   font=font_setting, style='pad.TEntry')
            entry_length = 30
            # self.username_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.username_str,
            #                                 font=font_setting, style='pad.TEntry')

            name_entry.place(x=root.winfo_width(), y=root.winfo_width())
            name_entry.update()

            # coord = [main_layout[0] / 2 - self.name_entry.winfo_width() / 2, main_layout[1] / 5]
            coord = [0, 0]

            gap_label_entry = 15
            gap_cat = 50
            title_lbl.place(x=edit_frame.winfo_width() / 2 - title_lbl.winfo_width() / 2, y=coord[1])
            coord[1] = coord[1] + title_lbl.winfo_height() + gap * 1.2
            name_lbl.place(x=coord[0], y=coord[1])
            name_lbl.update()
            coord[1] = coord[1] + name_lbl.winfo_height() + gap_label_entry
            name_entry.place(x=coord[0], y=coord[1])
            name_entry.update()
            y_btn_name = coord[1]
            # coord[1] = coord[1] + gap_cat
            # self.username_lbl.place(x=coord[0], y=coord[1])
            # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            # y_btn_username = coord[1] + gap_label_entry
            coord[1] = coord[1] + name_entry.winfo_height() + gap_cat
            pass_res_lbl.place(x=coord[0], y=coord[1])
            pass_res_lbl.update()
            y_btn_pass = coord[1]
            coord[1] = coord[1] + gap_cat

            font_setting = "Calibri " + str(round(font_size * 0.65))
            name_update_btn = Button(edit_frame, text="Update", font=font_setting, padx=8, pady=1,
                                     bg=CP[root.theme][10], fg=CP[root.theme][11],
                                     command=lambda a=root, b=edit, c=1, d=data: btn_event(a, b, c, d))
            name_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            name_update_btn.update()
            name_update_btn.place(x=coord[0] + name_entry.winfo_width() + margin[0] / 5,
                                  y=y_btn_name + name_entry.winfo_height() / 2 -
                                    name_update_btn.winfo_height() / 2)

            # self.username_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
            #                                   bg=CP[theme][5], fg=CP[theme][1],
            #                                   command=lambda a=2, b=root: self.update_profile(a, b))
            # self.username_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            # self.username_update_btn.update()
            # self.username_update_btn.place(x=coord[0] + self.username_entry.winfo_width() + margin_width / 5,
            #                                y=y_btn_username + self.username_entry.winfo_height() / 2 -
            #                                  self.username_update_btn.winfo_height() / 2)

            pass_res_btn = Button(edit_frame, text="Reset", font=font_setting, padx=8, pady=1,
                                  bg=CP[root.theme][10], fg=CP[root.theme][11],
                                  command=lambda a=root, b=edit, c=2, d=data: btn_event(a, b, c, d))
            pass_res_btn.place(x=root.winfo_width(), y=root.winfo_height())
            pass_res_btn.update()
            pass_res_btn.place(x=coord[0] + pass_res_lbl.winfo_width() + margin[0] / 2,
                               y=y_btn_pass + pass_res_lbl.winfo_height() / 2 -
                                 pass_res_btn.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 0.8))
            close_btn = Button(edit_main_canvas, text="Close", font=font_setting, padx=15, pady=1,
                               bg=CP[root.theme][10], fg=CP[root.theme][11],
                               command=lambda a=root, b=edit, c=3, d=data: btn_event(a, b, c, d))  # , command=
            close_btn.place(x=root.winfo_width(), y=root.winfo_height())
            close_btn.update()
            close_btn.place(x=width - margin[0] - close_btn.winfo_width() * 1.5,
                            y=height - margin[1] - close_btn.winfo_height())

            edit_frame.place(x=margin[0], y=margin[1])

            def btn_event(root, edit, type, data):
                if type == 1 and self.name_str.get().upper():
                    label_data = []
                    if data[0].cget('text').split(': ')[1].lower() == 'staff':
                        label_data = ['admin', 'staffID', 'name', data[1].cget('text').split(': ')[1].upper(),
                                      self.name_str.get().upper()]
                    elif data[0].cget('text').split(': ')[1].lower() == 'officer':
                        label_data = ['officer', 'officerID', 'officerName',
                                      data[1].cget('text').split(': ')[1].upper(),
                                      self.name_str.get().upper()]
                    stat, msg = db.edit_admin(label_data)
                    title = ''
                    if stat:
                        title = 'Success!'
                    else:
                        title = 'Failed...'
                    SentsGui.Notification(root, title, msg)
                elif type == 2:
                    label_data = []
                    if data[0].cget('text').split(': ')[1].lower() == 'staff':
                        label_data = ['admin', 'staffID', 'password', data[1].cget('text').split(': ')[1].upper(),
                                      data[1].cget('text').split(': ')[1].upper()]
                    elif data[0].cget('text').split(': ')[1].lower() == 'officer':
                        label_data = ['officer', 'officerID', 'password', data[1].cget('text').split(': ')[1].upper(),
                                      data[1].cget('text').split(': ')[1].upper()]
                    stat, msg = db.edit_admin(label_data)
                    title = ''
                    if stat:
                        title = 'Success!'
                    else:
                        title = 'Failed...'
                    SentsGui.Notification(root, title, msg)
                elif type == 3:
                    self.search_admin([root.margin_width, root.margin_height, self.mar_search], root)
                    edit.destroy()

        def on_press(self, event, type, theme):
            if type == 1:
                self.prev_label.configure(bg=CP[theme][3])
            elif type == 2:
                self.next_label.configure(bg=CP[theme][3])

        def on_release(self, event, type, root):
            if type == 1:
                self.prev_label.configure(bg=CP[root.theme][0])
                self.page_index = self.page_index - 1

                self.view_canvas.update()
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                y_coord = 0
                self.view_canvas.delete('all')
                self.canvas_item = []
                for frame in self.sub_frame[self.page_index - 1]:
                    frame.configure(width=self.view_canvas.winfo_width(), height=frame_height)
                    canvas_item = self.view_canvas.create_window((0, y_coord), window=frame, anchor=NW)
                    self.canvas_item.append(canvas_item)
                    y_coord = y_coord + frame_height

                self.num_pg_label.configure(text=(str(self.page_index) + " / " + str(len(self.sub_frame))))
                self.num_pg_label.update()
                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() -
                                          (root.margin_height - self.num_pg_label.winfo_height() / 2))

                self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                        self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                      y=(root.winfo_height() - root.margin_height) +
                                        (root.margin_height / 2 - self.next_label.winfo_height() / 2))

                if self.page_index > 1:
                    self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                            self.prev_label.winfo_width() * 1.5,
                                          y=(root.winfo_height() - root.margin_height) +
                                            (root.margin_height / 2 - self.next_label.winfo_height() / 2))
                else:
                    self.prev_label.place_forget()
            elif type == 2:
                self.next_label.configure(bg=CP[root.theme][0])
                self.page_index = self.page_index + 1

                self.view_canvas.update()
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                y_coord = 0
                self.view_canvas.delete('all')
                self.canvas_item = []
                for frame in self.sub_frame[self.page_index - 1]:
                    frame.configure(width=self.view_canvas.winfo_width(), height=frame_height)
                    canvas_item = self.view_canvas.create_window((0, y_coord), window=frame, anchor=NW)
                    self.canvas_item.append(canvas_item)
                    y_coord = y_coord + frame_height

                self.num_pg_label.configure(text=(str(self.page_index) + " / " + str(len(self.sub_frame))))
                self.num_pg_label.update()
                self.num_pg_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2,
                                        y=root.winfo_height() -
                                          (root.margin_height - self.num_pg_label.winfo_height() / 2))

                self.prev_label.place(x=(root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2) -
                                        self.prev_label.winfo_width() * 1.5,
                                      y=(root.winfo_height() - root.margin_height) +
                                        (root.margin_height / 2 - self.next_label.winfo_height() / 2))

                if self.page_index < len(self.sub_frame):
                    self.next_label.place(x=root.winfo_width() / 2 - self.num_pg_label.winfo_width() / 2 +
                                            self.num_pg_label.winfo_width() + self.next_label.winfo_width() / 2,
                                          y=(root.winfo_height() - root.margin_height) +
                                            (root.margin_height / 2 - self.next_label.winfo_height() / 2))
                else:
                    self.next_label.place_forget()

            if 1 <= type <= 2:
                GAP = round(0.25 / 100 * root.winfo_width())
                frame_height = math.floor(self.view_canvas.winfo_height() / self.prof_per_frame)
                frame_item_ind = (self.page_index - 1) * self.prof_per_frame
                division = math.ceil(len(self.frame_item) / self.prof_per_frame)
                remainder = len(self.frame_item) % self.prof_per_frame
                last_page = False
                # print("PG IND: ", self.page_index, "\tDIV", division)
                if self.page_index == division:
                    last_page = True
                else:
                    last_page = False
                for i, frame in enumerate(self.sub_frame[self.page_index - 1]):
                    if not last_page or (last_page and i < remainder) or remainder == 0:
                        font_setting = "Calibri " + str(round(root.font_size * 0.8))
                        self.frame_item[frame_item_ind + i][0].configure(font=font_setting)

                        font_setting = "Calibri " + str(round(root.font_size * 0.8))
                        self.frame_item[frame_item_ind + i][1].configure(font=font_setting)
                        self.frame_item[frame_item_ind + i][2].configure(font=font_setting)

                        self.frame_item[frame_item_ind + i][0].place(x=self.view_canvas.winfo_width(), y=frame_height)
                        self.frame_item[frame_item_ind + i][1].place(x=self.view_canvas.winfo_width(), y=frame_height)
                        self.frame_item[frame_item_ind + i][2].place(x=self.view_canvas.winfo_width(), y=frame_height)
                        self.frame_item[frame_item_ind + i][0].update()
                        self.frame_item[frame_item_ind + i][1].update()
                        self.frame_item[frame_item_ind + i][2].update()

                        coord = [round(20 / 100 * self.view_canvas.winfo_width()), round(18 / 100 * frame_height)]
                        self.frame_item[frame_item_ind + i][0].place(x=coord[0], y=coord[1])
                        coord[1] = coord[1] + self.frame_item[frame_item_ind + i][0].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][1].place(x=coord[0], y=coord[1])
                        y_coord_lbl = coord[1] + self.frame_item[frame_item_ind + i][1].winfo_height() + GAP
                        self.frame_item[frame_item_ind + i][2].place(x=coord[0], y=y_coord_lbl)

                        if self.frame_item[frame_item_ind + i][3]:
                            font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                            self.frame_item[frame_item_ind + i][3].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][3].update()
                            self.frame_item[frame_item_ind + i][3].place(
                                x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                    3].winfo_width() - self.borderwidth * 2, y=self.borderwidth)

                        if self.frame_item[frame_item_ind + i][4]:
                            font_setting = "Calibri " + str(round(root.font_size * 0.7)) + " bold"
                            self.frame_item[frame_item_ind + i][4].configure(font=font_setting)
                            self.frame_item[frame_item_ind + i][4].update()
                            self.frame_item[frame_item_ind + i][4].place(
                                x=frame.winfo_width() - self.frame_item[frame_item_ind + i][
                                    4].winfo_width() - self.borderwidth * 2,
                                y=self.frame_item[frame_item_ind + i][3].winfo_height() * 1.1)

        # Change Theme for ViewAdmin
        def change_theme(self, theme):
            self.configure(bg=CP[theme][0])

            # self.scroll_view.configure(bg=CP[theme][1])
            self.prev_label.bind("<ButtonPress-1>", func=lambda event, a=1, b=theme: self.on_press(event, a, b))
            self.next_label.bind("<ButtonPress-1>", func=lambda event, a=2, b=theme: self.on_press(event, a, b))

            for page in range(1, len(self.sub_frame) + 1):
                frame_item_ind = (page - 1) * self.prof_per_frame
                division = math.ceil(len(self.frame_item) / self.prof_per_frame)
                remainder = len(self.frame_item) % self.prof_per_frame
                last_page = False
                # print("PG IND: ", self.page_index, "\tDIV", division)
                if page == division:
                    last_page = True
                else:
                    last_page = False

                for i, frame in enumerate(self.sub_frame[page - 1]):
                    print(self.frame_item[frame_item_ind])
                    frame.configure(bg=CP[theme][5])

                    if not last_page or (last_page and i < remainder) or remainder == 0:
                        self.frame_item[frame_item_ind + i][0].configure(bg=CP[theme][5], fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][1].configure(bg=CP[theme][5], fg=CP[theme][1])
                        self.frame_item[frame_item_ind + i][2].configure(bg=CP[theme][5], fg=CP[theme][1])

                        if self.frame_item[frame_item_ind + i][3]:
                            self.frame_item[frame_item_ind + i][3].configure(bg=CP[theme][10], fg=CP[theme][11],
                                                                             activebackground=CP[theme][13],
                                                                             activeforeground=CP[theme][14])

                        if self.frame_item[frame_item_ind + i][4]:
                            self.frame_item[frame_item_ind + i][4].configure(bg=CP[theme][10], fg=CP[theme][11],
                                                                             activebackground=CP[theme][13],
                                                                             activeforeground=CP[theme][14])

            self.num_pg_label.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.prev_label.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.next_label.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.view_canvas.configure(bg=CP[theme][1])
            self.search_frame.configure(bg=CP[theme][0])
            self.search_btn.configure(bg=CP[theme][5], fg=CP[theme][1],
                                      activebackground=CP[theme][8], activeforeground=CP[theme][9])

    class AddAdmin(Frame):
        def __init__(self, root, canvas, theme, main_layout, font_size, margin_width, margin_height, canvas_index):
            super().__init__(master=canvas, width=main_layout[0], height=main_layout[1], bg=CP[theme][0],
                             highlightthickness=0)
            self.place(x=root.winfo_width(), y=root.winfo_height())

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.name_lbl = Label(self, text="Name: ", font=font_setting,
                                  bg=CP[theme][0], fg=CP[theme][1])
            self.privilege_lbl = Label(self, text="Job Type: ", font=font_setting,
                                       bg=CP[theme][0], fg=CP[theme][1])
            self.user_id_lbl = Label(self, text="", font=font_setting,
                                     bg=CP[theme][0], fg=CP[theme][1])
            # self.username_lbl = Label(self, text="User Name: ", font=font_setting,
            #                           bg=CP[theme][0], fg=CP[theme][1])
            font_setting = "Calibri " + str(round(font_size * 0.71))
            self.pass_lbl = Label(self, text="NOTE: Password will be the same as ID", font=font_setting,
                                  bg=CP[theme][0], fg=CP[theme][6])

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            self.name_str = StringVar()
            self.user_id_str = StringVar()
            # self.username_str = StringVar()
            self.privilege_str = StringVar()

            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            entry_length = 75
            self.name_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.name_str,
                                        font=font_setting, style='pad.TEntry')
            pc = str(round(self.winfo_width() / 118))
            self.privilege_cbox = ttk.Combobox(self, width=round(entry_length - 2), font=font_setting,
                                               textvariable=self.privilege_str, style='pad.TCombobox')
            self.privilege_cbox['values'] = ['Select...', 'Security', 'Admin']

            self.privilege_cbox['state'] = 'readonly'  # disabled or readonly
            self.privilege_cbox.current(0)
            self.privilege_prev = self.privilege_cbox.get()
            self.privilege_cbox.bind("<<ComboboxSelected>>",
                                     lambda event, a=main_layout: self.admin_role_event(event, a))
            entry_length = 30
            self.user_id_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.user_id_str,
                                           font=font_setting, style='pad.TEntry')
            # self.username_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.username_str,
            #                                 font=font_setting, style='pad.TEntry')

            self.name_entry.place(x=root.winfo_width(), y=root.winfo_width())
            self.name_entry.update()
            # self.privilege_cbox.place(x=root.winfo_width(), y=root.winfo_width())
            # self.privilege_cbox.update()

            coord = [main_layout[0] / 2 - self.privilege_cbox.winfo_width() / 2,
                     main_layout[1] / 5]

            gap_label_entry = round(main_layout[1] / 21)
            gap_cat = round(main_layout[1] / 7.3)
            self.name_lbl.place(x=coord[0], y=coord[1])
            self.name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.privilege_lbl.place(x=coord[0], y=coord[1])
            self.privilege_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
            if self.privilege_cbox.get() == self.privilege_cbox['values'][0]:
                pass
            elif self.privilege_cbox.get() == self.privilege_cbox['values'][1]:
                self.user_id_lbl.configure(text="Officer ID: ")
                font_setting = "Calibri " + str(round(font_size * 0.71))
                self.pass_lbl.configure(font=font_setting)
                coord[1] = coord[1] + gap_cat
                self.user_id_lbl.place(x=coord[0], y=coord[1])
                self.user_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                # coord[1] = coord[1] + gap_cat
                # self.username_lbl.place(x=coord[0], y=coord[1])
                # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.pass_lbl.place(x=coord[0], y=coord[1] + gap_label_entry * 2)
            elif self.privilege_cbox.get() == self.privilege_cbox['values'][2]:
                self.user_id_lbl.configure(text="Staff ID: ")
                font_setting = "Calibri " + str(round(font_size * 0.71))
                self.pass_lbl.configure(font=font_setting)
                coord[1] = coord[1] + gap_cat
                self.user_id_lbl.place(x=coord[0], y=coord[1])
                self.user_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                # coord[1] = coord[1] + gap_cat
                # self.username_lbl.place(x=coord[0], y=coord[1])
                # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.pass_lbl.place(x=coord[0], y=coord[1] + gap_label_entry * 2)

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.add_btn = Button(self, text="Save", font=font_setting, padx=15, pady=1,
                                  bg=CP[theme][5], fg=CP[theme][1], command=lambda a=root: self.save_admin(a))
            self.add_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.add_btn.update()
            self.add_btn.place(x=main_layout[0] - self.add_btn.winfo_width(),
                               y=main_layout[1] - self.add_btn.winfo_height())

            self.clear_btn = Button(self, text="Clear", font=font_setting, padx=15, pady=1,
                                    bg=CP[theme][5], fg=CP[theme][1],
                                    command=lambda a=main_layout: self.clear(a))
            self.clear_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.clear_btn.update()
            self.clear_btn.place(x=main_layout[0] - self.clear_btn.winfo_width() - self.add_btn.winfo_width() * 1.5,
                                 y=main_layout[1] - self.clear_btn.winfo_height())

            self.place_forget()

        def update_res(self, root):
            global PRIVILEGE
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size
            margin_width = root.margin_width
            margin_height = root.margin_height
            main_layout = root.main_layout
            canvas_index = root.canvas_index

            self.configure(width=main_layout[0], height=main_layout[1])

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.name_lbl.configure(font=font_setting)
            self.user_id_lbl.configure(font=font_setting)
            # self.username_lbl.configure(font=font_setting)
            self.privilege_lbl.configure(font=font_setting)

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            ttk.Style().configure('pad.TCombobox', padding=(pe + ' 1 ' + pe + ' 1'))
            entry_length = 75
            self.name_entry.configure(font=font_setting, style='pad.TEntry')
            entry_length = 30
            self.user_id_entry.configure(font=font_setting, style='pad.TEntry')
            # self.username_entry.configure(font=font_setting, style='pad.TEntry')
            pc = str(round(self.winfo_width() / 118))
            self.privilege_cbox.configure(font=font_setting, style='pad.TCombobox')
            print('Privilege:', PRIVILEGE)
            if PRIVILEGE == 'root':
                self.privilege_cbox['values'] = ['Select...', 'Security', 'Admin']
            else:
                self.privilege_cbox['values'] = ['Select...', 'Security']

            self.name_entry.place(x=width, y=height)
            self.name_entry.update()
            # self.privilege_cbox.place(x=width, y=height)
            # self.privilege_cbox.update()

            self.update()
            coord = [main_layout[0] / 2 - self.privilege_cbox.winfo_width() / 2,
                     main_layout[1] / 5]

            gap_label_entry = round(main_layout[1] / 21)
            gap_cat = round(main_layout[1] / 7.3)
            self.name_lbl.place(x=coord[0], y=coord[1])
            self.name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.privilege_lbl.place(x=coord[0], y=coord[1])
            self.privilege_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)
            if self.privilege_cbox.get() == self.privilege_cbox['values'][0]:
                pass
            elif self.privilege_cbox.get() == self.privilege_cbox['values'][1]:
                self.user_id_lbl.configure(text="Officer ID: ")
                font_setting = "Calibri " + str(round(font_size * 0.71))
                self.pass_lbl.configure(font=font_setting)
                coord[1] = coord[1] + gap_cat
                self.user_id_lbl.place(x=coord[0], y=coord[1])
                self.user_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                # coord[1] = coord[1] + gap_cat
                # self.username_lbl.place(x=coord[0], y=coord[1])
                # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.pass_lbl.place(x=coord[0], y=coord[1] + gap_label_entry * 2)
            elif self.privilege_cbox.get() == self.privilege_cbox['values'][2]:
                self.user_id_lbl.configure(text="Staff ID: ")
                font_setting = "Calibri " + str(round(font_size * 0.71))
                self.pass_lbl.configure(font=font_setting)
                coord[1] = coord[1] + gap_cat
                self.user_id_lbl.place(x=coord[0], y=coord[1])
                self.user_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                # coord[1] = coord[1] + gap_cat
                # self.username_lbl.place(x=coord[0], y=coord[1])
                # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.pass_lbl.place(x=coord[0], y=coord[1] + gap_label_entry * 2)

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.add_btn.configure(font=font_setting)
            self.add_btn.place(x=width, y=height)
            self.add_btn.update()
            self.add_btn.place(x=main_layout[0] - self.add_btn.winfo_width(),
                               y=main_layout[1] - self.add_btn.winfo_height())

            self.clear_btn.configure(font=font_setting)
            self.clear_btn.place(x=width, y=height)
            self.clear_btn.update()
            self.clear_btn.place(x=main_layout[0] - self.clear_btn.winfo_width() - self.add_btn.winfo_width() * 1.5,
                                 y=main_layout[1] - self.clear_btn.winfo_height())

            self.privilege_cbox.bind("<<ComboboxSelected>>",
                                     lambda event, a=main_layout: self.admin_role_event(event, a))

            self.update()

        def clear(self, main_layout):
            self.name_str.set("")
            # self.username_str.set("")
            self.user_id_str.set("")
            self.privilege_cbox.current(0)
            self.admin_role_event(None, main_layout)

        def save_admin(self, root):
            # self.name_str.get() and
            # self.username_str.get() and
            if self.name_str.get() and self.user_id_str.get() and self.privilege_str.get() != \
                    self.privilege_cbox['values'][0]:
                """
                # Input
                    self.user_id_str.get()
                    # self.username_str.get()
                    self.privilege_str.get()
                """

                print("Save")
                # Database Connection
                title = "Failed..."
                desc = "Reason Unknown"
                if self.privilege_str.get() == self.privilege_cbox['values'][1]:
                    title, desc = db.insert_officer(self.user_id_str.get(), self.name_str.get(),
                                                    password=self.user_id_str.get().upper())
                elif self.privilege_str.get() == self.privilege_cbox['values'][2]:
                    title, desc = db.insert_admin(self.name_str.get(), self.user_id_str.get(),
                                                  password=self.user_id_str.get().upper())

                SentsGui.Notification(root, title, desc)
            else:
                print("All Field Must be Filled")
                SentsGui.Notification(root, "Failed!", "All Field Must be Filled")

        def admin_role_event(self, event, main_layout):
            similar = None
            if self.privilege_prev == self.privilege_cbox.get():
                similar = True
            else:
                similar = False
                self.privilege_prev = self.privilege_cbox.get()

            # Clear Entry
            if not similar:
                self.user_id_str.set('')
                # self.username_str.set('')

            # Resize
            self.update()
            coord = [main_layout[0] / 2 - self.privilege_cbox.winfo_width() / 2,
                     main_layout[1] / 5]

            gap_label_entry = round(main_layout[1] / 21)
            gap_cat = round(main_layout[1] / 7.3)
            self.name_lbl.place(x=coord[0], y=coord[1])
            self.name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.privilege_lbl.place(x=coord[0], y=coord[1])
            self.privilege_cbox.place(x=coord[0], y=coord[1] + gap_label_entry)

            if self.privilege_cbox.get() == self.privilege_cbox['values'][0]:
                self.user_id_lbl.place_forget()
                self.user_id_entry.place_forget()
                # self.username_lbl.place_forget()
                # self.username_entry.place_forget()
                self.pass_lbl.place_forget()
            elif self.privilege_cbox.get() == self.privilege_cbox['values'][1]:
                self.user_id_lbl.configure(text="Officer ID: ")
                coord[1] = coord[1] + gap_cat
                self.user_id_lbl.place(x=coord[0], y=coord[1])
                self.user_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                # coord[1] = coord[1] + gap_cat
                # self.username_lbl.place(x=coord[0], y=coord[1])
                # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.pass_lbl.place(x=coord[0], y=coord[1] + gap_label_entry * 2)
            elif self.privilege_cbox.get() == self.privilege_cbox['values'][2]:
                self.user_id_lbl.configure(text="Staff ID: ")
                coord[1] = coord[1] + gap_cat
                self.user_id_lbl.place(x=coord[0], y=coord[1])
                self.user_id_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                # coord[1] = coord[1] + gap_cat
                # self.username_lbl.place(x=coord[0], y=coord[1])
                # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
                self.pass_lbl.place(x=coord[0], y=coord[1] + gap_label_entry * 2)

        # Change Theme for AddAdmin
        def change_theme(self, theme):
            self.configure(bg=CP[theme][0])
            self.name_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.privilege_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.user_id_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            # self.username_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.pass_lbl.configure(bg=CP[theme][0], fg=CP[theme][6])
            self.add_btn.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.clear_btn.configure(bg=CP[theme][5], fg=CP[theme][1])

    class ProfileAdmin(Frame):
        def __init__(self, root, canvas, theme, main_layout, font_size, margin_width, margin_height, canvas_index):
            super().__init__(master=canvas, width=main_layout[0], height=main_layout[1], bg=CP[theme][0],
                             highlightthickness=0)
            self.place(x=root.winfo_width(), y=root.winfo_height())
            self.place(x=margin_width, y=margin_height)

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.name_lbl = Label(self, text="Name: ", font=font_setting,
                                  bg=CP[theme][0], fg=CP[theme][1])
            # self.username_lbl = Label(self, text="User Name: ", font=font_setting,
            #                           bg=CP[theme][0], fg=CP[theme][1])
            self.new_pass_lbl = Label(self, text="New Password: ", font=font_setting,
                                      bg=CP[theme][0], fg=CP[theme][1])
            self.conf_pass_lbl = Label(self, text="Confirm Password: ", font=font_setting,
                                       bg=CP[theme][0], fg=CP[theme][1])

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            self.name_str = StringVar()
            # self.username_str = StringVar()
            self.new_pass_str = StringVar()
            self.conf_pass_str = StringVar()

            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            entry_length = 75
            self.name_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.name_str,
                                        font=font_setting, style='pad.TEntry')
            entry_length = 30
            # self.username_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.username_str,
            #                                 font=font_setting, style='pad.TEntry')
            self.new_pass_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.new_pass_str,
                                            font=font_setting, style='pad.TEntry', show='*')
            self.conf_pass_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.conf_pass_str,
                                             font=font_setting, style='pad.TEntry', show='*')

            self.name_entry.place(x=root.winfo_width(), y=root.winfo_width())
            self.name_entry.update()

            coord = [main_layout[0] / 2 - self.name_entry.winfo_width() / 2,
                     main_layout[1] / 5]

            gap_label_entry = round(main_layout[1] / 21)
            gap_cat = round(main_layout[1] / 7.3)
            self.name_lbl.place(x=coord[0], y=coord[1])
            self.name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            y_btn_name = coord[1] + gap_label_entry
            # coord[1] = coord[1] + gap_cat
            # self.username_lbl.place(x=coord[0], y=coord[1])
            # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            # y_btn_username = coord[1] + gap_label_entry
            coord[1] = coord[1] + gap_cat
            self.new_pass_lbl.place(x=coord[0], y=coord[1])
            self.new_pass_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.conf_pass_lbl.place(x=coord[0], y=coord[1])
            self.conf_pass_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            y_btn_pass = coord[1] + gap_label_entry

            font_setting = "Calibri " + str(round(font_size * 0.65))
            self.name_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
                                          bg=CP[theme][5], fg=CP[theme][1],
                                          command=lambda a=1, b=root: self.update_profile(a, b))
            self.name_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.name_update_btn.update()
            self.name_update_btn.place(x=coord[0] + self.name_entry.winfo_width() + margin_width / 5,
                                       y=y_btn_name + self.name_entry.winfo_height() / 2 -
                                         self.name_update_btn.winfo_height() / 2)

            # self.username_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
            #                                   bg=CP[theme][5], fg=CP[theme][1],
            #                                   command=lambda a=2, b=root: self.update_profile(a, b))
            # self.username_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            # self.username_update_btn.update()
            # self.username_update_btn.place(x=coord[0] + self.username_entry.winfo_width() + margin_width / 5,
            #                                y=y_btn_username + self.username_entry.winfo_height() / 2 -
            #                                  self.username_update_btn.winfo_height() / 2)

            self.pass_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
                                          bg=CP[theme][5], fg=CP[theme][1],
                                          command=lambda a=3, b=root: self.update_profile(a, b))
            self.pass_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.pass_update_btn.update()
            self.pass_update_btn.place(x=coord[0] + self.conf_pass_entry.winfo_width() + margin_width / 5,
                                       y=y_btn_pass + self.conf_pass_entry.winfo_height() / 2 -
                                         self.pass_update_btn.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.clear_btn = Button(self, text="Clear", font=font_setting, padx=15, pady=1,
                                    bg=CP[theme][5], fg=CP[theme][1], command=self.clear)
            self.clear_btn.place(x=root.winfo_width(), y=root.winfo_height())
            self.clear_btn.update()
            self.clear_btn.place(x=main_layout[0] - self.clear_btn.winfo_width() * 1.5,
                                 y=main_layout[1] - self.clear_btn.winfo_height())

            self.place_forget()

        def update_res(self, root):
            width = root.winfo_width()
            height = root.winfo_height()
            font_size = root.font_size
            margin_width = root.margin_width
            margin_height = root.margin_height
            main_layout = root.main_layout
            canvas_index = root.canvas_index

            self.configure(width=main_layout[0], height=main_layout[1])

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.name_lbl.configure(font=font_setting)
            # self.username_lbl.configure(font=font_setting)
            self.new_pass_lbl.configure(font=font_setting)
            self.conf_pass_lbl.configure(font=font_setting)

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(font_size, 0.87)))
            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            entry_length = 75
            self.name_entry.configure(font=font_setting)
            entry_length = 30
            # self.username_entry.configure(font=font_setting)
            self.new_pass_entry.configure(font=font_setting)
            self.conf_pass_entry.configure(font=font_setting)

            self.name_entry.place(x=width, y=height)
            self.name_entry.update()

            coord = [main_layout[0] / 2 - self.name_entry.winfo_width() / 2,
                     main_layout[1] / 5]

            gap_label_entry = round(main_layout[1] / 21)
            gap_cat = round(main_layout[1] / 7.3)
            self.name_lbl.place(x=coord[0], y=coord[1])
            self.name_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            y_btn_name = coord[1] + gap_label_entry
            # coord[1] = coord[1] + gap_cat
            # self.username_lbl.place(x=coord[0], y=coord[1])
            # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            # y_btn_username = coord[1] + gap_label_entry
            coord[1] = coord[1] + gap_cat
            self.new_pass_lbl.place(x=coord[0], y=coord[1])
            self.new_pass_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            coord[1] = coord[1] + gap_cat
            self.conf_pass_lbl.place(x=coord[0], y=coord[1])
            self.conf_pass_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            y_btn_pass = coord[1] + gap_label_entry

            font_setting = "Calibri " + str(round(font_size * 0.65))
            self.name_update_btn.configure(font=font_setting)
            self.name_update_btn.place(x=width, y=height)
            self.name_update_btn.update()
            self.name_update_btn.place(x=coord[0] + self.name_entry.winfo_width() + margin_width / 5,
                                       y=y_btn_name + self.name_entry.winfo_height() / 2 -
                                         self.name_update_btn.winfo_height() / 2)

            # self.username_update_btn.configure(font=font_setting)
            # self.username_update_btn.place(x=width, y=height)
            # self.username_update_btn.update()
            # self.username_update_btn.place(x=coord[0] + self.username_entry.winfo_width() + margin_width / 5,
            #                                y=y_btn_username + self.username_entry.winfo_height() / 2 -
            #                                  self.username_update_btn.winfo_height() / 2)

            self.pass_update_btn.configure(font=font_setting)
            self.pass_update_btn.place(x=width, y=height)
            self.pass_update_btn.update()
            self.pass_update_btn.place(x=coord[0] + self.conf_pass_entry.winfo_width() + margin_width / 5,
                                       y=y_btn_pass + self.conf_pass_entry.winfo_height() / 2 -
                                         self.pass_update_btn.winfo_height() / 2)

            font_setting = "Calibri " + str(round(font_size * 0.8))
            self.clear_btn.configure(font=font_setting)
            self.clear_btn.place(x=width, y=height)
            self.clear_btn.update()
            self.clear_btn.place(x=main_layout[0] - self.clear_btn.winfo_width() * 1.5,
                                 y=main_layout[1] - self.clear_btn.winfo_height())
            self.update()

        def clear(self):
            self.name_str.set("")
            # self.username_str.set("")
            self.new_pass_str.set("")
            self.conf_pass_str.set("")

        def update_profile(self, type, root):
            global CURR_USER
            if type == 1:
                if self.name_str.get():
                    """
                    # Input
                        self.name_str.get()
                    """
                    stats, msg = db.edit_admin_personal(CURR_USER, 'Staff', 'Name', self.name_str.get().upper())

                    title = ''
                    if stats:
                        title = 'Success!'
                    else:
                        title = 'Failed...'

                    print("Save Name")
                    # Database Connection

                    SentsGui.Notification(root, title, msg)
                else:
                    print("Name Field Must be Filled")
                    SentsGui.Notification(root, "Failed!", "Name Field Must be Filled")
            # elif type == 2:
            #     if self.username_str.get():
            #         """
            #         # Input
            #             self.username_str.get()
            #         """
            #         print("Save Username")
            #         # Database Connection
            #         SentsGui.Notification(root, "Test", "Test")
            #     else:
            #         print("Username Field Must be Filled")
            #         SentsGui.Notification(root, "Failed!", "Username Field Must be Filled")
            elif type == 3:
                if self.new_pass_str.get() and self.new_pass_str.get() == self.conf_pass_str.get():
                    """
                    # Input
                        self.new_pass_str.get()
                        self.conf_pass_str.get()
                    """
                    stats, msg = db.edit_admin_personal(CURR_USER, 'Staff', 'Password', self.conf_pass_str.get())

                    title = ''
                    if stats:
                        title = 'Success!'
                    else:
                        title = 'Failed...'

                    print("Save Password")
                    # Database Connection
                    SentsGui.Notification(root, title, msg)
                elif self.new_pass_str.get():
                    print("New Password and Confirm Password are not Same")
                    SentsGui.Notification(root, "Failed!", "New Password and Confirm Password\nare not Same", 0.78)
                else:
                    print("New Password and Confirm Password Field Must be Filled")
                    SentsGui.Notification(root, "Failed!", "New Password and Confirm Password\nField Must be Filled",
                                          0.78)

        # Change Theme for ProfileAdmin
        def change_theme(self, theme):
            self.configure(bg=CP[theme][0])
            self.name_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            # self.username_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.new_pass_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.conf_pass_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.name_update_btn.configure(bg=CP[theme][5], fg=CP[theme][1])
            # self.username_update_btn.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.pass_update_btn.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.clear_btn.configure(bg=CP[theme][5], fg=CP[theme][1])

    def __init__(self, canvas_index):
        self.theme = 1  # Dark Theme
        self.time = time.time()
        self.canvas_index = canvas_index

        super().__init__()
        # Setting icon of master window
        filename = 'logo_light_mode.png'
        try:
            filename = os.path.join(BASE_PATH, filename)
            print(filename)
        except Exception as e:
            print('Error:', e)
        self.icon = PhotoImage(file=filename)
        self.iconphoto(False, self.icon)

        self.title("UTeM SEntS Admin")
        self.geometry("{}x{}".format(round(67 / 100 * self.winfo_screenwidth()),
                                     round(67 / 100 * self.winfo_screenheight())))
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.update()
        self.curr_width = self.winfo_width()
        self.curr_height = self.winfo_height()
        self.margin_width = round(10 / 100 * self.winfo_width())
        self.margin_height = round(10 / 100 * self.winfo_height())
        self.main_layout = [round(self.winfo_width() - 2 * self.margin_width),
                            round(self.winfo_height() - 2 * self.margin_height)]
        self.ratio = self.main_layout[0] / self.main_layout[1]
        # print(self.curr_width, self.curr_height)

        self.font_style = "Calibri"
        self.font_size = 0
        self.FONTSIZE_RATIO = 30.87
        self.font_size = round(self.main_layout[1] / self.FONTSIZE_RATIO)

        self.s = ttk.Style()
        width_tab = round((self.main_layout[0] / 12.7))  # = 65
        self.s.theme_create("MyStyle", parent="clam", settings={
            "TNotebook": {"configure": {"tabmargins": [3, 1, 0, 0],
                                        "background": CP[self.theme][5],
                                        'borderwidth': 0,
                                        'highlightbackground': CP[self.theme][8],
                                        'highlightcolor': CP[self.theme][9]}},
            "TNotebook.Tab": {"configure": {"padding": [width_tab, 5], "borderwidth": 1,
                                            "font": (self.font_style, str(self.font_size - 2)),
                                            "background": CP[self.theme][8],
                                            "foreground": CP[self.theme][9]},
                              "map": {"background": [("selected", CP[self.theme][8])],
                                      "foreground": [("selected", CP[self.theme][9])],
                                      "expand": [("selected", [3, 1, 3, 1])]}},
            'TCombobox': {'configure': {'selectbackground': CP[self.theme][3],
                                        'fieldbackground': 'white',
                                        'borderwidth': 1,
                                        'background': CP[self.theme][8],
                                        'selectforeground': CP[self.theme][1]
                                        }},
            "DateEntry": {'configure': {'selectbackground': CP[self.theme][3],
                                        'background': CP[self.theme][8],
                                        'selectforeground': CP[self.theme][1]
                                        }},
            "TEntry": {'configure': {'selectbackground': CP[self.theme][3],
                                     'background': CP[self.theme][8],
                                     'selectforeground': CP[self.theme][1]
                                     }}
        })
        self.s.theme_use('MyStyle')

        self.menubar = Menu(self, background=CP[self.theme][0], foreground=CP[self.theme][1],
                            activebackground=CP[self.theme][3], activeforeground=CP[self.theme][4])
        self.file = Menu(self.menubar, tearoff=0, background=CP[self.theme][0],
                         foreground=CP[self.theme][1], selectcolor=CP[self.theme][2])
        self.view = Menu(self.menubar, tearoff=0, background=CP[self.theme][0],
                         foreground=CP[self.theme][1], selectcolor=CP[self.theme][2])
        self.file.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.view.add_radiobutton(label="Light Mode", command=lambda a=0: self.change_theme(a))
        self.view.add_radiobutton(label="Dark Mode")
        self.view.invoke(self.view.index("Dark Mode"))
        self.view.entryconfig(self.view.index("Dark Mode"), command=lambda a=1: self.change_theme(a))
        self.menubar.add_cascade(label="View", menu=self.view)
        self.config(menu=self.menubar)
        self.after(500, self.state_enable)

        # self.root.after(1500, state_enable)

        self.login_canvas = self.LoginCanvas(self, self.theme, self.winfo_screenwidth(), self.winfo_screenheight(),
                                             self.winfo_width(), self.winfo_height(), self.font_size, canvas_index)
        self.main_canvas = self.MainCanvas(self, self.theme, self.winfo_screenwidth(), self.winfo_screenheight(),
                                           self.winfo_width(), self.winfo_height(), self.main_layout, self.font_size,
                                           self.margin_width, self.margin_height, canvas_index)
        # self.add_driver = self.AddDriver(self, self.theme, self.winfo_screenwidth(), self.winfo_screenheight(),
        #                                    self.winfo_width(), self.winfo_height(), self.font_size,
        #                                    self.margin_width, self.margin_height, canvas_index)
        # self.add_admin = self.AddAdmin(self, self.theme, self.winfo_screenwidth(), self.winfo_screenheight(),
        #                                    self.winfo_width(), self.winfo_height(), self.font_size,
        #                                    self.margin_width, self.margin_height, canvas_index)

        self.bind("<Configure>", self.update_window)
        self.after(5, self.auto_resize)

    def update_window(self, event):
        self.time = time.time()

    def auto_resize(self):
        time_delta = time.time() - self.time
        if (self.curr_width != self.winfo_width() or self.curr_height != self.winfo_height()) and \
                time_delta > 0.1:
            self.curr_width = self.winfo_width()
            self.curr_height = self.winfo_height()

            width = round(self.curr_height * self.ratio)
            height = self.curr_height
            mar_percent = 10

            if self.curr_width > width:
                height = self.curr_height
                # self.margin_width = round(mar_percent / 100 * self.curr_width)
                self.margin_width = round(mar_percent / 100 * width) + (self.curr_width / 2 - width / 2)
                self.margin_height = round(mar_percent / 100 * height)
            elif self.curr_width < width:
                width = self.curr_width
                height = self.curr_width / self.ratio
                self.margin_width = round(mar_percent / 100 * width)
                # self.margin_height = round(mar_percent / 100 * self.curr_height)
                self.margin_height = round(mar_percent / 100 * height) + (self.curr_height / 2 - height / 2)
            else:
                self.margin_width = round(mar_percent / 100 * self.curr_width)
                self.margin_height = round(mar_percent / 100 * self.curr_height)

            mar_percent = mar_percent * 2
            self.main_layout = [round((100 - mar_percent) / 100 * width),
                                round((100 - mar_percent) / 100 * height)]
            if self.curr_width < 1029 or self.curr_height < 579:
                self.font_size = round(self.main_layout[1] / 1.1 / self.FONTSIZE_RATIO)
            else:
                self.font_size = round(self.main_layout[1] / self.FONTSIZE_RATIO)

            if self.canvas_index == 0:
                self.login_canvas.update_res(self)
            elif 1 <= self.canvas_index <= 5:
                self.main_canvas.update_res(self)
        self.after(10, self.auto_resize)

    def change_theme(self, theme):
        self.menubar.entryconfig("View", state=DISABLED)

        self.theme = theme

        self.menubar.configure(background=CP[self.theme][0], foreground=CP[self.theme][1],
                               activebackground=CP[self.theme][3],
                               activeforeground=CP[self.theme][4])
        self.file.configure(background=CP[self.theme][0], foreground=CP[self.theme][1],
                            selectcolor=CP[self.theme][2])
        self.view.configure(background=CP[self.theme][0], foreground=CP[self.theme][1],
                            selectcolor=CP[self.theme][2])
        self.config(menu=self.menubar)

        # Layout
        self.s.theme_settings("MyStyle", settings={
            "TNotebook": {"configure": {"background": CP[self.theme][5],
                                        'highlightbackground': CP[self.theme][8],
                                        'highlightcolor': CP[self.theme][9]}},
            "TNotebook.Tab": {"configure": {"background": CP[self.theme][8],
                                            "foreground": CP[self.theme][9]},
                              "map": {"background": [("selected", CP[self.theme][8])],
                                      "foreground": [("selected", CP[self.theme][9])]}},
            'TCombobox': {'configure': {'selectbackground': CP[self.theme][3],
                                        'background': CP[self.theme][8],
                                        'selectforeground': CP[self.theme][1]
                                        }},
            "DateEntry": {'configure': {'selectbackground': CP[self.theme][3],
                                        'background': CP[self.theme][8],
                                        'selectforeground': CP[self.theme][1]
                                        }},
            "TEntry": {'configure': {'selectbackground': CP[self.theme][3],
                                     'background': CP[self.theme][8],
                                     'selectforeground': CP[self.theme][1]
                                     }}
        })
        self.main_canvas.change_theme(self.theme)
        self.login_canvas.change_theme(self.theme)

        self.after(500, self.state_enable)

    def state_enable(self):
        self.menubar.entryconfig("View", state=NORMAL)

    def set_canvas_index(self, ci):
        self.canvas_index = ci

    def set_canvas(self):
        if self.canvas_index == 0:
            self.login_canvas.update_res(self)
        elif 1 <= self.canvas_index <= 5:
            self.main_canvas.update_res(self)

    def _on_mousewheel(self, event, frame, margin):
        x, y = self.winfo_pointerx() - self.winfo_rootx(), self.winfo_pointery() - self.winfo_rooty()
        if self.canvas_index == 1:
            x_right = frame.winfo_width() + margin[0]
            y_top = margin[1] + frame.winfo_height() * (1 - margin[2])
            y_bot = frame.winfo_height() + margin[1] + frame.winfo_height() * (1 - margin[2] + 0.007)
            # Additional 0.007 is due to the border width of the canvas
            # print("Coord: " , x, y, "\nMin : ", margin[0], y_top, "\nMax : ", x_right, y_bot)
            if margin[0] <= x <= x_right and y_top <= y <= y_bot:
                frame.view_canvas.yview_scroll(round(-1 * (event.delta / 120)), "units")
                # print("Scroll Driver")
        elif self.canvas_index == 3:
            x_right = frame.winfo_width() + margin[0]
            y_top = margin[1] + frame.winfo_height() * (1 - margin[2])
            y_bot = frame.winfo_height() + margin[1] + frame.winfo_height() * (1 - margin[2] + 0.007)
            # Additional 0.007 is due to the border width of the canvas
            # print("Coord: " , x, y, "\nMin : ", margin[0], y_top, "\nMax : ", x_right, y_bot)
            if margin[0] <= x <= x_right and y_top <= y <= y_bot:
                frame.view_canvas.yview_scroll(round(-1 * (event.delta / 120)), "units")
                print("Scroll Admin")

    def _on_mousewheel_pass(self, event):
        pass


def main():
    get_setting()
    app = SentsGui(0)
    app.mainloop()


def get_setting():
    global db, fl
    if not os.path.isdir(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)
    if not os.path.isdir(os.path.join(TEMP_FOLDER, DRIVER_FOLDER)):
        os.mkdir(os.path.join(TEMP_FOLDER, DRIVER_FOLDER))
    if not os.path.isdir(os.path.join(TEMP_FOLDER, PLT_NUM_FOLDER)):
        os.mkdir(os.path.join(TEMP_FOLDER, PLT_NUM_FOLDER))

    if not os.path.isfile('setting.txt'):
        f = open('setting.txt', 'x')
        text = ""
        text += "host=localhost\n"
        text += "\nMySQL\n"
        text += "port_sql=\n"
        text += "user_sql=\n"
        text += "pass_sql=\n"
        text += "\nFileZilla\n"
        text += "user_fl=pnradmin\n"
        text += "pass_fl=pnradmin\n"
        f.write(text)
        f.close()

    with open('setting.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.find("host=") == 0:
                server_setting[0] = line.split('=')[1].replace("\n", "")
                if server_setting[0] == "":
                    server_setting[0] = None
            elif line.find("user_sql=") == 0:
                server_setting[2] = line.split('=')[1].replace("\n", "")
                if server_setting[2] == "":
                    server_setting[2] = None
            elif line.find("pass_sql=") == 0:
                server_setting[3] = line.split('=')[1].replace("\n", "")
                if server_setting[3] == "":
                    server_setting[3] = None
            elif line.find("user_fl=") == 0:
                server_setting[4] = line.split('=')[1].replace("\n", "")
                if server_setting[4] == "":
                    server_setting[4] = None
            elif line.find("pass_fl=") == 0:
                server_setting[5] = line.split('=')[1].replace("\n", "")
                if server_setting[5] == "":
                    server_setting[5] = None
    db = MySQL(server_setting[0], server_setting[2], server_setting[3])
    fl = Filezilla(host=server_setting[0], user=server_setting[4], password=server_setting[5])


if __name__ == "__main__":
    main()
