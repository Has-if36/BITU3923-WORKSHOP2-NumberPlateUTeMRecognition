# Hidden
import numpy as np
from local_utils import detect_lp
from sklearn.preprocessing import LabelEncoder
from model import WPOD_NET, MOBILE_NET
from os.path import splitext
from keras.models import model_from_json
from keras.preprocessing.image import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder
import shutil
import ftplib
import zipfile
import mysql.connector
from datetime import datetime

# Main
from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkcalendar as cal
import cv2
from PIL import Image, ImageTk, ImageFont, ImageDraw
import urllib.request
import ssl
import threading
import time
import datetime
import math
import sys
import wmi
import re
import os
from PlateRecognition import plate_recognition
from Database import MySQL
from Database import Filezilla

"""
    Search Tag: 
        Database Connection
        Potential Bug
    
Colour Palette
    Black Bluish
        #261C2C
        #3E2C41
        #5C527F
        #6E85B2

    Gray Black
        #362222
        #171010
        #423F3E
        #2B2B2B
        
    DarkShades2
        #0c242b
        #080a3f
        #01263f
        #0e384b
        #0b3243
        
    Text Color
        #EEEEEE
        #FFF5FD
        #DBE6FD
"""

MIN_WIDTH = 853
MIN_HEIGHT = 480

# [bg, fg, selector, actBg, actFg, bg2, fg2, selector2, actBg2, actFg2, fontColor2]
CP = [['#ECEFF1', '#171010', '#EEEEEE', "#CFD8DC", None,
       '#90A4AE', '#DA0037', '#EEEEEE', '#CFD8DC', 'black',
       '#6E85B2', 'black', None, '#B0BEC5', 'black'],
      ['#2B2B2B', '#EEEEEE', '#5C527F', "#423F3E", None,
       '#261C2C', '#FFD369', '#5C527F', '#5C527F', '#EEEEEE',
       '#6E85B2', 'black', None, '#5C527F', 'black']]
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
server_setting = ["localhost", None, None, None, 'pnradmin', 'pnradmin', '']
db = None
fl = None
TEMP_FOLDER = 'temp'
DRIVER_FOLDER = 'driver'
PLT_NUM_FOLDER = 'plate_number'
PRIVILEGE = ''
CURR_USER = ''

ssl._create_default_https_context = ssl._create_unverified_context

MONTH = {
    '01': "JAN",
    '02': "FEB",
    '03': "MAR",
    '04': "APR",
    '05': "MAY",
    '06': "JUN",
    '07': "JUL",
    '08': "AUG",
    '09': "SEP",
    '10': "OCT",
    '11': "NOV",
    '12': "DEC"
}

MONTH_NUM = {
    "JAN": '01',
    "FEB": '02',
    "MAR": '03',
    "APR": '04',
    "MAY": '05',
    "JUN": '06',
    "JUL": '07',
    "AUG": '08',
    "SEP": '09',
    "OCT": '10',
    "NOV": '11',
    "DEC": '12'
}


# url = "https://192.168.1.17:8080/video"
# sys.setrecursionlimit(1000)

# Fetch Database
def fetch_history_owner(date):
    pass


def fetch_plate_owner(plate_number):
    pass


class SentsGui(Tk):
    """
        class LoginCanvas(Canvas):
        def __init__(self, root, theme, screen_width, screen_height, width, height, font_size,
                     canvas_index):
            super().__init__(width=screen_width, height=screen_height, bg=CP[theme][0], highlightthickness=0)
            self.canvas_index = canvas_index
            self.root = root.root
            self.root_2 = root
            self.place(x=width, y=height)

            if root.theme == 1:
                self.ori_logo = Image.open("./logo_dark_mode.png")
            else:
                self.ori_logo = Image.open("./logo_light_mode.png")
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

            font_setting = "Calibri " + str(round(font_size * 1))
            self.login_user_text = Label(self.login_user_frame, text="{:<9} : ".format("Username"),
                                         bg=CP[theme][0], fg=CP[theme][1], font=font_setting)
            self.login_user_text.place(x=0, y=0)
            self.login_user_text.update()

            self.login_pass_text = Label(self.login_user_frame, text="{:<10} : ".format("Password"),
                                         bg=CP[theme][0], fg=CP[theme][1], font=font_setting)
            self.login_pass_text.place(x=0, y=self.login_user_text.winfo_height() * 1.5)
            self.login_pass_text.update()

            font_setting = "Calibri " + str(round(font_size * 0.85))
            self.login_user_strvar = StringVar()
            self.login_user_field = ttk.Entry(self.login_user_frame, width=20, textvariable=self.login_user_strvar,
                                              font=font_setting)
            self.login_user_field.place(x=self.login_user_text.winfo_width(),
                                        y=round(0.05 * self.login_user_text.winfo_height()))

            self.login_pass_strvar = StringVar()
            self.login_pass_field = ttk.Entry(self.login_user_frame, width=20, textvariable=self.login_pass_strvar,
                                              font=font_setting, show='*')
            self.login_pass_field.place(x=self.login_pass_text.winfo_width(),
                                        y=self.login_user_text.winfo_height() * 1.5 +
                                          round(0.05 * self.login_user_text.winfo_height()))
            self.login_user_field.update()
            self.login_pass_field.update()

            font_setting = "Calibri " + str(round(font_size * 0.75)) + " bold"
            self.login_btn = Button(self.login_user_frame, bg=CP[theme][5], fg=CP[theme][6],
                                    activebackground=CP[theme][8], activeforeground=CP[theme][9], border=1,
                                    text="Login", font=font_setting, padx=10, pady=1, command=self.button_event)
            self.login_btn.place(x=self.login_user_frame.winfo_width(), y=self.login_user_frame.winfo_height())
            self.login_btn.update()
            self.login_user_frame.config(width=self.login_user_text.winfo_width() + self.login_user_field.winfo_width(),
                                         height=self.login_user_text.winfo_height() * 2.5 +
                                                self.login_pass_text.winfo_height())
            self.login_user_frame.update()
            self.login_btn.place(x=round(self.login_user_frame.winfo_width() / 2 - self.login_btn.winfo_width() / 2),
                                 y=round(self.login_user_text.winfo_height() * 2.5 +
                                         self.login_pass_text.winfo_height()))

            self.login_user_frame.config(height=self.login_user_frame.winfo_height() + self.login_btn.winfo_height())
            self.login_user_frame.update()
            self.login_user_frame.place(x=width / 2 - self.login_user_frame.winfo_width() / 2,
                                        y=height * 3 / 4 - self.login_user_frame.winfo_height() / 2)

            self.update()
            if self.canvas_index != 0:
                self.place_forget()
            else:
                self.place(x=0, y=0)

        def button_event(self):
            # Input
            #     self.login_user_strvar.get()
            #     self.login_pass_strvar.get()

            if self.login_user_strvar.get() and self.login_pass_strvar.get():
                # Database Connection
                match_account = False
                privilege = None

                # Output
                #     match_account
                #     privilege

                # Login Frame
                if match_account:
                    pass
                else:
                    print("Incorrect Username or Password")

                # Temporary Login
                self.canvas_index = 1
                self.root_2.set_canvas_index(self.canvas_index)
                self.place_forget()
                self.root_2.set_canvas()
                self.login_user_strvar.set("")
                self.login_pass_strvar.set("")
                self.login_user_field.focus_set()

            else:
                print("All Field Must be Filled")

        def update_res(self, width, height, font_size):
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

            font_setting = "Calibri " + str(round(font_size * 0.85))
            self.login_user_field.configure(font=font_setting)
            self.login_user_field.place(x=self.login_user_text.winfo_width(),
                                        y=round(0.05 * self.login_user_text.winfo_height()))

            self.login_pass_field.configure(font=font_setting)
            self.login_pass_field.place(x=self.login_pass_text.winfo_width(),
                                        y=self.login_user_text.winfo_height() * 1.5 +
                                          round(0.05 * self.login_user_text.winfo_height()))
            self.login_user_field.update()
            self.login_pass_field.update()

            font_setting = "Calibri " + str(round(font_size * 0.75)) + " bold"
            self.login_btn.configure(font=font_setting)
            self.login_btn.place(x=self.login_user_frame.winfo_width(), y=self.login_user_frame.winfo_height())
            self.login_btn.update()
            self.login_user_frame.config(width=self.login_user_text.winfo_width() + self.login_user_field.winfo_width(),
                                         height=self.login_user_text.winfo_height() * 2.5 +
                                                self.login_pass_text.winfo_height())
            self.login_user_frame.update()
            self.login_btn.place(x=round(self.login_user_frame.winfo_width() / 2 - self.login_btn.winfo_width() / 2),
                                 y=round(self.login_user_text.winfo_height() * 2.5 +
                                         self.login_pass_text.winfo_height()))

            self.login_user_frame.config(height=self.login_user_frame.winfo_height() + self.login_btn.winfo_height())
            self.login_user_frame.update()
            self.login_user_frame.place(x=width / 2 - self.login_user_frame.winfo_width() / 2,
                                        y=height * 3 / 4 - self.login_user_frame.winfo_height() / 2)

            self.update()

        def change_theme(self, theme):
            if theme == 1:
                self.ori_logo = Image.open("./logo_dark_mode.png")
            else:
                self.ori_logo = Image.open("./logo_light_mode.png")
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
            self.login_btn.configure(bg=CP[theme][5], fg=CP[theme][6],
                                     activebackground=CP[theme][8], activeforeground=CP[theme][9])
            self.update()
    """

    class LoginCanvas(Canvas):
        class Setting(Toplevel):
            def __init__(self, root):
                super().__init__(root)
                filename = 'logo_light_mode.png'
                try:
                    filename = os.path.join(BASE_PATH, filename)
                    print(filename)
                except Exception as e:
                    print('Error:', e)
                self.icon = PhotoImage(file=filename)
                self.iconphoto(False, self.icon)

                title = "Server Setting "
                width = 514  # round(self.root.winfo_width() / 2)
                height = 500  # round(self.root.winfo_height() / 1.2) # 530
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
                self.gate_label = Label(self.server_frame, font=font_setting, text="Gate \t\t: ",
                                        bg=CP[root.theme][5], fg=CP[root.theme][1])
                self.server_label.place(x=0, y=0)
                self.host_label.place(x=0, y=0)
                self.user_sql_label.place(x=0, y=0)
                self.pass_sql_label.place(x=0, y=0)
                self.user_fl_label.place(x=0, y=0)
                self.pass_fl_label.place(x=0, y=0)
                self.gate_label.place(x=0, y=0)
                self.server_label.update()
                self.host_label.update()
                self.user_sql_label.update()
                self.pass_sql_label.update()
                self.user_fl_label.update()
                self.pass_fl_label.update()
                self.gate_label.update()
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
                y_coord = y_coord + gap
                self.gate_label.place(x=0, y=y_coord)
                self.host_label.update()
                self.user_sql_label.update()
                self.pass_sql_label.update()
                self.user_fl_label.update()
                self.pass_fl_label.update()
                self.gate_label.update()

                self.host_str = StringVar()
                self.user_sql_str = StringVar()
                self.pass_sql_str = StringVar()
                self.user_fl_str = StringVar()
                self.pass_fl_str = StringVar()
                self.gate_str = StringVar()

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
                        elif line.find("gate=") == 0:
                            server_setting[6] = line.split('=')[1].replace("\n", "")
                            self.gate_str.set(server_setting[6])

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
                self.gate_entry = ttk.Entry(self.server_frame, width=entry_length, textvariable=self.gate_str,
                                            font=font_setting, style='pad.TEntry')
                self.host_entry.place(x=0, y=0)
                self.user_sql_entry.place(x=0, y=0)
                self.pass_sql_entry.place(x=0, y=0)
                self.user_fl_entry.place(x=0, y=0)
                self.pass_fl_entry.place(x=0, y=0)
                self.gate_entry.place(x=0, y=0)
                self.host_entry.update()
                self.user_sql_entry.update()
                self.pass_sql_entry.update()
                self.user_fl_entry.update()
                self.pass_fl_entry.update()
                self.gate_entry.update()
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
                y_coord = y_coord + gap
                self.gate_entry.place(x=self.gate_label.winfo_width(),
                                      y=y_coord +
                                        (
                                                self.gate_label.winfo_height() / 2 - self.gate_entry.winfo_height() / 2))
                self.host_entry.update()
                self.user_sql_entry.update()
                self.pass_sql_entry.update()
                self.user_fl_entry.update()
                self.pass_fl_entry.update()
                self.gate_entry.update()

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
                self.gate_def_btn = Button(self.server_frame, font=font_setting, text="Default", padx=2,
                                           bg=CP[root.theme][10], fg=CP[root.theme][11],
                                           activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                           command=lambda a=7, b=root: self.btn_event(a, b))
                self.host_def_btn.place(x=0, y=0)
                self.user_sql_def_btn.place(x=0, y=0)
                self.pass_sql_def_btn.place(x=0, y=0)
                self.user_fl_def_btn.place(x=0, y=0)
                self.pass_fl_def_btn.place(x=0, y=0)
                self.gate_def_btn.place(x=0, y=0)
                self.host_def_btn.update()
                self.user_sql_def_btn.update()
                self.pass_sql_def_btn.update()
                self.user_fl_def_btn.update()
                self.pass_fl_def_btn.update()
                self.gate_def_btn.update()
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
                y_coord = y_coord + gap
                self.gate_def_btn.place(
                    x=self.gate_label.winfo_width() + self.gate_entry.winfo_width() + 10,
                    y=y_coord +
                      (
                              self.host_label.winfo_height() / 2 - self.gate_def_btn.winfo_height() / 2))
                # y_coord = y_coord + gap * 1.1
                self.host_def_btn.update()
                self.user_sql_def_btn.update()
                self.pass_sql_def_btn.update()
                self.user_fl_def_btn.update()
                self.pass_fl_def_btn.update()
                self.gate_def_btn.update()

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
                                     command=lambda a=8, b=root: self.btn_event(a, b))
                self.conn_btn = Button(self.server_frame, font=font_setting, text="Test", width=8,
                                       bg=CP[root.theme][10], fg=CP[root.theme][11],
                                       activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                       command=lambda a=9, b=root: self.btn_event(a, b))
                self.cancel_btn = Button(self.server_frame, font=font_setting, text="Cancel", width=8,
                                         bg=CP[root.theme][10], fg=CP[root.theme][11],
                                         activebackground=CP[root.theme][13], activeforeground=CP[root.theme][14],
                                         command=lambda a=10, b=root: self.btn_event(a, b))
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
                    self.gate_str.set("")
                elif type == 8:
                    # Ok Stuff
                    server_setting[0] = self.host_str.get()
                    server_setting[2] = self.user_sql_str.get()
                    server_setting[3] = self.pass_sql_str.get()
                    server_setting[4] = self.user_fl_str.get()
                    server_setting[5] = self.pass_fl_str.get()
                    server_setting[6] = self.gate_str.get()

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
                        elif line.find("gate=") == 0:
                            line = "gate=" + server_setting[6] + "\n"
                            f.write(line)
                        else:
                            f.write(line)
                    f.close()

                    for i in range(0, len(server_setting)):
                        if server_setting[i] == "" and i != 6:
                            server_setting[i] = None
                    # print(server_setting)

                    self.destroy()
                elif type == 9:
                    if db.update_connection(host=self.host_str.get(), user=self.user_sql_str.get(),
                                            password=self.pass_sql_str.get()) and \
                            fl.update_connection(host=self.host_str.get(), user=self.user_fl_str.get(),
                                                 password=self.pass_fl_str.get()):
                        self.stats_lbl.configure(text="Successfully Connect", fg=CP[root.theme][6])
                    else:
                        self.stats_lbl.configure(text="Failed to Connect", fg=CP[root.theme][6])
                    self.after(3000, lambda a=root: self.status_fade(a))
                elif type == 10:
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

            filename = 'logo_dark_mode.png'
            self.ori_logo = Image.open(os.path.join(BASE_PATH, filename))
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
            self.login_user_text = Label(self.login_user_frame, text="Officer ID\t : ", bg=CP[theme][0],
                                         fg=CP[theme][1],
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

                    match_account, msg = db.login_officer(self.login_user_strvar.get(), self.login_pass_strvar.get())

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
            if theme == 1:
                filename = 'logo_dark_mode.png'
                self.ori_logo = Image.open(os.path.join(BASE_PATH, filename))
            else:
                filename = 'logo_light_mode.png'
                self.ori_logo = Image.open(os.path.join(BASE_PATH, filename))
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

    class Result(Canvas):
        def __init__(self, root, tab_size):
            self.borderwidth = 1
            self.canvas_item = []
            self.canvas_frame = []
            self.enter_occupied = False
            self.exit_occupied = False
            self.enter_rec = 'UNRECOGNISED'
            self.exit_rec = 'UNRECOGNISED'
            margin = [round(0.01 * tab_size[0]), round(0.01 * tab_size[1])]

            super().__init__(root.tabs, width=tab_size[0], height=tab_size[1], bg=CP[root.theme][1],
                             highlightthickness=0)
            # Frame(self.tabs, width=tab_size[0], height=tab_size[1],
            #                           bg=self.color_root[self.theme][1])
            self.place(x=0, y=0)
            self.update()

            y_coord = 0
            enter_frame = Frame(self, width=tab_size[0], height=round(tab_size[1] / 2), bg=CP[root.theme][5],
                                highlightthickness=self.borderwidth)
            enter_item = self.create_window((0, y_coord), window=enter_frame, anchor=NW)
            self.canvas_frame.append(enter_frame)
            self.canvas_item.append(enter_item)
            y_coord = y_coord + round(tab_size[1] / 2)

            exit_frame = Frame(self, width=tab_size[0], height=round(tab_size[1] / 2), bg=CP[root.theme][5],
                               highlightthickness=self.borderwidth)
            exit_item = self.create_window((0, y_coord), window=exit_frame, anchor=NW)
            self.canvas_frame.append(exit_frame)
            self.canvas_item.append(exit_item)

            font_setting = "calibri " + str(root.font_size) + " bold"
            self.enter_label = Label(enter_frame, text='Enter', font=font_setting,
                                     bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_label = Label(exit_frame, text='Exit', font=font_setting,
                                    bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_label.place(x=margin[0], y=0)
            self.exit_label.place(x=margin[0], y=0)
            self.enter_label.update()
            self.exit_label.update()

            # ENTER INIT
            font_setting = "calibri " + str(round(root.font_size * 0.75))
            self.enter_manual_label = Label(enter_frame, text='Manual\t: ', font=font_setting,
                                            bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_scan_label = Label(enter_frame, text='Scanned\t: ', font=font_setting,
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_stat_label = Label(enter_frame, text='Status\t: ', font=font_setting,  # Recognised or not
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_role_label = Label(enter_frame, text='Role\t: ', font=font_setting,
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_name_label = Label(enter_frame, text='Name\t: ', font=font_setting,
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_id_label = Label(enter_frame, text='ID Num.\t: ', font=font_setting,
                                        bg=CP[root.theme][5], fg=CP[root.theme][1])

            enter_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                  color='#171010')
            self.enter_img_tk = ImageTk.PhotoImage(enter_img)
            self.enter_img_label = Label(enter_frame, font=font_setting, bg=CP[root.theme][1], image=self.enter_img_tk)

            self.enter_manual_str = StringVar()

            font_setting = "calibri " + str(round(root.font_size * 0.7))
            entry_length = 20
            self.enter_manual_entry = ttk.Entry(enter_frame, width=round(entry_length),
                                                textvariable=self.enter_manual_str,
                                                font=font_setting, style='pad.TEntry')

            font_setting = "calibri " + str(round(root.font_size ** (1. / 1.28))) + " bold"
            self.enter_enter_btn = Button(enter_frame, text="Enter", font=font_setting,
                                          width=round(tab_size[0] * 0.02), pady=0,
                                          bg=CP[root.theme][10], fg=CP[root.theme][11],
                                          command=lambda a=1, b=tab_size: self.button_enter(a, b)
                                          )
            self.enter_confirm_btn = Button(enter_frame, text="Confirm", font=font_setting,
                                            width=round(tab_size[0] * 0.02), pady=0,
                                            bg=CP[root.theme][10], fg=CP[root.theme][11],
                                            command=lambda a=1, b=root: self.button_confirm(a, b)
                                            )
            self.enter_clear_btn = Button(enter_frame, text="Clear", font=font_setting,
                                          width=round(tab_size[0] * 0.02), pady=0,
                                          bg=CP[root.theme][10], fg=CP[root.theme][11],
                                          command=lambda a=1, b=root, c=tab_size: self.button_clear(a, b, c))
            self.enter_scan_btn = Button(enter_frame, text="Scan", font=font_setting,
                                         width=round(tab_size[0] * 0.02), pady=0,
                                         bg=CP[root.theme][10], fg=CP[root.theme][11],
                                         command=lambda a=1, b=root, c=tab_size: self.button_scan(a, b, c))

            self.enter_manual_label.place(x=0, y=0)
            self.enter_scan_label.place(x=0, y=0)
            self.enter_img_label.place(x=0, y=0)
            self.enter_stat_label.place(x=0, y=0)
            self.enter_role_label.place(x=0, y=0)
            self.enter_name_label.place(x=0, y=0)
            self.enter_id_label.place(x=0, y=0)
            self.enter_manual_label.update()
            self.enter_scan_label.update()
            self.enter_img_label.update()
            self.enter_stat_label.update()
            self.enter_role_label.update()
            self.enter_name_label.update()
            self.enter_id_label.update()

            self.enter_manual_entry.place(x=0, y=0)
            self.enter_manual_entry.update()

            self.enter_enter_btn.place(x=0, y=0)
            self.enter_confirm_btn.place(x=0, y=0)
            self.enter_clear_btn.place(x=0, y=0)
            self.enter_scan_btn.place(x=0, y=0)
            self.enter_enter_btn.update()
            self.enter_confirm_btn.update()
            self.enter_clear_btn.update()
            self.enter_scan_btn.update()

            # EXIT INIT
            font_setting = "calibri " + str(round(root.font_size * 0.75))
            self.exit_manual_label = Label(exit_frame, text='Manual\t: ', font=font_setting,
                                           bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_scan_label = Label(exit_frame, text='Scanned\t: ', font=font_setting,
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_stat_label = Label(exit_frame, text='Status\t: ', font=font_setting,  # Recognised or not
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_role_label = Label(exit_frame, text='Role\t: ', font=font_setting,
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_name_label = Label(exit_frame, text='Name\t: ', font=font_setting,
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_id_label = Label(exit_frame, text='ID Num.\t: ', font=font_setting,
                                       bg=CP[root.theme][5], fg=CP[root.theme][1])

            exit_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                 color='#171010')
            self.exit_img_tk = ImageTk.PhotoImage(exit_img)
            self.exit_img_label = Label(exit_frame, font=font_setting, bg=CP[root.theme][1], image=self.exit_img_tk)

            self.exit_manual_str = StringVar()

            font_setting = "calibri " + str(round(root.font_size * 0.7))
            entry_length = 20
            self.exit_manual_entry = ttk.Entry(exit_frame, width=round(entry_length),
                                               textvariable=self.exit_manual_str,
                                               font=font_setting, style='pad.TEntry')

            font_setting = "calibri " + str(round(root.font_size ** (1. / 1.28))) + " bold"
            self.exit_enter_btn = Button(exit_frame, text="Enter", font=font_setting,
                                         width=round(tab_size[0] * 0.02), pady=0,
                                         bg=CP[root.theme][10], fg=CP[root.theme][11],
                                         command=lambda a=2, b=tab_size: self.button_enter(a, b)
                                         )
            self.exit_confirm_btn = Button(exit_frame, text="Confirm", font=font_setting,
                                           width=round(tab_size[0] * 0.02), pady=0,
                                           bg=CP[root.theme][10], fg=CP[root.theme][11],
                                           command=lambda a=2, b=root: self.button_confirm(a, b)
                                           )
            self.exit_clear_btn = Button(exit_frame, text="Clear", font=font_setting,
                                         width=round(tab_size[0] * 0.02), pady=0,
                                         bg=CP[root.theme][10], fg=CP[root.theme][11],
                                         command=lambda a=2, b=root, c=tab_size: self.button_clear(a, b, c))
            self.exit_scan_btn = Button(exit_frame, text="Scan", font=font_setting,
                                        width=round(tab_size[0] * 0.02), pady=0,
                                        bg=CP[root.theme][10], fg=CP[root.theme][11],
                                        command=lambda a=2, b=root, c=tab_size: self.button_scan(a, b, c))

            self.exit_manual_label.place(x=0, y=0)
            self.exit_scan_label.place(x=0, y=0)
            self.exit_img_label.place(x=0, y=0)
            self.exit_stat_label.place(x=0, y=0)
            self.exit_role_label.place(x=0, y=0)
            self.exit_name_label.place(x=0, y=0)
            self.exit_id_label.place(x=0, y=0)
            self.exit_manual_label.update()
            self.exit_scan_label.update()
            self.exit_img_label.update()
            self.exit_stat_label.update()
            self.exit_role_label.update()
            self.exit_name_label.update()
            self.exit_id_label.update()

            self.exit_manual_entry.place(x=0, y=0)
            self.exit_manual_entry.update()

            self.exit_enter_btn.place(x=0, y=0)
            self.exit_confirm_btn.place(x=0, y=0)
            self.exit_clear_btn.place(x=0, y=0)
            self.exit_scan_btn.place(x=0, y=0)
            self.exit_enter_btn.update()
            self.exit_confirm_btn.update()
            self.exit_clear_btn.update()
            self.exit_scan_btn.update()

            # ENTER COORD
            y_coord_enter = self.enter_label.winfo_height()
            self.enter_manual_label.place(x=margin[0], y=y_coord_enter)
            self.enter_manual_entry.place(x=margin[0] + self.enter_manual_label.winfo_width(), y=y_coord_enter)
            y_coord_enter = y_coord_enter + self.enter_manual_label.winfo_height()
            self.enter_enter_btn.place(x=margin[0] + self.enter_manual_label.winfo_width() +
                                         self.enter_manual_entry.winfo_width() - self.enter_enter_btn.winfo_width() * 0.95,
                                       y=y_coord_enter)
            y_coord_enter = y_coord_enter + self.enter_enter_btn.winfo_height() * 1.1
            self.enter_scan_label.place(x=margin[0], y=y_coord_enter)

            y_coord_enter = (tab_size[1] / 2) - self.enter_id_label.winfo_height() * 1.1
            self.enter_id_label.place(x=margin[0], y=y_coord_enter)
            y_coord_enter = y_coord_enter - self.enter_name_label.winfo_height()
            self.enter_name_label.place(x=margin[0], y=y_coord_enter)
            y_coord_enter = y_coord_enter - self.enter_role_label.winfo_height()
            self.enter_role_label.place(x=margin[0], y=y_coord_enter)
            y_coord_enter = y_coord_enter - self.enter_stat_label.winfo_height()
            self.enter_stat_label.place(x=margin[0], y=y_coord_enter)

            self.enter_img_label.place(x=tab_size[0] - self.enter_img_label.winfo_width(), y=0)

            y_coord_btn = tab_size[1] / 2 - self.enter_confirm_btn.winfo_height() - margin[1]
            self.enter_confirm_btn.place(x=tab_size[0] - self.enter_confirm_btn.winfo_width() - margin[0],
                                         y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.enter_confirm_btn.winfo_height() * 1.1
            self.enter_clear_btn.place(x=tab_size[0] - self.enter_confirm_btn.winfo_width() - margin[0],
                                       y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.enter_clear_btn.winfo_height() * 1.1
            self.enter_scan_btn.place(x=tab_size[0] - self.enter_confirm_btn.winfo_width() - margin[0],
                                      y=y_coord_btn)

            # ENTER COORD
            y_coord_exit = self.exit_label.winfo_height()
            self.exit_manual_label.place(x=margin[0], y=y_coord_exit)
            self.exit_manual_entry.place(x=margin[0] + self.exit_manual_label.winfo_width(), y=y_coord_exit)
            y_coord_exit = y_coord_exit + self.exit_manual_label.winfo_height()
            self.exit_enter_btn.place(x=margin[0] + self.exit_manual_label.winfo_width() +
                                        self.exit_manual_entry.winfo_width() - self.exit_enter_btn.winfo_width() * 0.95,
                                      y=y_coord_exit)
            y_coord_exit = y_coord_exit + self.exit_enter_btn.winfo_height() * 1.1
            self.exit_scan_label.place(x=margin[0], y=y_coord_exit)

            y_coord_exit = (tab_size[1] / 2) - self.exit_id_label.winfo_height() * 1.1
            self.exit_id_label.place(x=margin[0], y=y_coord_exit)
            y_coord_exit = y_coord_exit - self.exit_name_label.winfo_height()
            self.exit_name_label.place(x=margin[0], y=y_coord_exit)
            y_coord_exit = y_coord_exit - self.exit_role_label.winfo_height()
            self.exit_role_label.place(x=margin[0], y=y_coord_exit)
            y_coord_exit = y_coord_exit - self.exit_stat_label.winfo_height()
            self.exit_stat_label.place(x=margin[0], y=y_coord_exit)

            self.exit_img_label.place(x=tab_size[0] - self.exit_img_label.winfo_width(), y=0)

            y_coord_btn = tab_size[1] / 2 - self.exit_confirm_btn.winfo_height() - margin[1]
            self.exit_confirm_btn.place(x=tab_size[0] - self.exit_confirm_btn.winfo_width() - margin[0],
                                        y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.exit_confirm_btn.winfo_height() * 1.1
            self.exit_clear_btn.place(x=tab_size[0] - self.exit_confirm_btn.winfo_width() - margin[0],
                                      y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.exit_clear_btn.winfo_height() * 1.1
            self.exit_scan_btn.place(x=tab_size[0] - self.exit_confirm_btn.winfo_width() - margin[0],
                                     y=y_coord_btn)

        def button_confirm(self, type, root):
            if type == 1:
                title = ''
                msg = ''
                if self.enter_occupied:
                    stat, msg = db.insert_log_driver(self.enter_manual_str.get().upper(), self.enter_rec,
                                                     type_ent='enter', gate=server_setting[6])
                    if stat:
                        title = 'Successful!'
                    else:
                        title = 'Failed...'
                else:
                    title = 'Failed'
                    msg = 'Unable to Insert Log'

                self.enter_rec = 'UNRECOGNISED'
                SentsGui.Notification(root, title, msg)
                self.enter_occupied = False
            elif type == 2:
                title = ''
                msg = ''
                if self.exit_occupied:
                    stat, msg = db.insert_log_driver(self.exit_manual_str.get().upper(), self.exit_rec,
                                                     type_ent='exit', gate=server_setting[6])
                    if stat:
                        title = 'Successful!'
                    else:
                        title = 'Failed...'
                else:
                    title = 'Failed...'
                    msg = 'Unable to Insert Log'

                self.exit_rec = 'UNRECOGNISED'
                SentsGui.Notification(root, title, msg)
                self.exit_occupied = False

        def button_clear(self, type, root, tab_size):
            if type == 1:
                self.enter_occupied = False
                self.enter_rec = 'UNRECOGNISED'
                self.enter_scan_label.configure(text='Scanned\t: ')
                self.enter_stat_label.configure(text='Status\t: ')
                self.enter_role_label.configure(text='Role\t: ')
                self.enter_name_label.configure(text='Name\t: ')
                self.enter_id_label.configure(text='ID Num.\t: ')

                enter_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)), color='#171010')
                self.enter_img_tk = ImageTk.PhotoImage(enter_img)
                self.enter_img_label.configure(image=self.enter_img_tk)
                self.enter_manual_str.set('')
                root.plt_num_enter = ''
            if type == 2:
                self.exit_occupied = False
                self.exit_rec = 'UNRECOGNISED'
                self.exit_scan_label.configure(text='Scanned\t: ')
                self.exit_stat_label.configure(text='Status\t: ')
                self.exit_role_label.configure(text='Role\t: ')
                self.exit_name_label.configure(text='Name\t: ')
                self.exit_id_label.configure(text='ID Num.\t: ')

                exit_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                     color='#171010')
                self.exit_img_tk = ImageTk.PhotoImage(exit_img)
                self.exit_img_label.configure(image=self.exit_img_tk)
                self.exit_manual_str.set('')
                root.plt_num_exit = ''

        def button_scan(self, type, root, tab_size):
            # Binding of scan button need to change (Have not change yet)
            """
            Used Enter Since The value is Constant
            root.ai_enter
            root.ai_exit

            Input
                root.plt_num_enter
                root.plt_num_exit
            """
            if type == 1:
                root.plt_num_enter = root.plt_num_enter.upper()
                self.enter_scan_label.configure(text='Scanned\t: ' + root.plt_num_enter)

                if root.plt_num_enter and root.plt_num_enter != root.ai_enter.NO_DETECT.upper():
                    self.enter_manual_str.set(root.plt_num_enter)
                    self.button_enter(type, tab_size)
            elif type == 2:
                root.plt_num_exit = root.plt_num_exit.upper()
                self.exit_scan_label.configure(text='Scanned\t: ' + root.plt_num_exit)

                if root.plt_num_exit and root.plt_num_exit != root.ai_enter.NO_DETECT.upper():
                    self.exit_manual_str.set(root.plt_num_exit)
                    self.button_enter(type, tab_size)

        def button_enter(self, type, tab_size):
            path_driver = os.path.join(TEMP_FOLDER, DRIVER_FOLDER)
            if type == 1 and self.enter_manual_str.get():
                self.enter_occupied = True
                db_stat, result, role = db.find_driver(self.enter_manual_str.get())
                print('Search:', result)
                fl_stat = False
                if result:
                    fl_stat, file = fl.dw_from_server(path_driver, result[0][0], 1)
                    print('Image: ', file)
                if fl_stat:
                    img_driver = Image.open(os.path.join(path_driver, file))
                    img_resized_driver = img_driver.resize((round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                                           Image.ANTIALIAS)
                    self.enter_img_tk = ImageTk.PhotoImage(img_resized_driver)
                    self.enter_img_label.configure(image=self.enter_img_tk)
                else:
                    enter_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                          color='#171010')
                    self.enter_img_tk = ImageTk.PhotoImage(enter_img)
                    self.enter_img_label.configure(image=self.enter_img_tk)

                self.enter_scan_label.configure(text='Scanned\t: ' + self.enter_manual_str.get().upper())
                self.enter_stat_label.configure(text='Status\t: ' + db_stat)
                if result:
                    self.enter_rec = 'RECOGNISED'
                    self.enter_manual_str.set(result[0][2])
                    self.enter_role_label.configure(text='Role\t: ' + role)
                    self.enter_name_label.configure(text='Name\t: ' + result[0][1])
                    self.enter_id_label.configure(text='ID Num.\t: ' + result[0][0])
                else:
                    self.enter_rec = 'UNRECOGNISED'
                    self.enter_manual_str.set(self.enter_manual_str.get().upper())
                    self.enter_role_label.configure(text='Role\t: -')
                    self.enter_name_label.configure(text='Name\t: -')
                    self.enter_id_label.configure(text='ID Num.\t: -')
            elif type == 2 and self.exit_manual_str.get():
                self.exit_occupied = True
                db_stat, result, role = db.find_driver(self.exit_manual_str.get())
                print('Search:', result)
                fl_stat = False
                if result:
                    fl_stat, file = fl.dw_from_server(path_driver, result[0][0], 1)
                    print('Image: ', file)
                if fl_stat:
                    img_driver = Image.open(os.path.join(path_driver, file))
                    img_resized_driver = img_driver.resize((round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                                           Image.ANTIALIAS)
                    self.exit_img_tk = ImageTk.PhotoImage(img_resized_driver)
                    self.exit_img_label.configure(image=self.exit_img_tk)
                else:
                    exit_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                         color='#171010')
                    self.exit_img_tk = ImageTk.PhotoImage(exit_img)
                    self.exit_img_label.configure(image=self.exit_img_tk)

                self.exit_scan_label.configure(text='Scanned\t: ' + self.exit_manual_str.get().upper())
                self.exit_stat_label.configure(text='Status\t: ' + db_stat)
                if result:
                    self.exit_rec = 'RECOGNISED'
                    self.exit_manual_str.set(result[0][2])
                    self.exit_role_label.configure(text='Role\t: ' + role)
                    self.exit_name_label.configure(text='Name\t: ' + result[0][1])
                    self.exit_id_label.configure(text='ID Num.\t: ' + result[0][0])
                else:
                    self.exit_rec = 'UNRECOGNISED'
                    self.exit_manual_str.set(self.exit_manual_str.get().upper())
                    self.exit_role_label.configure(text='Role\t: -')
                    self.exit_name_label.configure(text='Name\t: -')
                    self.exit_id_label.configure(text='ID Num.\t: -')

        def update_res(self, root, tab_size):
            margin = [round(0.01 * tab_size[0]), round(0.01 * tab_size[1])]

            self.configure(width=tab_size[0], height=tab_size[1])
            # Frame(self.tabs, width=tab_size[0], height=tab_size[1],
            #                           bg=self.color_root[self.theme][1])
            self.update()

            y_coord = 0
            self.canvas_frame[0].configure(width=tab_size[0], height=round(tab_size[1] / 2))
            self.coords(self.canvas_item[0], (0, y_coord))
            y_coord = y_coord + round(tab_size[1] / 2)

            self.canvas_frame[1].configure(width=tab_size[0], height=round(tab_size[1] / 2))
            self.coords(self.canvas_item[1], (0, y_coord))

            font_setting = "calibri " + str(root.font_size) + " bold"
            self.enter_label.configure(font=font_setting)
            self.exit_label.configure(font=font_setting)
            self.enter_label.update()
            self.exit_label.update()

            # ENTER INIT
            font_setting = "calibri " + str(round(root.font_size * 0.75))
            self.enter_manual_label.configure(font=font_setting)
            self.enter_scan_label.configure(font=font_setting)
            self.enter_stat_label.configure(font=font_setting)
            self.enter_role_label.configure(font=font_setting)
            self.enter_name_label.configure(font=font_setting)
            self.enter_id_label.configure(font=font_setting, )

            enter_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                  color='#171010')
            self.enter_img_tk = ImageTk.PhotoImage(enter_img)
            self.enter_img_label.configure(font=font_setting, image=self.enter_img_tk)

            font_setting = "calibri " + str(round(root.font_size * 0.7))
            self.enter_manual_entry.configure(font=font_setting)

            font_setting = "calibri " + str(round(root.font_size ** (1. / 1.28))) + " bold"
            self.enter_enter_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))
            self.enter_confirm_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))
            self.enter_clear_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))
            self.enter_scan_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))

            self.enter_manual_label.update()
            self.enter_scan_label.update()
            self.enter_img_label.update()
            self.enter_stat_label.update()
            self.enter_role_label.update()
            self.enter_name_label.update()
            self.enter_id_label.update()

            self.enter_manual_entry.update()

            self.enter_enter_btn.update()
            self.enter_confirm_btn.update()
            self.enter_clear_btn.update()
            self.enter_scan_btn.update()

            # EXIT INIT
            font_setting = "calibri " + str(round(root.font_size * 0.75))
            self.exit_manual_label.configure(font=font_setting)
            self.exit_scan_label.configure(font=font_setting)
            self.exit_stat_label.configure(font=font_setting)
            self.exit_role_label.configure(font=font_setting)
            self.exit_name_label.configure(font=font_setting)
            self.exit_id_label.configure(font=font_setting)

            exit_img = Image.new('RGB', (round(tab_size[0] * 0.3), round(tab_size[0] * 0.3)),
                                 color='#171010')
            self.exit_img_tk = ImageTk.PhotoImage(exit_img)
            self.exit_img_label.configure(font=font_setting, image=self.exit_img_tk)

            font_setting = "calibri " + str(round(root.font_size * 0.7))
            self.exit_manual_entry.configure(font=font_setting)

            font_setting = "calibri " + str(round(root.font_size ** (1. / 1.28))) + " bold"
            self.exit_enter_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))
            self.exit_confirm_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))
            self.exit_clear_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))
            self.exit_scan_btn.configure(font=font_setting, width=round(tab_size[0] * 0.02))

            self.exit_manual_label.update()
            self.exit_scan_label.update()
            self.exit_img_label.update()
            self.exit_stat_label.update()
            self.exit_role_label.update()
            self.exit_name_label.update()
            self.exit_id_label.update()

            self.exit_manual_entry.update()

            self.exit_enter_btn.update()
            self.exit_confirm_btn.update()
            self.exit_clear_btn.update()
            self.exit_scan_btn.update()

            # ENTER COORD
            y_coord_enter = self.enter_label.winfo_height()
            self.enter_manual_label.place(x=margin[0], y=y_coord_enter)
            self.enter_manual_entry.place(x=margin[0] + self.enter_manual_label.winfo_width(), y=y_coord_enter)
            y_coord_enter = y_coord_enter + self.enter_manual_label.winfo_height()
            self.enter_enter_btn.place(x=margin[0] + self.enter_manual_label.winfo_width() +
                                         self.enter_manual_entry.winfo_width() - self.enter_enter_btn.winfo_width() * 0.95,
                                       y=y_coord_enter)
            y_coord_enter = y_coord_enter + self.enter_enter_btn.winfo_height() * 1.1
            self.enter_scan_label.place(x=margin[0], y=y_coord_enter)

            y_coord_enter = (tab_size[1] / 2) - self.enter_id_label.winfo_height() * 1.1
            self.enter_id_label.place(x=margin[0], y=y_coord_enter)
            y_coord_enter = y_coord_enter - self.enter_name_label.winfo_height()
            self.enter_name_label.place(x=margin[0], y=y_coord_enter)
            y_coord_enter = y_coord_enter - self.enter_role_label.winfo_height()
            self.enter_role_label.place(x=margin[0], y=y_coord_enter)
            y_coord_enter = y_coord_enter - self.enter_stat_label.winfo_height()
            self.enter_stat_label.place(x=margin[0], y=y_coord_enter)

            self.enter_img_label.place(x=tab_size[0] - self.enter_img_label.winfo_width(), y=0)

            y_coord_btn = tab_size[1] / 2 - self.enter_confirm_btn.winfo_height() - margin[1]
            self.enter_confirm_btn.place(x=tab_size[0] - self.enter_confirm_btn.winfo_width() - margin[0],
                                         y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.enter_confirm_btn.winfo_height() * 1.1
            self.enter_clear_btn.place(x=tab_size[0] - self.enter_confirm_btn.winfo_width() - margin[0],
                                       y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.enter_clear_btn.winfo_height() * 1.1
            self.enter_scan_btn.place(x=tab_size[0] - self.enter_confirm_btn.winfo_width() - margin[0],
                                      y=y_coord_btn)

            # ENTER COORD
            y_coord_exit = self.exit_label.winfo_height()
            self.exit_manual_label.place(x=margin[0], y=y_coord_exit)
            self.exit_manual_entry.place(x=margin[0] + self.exit_manual_label.winfo_width(), y=y_coord_exit)
            y_coord_exit = y_coord_exit + self.exit_manual_label.winfo_height()
            self.exit_enter_btn.place(x=margin[0] + self.exit_manual_label.winfo_width() +
                                        self.exit_manual_entry.winfo_width() - self.exit_enter_btn.winfo_width() * 0.95,
                                      y=y_coord_exit)
            y_coord_exit = y_coord_exit + self.exit_enter_btn.winfo_height() * 1.1
            self.exit_scan_label.place(x=margin[0], y=y_coord_exit)

            y_coord_exit = (tab_size[1] / 2) - self.exit_id_label.winfo_height() * 1.1
            self.exit_id_label.place(x=margin[0], y=y_coord_exit)
            y_coord_exit = y_coord_exit - self.exit_name_label.winfo_height()
            self.exit_name_label.place(x=margin[0], y=y_coord_exit)
            y_coord_exit = y_coord_exit - self.exit_role_label.winfo_height()
            self.exit_role_label.place(x=margin[0], y=y_coord_exit)
            y_coord_exit = y_coord_exit - self.exit_stat_label.winfo_height()
            self.exit_stat_label.place(x=margin[0], y=y_coord_exit)

            self.exit_img_label.place(x=tab_size[0] - self.exit_img_label.winfo_width(), y=0)

            y_coord_btn = tab_size[1] / 2 - self.exit_confirm_btn.winfo_height() - margin[1]
            self.exit_confirm_btn.place(x=tab_size[0] - self.exit_confirm_btn.winfo_width() - margin[0],
                                        y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.exit_confirm_btn.winfo_height() * 1.1
            self.exit_clear_btn.place(x=tab_size[0] - self.exit_confirm_btn.winfo_width() - margin[0],
                                      y=y_coord_btn)
            y_coord_btn = y_coord_btn - self.exit_clear_btn.winfo_height() * 1.1
            self.exit_scan_btn.place(x=tab_size[0] - self.exit_confirm_btn.winfo_width() - margin[0],
                                     y=y_coord_btn)

            self.enter_scan_btn.configure(command=lambda a=1, b=root, c=tab_size: self.button_scan(a, b, c))
            self.enter_clear_btn.configure(command=lambda a=1, b=tab_size: self.button_clear(a, b))
            self.enter_enter_btn.configure(command=lambda a=1, b=tab_size: self.button_enter(a, b))
            self.enter_confirm_btn.configure(command=lambda a=1, b=root: self.button_confirm(a, b))

            self.exit_scan_btn.configure(command=lambda a=2, b=root, c=tab_size: self.button_scan(a, b, c))
            self.exit_clear_btn.configure(command=lambda a=2, b=tab_size: self.button_clear(a, b))
            self.exit_enter_btn.configure(command=lambda a=2, b=tab_size: self.button_enter(a, b))
            self.exit_confirm_btn.configure(command=lambda a=2, b=root: self.button_confirm(a, b))

        def change_theme(self, theme):
            self.configure(bg=CP[theme][1])
            # Frame(self.tabs, width=tab_size[0], height=tab_size[1],
            #                           bg=self.color_root[self.theme][1])
            self.canvas_frame[0].configure(bg=CP[theme][5])
            self.canvas_frame[1].configure(bg=CP[theme][5])
            # self.itemconfigure(self.canvas_item[0], bg=CP[theme][5])
            # self.itemconfigure(self.canvas_item[1], bg=CP[theme][5])

            self.enter_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_label.configure(bg=CP[theme][5], fg=CP[theme][1])

            # ENTER INIT
            self.enter_manual_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.enter_scan_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.enter_stat_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.enter_role_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.enter_name_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.enter_id_label.configure(bg=CP[theme][5], fg=CP[theme][1])

            self.enter_img_label.configure(bg=CP[theme][1])
            self.enter_enter_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.enter_confirm_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.enter_clear_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.enter_scan_btn.configure(bg=CP[theme][10], fg=CP[theme][11])

            # EXIT INIT
            self.exit_manual_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_scan_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_stat_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_role_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_name_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_id_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_img_label.configure(bg=CP[theme][1])

            self.exit_enter_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.exit_confirm_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.exit_clear_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.exit_scan_btn.configure(bg=CP[theme][10], fg=CP[theme][11])

    class LogFrame(Frame):
        def __init__(self, root, tab_size):
            self.borderwidth = 1
            self.canvas_item = []
            self.canvas_frame = []
            self.enter_log = []
            self.exit_log = []
            self.enter_frame = []
            self.exit_frame = []
            self.enter_item = []
            self.exit_item = []
            self.enter_frame_height = 0
            self.exit_frame_height = 0

            super().__init__(root.tabs, width=tab_size[0], height=tab_size[1], bg=CP[root.theme][5])
            self.place(x=0, y=0)
            self.update()

            font_setting = root.font_style + " " + str(round(root.font_size + root.font_size / 4)) + " bold"
            self.label_date_prev = Label(self, text='<', font=font_setting, padx=5,
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.label_date_next = Label(self, text='>', font=font_setting, padx=5,
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.label_date_prev.place(x=self.winfo_width(), y=self.winfo_height())
            self.label_date_next.place(x=self.winfo_width(), y=self.winfo_height())
            self.label_date_prev.update()
            self.label_date_next.update()

            """
            self.frame_scroll = Frame(self, width=self.winfo_width(),
                                      height=self.winfo_height() - self.label_date_prev.winfo_height())
            self.frame_scroll.place(x=0, y=self.label_date_prev.winfo_height())

            self.scroll = Scrollbar(self.frame_scroll, bg=CP[root.theme][1], orient="vertical")
            self.scroll.pack(side=RIGHT, fill=Y)
            # self.scroll_view.place(x=0, y=0)
            self.scroll.update()
            self.frame_scroll.config(width=self.winfo_width() - self.scroll.winfo_width() / 2)
            self.frame_scroll.update()

            self.canvas = Canvas(self.frame_scroll, width=self.frame_scroll.winfo_width(),
                                 height=self.frame_scroll.winfo_height(),
                                 bg=CP[root.theme][5], highlightthickness=0)
            self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
            self.canvas.configure(yscrollcommand=self.scroll.set)
            self.scroll.configure(command=self.canvas.yview)

            if self.list_log:
                self.scroll.pack(side=RIGHT, fill=Y)
                # self.scroll_view.place(x=0, y=0)
                self.scroll.update()
                self.frame_scroll.config(width=self.winfo_width())
                self.frame_scroll.update()
                self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.canvas.configure(yscrollcommand=self.scroll.set,
                                      width=self.frame_scroll.winfo_width() - self.scroll.winfo_width() / 2,
                                      height=self.frame_scroll.winfo_height())
            else:
                # self.scroll_view.place(x=0, y=0)
                self.frame_scroll.config(width=self.winfo_width())
                self.frame_scroll.update()
                self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.canvas.configure(yscrollcommand=self.scroll.set,
                                      width=self.frame_scroll.winfo_width(),
                                      height=self.frame_scroll.winfo_height())

            self.scroll.configure(command=self.canvas.yview)
            """

            self.view_canvas = Canvas(self, bg=CP[root.theme][1], width=self.winfo_width(),
                                      height=self.winfo_height() - self.label_date_prev.winfo_height())
            self.view_canvas.place(x=0, y=self.label_date_prev.winfo_height())
            self.view_canvas.update()

            y_coord = 0
            enter_frame = Frame(self.view_canvas, width=self.winfo_width(),
                                height=round((self.winfo_height() - self.label_date_prev.winfo_height()) / 2),
                                bg=CP[root.theme][5], highlightthickness=self.borderwidth)
            enter_frame.place(x=self.view_canvas.winfo_width(), y=self.view_canvas.winfo_height())
            enter_frame.update()
            enter_frame.place_forget()
            enter_item = self.view_canvas.create_window((0, y_coord), window=enter_frame, anchor=NW)
            self.canvas_frame.append(enter_frame)
            self.canvas_item.append(enter_item)

            y_coord = y_coord + round(self.view_canvas.winfo_height() / 2)
            exit_frame = Frame(self.view_canvas, width=self.winfo_width(),
                               height=round((self.winfo_height() - self.label_date_prev.winfo_height()) / 2),
                               bg=CP[root.theme][5], highlightthickness=self.borderwidth)
            exit_frame.place(x=self.view_canvas.winfo_width(), y=self.view_canvas.winfo_height())
            exit_frame.update()
            exit_frame.place_forget()
            exit_item = self.view_canvas.create_window((0, y_coord), window=exit_frame, anchor=NW)
            self.canvas_frame.append(exit_frame)
            self.canvas_item.append(exit_item)

            self.enter_lbl_frame = Frame(enter_frame, width=enter_frame.winfo_width() - self.borderwidth * 2,
                                         height=1, bg=CP[root.theme][5])
            self.enter_lbl_frame.place(x=0, y=0)
            self.enter_lbl_frame.update()
            self.exit_lbl_frame = Frame(exit_frame, width=exit_frame.winfo_width() - self.borderwidth * 2,
                                        height=1, bg=CP[root.theme][5])
            self.exit_lbl_frame.place(x=0, y=0)
            self.exit_lbl_frame.update()

            font_setting = root.font_style + " " + str(round(root.font_size * 0.75)) + " bold"
            self.enter_label = Label(self.enter_lbl_frame, font=font_setting, text='Enter',
                                     bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.exit_label = Label(self.exit_lbl_frame, font=font_setting, text='Exit',
                                    bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.enter_label.place(x=0, y=0)
            self.exit_label.place(x=0, y=0)
            self.enter_label.update()
            self.exit_label.update()
            self.enter_label.place(x=enter_frame.winfo_width() / 2 - self.enter_label.winfo_width() / 2, y=0)
            self.exit_label.place(x=exit_frame.winfo_width() / 2 - self.exit_label.winfo_width() / 2, y=0)
            self.enter_lbl_frame.config(height=self.enter_label.winfo_height())
            self.exit_lbl_frame.config(height=self.exit_label.winfo_height())
            self.enter_lbl_frame.update()
            self.exit_lbl_frame.update()

            # ENTER SCROLL LAYOOUT
            self.enter_scroll_frame = Frame(enter_frame, width=enter_frame.winfo_width() - self.borderwidth * 2,
                                            height=enter_frame.winfo_height() - self.enter_lbl_frame.winfo_height() -
                                                   self.borderwidth * 2, highlightthickness=0)
            self.enter_scroll_frame.place(x=0, y=self.enter_lbl_frame.winfo_height())

            self.enter_scroll = Scrollbar(self.enter_scroll_frame, bg=CP[root.theme][1], orient="vertical")
            self.enter_scroll.pack(side=RIGHT, fill=Y)
            # self.enter_scroll.place(x=enter_frame.winfo_width(),
            #                         y=self.enter_lbl_frame.winfo_height())
            # self.scroll_view.place(x=0, y=0)
            self.enter_scroll.update()
            self.enter_scroll_canvas = Canvas(self.enter_scroll_frame,
                                              width=enter_frame.winfo_width() - self.borderwidth * 2,
                                              height=enter_frame.winfo_height() - self.enter_lbl_frame.winfo_height() -
                                                     self.borderwidth * 2,
                                              bg=CP[root.theme][5], highlightthickness=0)
            self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            # self.enter_scroll_canvas.place(x=0, y=self.enter_lbl_frame.winfo_height())
            self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set)
            self.enter_scroll.configure(command=self.enter_scroll_canvas.yview)
            # self.enter_scroll_canvas.configure(width=enter_frame.winfo_width() - self.borderwidth * 2 - self.enter_scroll.winfo_width())

            # EXIT SCROLL LAYOOUT
            self.exit_scroll_frame = Frame(exit_frame, width=exit_frame.winfo_width() - self.borderwidth * 2,
                                           height=exit_frame.winfo_height() - self.exit_lbl_frame.winfo_height() -
                                                  self.borderwidth * 2, highlightthickness=0)
            self.exit_scroll_frame.place(x=0, y=self.exit_lbl_frame.winfo_height())

            self.exit_scroll = Scrollbar(self.exit_scroll_frame, bg=CP[root.theme][1], orient="vertical")
            self.exit_scroll.pack(side=RIGHT, fill=Y)
            # self.exit_scroll.place(x=exit_frame.winfo_width(),
            #                         y=self.exit_lbl_frame.winfo_height())
            # self.scroll_view.place(x=0, y=0)
            self.exit_scroll.update()
            self.exit_scroll_canvas = Canvas(self.exit_scroll_frame,
                                             width=exit_frame.winfo_width() - self.borderwidth * 2,
                                             height=exit_frame.winfo_height() - self.exit_lbl_frame.winfo_height() -
                                                    self.borderwidth * 2,
                                             bg=CP[root.theme][5], highlightthickness=0)
            self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            # self.exit_scroll_canvas.place(x=0, y=self.exit_lbl_frame.winfo_height())
            self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set)
            self.exit_scroll.configure(command=self.exit_scroll_canvas.yview)
            # self.exit_scroll_canvas.configure(width=exit_frame.winfo_width() - self.borderwidth * 2 - self.exit_scroll.winfo_width())

            # DATE
            temp = str(root.today).split('-')
            font_setting = root.font_style + " " + str(root.font_size)
            text_date = str(temp[2]) + " " + MONTH[temp[1]] + " " + str(temp[0])
            self.label_date = Label(self, text=text_date, font=font_setting, padx=7, pady=3,
                                    bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.label_date.place(x=self.winfo_width(), y=self.winfo_height())
            self.label_date.update()
            self.calendar = cal.Calendar(self, year=int(temp[0]),
                                         month=int(temp[1]), day=int(temp[2]))  # selectmode="day"

            # SEARCHING LOG
            self.enter_log, self.exit_log = db.get_log(str(root.today))
            print(self.enter_log)
            print(self.exit_log)
            font_setting = root.font_style + " " + str(round(root.font_size * 0.7))
            if self.enter_log:
                y_coord = 0
                # Partitioning
                x_part_3 = self.enter_scroll_canvas.winfo_width() / 3
                x_part_4 = self.enter_scroll_canvas.winfo_width() / 4
                x_part_5 = self.enter_scroll_canvas.winfo_width() / 5
                font_setting_2 = root.font_style + " " + str(round(root.font_size * 0.71)) + ' bold'
                for i in range(-1, len(self.enter_log)):
                    sub_frame = Frame(self.enter_scroll_canvas, width=self.enter_scroll_canvas.winfo_width(),
                                      height=1, bg=CP[root.theme][5], highlightthickness=0)

                    time_lbl = None
                    plate_lbl = None
                    recog_lbl = None
                    gate_lbl = None
                    if i == -1:
                        time_lbl = Label(sub_frame, font=font_setting_2, text='TIME',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting_2, text='PLATE NUM',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting_2, text='RECOGNITION',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting_2, text='GATE',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                    else:
                        time_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][0],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][1],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][2],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][3],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])

                    x_coord = 0
                    time_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_5
                    plate_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_4
                    recog_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_3
                    gate_lbl.place(x=x_coord, y=0)
                    time_lbl.update()
                    plate_lbl.update()
                    recog_lbl.update()
                    gate_lbl.update()

                    sub_frame.config(height=time_lbl.winfo_height())
                    sub_frame.update()

                    enter_item = self.enter_scroll_canvas.create_window((0, y_coord), window=sub_frame, anchor=NW)
                    self.enter_frame.append([sub_frame, time_lbl, plate_lbl, recog_lbl, gate_lbl])
                    self.enter_item.append(enter_item)
                    y_coord = y_coord + time_lbl.winfo_height()
                self.enter_frame_height = y_coord

            if self.exit_log:
                y_coord = 0
                # Partitioning
                x_part_3 = self.exit_scroll_canvas.winfo_width() / 3
                x_part_4 = self.exit_scroll_canvas.winfo_width() / 4
                x_part_5 = self.exit_scroll_canvas.winfo_width() / 5
                font_setting_2 = root.font_style + " " + str(round(root.font_size * 0.71)) + ' bold'
                for i in range(-1, len(self.exit_log)):
                    sub_frame = Frame(self.exit_scroll_canvas, width=self.exit_scroll_canvas.winfo_width(),
                                      height=1, bg=CP[root.theme][5], highlightthickness=0)

                    time_lbl = None
                    plate_lbl = None
                    recog_lbl = None
                    gate_lbl = None
                    if i == -1:
                        time_lbl = Label(sub_frame, font=font_setting_2, text='TIME',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting_2, text='PLATE NUM',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting_2, text='RECOGNITION',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting_2, text='GATE',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                    else:
                        time_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][0],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][1],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][2],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][3],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])

                    x_coord = 0
                    time_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_5
                    plate_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_4
                    recog_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_3
                    gate_lbl.place(x=x_coord, y=0)
                    time_lbl.update()
                    plate_lbl.update()
                    recog_lbl.update()
                    gate_lbl.update()

                    sub_frame.config(height=time_lbl.winfo_height())
                    sub_frame.update()

                    exit_item = self.exit_scroll_canvas.create_window((0, y_coord), window=sub_frame, anchor=NW)
                    self.exit_frame.append([sub_frame, time_lbl, plate_lbl, recog_lbl, gate_lbl])
                    self.exit_item.append(exit_item)
                    y_coord = y_coord + time_lbl.winfo_height()
                self.exit_frame_height = y_coord
                self.exit_scroll_canvas.configure(scrollregion=self.exit_scroll_canvas.bbox("all"))

            # ENTER SCROLLING CONFIGURATION
            if self.enter_scroll_canvas.winfo_height() <= self.enter_frame_height:
                self.enter_scroll.pack(side=RIGHT, fill=Y)
                # self.scroll_view.place(x=0, y=0)
                self.enter_scroll.update()
                # self.enter_scroll_canvas.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set,
                                                   width=enter_frame.winfo_width() - self.borderwidth * 2 -
                                                         self.enter_scroll.winfo_width())
                self.enter_scroll_canvas.configure(scrollregion=self.enter_scroll_canvas.bbox("all"))
            else:
                # self.scroll_view.place(x=0, y=0)
                # self.frame_scroll.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set,
                                                   width=enter_frame.winfo_width() - self.borderwidth * 2)

            # EXIT SCROLLING CONFIGURATION
            if self.exit_scroll_canvas.winfo_height() <= self.exit_frame_height:
                self.exit_scroll.pack(side=RIGHT, fill=Y)
                # self.scroll_view.place(x=0, y=0)
                self.exit_scroll.update()
                # self.exit_scroll_canvas.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set,
                                                  width=exit_frame.winfo_width() - self.borderwidth * 2 -
                                                        self.exit_scroll.winfo_width())
                self.exit_scroll_canvas.configure(scrollregion=self.exit_scroll_canvas.bbox("all"))
            else:
                # self.scroll_view.place(x=0, y=0)
                # self.frame_scroll.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set,
                                                  width=exit_frame.winfo_width() - self.borderwidth * 2)

            """
            self.label_date.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2,
                                  y=round(5 / 100 * tab_size[1]) +
                                    (self.label_date_prev.winfo_height() - self.label_date.winfo_height()) / 2)
            self.label_date_prev.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2 -
                                         self.label_date_prev.winfo_width(), y=round(5 / 100 * tab_size[1]))
            self.label_date_next.place(x=tab_size[0] / 2 + self.label_date.winfo_width() / 2,
                                       y=round(5 / 100 * tab_size[1]))
            """

            self.label_date_prev.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2 -
                                         self.label_date_prev.winfo_width(), y=0)
            self.label_date_next.place(x=tab_size[0] / 2 + self.label_date.winfo_width() / 2, y=0)
            self.label_date.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2,
                                  y=self.label_date_prev.winfo_height() / 2 - self.label_date.winfo_height() / 2)

            self.calendar_visib = False
            self.calendar.place(x=root.tabs.winfo_width(), y=root.tabs.winfo_height())
            self.calendar.update()
            self.calendar.place_forget()

            # self.enter_scroll_canvas.bind_all("<MouseWheel>", lambda event, a=1: self._on_mousewheel(event, a))
            # self.exit_scroll_canvas.bind_all("<MouseWheel>", lambda event, a=2: self._on_mousewheel(event, a))
            self.enter_scroll_canvas.bind('<Enter>', lambda event, a=1: self._bound_to_mousewheel(event, a))
            self.enter_scroll_canvas.bind('<Leave>', lambda event, a=1: self._unbound_to_mousewheel(event, a))
            self.exit_scroll_canvas.bind('<Enter>', lambda event, a=2: self._bound_to_mousewheel(event, a))
            self.exit_scroll_canvas.bind('<Leave>', lambda event, a=2: self._unbound_to_mousewheel(event, a))

            self.label_date.bind("<ButtonPress>", lambda event, a=2: root.on_press(event, a))
            self.label_date_prev.bind("<ButtonPress>", lambda event, a=3: root.on_press(event, a))
            self.label_date_next.bind("<ButtonPress>", lambda event, a=4: root.on_press(event, a))
            root.tabs.bind("<ButtonRelease>", lambda event, a=5: root.on_release(event, a))
            self.label_date.bind("<ButtonRelease>", lambda event, a=2: root.on_release(event, a))
            self.label_date_prev.bind("<ButtonRelease>", lambda event, a=3: root.on_release(event, a))
            self.label_date_next.bind("<ButtonRelease>", lambda event, a=4: root.on_release(event, a))
            root.tabs.bind("<ButtonRelease>", lambda event, a=5: root.on_release(event, a))
            self.calendar.bind("<<CalendarSelected>>", lambda event: root.select_date(event))

        def update_res(self, root, tab_size):
            self.config(width=tab_size[0], height=tab_size[1])
            self.update()

            font_setting = root.font_style + " " + str(round(root.font_size + root.font_size / 4)) + " bold"
            self.label_date_prev.configure(font=font_setting)
            self.label_date_next.configure(font=font_setting)
            self.label_date_prev.place(x=tab_size[0], y=tab_size[1])
            self.label_date_next.place(x=tab_size[0], y=tab_size[1])
            self.label_date_prev.update()
            self.label_date_next.update()

            print(tab_size[1])
            print(self.label_date_prev.winfo_height())

            self.view_canvas.configure(width=tab_size[0],
                                       height=tab_size[1] - self.label_date_prev.winfo_height())
            self.view_canvas.place(x=0, y=self.label_date_prev.winfo_height())
            self.view_canvas.update()

            self.view_canvas.delete('all')
            self.canvas_frame[0].configure(width=tab_size[0],
                                           height=round(
                                               (tab_size[1] - self.label_date_prev.winfo_height()) / 2))
            self.canvas_frame[0].place(x=self.view_canvas.winfo_width(), y=self.view_canvas.winfo_height())
            self.canvas_frame[0].update()
            self.canvas_frame[0].place_forget()
            self.canvas_frame[1].configure(width=tab_size[0],
                                           height=round(
                                               (tab_size[1] - self.label_date_prev.winfo_height()) / 2))
            self.canvas_frame[1].place(x=self.view_canvas.winfo_width(), y=self.view_canvas.winfo_height())
            self.canvas_frame[1].update()
            self.canvas_frame[1].place_forget()

            self.canvas_item = []
            y_coord = 0
            frame_item = self.view_canvas.create_window((0, y_coord), window=self.canvas_frame[0], anchor=NW)
            self.canvas_item.append(frame_item)
            # self.view_canvas.coords(self.canvas_item[0], (0, y_coord))
            y_coord = y_coord + round(self.view_canvas.winfo_height() / 2)
            frame_item = self.view_canvas.create_window((0, y_coord), window=self.canvas_frame[1], anchor=NW)
            self.canvas_item.append(frame_item)
            # self.view_canvas.coords(self.canvas_item[1], (0, y_coord))

            self.enter_lbl_frame.configure(width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2,
                                           height=1)
            self.enter_lbl_frame.place(x=0, y=0)
            self.enter_lbl_frame.update()
            self.exit_lbl_frame.configure(width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2,
                                          height=1)
            self.exit_lbl_frame.place(x=0, y=0)
            self.exit_lbl_frame.update()

            font_setting = root.font_style + " " + str(round(root.font_size * 0.75)) + " bold"
            self.enter_label.configure(font=font_setting)
            self.exit_label.configure(font=font_setting)
            self.enter_label.place(x=0, y=0)
            self.exit_label.place(x=0, y=0)
            self.enter_label.update()
            self.exit_label.update()
            self.enter_label.place(x=self.canvas_frame[0].winfo_width() / 2 - self.enter_label.winfo_width() / 2, y=0)
            self.exit_label.place(x=self.canvas_frame[1].winfo_width() / 2 - self.exit_label.winfo_width() / 2, y=0)
            self.enter_lbl_frame.config(height=self.enter_label.winfo_height())
            self.exit_lbl_frame.config(height=self.exit_label.winfo_height())
            self.enter_lbl_frame.update()
            self.exit_lbl_frame.update()

            # ENTER SCROLL LAYOOUT
            self.enter_scroll_frame.configure(width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2,
                                              height=self.canvas_frame[
                                                         0].winfo_height() - self.enter_lbl_frame.winfo_height() -
                                                     self.borderwidth * 2)
            self.enter_scroll_frame.place(x=0, y=self.enter_lbl_frame.winfo_height())
            self.enter_scroll.pack(side=RIGHT, fill=Y)
            self.enter_scroll.update()
            self.enter_scroll_canvas.configure(width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2,
                                               height=self.canvas_frame[
                                                          0].winfo_height() - self.enter_lbl_frame.winfo_height() -
                                                      self.borderwidth * 2)
            self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            self.enter_scroll_canvas.update()
            # self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set)
            # self.enter_scroll.configure(command=self.enter_scroll_canvas.yview)
            # self.enter_scroll_canvas.configure(width=enter_frame.winfo_width() - self.borderwidth * 2 - self.enter_scroll.winfo_width())

            # EXIT SCROLL LAYOOUT
            self.exit_scroll_frame.configure(width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2,
                                             height=self.canvas_frame[
                                                        1].winfo_height() - self.exit_lbl_frame.winfo_height() -
                                                    self.borderwidth * 2)
            self.exit_scroll_frame.place(x=0, y=self.exit_lbl_frame.winfo_height())

            self.exit_scroll.pack(side=RIGHT, fill=Y)
            self.exit_scroll.update()
            self.exit_scroll_canvas.configure(width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2,
                                              height=self.canvas_frame[
                                                         1].winfo_height() - self.exit_lbl_frame.winfo_height() -
                                                     self.borderwidth * 2)
            self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            self.exit_scroll_canvas.update()
            # self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set)
            # self.exit_scroll.configure(command=self.exit_scroll_canvas.yview)

            # DATE
            font_setting = root.font_style + " " + str(root.font_size)
            self.label_date.configure(font=font_setting)
            self.label_date.place(x=tab_size[0], y=tab_size[1])
            self.label_date.update()

            self.update_log_date(root)
            """
            # SEARCHING LOG
            font_setting = root.font_style + " " + str(round(root.font_size * 0.7))
            if self.enter_log:
                y_coord = 0
                # Partitioning
                x_part_3 = self.enter_scroll_canvas.winfo_width() / 3
                x_part_4 = self.enter_scroll_canvas.winfo_width() / 4
                x_part_5 = self.enter_scroll_canvas.winfo_width() / 5
                font_setting_2 = root.font_style + " " + str(round(root.font_size * 0.71)) + ' bold'
                for i, each in enumerate(self.enter_frame):
                    each[0].configure(width=self.enter_scroll_canvas.winfo_width(),
                                      height=1)
                    if i == 0:
                        each[1].configure(font=font_setting_2)
                        each[2].configure(font=font_setting_2)
                        each[3].configure(font=font_setting_2)
                        each[4].configure(font=font_setting_2)
                    else:
                        each[1].configure(font=font_setting)
                        each[2].configure(font=font_setting)
                        each[3].configure(font=font_setting)
                        each[4].configure(font=font_setting)

                    x_coord = 0
                    each[1].place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_5
                    each[2].place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_4
                    each[3].place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_3
                    each[4].place(x=x_coord, y=0)
                    each[1].update()
                    each[2].update()
                    each[3].update()
                    each[4].update()

                    each[0].config(height=each[1].winfo_height())
                    each[0].update()

                    self.enter_scroll_canvas.coords(self.enter_item[i], (0, y_coord))
                    y_coord = y_coord + each[0].winfo_height()
                self.enter_frame_height = y_coord
                self.enter_scroll_canvas.configure(scrollregion=self.enter_scroll_canvas.bbox("all"))

            if self.exit_log:
                y_coord = 0
                # Partitioning
                x_part_3 = self.exit_scroll_canvas.winfo_width() / 3
                x_part_4 = self.exit_scroll_canvas.winfo_width() / 4
                x_part_5 = self.exit_scroll_canvas.winfo_width() / 5
                font_setting_2 = root.font_style + " " + str(round(root.font_size * 0.71)) + ' bold'
                for i, each in enumerate(self.exit_frame):
                    each[0].configure(width=self.exit_scroll_canvas.winfo_width(),
                                      height=1)
                    if i == 0:
                        each[1].configure(font=font_setting_2)
                        each[2].configure(font=font_setting_2)
                        each[3].configure(font=font_setting_2)
                        each[4].configure(font=font_setting_2)
                    else:
                        each[1].configure(font=font_setting)
                        each[2].configure(font=font_setting)
                        each[3].configure(font=font_setting)
                        each[4].configure(font=font_setting)

                    x_coord = 0
                    each[1].place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_5
                    each[2].place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_4
                    each[3].place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_3
                    each[4].place(x=x_coord, y=0)
                    each[1].update()
                    each[2].update()
                    each[3].update()
                    each[4].update()

                    each[0].config(height=each[1].winfo_height())
                    each[0].update()

                    self.exit_scroll_canvas.coords(self.exit_item[i], (0, y_coord))
                    y_coord = y_coord + each[0].winfo_height()
                self.exit_frame_height = y_coord
                self.exit_scroll_canvas.configure(scrollregion=self.exit_scroll_canvas.bbox("all"))

            # ENTER SCROLLING CONFIGURATION
            if self.enter_scroll_canvas.winfo_height() <= self.enter_frame_height:
                self.enter_scroll.pack(side=RIGHT, fill=Y)
                self.enter_scroll_canvas.place(x=0, y=0)
                self.enter_scroll.update()
                self.enter_scroll_canvas.config(width=tab_size[0])
                self.enter_scroll_canvas.update()
                self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set,
                                                   width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2 -
                                                         self.enter_scroll.winfo_width())
            else:
                self.enter_scroll_canvas.place(x=0, y=0)
                self.enter_scroll_canvas.config(width=tab_size[0])
                self.enter_scroll_canvas.update()
                self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set,
                                                   width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2)
            self.enter_scroll_canvas.configure(scrollregion=self.enter_scroll_canvas.bbox("all"))

            # EXIT SCROLLING CONFIGURATION
            if self.exit_scroll_canvas.winfo_height() <= self.exit_frame_height:
                self.exit_scroll.pack(side=RIGHT, fill=Y)
                self.exit_scroll.place(x=0, y=0)
                self.exit_scroll.update()
                self.exit_scroll_canvas.config(width=tab_size[0])
                self.exit_scroll_canvas.update()
                self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set,
                                                  width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2 -
                                                        self.exit_scroll.winfo_width())
            else:
                self.exit_scroll.place(x=0, y=0)
                self.exit_scroll_canvas.config(width=tab_size[0])
                self.exit_scroll_canvas.update()
                self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set,
                                                  width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2)
            self.enter_scroll_canvas.configure(scrollregion=self.enter_scroll_canvas.bbox("all"))
            """

            self.label_date_prev.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2 -
                                         self.label_date_prev.winfo_width(), y=0)
            self.label_date_next.place(x=tab_size[0] / 2 + self.label_date.winfo_width() / 2, y=0)
            self.label_date.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2,
                                  y=self.label_date_prev.winfo_height() / 2 - self.label_date.winfo_height() / 2)
            self.calendar_visib = False
            self.calendar.place(x=root.tabs.winfo_width(), y=root.tabs.winfo_height())
            self.calendar.update()
            self.calendar.place_forget()

        def _bound_to_mousewheel(self, event, type):
            if type == 1:
                self.enter_scroll_canvas.bind_all("<MouseWheel>", lambda event, a=1: self._on_mousewheel(event, a))
            elif type == 2:
                self.exit_scroll_canvas.bind_all("<MouseWheel>", lambda event, a=2: self._on_mousewheel(event, a))

        def _unbound_to_mousewheel(self, event, type):
            if type == 1:
                self.enter_scroll_canvas.unbind_all("<MouseWheel>")
            elif type == 2:
                self.exit_scroll_canvas.unbind_all("<MouseWheel>")

        def _on_mousewheel(self, event, type):
            if type == 1:
                self.enter_scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif type == 2:
                self.exit_scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def update_log_date(self, root):
            date = self.label_date.cget('text')
            date = date.split(' ')
            date = date[2] + '-' + MONTH_NUM[date[1]] + '-' + date[0]
            self.enter_scroll_canvas.delete('all')
            self.exit_scroll_canvas.delete('all')
            self.enter_frame = []
            self.exit_frame = []
            self.enter_frame_height = 0
            self.exit_frame_height = 0

            # SEARCHING LOG
            self.enter_log, self.exit_log = db.get_log(date)
            print(self.enter_log)
            print(self.exit_log)
            font_setting = root.font_style + " " + str(round(root.font_size * 0.7))
            if self.enter_log:
                y_coord = 0
                # Partitioning
                x_part_3 = self.enter_scroll_canvas.winfo_width() / 3
                x_part_4 = self.enter_scroll_canvas.winfo_width() / 4
                x_part_5 = self.enter_scroll_canvas.winfo_width() / 5
                font_setting_2 = root.font_style + " " + str(round(root.font_size * 0.71)) + ' bold'
                for i in range(-1, len(self.enter_log)):
                    sub_frame = Frame(self.enter_scroll_canvas, width=self.enter_scroll_canvas.winfo_width(),
                                      height=1, bg=CP[root.theme][5], highlightthickness=0)

                    time_lbl = None
                    plate_lbl = None
                    recog_lbl = None
                    gate_lbl = None
                    if i == -1:
                        time_lbl = Label(sub_frame, font=font_setting_2, text='TIME',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting_2, text='PLATE NUM',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting_2, text='RECOGNITION',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting_2, text='GATE',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                    else:
                        time_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][0],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][1],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][2],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting, text=self.enter_log[i][3],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])

                    x_coord = 0
                    time_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_5
                    plate_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_4
                    recog_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_3
                    gate_lbl.place(x=x_coord, y=0)
                    time_lbl.update()
                    plate_lbl.update()
                    recog_lbl.update()
                    gate_lbl.update()

                    sub_frame.config(height=time_lbl.winfo_height())
                    sub_frame.update()

                    enter_item = self.enter_scroll_canvas.create_window((0, y_coord), window=sub_frame, anchor=NW)
                    self.enter_frame.append([sub_frame, time_lbl, plate_lbl, recog_lbl, gate_lbl])
                    self.enter_item.append(enter_item)
                    y_coord = y_coord + time_lbl.winfo_height()
                self.enter_frame_height = y_coord

            if self.exit_log:
                y_coord = 0
                # Partitioning
                x_part_3 = self.exit_scroll_canvas.winfo_width() / 3
                x_part_4 = self.exit_scroll_canvas.winfo_width() / 4
                x_part_5 = self.exit_scroll_canvas.winfo_width() / 5
                font_setting_2 = root.font_style + " " + str(round(root.font_size * 0.71)) + ' bold'
                for i in range(-1, len(self.exit_log)):
                    sub_frame = Frame(self.exit_scroll_canvas, width=self.exit_scroll_canvas.winfo_width(),
                                      height=1, bg=CP[root.theme][5], highlightthickness=0)

                    time_lbl = None
                    plate_lbl = None
                    recog_lbl = None
                    gate_lbl = None
                    if i == -1:
                        time_lbl = Label(sub_frame, font=font_setting_2, text='TIME',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting_2, text='PLATE NUM',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting_2, text='RECOGNITION',
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting_2, text='GATE',
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                    else:
                        time_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][0],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])
                        plate_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][1],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        recog_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][2],
                                          bg=CP[root.theme][5], fg=CP[root.theme][1])
                        gate_lbl = Label(sub_frame, font=font_setting, text=self.exit_log[i][3],
                                         bg=CP[root.theme][5], fg=CP[root.theme][1])

                    x_coord = 0
                    time_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_5
                    plate_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_4
                    recog_lbl.place(x=x_coord, y=0)
                    x_coord = x_coord + x_part_3
                    gate_lbl.place(x=x_coord, y=0)
                    time_lbl.update()
                    plate_lbl.update()
                    recog_lbl.update()
                    gate_lbl.update()

                    sub_frame.config(height=time_lbl.winfo_height())
                    sub_frame.update()

                    exit_item = self.exit_scroll_canvas.create_window((0, y_coord), window=sub_frame, anchor=NW)
                    self.exit_frame.append([sub_frame, time_lbl, plate_lbl, recog_lbl, gate_lbl])
                    self.exit_item.append(exit_item)
                    y_coord = y_coord + time_lbl.winfo_height()
                self.exit_frame_height = y_coord
                self.exit_scroll_canvas.configure(scrollregion=self.exit_scroll_canvas.bbox("all"))

            # ENTER SCROLLING CONFIGURATION
            if self.enter_scroll_canvas.winfo_height() <= self.enter_frame_height:
                self.enter_scroll.pack(side=RIGHT, fill=Y)
                # self.scroll_view.place(x=0, y=0)
                self.enter_scroll.update()
                # self.enter_scroll_canvas.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set,
                                                   width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2 -
                                                         self.enter_scroll.winfo_width())
                self.enter_scroll_canvas.configure(scrollregion=self.enter_scroll_canvas.bbox("all"))
            else:
                # self.scroll_view.place(x=0, y=0)
                # self.frame_scroll.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.enter_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.enter_scroll_canvas.configure(yscrollcommand=self.enter_scroll.set,
                                                   width=self.canvas_frame[0].winfo_width() - self.borderwidth * 2)

            # EXIT SCROLLING CONFIGURATION
            if self.exit_scroll_canvas.winfo_height() <= self.exit_frame_height:
                self.exit_scroll.pack(side=RIGHT, fill=Y)
                # self.scroll_view.place(x=0, y=0)
                self.exit_scroll.update()
                # self.exit_scroll_canvas.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set,
                                                  width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2 -
                                                        self.exit_scroll.winfo_width())
                self.exit_scroll_canvas.configure(scrollregion=self.exit_scroll_canvas.bbox("all"))
            else:
                # self.scroll_view.place(x=0, y=0)
                # self.frame_scroll.config(width=self.winfo_width())
                # self.frame_scroll.update()
                self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
                self.exit_scroll_canvas.configure(yscrollcommand=self.exit_scroll.set,
                                                  width=self.canvas_frame[1].winfo_width() - self.borderwidth * 2)

        def change_theme(self, theme):
            self.configure(bg=CP[theme][5])

            self.label_date_prev.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.label_date_next.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.view_canvas.configure(bg=CP[theme][1])

            for frame in self.canvas_frame:
                frame.configure(bg=CP[theme][5])

            self.enter_lbl_frame.configure(bg=CP[theme][5])
            self.exit_lbl_frame.configure(bg=CP[theme][5])
            self.enter_label.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.exit_label.configure(bg=CP[theme][5], fg=CP[theme][1])

            # ENTER SCROLL LAYOOUT
            self.enter_scroll.configure(bg=CP[theme][1])
            self.enter_scroll_canvas.configure(bg=CP[theme][5])

            # EXIT SCROLL LAYOOUT
            self.exit_scroll.configure(bg=CP[theme][1])
            self.exit_scroll_canvas.configure(bg=CP[theme][5])
            self.exit_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)

            # DATE
            self.label_date.configure(bg=CP[theme][5], fg=CP[theme][1])

            # SEARCHING LOG
            if self.enter_log:
                for i, each in enumerate(self.enter_frame):
                    each[0].configure(bg=CP[theme][5])
                    each[1].configure(bg=CP[theme][5], fg=CP[theme][1])
                    each[2].configure(bg=CP[theme][5], fg=CP[theme][1])
                    each[3].configure(bg=CP[theme][5], fg=CP[theme][1])
                    each[4].configure(bg=CP[theme][5], fg=CP[theme][1])

            if self.exit_log:
                for i, each in enumerate(self.exit_frame):
                    each[0].configure(bg=CP[theme][5])
                    each[1].configure(bg=CP[theme][5], fg=CP[theme][1])
                    each[2].configure(bg=CP[theme][5], fg=CP[theme][1])
                    each[3].configure(bg=CP[theme][5], fg=CP[theme][1])
                    each[4].configure(bg=CP[theme][5], fg=CP[theme][1])

    class Profile(Frame):
        def __init__(self, root, tab_size):
            super().__init__(root.tabs, width=tab_size[0], height=tab_size[1], bg=CP[root.theme][5])
            self.place(x=0, y=0)
            self.update()

            margin = [round(0.03 * tab_size[0]), round(0.05 * tab_size[1])]
            font_setting = "Calibri " + str(round(root.font_size * 1))
            self.profile_title = Label(self, text="Update Profile", font=font_setting,
                                       bg=CP[root.theme][5], fg=CP[root.theme][1])

            font_setting = "Calibri " + str(round(root.font_size * 0.8))
            self.name_lbl = Label(self, text="Name: ", font=font_setting,
                                  bg=CP[root.theme][5], fg=CP[root.theme][1])
            # self.username_lbl = Label(self, text="User Name: ", font=font_setting,
            #                           bg=CP[theme][0], fg=CP[theme][1])
            self.new_pass_lbl = Label(self, text="New Password: ", font=font_setting,
                                      bg=CP[root.theme][5], fg=CP[root.theme][1])
            self.conf_pass_lbl = Label(self, text="Confirm Password: ", font=font_setting,
                                       bg=CP[root.theme][5], fg=CP[root.theme][1])

            self.profile_title.place(x=tab_size[0], y=tab_size[1])
            self.name_lbl.place(x=tab_size[0], y=tab_size[1])
            self.new_pass_lbl.place(x=tab_size[0], y=tab_size[1])
            self.conf_pass_lbl.place(x=tab_size[0], y=tab_size[1])
            self.profile_title.update()
            self.name_lbl.update()
            self.new_pass_lbl.update()
            self.conf_pass_lbl.update()

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(root.font_size, 0.87)))
            self.name_str = StringVar()
            # self.username_str = StringVar()
            self.new_pass_str = StringVar()
            self.conf_pass_str = StringVar()

            pe = str(round(self.winfo_width() / 412))
            ttk.Style().configure('pad.TEntry', padding=(pe + ' 1 ' + pe + ' 1'))
            entry_length = 45
            self.name_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.name_str,
                                        font=font_setting, style='pad.TEntry')
            entry_length = round(entry_length / 2)
            # self.username_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.username_str,
            #                                 font=font_setting, style='pad.TEntry')
            self.new_pass_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.new_pass_str,
                                            font=font_setting, style='pad.TEntry', show='*')
            self.conf_pass_entry = ttk.Entry(self, width=round(entry_length), textvariable=self.conf_pass_str,
                                             font=font_setting, style='pad.TEntry', show='*')

            self.name_entry.place(x=tab_size[0], y=tab_size[1])
            self.new_pass_entry.place(x=tab_size[0], y=tab_size[1])
            self.conf_pass_entry.place(x=tab_size[0], y=tab_size[1])
            self.name_entry.update()
            self.new_pass_entry.update()
            self.conf_pass_entry.update()

            font_setting = "Calibri " + str(round(root.font_size * 0.65))
            self.name_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
                                          bg=CP[root.theme][10], fg=CP[root.theme][11],
                                          command=lambda a=1, b=root: self.update_profile(a, b))
            self.name_update_btn.place(x=tab_size[0], y=tab_size[1])
            self.name_update_btn.update()

            # self.username_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
            #                                   bg=CP[theme][5], fg=CP[theme][1],
            #                                   command=lambda a=2, b=root: self.update_profile(a, b))
            # self.username_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            # self.username_update_btn.update()
            # self.username_update_btn.place(x=coord[0] + self.username_entry.winfo_width() + margin_width / 5,
            #                                y=y_btn_username + self.username_entry.winfo_height() / 2 -
            #                                  self.username_update_btn.winfo_height() / 2)

            self.pass_update_btn = Button(self, text="Update", font=font_setting, padx=8, pady=1,
                                          bg=CP[root.theme][10], fg=CP[root.theme][11],
                                          command=lambda a=3, b=root: self.update_profile(a, b))
            # , command=lambda a=3, b=root: self.update_profile(a, b)
            self.pass_update_btn.place(x=tab_size[0], y=tab_size[1])
            self.pass_update_btn.update()

            font_setting = "Calibri " + str(round(root.font_size * 0.8))
            self.clear_btn = Button(self, text="Clear", font=font_setting, padx=15, pady=1,
                                    bg=CP[root.theme][10], fg=CP[root.theme][11], command=self.clear)
            self.clear_btn.place(x=tab_size[0], y=tab_size[1])
            self.clear_btn.update()

            # main_layout
            coord = [margin[0],  # tab_size[0] / 2 - self.name_entry.winfo_width() / 2
                     tab_size[1] / 7]

            self.profile_title.place(x=tab_size[0] / 2 - self.profile_title.winfo_width() / 2, y=margin[1])

            gap_label_entry = round(margin[1])
            gap_cat = round(margin[1])
            self.name_lbl.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.name_lbl.winfo_height()
            self.name_entry.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.name_entry.winfo_height() * 2 - self.name_update_btn.winfo_height() / 2
            self.name_update_btn.place(x=coord[0], y=coord[1])
            # coord[1] = coord[1] + gap_cat
            # self.username_lbl.place(x=coord[0], y=coord[1])
            # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            # y_btn_username = coord[1] + gap_label_entry
            coord[1] = coord[1] + self.name_update_btn.winfo_height() + gap_cat
            self.new_pass_lbl.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.new_pass_lbl.winfo_height()
            self.new_pass_entry.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.new_pass_entry.winfo_height() + gap_cat
            self.conf_pass_lbl.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.conf_pass_entry.winfo_height()
            self.conf_pass_entry.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.conf_pass_entry.winfo_height() * 2 - self.pass_update_btn.winfo_height() / 2
            self.pass_update_btn.place(x=coord[0], y=coord[1])
            self.clear_btn.place(x=tab_size[0] - margin[0] - self.clear_btn.winfo_width(),
                                 y=tab_size[1] - margin[1] - self.clear_btn.winfo_height())

            self.place_forget()

        def update_res(self, root, tab_size):
            self.configure(width=tab_size[0], height=tab_size[1])

            margin = [round(0.03 * tab_size[0]), round(0.05 * tab_size[1])]
            font_setting = "Calibri " + str(round(root.font_size * 1))
            self.profile_title.configure(font=font_setting)

            font_setting = "Calibri " + str(round(root.font_size * 0.8))
            self.name_lbl.configure(font=font_setting)
            # self.username_lbl.configure(font=font_setting)
            self.new_pass_lbl.configure(font=font_setting)
            self.conf_pass_lbl.configure(font=font_setting)

            self.profile_title.place(x=tab_size[0], y=tab_size[1])
            self.name_lbl.place(x=tab_size[0], y=tab_size[1])
            self.new_pass_lbl.place(x=tab_size[0], y=tab_size[1])
            self.conf_pass_lbl.place(x=tab_size[0], y=tab_size[1])
            self.profile_title.update()
            self.name_lbl.update()
            self.new_pass_lbl.update()
            self.conf_pass_lbl.update()

            # font_setting = "Calibri " + str(round(font_size * 0.75))
            font_setting = "Calibri " + str(round(math.pow(root.font_size, 0.87)))
            entry_length = 45
            self.name_entry.configure(font=font_setting)
            # self.username_entry.configure(font=font_setting)
            self.new_pass_entry.configure(font=font_setting)
            self.conf_pass_entry.configure(font=font_setting)

            self.name_entry.place(x=tab_size[0], y=tab_size[1])
            self.new_pass_entry.place(x=tab_size[0], y=tab_size[1])
            self.conf_pass_entry.place(x=tab_size[0], y=tab_size[1])
            self.name_entry.update()
            self.new_pass_entry.update()
            self.conf_pass_entry.update()

            font_setting = "Calibri " + str(round(root.font_size * 0.65))
            self.name_update_btn.configure(font=font_setting)
            self.name_update_btn.place(x=tab_size[0], y=tab_size[1])
            self.name_update_btn.update()

            # self.username_update_btn.configure(font=font_setting)
            # self.username_update_btn.place(x=root.winfo_width(), y=root.winfo_height())
            # self.username_update_btn.update()
            # self.username_update_btn.place(x=coord[0] + self.username_entry.winfo_width() + margin_width / 5,
            #                                y=y_btn_username + self.username_entry.winfo_height() / 2 -
            #                                  self.username_update_btn.winfo_height() / 2)

            self.pass_update_btn.configure(font=font_setting)
            # , command=lambda a=3, b=root: self.update_profile(a, b)
            self.pass_update_btn.place(x=tab_size[0], y=tab_size[1])
            self.pass_update_btn.update()

            font_setting = "Calibri " + str(round(root.font_size * 0.8))
            self.clear_btn.configure(font=font_setting)
            self.clear_btn.place(x=tab_size[0], y=tab_size[1])
            self.clear_btn.update()

            # main_layout
            coord = [margin[0],  # tab_size[0] / 2 - self.name_entry.winfo_width() / 2
                     tab_size[1] / 7]

            self.profile_title.place(x=tab_size[0] / 2 - self.profile_title.winfo_width() / 2, y=margin[1])

            gap_label_entry = round(margin[1])
            gap_cat = round(margin[1])
            self.name_lbl.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.name_lbl.winfo_height()
            self.name_entry.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.name_entry.winfo_height() * 2 - self.name_update_btn.winfo_height() / 2
            self.name_update_btn.place(x=coord[0], y=coord[1])
            # coord[1] = coord[1] + gap_cat
            # self.username_lbl.place(x=coord[0], y=coord[1])
            # self.username_entry.place(x=coord[0], y=coord[1] + gap_label_entry)
            # y_btn_username = coord[1] + gap_label_entry
            coord[1] = coord[1] + self.name_update_btn.winfo_height() + gap_cat
            self.new_pass_lbl.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.new_pass_lbl.winfo_height()
            self.new_pass_entry.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.new_pass_entry.winfo_height() + gap_cat
            self.conf_pass_lbl.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.conf_pass_entry.winfo_height()
            self.conf_pass_entry.place(x=coord[0], y=coord[1])
            coord[1] = coord[1] + self.conf_pass_entry.winfo_height() * 2 - self.pass_update_btn.winfo_height() / 2
            self.pass_update_btn.place(x=coord[0], y=coord[1])
            self.clear_btn.place(x=tab_size[0] - margin[0] - self.clear_btn.winfo_width(),
                                 y=tab_size[1] - margin[1] - self.clear_btn.winfo_height())

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
                    stats, msg = db.edit_admin_personal(CURR_USER, 'Officer', 'Name', self.name_str.get().upper())

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
                    stats, msg = db.edit_admin_personal(CURR_USER, 'Officer', 'Password', self.conf_pass_str.get())

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

        def change_theme(self, theme):
            self.configure(bg=CP[theme][5])
            self.profile_title.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.name_lbl.configure(bg=CP[theme][5], fg=CP[theme][1])
            # self.username_lbl.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.new_pass_lbl.configure(bg=CP[theme][5], fg=CP[theme][1])
            self.conf_pass_lbl.configure(bg=CP[theme][5], fg=CP[theme][1])

            self.name_update_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            # self.username_update_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.pass_update_btn.configure(bg=CP[theme][10], fg=CP[theme][11])
            self.clear_btn.configure(bg=CP[theme][10], fg=CP[theme][11])

    class Notification(Toplevel):
        def __init__(self, root, title, desc, size=0.85):
            super().__init__(root)
            filename = 'logo_light_mode.png'
            try:
                filename = os.path.join(BASE_PATH, filename)
                print(filename)
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

    def __init__(self):
        super().__init__()
        filename = 'logo_light_mode.png'
        try:
            filename = os.path.join(BASE_PATH, filename)
            print(filename)
        except Exception as e:
            print('Error:', e)
        self.icon = PhotoImage(file=filename)
        self.iconphoto(False, self.icon)

        self.cam_enter = None  # cv2.VideoCapture(0)
        self.cam_exit = None  # cv2.VideoCapture(url)
        self.cam_prev = None
        self.url = ""
        self.theme = 1
        self.canvas_index = 0

        # COLOR PALETTE
        # self.font_color = ['black', "#EEEEEE"]
        # # [border, bg, bg2, selectbg]
        # self.color_root = [["#171010", "#E1D89F", "#D89216", "#EEB76B"], ["#171010", "#261C2C", "#2B2B2B", "#3E2C41"]]
        # self.color_bg = ["#6E85B2", "#2B2B2B"]
        # self.color_bg_2 = ["#EEB76B", "#261C2C"]
        # self.color_unavailable = ["#171010", "#171010"]
        # # [bg, fg, selectorcolor, activebackground, activeforeground]
        # self.color_radiobutton = [[self.color_bg_2[0], self.font_color[0], "#EEEEEE", "#E1D89F", self.font_color[0]],
        #                           [self.color_bg_2[1], self.font_color[1], "#5C527F", "#3E2C41", self.font_color[1]]]
        # # [bg, fg, activebackground, activeforeground]
        # self.color_optionmenu = ["#261C2C", "#6E85B2", "#3E2C41", "#EEEEEE", "#916BBF"]
        # # [bg, fg, activebackground, activeforeground]
        # self.color_button = ["#6E85B2", "#171010", "#5C527F", "#171010"]
        # # [bg, fg, activebackground, activeforeground]
        # self.color_menu = [["#EEEEEE", self.font_color[0], "#EEEEEE", self.font_color[0]],
        #                    ["#261C2C", self.font_color[1], "#5C527F", self.font_color[1]]]

        """
        # [bg, fg, selector, actBg, actFg, bg2, fg2, selector2, actBg2, actFg2, fontColor2]
        CP = [['#ECEFF1', '#171010', '#EEEEEE', "#D89216", None,
               '#90A4AE', '#DA0037', '#EEEEEE', '#CFD8DC', 'black',
               '#6E85B2', 'black', None, '#B0BEC5', 'black'],
              ['#2B2B2B', '#EEEEEE', '#5C527F', "#423F3E", None,
               '#261C2C', '#FFD369', '#5C527F', '#5C527F', '#EEEEEE',
               '#6E85B2', 'black', None, '#5C527F', 'black']]
        """
        self.font_color = [CP[0][1], CP[1][1]]
        # [border, bg, bg2, selectbg]
        self.color_root = [["#171010", CP[0][0], CP[0][5], CP[0][3]], ["#171010", CP[1][0], CP[1][5], CP[1][3]]]
        self.color_bg = [CP[0][0], CP[1][0]]
        self.color_bg_2 = [CP[0][5], CP[1][5]]
        self.color_unavailable = ["#171010", "#171010"]
        # [bg, fg, selectorcolor, activebackground, activeforeground]
        self.color_radiobutton = [[self.color_bg_2[0], self.font_color[0], CP[0][7], CP[0][5], self.font_color[0]],
                                  [self.color_bg_2[1], self.font_color[1], CP[1][7], CP[1][5], self.font_color[1]]]
        # [bg, fg, activebackground, activeforeground]
        self.color_optionmenu = ["#261C2C", "#6E85B2", "#3E2C41", "#EEEEEE", "#916BBF"]
        # [bg, fg, activebackground, activeforeground]
        self.color_button = ["#6E85B2", "#171010", "#5C527F", "#171010"]
        # [bg, fg, activebackground, activeforeground]
        self.color_menu = [[CP[0][5], self.font_color[0], CP[0][8], self.font_color[0]],
                           [CP[1][5], self.font_color[1], CP[1][8], self.font_color[1]]]

        self.font_style = "Calibri"
        self.font_size = 0
        self.FONTSIZE_RATIO = 30.87
        self.time_called = time.time()
        self.list_cam = ['None']
        self.list_cam_index = []
        self.cam_used_index = [None, None]
        self.cam_used = None
        self.update_setting = False
        self.cam_setting = [ttk.Combobox, Entry, StringVar, Button, Entry, StringVar, Button]
        self.PREVIEW_MAXHEIGHT = 120
        self.update_frame_mode = 0

        self.cam_enter_res = [640, 360]
        self.cam_exit_res = [640, 360]
        self.cam_prev_res = [160, 120]

        # self.root = Tk()
        self.width = round(67 / 100 * self.winfo_screenwidth())
        self.height = round(67 / 100 * self.winfo_screenheight())
        self.margin_width = round(10 / 100 * self.width)
        self.margin_height = round(10 / 100 * self.height)
        self.main_layout = [round(self.width - 2 * self.margin_width), round(self.height - 2 * self.margin_height)]
        self.font_size = round(self.main_layout[1] / self.FONTSIZE_RATIO)
        # print(self.main_layout[1])

        self.today = datetime.date.today()
        self.date = datetime.date.today()

        self.title("UTeM SEntS Security")
        self.geometry('{}x{}'.format(self.width, self.height))
        self.minsize(MIN_WIDTH, MIN_HEIGHT)

        # self.resizable(False, False)
        # self.attributes('-fullscreen', True)

        self.update()

        temp_frame = Frame(self, width=self.winfo_width(), height=self.winfo_height(),
                           bg=self.color_bg[self.theme], borderwidth=0, highlightthickness=0)
        temp_frame.place(x=0, y=0)
        temp_frame.update()
        font_setting = "Calibri " + str(round(self.font_size * 2.5))
        loading_lbl = Label(temp_frame, font=font_setting, text='Loading...',
                            bg=CP[self.theme][0], fg=CP[self.theme][1])
        loading_lbl.place(x=0, y=0)
        loading_lbl.update()
        loading_lbl.place(x=temp_frame.winfo_width() / 2 - loading_lbl.winfo_width() / 2,
                          y=temp_frame.winfo_height() / 2 - loading_lbl.winfo_height() / 2)

        # self.login_canvas = self.LoginCanvas(self, self.theme, self.winfo_screenwidth(),
        #                                      self.winfo_screenheight(),
        #                                      self.winfo_width(), self.winfo_height(), self.font_size,
        #                                      self.canvas_index)
        self.login_canvas = self.LoginCanvas(self, self.theme, self.winfo_screenwidth(), self.winfo_screenheight(),
                                             self.winfo_width(), self.winfo_height(), self.font_size, 0)
        self.canvas = Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(),
                             bg=self.color_bg[self.theme], borderwidth=0, highlightthickness=0)

        filename = 'logo_dark_mode.png'
        self.ai_enter = plate_recognition(init_img_path=os.path.join(BASE_PATH, filename))
        # self.ai_exit = plate_recognition(init_img_path='./logo_dark_mode.png')
        self.plt_num_enter = ''
        self.plt_num_exit = ''

        temp_frame.place_forget()

        self.canvas.place(x=self.winfo_width(), y=self.winfo_width())

        self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                   round(40 / 100 * self.main_layout[1])),
                                           color=self.color_unavailable[0])  # set index 0, it's okay bcos this is prep

        self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
        self.msg = "Video Output is Unavailable.\nClick Here to Set Up Camera"
        draw = ImageDraw.Draw(self.frame_unavailable)
        w, h = draw.textsize(self.msg, font=self.font)
        draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                   round(self.frame_unavailable.height / 2 - h / 2)),
                  self.msg, "#EEEEEE", font=self.font, align=CENTER)
        self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
        self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)

        no_preview = Image.new('RGB', (160, 120),
                               color=self.color_unavailable[0])
        font_preview = ImageFont.truetype("arial.ttf", 17)
        msg_preview = "No Camera\nSelected"
        draw = ImageDraw.Draw(no_preview)
        w, h = draw.textsize(msg_preview, font=self.font)
        draw.text((round((no_preview.width / 2 - w / 2)),
                   round(no_preview.height / 2 - h / 2)),
                  msg_preview, "#EEEEEE", font=font_preview, align=CENTER)
        self.no_preview = ImageTk.PhotoImage(no_preview)

        self.preview_tk = self.no_preview
        self.label_prev = Label()

        self.close = False
        self.status_text_1 = Label()
        self.status_text_2 = Label()
        self.time_stats_1 = time.time()
        self.time_stats_2 = time.time()

        font_setting = "Calibri " + str(round(self.font_size * 0.73))
        self.logout_btn = Button(self.canvas, text="Logout", font=font_setting, padx=10, pady=1,
                                 bg=CP[self.theme][5], fg=CP[self.theme][1],
                                 activebackground=CP[self.theme][8], activeforeground=CP[self.theme][9],
                                 command=lambda a=0: self.button_event(a))
        self.logout_btn.place(x=0, y=0)
        self.logout_btn.update()
        self.logout_btn.place(x=self.width - (self.margin_width / 2 + self.logout_btn.winfo_width() / 2),
                              y=self.margin_height / 2 - self.logout_btn.winfo_height() / 2)

        def state_disable():
            pass

        def state_enable():
            self.menubar.entryconfig("Setting", state=NORMAL)
            """
            self.tabs.tab(0, state=NORMAL)
            self.tabs.tab(1, state=NORMAL)
            self.label_enter.bind("<ButtonPress>", lambda event, a=0: self.on_press(event, a))
            self.label_exit.bind("<ButtonPress>", lambda event, a=1: self.on_press(event, a))
            self.label_enter.bind("<ButtonRelease>", lambda event, a=0: self.on_release(event, a))
            self.label_exit.bind("<ButtonRelease>", lambda event, a=1: self.on_release(event, a))
            self.label_date.bind("<ButtonPress>", lambda event, a=2: self.on_press(event, a))
            self.label_date_prev.bind("<ButtonPress>", lambda event, a=3: self.on_press(event, a))
            self.label_date_next.bind("<ButtonPress>", lambda event, a=4: self.on_press(event, a))
            self.tabs.bind("<ButtonRelease>", lambda event, a=5: self.on_release(event, a))
            self.label_date.bind("<ButtonRelease>", lambda event, a=2: self.on_release(event, a))
            self.label_date_prev.bind("<ButtonRelease>", lambda event, a=3: self.on_release(event, a))
            self.label_date_next.bind("<ButtonRelease>", lambda event, a=4: self.on_release(event, a))
            self.tabs.bind("<ButtonRelease>", lambda event, a=5: self.on_release(event, a))
            self.calendar.bind("<<CalendarSelected>>", lambda event: self.select_date(event))
            """

        def change_theme(theme):
            self.menubar.entryconfig("Setting", state=DISABLED)
            """
            self.tabs.tab(0, state=DISABLED)
            self.tabs.tab(1, state=DISABLED)
            self.label_enter.bind("<ButtonPress>", state_disable)
            self.label_exit.bind("<ButtonPress>", state_disable)
            self.label_enter.bind("<ButtonRelease>", state_disable)
            self.label_exit.bind("<ButtonRelease>", state_disable)
            self.label_date.bind("<ButtonPress>", state_disable)
            self.label_date_prev.bind("<ButtonPress>", state_disable)
            self.label_date_next.bind("<ButtonPress>", state_disable)
            self.tabs.bind("<ButtonRelease>", state_disable)
            self.label_date.bind("<ButtonRelease>", state_disable)
            self.label_date_prev.bind("<ButtonRelease>", state_disable)
            self.label_date_next.bind("<ButtonRelease>", state_disable)
            self.tabs.bind("<ButtonRelease>", state_disable)
            self.calendar.bind("<<CalendarSelected>>", state_disable)
            """

            self.theme = theme
            change_layout()
            self.login_canvas.change_theme(self.theme)
            self.frame_result.change_theme(self.theme)
            self.frame_hist.change_theme(self.theme)
            self.frame_prof.change_theme(self.theme)
            self.after(1000, state_enable)

        self.menubar = Menu(self, background=self.color_menu[self.theme][0],
                            foreground=self.color_menu[self.theme][1],
                            activebackground=self.color_menu[self.theme][2],
                            activeforeground=self.color_menu[self.theme][3])
        self.setting = Menu(self.menubar, tearoff=0, background=self.color_menu[self.theme][0],
                            foreground=self.color_menu[self.theme][1],
                            selectcolor=self.color_menu[self.theme][3])
        self.setting.add_command(label="Camera Enter", command=lambda a=0: self.setup_cam(a), state=DISABLED)
        self.setting.add_command(label="Camera Exit", command=lambda a=1: self.setup_cam(a), state=DISABLED)
        self.setting.add_separator()
        self.setting.add_radiobutton(label="Light Mode", command=lambda a=0: change_theme(a))
        self.setting.add_radiobutton(label="Dark Mode")
        self.setting.invoke(self.setting.index("Dark Mode"))
        self.setting.entryconfig(self.setting.index("Dark Mode"), command=lambda a=1: change_theme(a))
        self.setting.add_separator()
        self.setting.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="Setting", menu=self.setting)
        self.config(menu=self.menubar)
        self.after(1500, state_enable)

        """
        self.top_frame = Frame(self, bg=self.color_bg[self.theme], width=self.width, height=self.margin_height, pady=3,
                               borderwidth=0, highlightthickness=0)
        self.top_frame.grid(row=0, columnspan=3)
        # self.mid_frame = Frame(self, bg='white', width=self.main_layout[0], height=self.main_layout[1], pady=3)
        # self.mid_frame.grid(row=1, column=1, columnspan=1)
        self.bot_frame = Frame(self, bg=self.color_bg[self.theme], width=self.width, height=self.margin_height, pady=3,
                               borderwidth=0, highlightthickness=0)
        self.bot_frame.grid(row=2, columnspan=3)

        self.midleft_frame = Frame(self, bg=self.color_bg[self.theme], width=self.margin_width,
                                   height=self.main_layout[1], pady=0, borderwidth=0, highlightthickness=0)
        self.midleft_frame.grid(row=1, column=0, rowspan=1)
        self.midright_frame = Frame(self, bg=self.color_bg[self.theme], width=self.margin_width,
                                    height=self.main_layout[1], pady=1, borderwidth=0, highlightthickness=0)
        self.midright_frame.grid(row=1, column=2, rowspan=1)
        """

        offset = [
            # 0 = enter frame
            [(50 / 100 * self.main_layout[0] / 2),
             (10 / 100 * self.main_layout[1]) + (40 / 100 * self.main_layout[1] / 2)],
            # 1 = exit frame
            [(50 / 100 * self.main_layout[0] / 2),
             (60 / 100 * self.main_layout[1]) + (40 / 100 * self.main_layout[1] / 2)]
        ]

        font_setting = self.font_style + " " + str(self.font_size) + " bold"
        self.id_enter = self.canvas.create_text(self.margin_width, self.margin_height, anchor=CENTER,
                                                fill=self.font_color[self.theme], font=font_setting, text="ENTER")
        self.label_enter = Label(self.canvas, bg=self.color_bg[self.theme], borderwidth=0, highlightthickness=0)
        self.id_exit = self.canvas.create_text(self.margin_width, self.margin_height, anchor=CENTER,
                                               fill=self.font_color[self.theme], font=font_setting, text="EXIT")
        self.label_exit = Label(self.canvas, bg=self.color_bg[self.theme], borderwidth=0, highlightthickness=0)

        self.label_enter.place(x=self.margin_width, y=round(10 / 100 * self.main_layout[1]) + self.margin_height)
        self.label_exit.place(x=self.margin_width, y=round(60 / 100 * self.main_layout[1]) + self.margin_height)
        self.label_enter.configure(image=self.frame_enter_tk)
        self.label_exit.configure(image=self.frame_exit_tk)
        # self.canvas.create_window(0, round(10 / 100 * self.main_layout[1] / 2), window=self.label_enter)
        # self.canvas.create_window(0, round(60 / 100 * self.main_layout[1] / 2), window=self.label_exit)

        """
        coords = [self.canvas.bbox(self.id_enter),
                  self.canvas.bbox(self.id_exit)]

        self.offset = [
            # 0 = enter text
            [(50 / 100 * self.main_layout[0] / 2), (10 / 100 * self.main_layout[1] / 2)],
            # 1 = enter frame
            [(50 / 100 * self.main_layout[0] / 2),
             (10 / 100 * self.main_layout[1]) + (40 / 100 * self.main_layout[1] / 2)],
            # 2 = exit text
            [(50 / 100 * self.main_layout[0] / 2) + self.width,
             (50 / 100 * self.main_layout[1]) + (10 / 100 * self.main_layout[1] / 2) ],
            # 3 = enter frame
            [(50 / 100 * self.main_layout[0] / 2),
             (60 / 100 * self.main_layout[1]) + (40 / 100 * self.main_layout[1] / 2)]
        ]
        """
        # self.canvas.move(self.id_enter, self.offset[0][0], self.offset[0][1])
        # self.canvas.move(self.id_frame_enter, self.offset[1][0], self.offset[1][1])
        # self.canvas.move(self.id_exit, self.offset[2][0], self.offset[2][1])
        # self.canvas.move(self.id_frame_exit, self.offset[3][0], self.offset[3][1])
        enter_coords = (self.margin_width + (50 / 100 * self.main_layout[0] / 2),
                        self.margin_height + (10 / 100 * self.main_layout[1] / 2))
        exit_coords = (self.margin_width + (50 / 100 * self.main_layout[0] / 2),
                       self.margin_height + (self.main_layout[1] / 2) + (10 / 100 * self.main_layout[1] / 2))
        self.canvas.coords(self.id_enter, enter_coords)
        self.canvas.coords(self.id_exit, exit_coords)

        """
        self.text_enter = Text(self)
        self.text_enter.grid(row=1, column=1, columnspan=1)
        self.text_enter.config(font=('Arial', 8, 'bold'))
        self.text_enter.tag_configure("Enter", foreground="black", underline=False)
        self.text_enter.bind("<Enter>", click_text)
        self.text_enter.bind("<Leave>", hover_text)
        self.label_enter = Label(self, text=self.text_enter)
        """
        self.bind("<Configure>", self.config_event)
        # self.label_enter.bind("<Button 1>", lambda event, a=0: self.setup_cam(event, a))
        # self.label_exit.bind("<Button 1>", lambda event, a=1: self.setup_cam(event, a))
        self.label_enter.bind("<ButtonPress>", lambda event, a=0: self.on_press(event, a))
        self.label_exit.bind("<ButtonPress>", lambda event, a=1: self.on_press(event, a))
        self.label_enter.bind("<ButtonRelease>", lambda event, a=0: self.on_release(event, a))
        self.label_exit.bind("<ButtonRelease>", lambda event, a=1: self.on_release(event, a))
        self.label_enter.focus_set()
        self.label_exit.focus_set()

        self.left_layout = Frame(self.canvas, highlightthickness=1,
                                 highlightbackground=self.color_root[self.theme][0],
                                 highlightcolor=self.color_root[self.theme][0], width=self.main_layout[0] / 2 - 50,
                                 height=self.main_layout[1] - round(self.margin_height / 1.6))
        self.left_layout.place(x=self.width / 2 + 50, y=self.margin_height)

        self.s = ttk.Style()
        width_tab = round((self.main_layout[0] / 25))  # = 65 or round((self.main_layout[0] / 12.7))
        self.s.theme_create("MyStyle", parent="clam", settings={
            "TNotebook": {"configure": {"tabmargins": [3, 1, 0, 0],
                                        "background": self.color_root[self.theme][2],
                                        'borderwidth': 0,
                                        'highlightbackground': self.color_root[self.theme][2],
                                        'highlightcolor': self.color_root[self.theme][2]}},
            "TNotebook.Tab": {"configure": {"padding": [width_tab, 5], "borderwidth": 1,
                                            "font": (self.font_style, str(self.font_size - 2)),
                                            "background": self.color_root[self.theme][2],
                                            "foreground": self.font_color[self.theme]},
                              "map": {"background": [("selected", self.color_root[self.theme][1])],
                                      "foreground": [("selected", self.font_color[self.theme])],
                                      "expand": [("selected", [3, 1, 3, 1])]}},
            'TCombobox': {'configure': {'selectbackground': self.color_optionmenu[4],
                                        'fieldbackground': 'white',
                                        'borderwidth': 0,
                                        'background': self.color_optionmenu[1]
                                        }}
        })
        # self.default_theme = self.s.theme_use()
        self.s.theme_use('MyStyle')

        # print(self.s.theme_names())

        self.tabs = ttk.Notebook(self.left_layout)
        # self.tabs.place(x=self.width / 2 + 50, y=self.margin_height)
        tab_size = [self.main_layout[0] / 2 - 50, self.main_layout[1] - round(self.margin_height / 1.6)]
        self.frame_result = self.Result(self, tab_size)
        # Frame(self.tabs, width=tab_size[0], height=tab_size[1],
        #                           bg=self.color_root[self.theme][1])
        # width=self.main_layout[0] / 2 - 50, height=self.main_layout[1]-round(self.margin_height/1.6)
        self.frame_hist = self.LogFrame(self, tab_size)
        self.frame_prof = self.Profile(self, tab_size)
        # width=self.main_layout[0] / 2 - 50, height=self.main_layout[1]-round(self.margin_height/1.6)

        self.tabs.add(self.frame_result, text=f'{"Result": ^5s}')
        self.tabs.add(self.frame_hist, text=f'{"History": ^5s}')
        self.tabs.add(self.frame_prof, text=f'{"Profile": ^5s}')
        self.tabs.pack(expand=1, fill="both")

        # self.calendar.place(x=self.margin_width * 6, y=self.margin_height * 3)
        self.canvas.place_forget()

        def change_layout():
            self.menubar.configure(background=self.color_menu[self.theme][0], foreground=self.color_menu[self.theme][1],
                                   activebackground=self.color_menu[self.theme][2],
                                   activeforeground=self.color_menu[self.theme][3])
            self.setting.configure(background=self.color_menu[self.theme][0], foreground=self.color_menu[self.theme][1],
                                   selectcolor=self.color_menu[self.theme][3])
            self.config(menu=self.menubar)

            self.canvas.configure(bg=self.color_bg[self.theme])
            self.canvas.itemconfig(self.id_enter, fill=self.font_color[self.theme])
            self.label_enter.configure(bg=self.color_bg[self.theme])
            self.canvas.itemconfig(self.id_exit, fill=self.font_color[self.theme])
            self.label_exit.configure(bg=self.color_bg[self.theme])

            self.left_layout.configure(highlightbackground=self.color_root[self.theme][0],
                                       highlightcolor=self.color_root[self.theme][0])

            # Theme
            width_tab = round((self.main_layout[0] / 25))  # = 65 or round((self.main_layout[0] / 12.7))
            self.s.theme_settings("MyStyle", settings={
                "TNotebook": {"configure": {"tabmargins": [3, 1, 0, 0],
                                            "background": self.color_root[self.theme][2],
                                            'borderwidth': 0,
                                            'highlightbackground': self.color_root[self.theme][2],
                                            'highlightcolor': self.color_root[self.theme][2]}},
                "TNotebook.Tab": {"configure": {"padding": [width_tab, 5], "borderwidth": 1,
                                                "font": (self.font_style, str(self.font_size - 2)),
                                                "background": self.color_root[self.theme][2],
                                                "foreground": self.font_color[self.theme]},
                                  "map": {"background": [("selected", self.color_root[self.theme][1])],
                                          "foreground": [("selected", self.font_color[self.theme])],
                                          "expand": [("selected", [3, 1, 3, 1])]}},
                'TCombobox': {'configure': {'selectbackground': self.color_optionmenu[4],
                                            'fieldbackground': 'white',
                                            'borderwidth': 0,
                                            'background': self.color_optionmenu[1]
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

            self.frame_result.configure(bg=self.color_root[self.theme][1])
            self.frame_hist.configure(bg=self.color_root[self.theme][1])

            self.frame_hist.label_date.configure(bg=self.color_root[self.theme][1], fg=self.font_color[self.theme])

            self.frame_hist.label_date_prev.configure(bg=self.color_root[self.theme][1], fg=self.font_color[self.theme])
            self.frame_hist.label_date_next.configure(bg=self.color_root[self.theme][1], fg=self.font_color[self.theme])
            self.logout_btn.configure(bg=CP[self.theme][5], fg=CP[self.theme][1],
                                      activebackground=CP[self.theme][8], activeforeground=CP[self.theme][9])

        self.update()

        self.width = self.winfo_width()
        self.height = self.winfo_height()
        # print(self.width, self.height)

    def on_press(self, event, layout):
        # print("button was pressed")
        if layout == 0:
            if not self.cam_enter:
                self.color_unavailable[0] = "#362222"
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[0])
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, self.font_color[self.theme], font=self.font, align=CENTER)

                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_enter.configure(image=self.frame_enter_tk)
        elif layout == 1:
            if not self.cam_exit:
                self.color_unavailable[1] = "#362222"
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[1])
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, self.font_color[self.theme], font=self.font, align=CENTER)

                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_exit.configure(image=self.frame_exit_tk)
        elif layout == 2:
            self.frame_hist.label_date.configure(bg=self.color_root[self.theme][3])
        elif layout == 3:
            self.frame_hist.label_date_prev.configure(bg=self.color_root[self.theme][3])
        elif layout == 4:
            self.frame_hist.label_date_next.configure(bg=self.color_root[self.theme][3])
        elif layout == 5:
            pass

    def on_release(self, event, layout):
        # print("button was released")
        if layout == 0:
            if not self.cam_enter:
                self.color_unavailable[0] = "#171010"
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[0])
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, self.font_color[self.theme], font=self.font, align=CENTER)

                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_enter.configure(image=self.frame_enter_tk)

            self.setup_cam(0)
        elif layout == 1:
            if not self.cam_exit:
                self.color_unavailable[1] = "#171010"
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[1])
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, self.font_color[self.theme], font=self.font, align=CENTER)

                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_exit.configure(image=self.frame_exit_tk)

            self.setup_cam(1)
        elif layout == 2:
            self.frame_hist.label_date.configure(bg=CP[self.theme][5])
            if self.frame_hist.calendar_visib:
                self.frame_hist.calendar.place_forget()
                self.frame_hist.calendar_visib = False
            else:
                self.frame_hist.calendar.place(x=self.tabs.winfo_width() / 2 -
                                                 self.frame_hist.calendar.winfo_width() / 2,
                                               y=5 / 100 * self.tabs.winfo_width() +
                                                 self.frame_hist.label_date.winfo_height())
                self.frame_hist.calendar_visib = True
            # Calendar and DB Stuff
            self.frame_hist.update_log_date(self)
        elif layout == 3:
            self.frame_hist.label_date_prev.configure(bg=CP[self.theme][5])
            self.date = self.date - datetime.timedelta(days=1)
            temp = str(self.date).split('-')
            temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
            self.frame_hist.label_date.configure(text=temp)
            self.frame_hist.calendar.selection_set(self.date)
            # self.label_date.

            # Database Stuff
            self.frame_hist.update_log_date(self)
        elif layout == 4:
            self.frame_hist.label_date_next.configure(bg=CP[self.theme][5])
            self.date = self.date + datetime.timedelta(days=1)
            temp = str(self.date).split('-')
            temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
            self.frame_hist.label_date.configure(text=temp)
            self.frame_hist.calendar.selection_set(self.date)
            # self.label_date.
            # Database Stuff
            self.frame_hist.update_log_date(self)
        elif layout == 5:
            clicked_tab = self.tabs.tk.call(self.tabs._w, "identify", "tab", event.x, event.y)
            # print("TAB: ", clicked_tab)
            if clicked_tab != 1:
                # Potential Bug
                # self.frame_hist.calendar.place_forget()
                self.frame_hist.calendar_visib = False
                self.date = self.today
                temp = str(self.today).split('-')
                temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
                self.frame_hist.label_date.configure(text=temp)
                self.frame_hist.calendar.selection_set(self.date)
                self.frame_hist.update_log_date(self)

    def button_event(self, type):
        if type == 0:
            print("Logout")
            self.login_canvas.place(x=0, y=0)
            self.canvas.place_forget()

            # Close All Functions
            self.setting.entryconfig(self.setting.index("Camera Enter"), state=DISABLED)
            self.setting.entryconfig(self.setting.index("Camera Exit"), state=DISABLED)

            self.tabs.select(0)
            self.cam_enter = None
            self.cam_exit = None
            self.cam_used_index[0] = None
            self.cam_used_index[1] = None

            self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
            self.label_enter.configure(image=self.frame_enter_tk)
            self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
            self.label_exit.configure(image=self.frame_exit_tk)

            self.label_enter.place(x=self.margin_width +
                                     (50 / 100 * self.main_layout[0] - self.frame_enter_tk.width()) / 2,
                                   y=round(10 / 100 * self.main_layout[1]) + self.margin_height)
            self.label_exit.place(x=self.margin_width +
                                    (50 / 100 * self.main_layout[0] - self.frame_exit_tk.width()) / 2,
                                  y=round(60 / 100 * self.main_layout[1]) + self.margin_height)

    def select_date(self, event):
        temp = datetime.datetime.strptime(self.frame_hist.calendar.get_date(), '%m/%d/%y')
        self.date = datetime.datetime.strptime(self.frame_hist.calendar.get_date(), '%m/%d/%y')
        self.date = self.date.date()
        temp = str(temp).split(' ')[0].split('-')
        temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
        self.frame_hist.label_date.configure(text=temp)

    def setup_cam(self, camera):
        title = "Camera Setting "
        width = 514  # round(self.winfo_width() / 2)
        height = 530  # round(self.winfo_height() / 1.2)
        # print(width, height)
        x = round(self.winfo_width() / 2 - width / 2) + self.winfo_x()
        y = round(self.winfo_height() / 2 - height / 2) + self.winfo_y()
        self.update_frame_mode = 1  # Remember to set back to 0

        if camera == 0:
            title = title + "Enter"
        elif camera == 1:
            title = title + "Exit"

        child_camera = Toplevel(self)
        filename = 'logo_light_mode.png'
        try:
            filename = os.path.join(BASE_PATH, filename)
            print(filename)
        except Exception as e:
            print('Error:', e)
        self.icon = PhotoImage(file=filename)
        child_camera.iconphoto(False, self.icon)

        child_camera.title(title)
        child_camera.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        # child_camera.attributes('-topmost', True)
        child_camera.grab_set()
        # child_camera.grab_release()  # After Finish Setting
        child_camera.resizable(False, False)

        def on_closing_disable():
            pass

        child_camera.protocol("WM_DELETE_WINDOW", on_closing_disable)

        margin_width = 10 / 100 * width
        margin_height = 10 / 100 * height
        main_layout = [round(width - 2 * margin_width), round(height - 2 * margin_height)]

        self.cam_used = None

        canvas_loading = Canvas(child_camera, width=width, height=height, bg=self.color_bg_2[self.theme],
                                borderwidth=0, highlightthickness=0)
        canvas_loading.place(x=0, y=0)

        font_size = round(main_layout[1] / self.FONTSIZE_RATIO * 2)
        font_setting = self.font_style + " " + str(font_size)
        label_loading = Label(canvas_loading, bg=self.color_bg_2[self.theme], fg=self.font_color[self.theme],
                              text="Loading...", font=font_setting)
        label_loading.place(x=0, y=0)
        label_loading.update()
        label_loading.place(x=width / 2 - label_loading.winfo_width() / 2,
                            y=height / 2 - label_loading.winfo_height() / 2)
        canvas_loading.update()

        thread_cam = threading.Thread(target=self.detect_cam(), daemon=True)
        thread_cam.start()
        canvas_loading.place_forget()

        """
        top_frame = Frame(child_camera, bg=self.color_bg_2[self.theme], width=width, height=margin_height, pady=3,
                          borderwidth=0, highlightthickness=0)
        top_frame.grid(row=0, columnspan=3)
        # self.mid_frame = Frame(self, bg='white', width=main_layout[0], height=main_layout[1], pady=3)
        # self.mid_frame.grid(row=1, column=1, columnspan=1)
        bot_frame = Frame(child_camera, bg=self.color_bg_2[self.theme], width=width, height=margin_height, pady=3,
                          borderwidth=0, highlightthickness=0)
        bot_frame.grid(row=2, columnspan=3)

        midleft_frame = Frame(child_camera, bg=self.color_bg_2[self.theme], width=margin_width,
                              height=main_layout[1], pady=0, borderwidth=0, highlightthickness=0)
        midleft_frame.grid(row=1, column=0, rowspan=1)
        midright_frame = Frame(child_camera, bg=self.color_bg_2[self.theme], width=margin_width,
                               height=main_layout[1], pady=1, borderwidth=0, highlightthickness=0)
        midright_frame.grid(row=1, column=2, rowspan=1)
        """

        font_size = round(main_layout[1] / self.FONTSIZE_RATIO) + 4
        font_setting = self.font_style + " " + str(font_size)
        canvas = Canvas(child_camera, width=width, height=height, bg=self.color_bg_2[self.theme],
                        borderwidth=0, highlightthickness=0)

        canvas.place(x=0, y=0)
        # canvas.grid(row=1, column=1)

        """
        self.list_cam = ["None"]
        self.list_cam_index = []

        camera = 0
        while True:
            temp = cv2.VideoCapture(camera)
            if temp.read()[0]:
                camera = camera + 1
                name = "Camera " + str(camera)
                self.list_cam.append(name)
                self.list_cam_index.append(camera)
                temp.release()
            else:
                cv2.destroyAllWindows()
                break
        """

        self.label_prev = Label(child_camera, bg=self.color_bg_2[self.theme], borderwidth=0, highlightthickness=0)
        self.label_prev.place(x=(width / 2 - self.no_preview.width() / 2), y=margin_height)
        self.label_prev.configure(image=self.no_preview)

        option = 0
        label_device = Label(child_camera, text="Devices:", font=font_setting, fg=self.font_color[self.theme],
                             bg=self.color_bg_2[self.theme], borderwidth=0, highlightthickness=0)

        font_size = font_size - 4
        font_setting = self.font_style + " " + str(font_size)

        radio_opt1 = Radiobutton(child_camera, text="Connected Device", variable=option, value=0,
                                 bg=self.color_radiobutton[self.theme][0], fg=self.color_radiobutton[self.theme][1],
                                 selectcolor=self.color_radiobutton[self.theme][2],
                                 activebackground=self.color_radiobutton[self.theme][3],
                                 activeforeground=self.color_radiobutton[self.theme][4],
                                 command=lambda a=1: self.radiocam_func(a),
                                 font=font_setting, width=40, justify=LEFT, anchor=NW)
        radio_opt2 = Radiobutton(child_camera, text="IP Address via IP Webcam", variable=option, value=1,
                                 bg=self.color_radiobutton[self.theme][0], fg=self.color_radiobutton[self.theme][1],
                                 selectcolor=self.color_radiobutton[self.theme][2],
                                 activebackground=self.color_radiobutton[self.theme][3],
                                 activeforeground=self.color_radiobutton[self.theme][4],
                                 command=lambda a=2: self.radiocam_func(a),
                                 font=font_setting, width=40, justify=LEFT, anchor=NW)
        radio_opt3 = Radiobutton(child_camera, text="Other Link URL", variable=option, value=2,
                                 bg=self.color_radiobutton[self.theme][0], fg=self.color_radiobutton[self.theme][1],
                                 selectcolor=self.color_radiobutton[self.theme][2],
                                 activebackground=self.color_radiobutton[self.theme][3],
                                 activeforeground=self.color_radiobutton[self.theme][4],
                                 command=lambda a=3: self.radiocam_func(a),
                                 font=font_setting, width=40, justify=LEFT, anchor=NW)
        # button_ok = Button(child_camera, text='Ok', command=sendGift, default='active')

        radio_opt1.select()
        radio_opt2.deselect()
        radio_opt3.deselect()

        """
        option1 = StringVar(child_camera)
        option1.set("None")  # default value

        dropdown1 = OptionMenu(child_camera, option1, "Select...\t", "One\t", "Two\t")
        dropdown1["borderwidth"] = 0
        dropdown1["highlightthickness"] = 0
        dropdown1["relief"] = FLAT
        dropdown1["anchor"] = NW
        dropdown1["bg"] = self.color_optionmenu[0]
        dropdown1["fg"] = self.color_optionmenu[1]
        dropdown1["activebackground"] = self.color_optionmenu[2]
        dropdown1["activeforeground"] = self.color_optionmenu[3]
        dropdown1["menu"]["bg"] = self.color_optionmenu[0]
        dropdown1["menu"]["fg"] = self.color_optionmenu[1]
        dropdown1["menu"]["activebackground"] = self.color_optionmenu[2]
        dropdown1["menu"]["activeforeground"] = self.color_optionmenu[3]
        """

        """
        def detect_cam():
            camera = 0
            while True:
                temp = cv2.VideoCapture(camera)
                if temp.read()[0]:
                    camera = camera + 1
                    name = "Camera " + str(camera)
                    self.list_cam.append(name)
                    self.list_cam_index.append(camera)
                    temp.release()
                else:
                    cv2.destroyAllWindows()
                    combobox1['values'] = self.list_cam
                    break
        """

        def combobox_cam(event):
            if combobox1.get() == combobox1["values"][0]:
                self.cam_prev = None
                self.label_prev.configure(image=self.no_preview)
                self.label_prev.update()
                self.label_prev.place(x=(514 / 2 - self.PREVIEW_MAXHEIGHT *
                                         (self.label_prev.winfo_width() / self.label_prev.winfo_height()) / 2)
                                      , y=48.2)
                return
            else:
                # self.cam_prev = cv2.VideoCapture()
                child_camera.after(1, lambda a=int(combobox1.get().split(" ")[1]) - 1, b=camera: conn_cam(a, b))
                # self.cam_prev_res[0] = int(self.cam_prev.get(cv2.CAP_PROP_FRAME_WIDTH))
                # self.cam_prev_res[1] = int(self.cam_prev.get(cv2.CAP_PROP_FRAME_HEIGHT))
                """
                for i in range(1, len(combobox["values"])):
                    if combobox.get() == combobox["values"][i]:
                        self.cam_prev = cv2.VideoCapture(i - 1)
                        self.cam_prev_res[0] = int(self.cam_prev.get(cv2.CAP_PROP_FRAME_WIDTH))
                        self.cam_prev_res[1] = int(self.cam_prev.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        return
                """

        combobox1 = ttk.Combobox(child_camera)
        combobox1['values'] = self.list_cam
        combobox1['state'] = 'readonly'  # disabled or readonly
        combobox1.current(0)
        combobox1.bind("<<ComboboxSelected>>", combobox_cam)
        # child_camera.after(1, detect_cam)

        ip_web = StringVar()
        ip_add = ttk.Entry(child_camera, width=15, textvariable=ip_web)
        ip_web.trace("w", lambda *args: self.character_limit(ip_web))
        ip_add['state'] = 'disabled'

        other_text = StringVar()
        other_layout = ttk.Entry(child_camera, width=40, textvariable=other_text)
        other_layout['state'] = 'disabled'

        font_setting = self.font_style + " " + str(round(font_size * 0.7))
        self.status_text_1 = Label(child_camera, bg=self.color_bg_2[self.theme],
                                   fg=self.color_radiobutton[self.theme][1], font=font_setting)
        self.status_text_2 = Label(child_camera, bg=self.color_bg_2[self.theme],
                                   fg=self.color_radiobutton[self.theme][1], font=font_setting)

        label_device.place(x=margin_width, y=margin_height + 120)
        temp_ori = margin_width + 35 + 120
        radio_opt1.place(x=margin_width, y=temp_ori)
        temp = temp_ori + 35
        combobox1.place(x=margin_width * 2, y=temp)
        temp = temp + 40
        radio_opt2.place(x=margin_width, y=temp)
        temp = temp + 35
        ip_add.place(x=margin_width * 2, y=temp)
        temp = temp + 40
        radio_opt3.place(x=margin_width, y=temp)
        temp = temp + 35
        other_layout.place(x=margin_width * 2, y=temp)

        def label_fade_1():
            self.time_stats_1 = time.time()
            # time.sleep(3)
            # self.status_text_1.configure(text="")

        def label_fade_2():
            self.time_stats_2 = time.time()
            # time.sleep(3)
            # self.status_text_2.configure(text="")

        def conn_cam(cam, m):
            canvas_loading_2 = Canvas(child_camera, width=160, height=110, bg=self.color_unavailable[camera],
                                      borderwidth=0, highlightthickness=0)
            canvas_loading_2.place(x=width, y=height)
            canvas_loading_2.update()

            font_size_2 = round(main_layout[1] / self.FONTSIZE_RATIO)
            font_setting_2 = self.font_style + " " + str(font_size_2)
            label_loading_2 = Label(canvas_loading_2, bg=self.color_unavailable[camera], fg="#EEEEEE",
                                    text="Loading...", font=font_setting_2, padx=3)
            label_loading_2.place(x=0, y=0)
            label_loading_2.update()
            canvas_loading_2.place(x=width / 2 - canvas_loading_2.winfo_width() / 2, y=margin_height)
            label_loading_2.place(x=canvas_loading_2.winfo_width() / 2 - label_loading_2.winfo_width() / 2,
                                  y=canvas_loading_2.winfo_height() / 2 - label_loading_2.winfo_height() / 2)
            label_loading_2.update()
            canvas_loading_2.update()

            ok_btn.configure(state=DISABLED)
            cancel_btn.configure(state=DISABLED)
            # child_camera.protocol("WM_DELETE_WINDOW", on_closing_disable())
            ok_btn.update()
            cancel_btn.update()

            self.cam_prev = cv2.VideoCapture(cam)
            self.cam_prev_res[0] = int(self.cam_prev.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.cam_prev_res[1] = int(self.cam_prev.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.cam_used = cam

            canvas_loading_2.place_forget()
            child_camera.after(1500, normal_btn)

        def normal_btn():
            ok_btn.configure(state=NORMAL)
            cancel_btn.configure(state=NORMAL)
            # child_camera.protocol("WM_DELETE_WINDOW", on_closing_disable())

        def conn_ip(ip_web):
            test_ip = ip_web.get().split('.')
            valid_ip = True
            if len(test_ip) == 4:
                for section in test_ip:
                    if len(section) > 3 or not section:
                        valid_ip = False

                if valid_ip:
                    self.url = "https://" + ip_web.get() + ":8080/video"
                    try:
                        urllib.request.urlopen(self.url).getcode()
                    except:
                        print("Failed to Connect")
                        self.status_text_1.configure(text="Failed to Connect")
                        self.status_text_1.place(x=margin_width * 2, y=temp_ori + 110 + 23)
                        child_camera.after(1, label_fade_1)
                        return
                    if self.url != self.cam_used_index[0] and self.url != self.cam_used_index[1]:
                        print("Successfully Connect")
                        self.status_text_1.configure(text="Successfully Connect")
                        self.status_text_1.place(x=margin_width * 2, y=temp_ori + 110 + 23)
                        # self.cam_prev = cv2.VideoCapture(self.url)
                        child_camera.after(1, lambda a=self.url, b=camera: conn_cam(a, b))
                        child_camera.after(1, label_fade_1)
                        return
                    else:
                        print("This Camera has already Connected")
                        self.status_text_1.configure(text="This Camera has already Connected")
                        self.status_text_1.place(x=margin_width * 2, y=temp_ori + 110 + 23)
                        child_camera.after(1, label_fade_1)
                        return

            print("Invalid IP Address")
            self.status_text_1.configure(text="Invalid IP Address")
            self.status_text_1.place(x=margin_width * 2, y=temp_ori + 110 + 23)
            child_camera.after(1, label_fade_1)
            return

        def conn_other(other_text):
            if other_text.get():
                try:
                    urllib.request.urlopen(other_text.get()).getcode()
                except:
                    print("Failed to Connect")
                    self.status_text_2.configure(text="Failed to Connect")
                    self.status_text_2.place(x=margin_width * 2, y=temp_ori + 185 + 23)
                    child_camera.after(1, label_fade_2)
                    return

                if other_text.get() != self.cam_used_index[0] and other_text.get() != self.cam_used_index[1]:
                    print("Successfully Connect")
                    self.status_text_2.configure(text="Successfully Connect")
                    self.status_text_2.place(x=margin_width * 2, y=temp_ori + 185 + 23)
                    # self.cam_prev = cv2.VideoCapture(other_text.get())
                    child_camera.after(1, lambda a=other_text.get(), b=camera: conn_cam(a, b))
                    child_camera.after(1, label_fade_2)
                    return
                else:
                    print("This Camera has already Connected")
                    self.status_text_2.configure(text="This Camera has already Connected")
                    self.status_text_2.place(x=margin_width * 2, y=temp_ori + 185 + 23)
                    child_camera.after(1, label_fade_1)
                    return
            else:
                print("Failed to Connect")
                self.status_text_2.configure(text="Failed to Connect")
                self.status_text_2.place(x=margin_width * 2, y=temp_ori + 185 + 23)
                child_camera.after(1, label_fade_2)
                return

        conn_ip_btn = Button(child_camera, text="Connect", bd=1, bg=self.color_button[0], fg=self.color_button[1],
                             activebackground=self.color_button[2], activeforeground=self.color_button[3],
                             command=lambda a=ip_web: conn_ip(a))
        conn_ip_btn['state'] = DISABLED
        conn_other_btn = Button(child_camera, text="Connect", bd=1, bg=self.color_button[0], fg=self.color_button[1],
                                activebackground=self.color_button[2], activeforeground=self.color_button[3],
                                command=lambda a=other_text: conn_other(a))
        conn_other_btn['state'] = DISABLED

        temp = temp_ori + 110
        conn_ip_btn.place(x=margin_width * 4 + 3, y=temp)
        temp = temp + 75
        conn_other_btn.place(x=margin_width * 7, y=temp)

        self.cam_setting[0] = combobox1
        self.cam_setting[1] = ip_add
        self.cam_setting[2] = ip_web
        self.cam_setting[3] = conn_ip_btn
        self.cam_setting[4] = other_layout
        self.cam_setting[5] = other_text
        self.cam_setting[6] = conn_other_btn

        def on_closing():
            self.update_frame_mode = 0
            self.cam_prev = None
            self.close = True
            self.update_screen(False)
            # self.update_setting = True
            """
            if camera == 0 and self.cam_enter:
                self.cam_enter = cv2.VideoCapture(self.cam_used_index[0])
            elif camera == 1 and self.cam_exit:
                self.cam_exit = cv2.VideoCapture(self.cam_used_index[1])
            """

            child_camera.destroy()

        def on_closing_ok():
            if camera == 0:
                self.cam_enter = self.cam_prev
                if self.cam_prev:
                    self.cam_used_index[0] = self.cam_used
                else:
                    self.cam_used_index[0] = None
            elif camera == 1:
                self.cam_exit = self.cam_prev
                if self.cam_prev:
                    self.cam_used_index[1] = self.cam_used
                else:
                    self.cam_used_index[1] = None

            self.update_frame_mode = 0
            self.cam_prev = None
            self.close = True
            self.update_screen(False)
            # self.update_setting = True
            child_camera.destroy()

        ok_btn = Button(child_camera, text="Ok", bd=1, bg=self.color_button[0], fg=self.color_button[1],
                        activebackground=self.color_button[2], activeforeground=self.color_button[3],
                        width=10, command=on_closing_ok)
        cancel_btn = Button(child_camera, text="Cancel", bd=1, bg=self.color_button[0], fg=self.color_button[1],
                            activebackground=self.color_button[2], activeforeground=self.color_button[3],
                            width=10, command=on_closing)

        ok_btn.place(x=margin_width * 3,
                     y=height - margin_width)
        cancel_btn.place(x=width - margin_width * 3,
                         y=height - margin_width)

        ok_btn.update()
        cancel_btn.update()

        ok_btn.place(x=margin_width * 3,
                     y=height - margin_width - ok_btn.winfo_height())
        cancel_btn.place(x=width - margin_width * 3 - cancel_btn.winfo_width(),
                         y=height - margin_width - cancel_btn.winfo_height())

        child_camera.protocol("WM_DELETE_WINDOW", on_closing)
        child_camera.bind("<Configure>", self.config_event)

    def radiocam_func(self, opt):
        combobox1 = self.cam_setting[0]
        ip_add = self.cam_setting[1]
        ip_web = self.cam_setting[2]
        conn_ip_btn = self.cam_setting[3]
        other_layout = self.cam_setting[4]
        other_text = self.cam_setting[5]
        conn_other_btn = self.cam_setting[6]

        if opt == 1:
            print("Connected Device")
            combobox1['state'] = 'readonly'
            ip_add['state'] = 'disabled'
            other_layout['state'] = 'disabled'
            conn_ip_btn['state'] = DISABLED
            conn_other_btn['state'] = DISABLED
            if combobox1.get() == combobox1["values"][0]:
                self.cam_prev = None
                self.label_prev.configure(image=self.no_preview)
                self.label_prev.update()
                self.label_prev.place(x=(514 / 2 - self.PREVIEW_MAXHEIGHT *
                                         (self.label_prev.winfo_width() / self.label_prev.winfo_height()) / 2)
                                      , y=48.2)

            ip_web.set("")
            other_text.set("")
        elif opt == 2:
            print("IP Address via IP Webcam")
            combobox1['state'] = 'disabled'
            ip_add['state'] = 'normal'
            other_layout['state'] = 'disabled'
            conn_ip_btn['state'] = NORMAL
            conn_other_btn['state'] = DISABLED
            self.cam_prev = None
            self.label_prev.configure(image=self.no_preview)
            self.label_prev.update()
            self.label_prev.place(x=(514 / 2 - self.PREVIEW_MAXHEIGHT *
                                     (self.label_prev.winfo_width() / self.label_prev.winfo_height()) / 2)
                                  , y=48.2)

            combobox1.current(0)
            other_text.set("")
        elif opt == 3:
            print("Other")
            combobox1['state'] = 'disabled'
            ip_add['state'] = 'disabled'
            other_layout['state'] = 'normal'
            conn_ip_btn['state'] = DISABLED
            conn_other_btn['state'] = NORMAL
            self.cam_prev = None
            self.label_prev.configure(image=self.no_preview)
            self.label_prev.update()
            self.label_prev.place(x=(514 / 2 - self.PREVIEW_MAXHEIGHT *
                                     (self.label_prev.winfo_width() / self.label_prev.winfo_height()) / 2)
                                  , y=48.2)

            combobox1.current(0)
            ip_web.set("")

    def detect_cam(self):
        self.list_cam = ["None"]
        self.list_cam_index = []

        camera = 0

        try:
            cam_enter = int(self.cam_used_index[0])
        except:
            cam_enter = -1

        try:
            cam_exit = int(self.cam_used_index[1])
        except:
            cam_exit = -1

        # print("Cam Enter: ", self.cam_used_index[0], cam_enter)
        # print("Cam Exit : ", self.cam_used_index[1], cam_exit)

        while True:
            if cam_enter != camera and cam_exit != camera:
                temp = cv2.VideoCapture(camera)
                if temp.read()[0]:
                    camera = camera + 1
                    name = "Camera " + str(camera)
                    self.list_cam.append(name)
                    self.list_cam_index.append(camera)
                    temp.release()
                else:
                    cv2.destroyAllWindows()
                    break
            else:
                camera = camera + 1

    def character_limit(self, entry_text):
        # print(ord(entry_text.get()[len(entry_text.get())-1]))
        if len(entry_text.get()) > 0:
            ascii_char = ord(entry_text.get()[len(entry_text.get()) - 1])
            # 48 is 0, 57 is 9, 46 is .
            if (ascii_char < 48 or ascii_char > 57) and ascii_char != 46:
                temp = len(entry_text.get()) - 1
                entry_text.set(entry_text.get()[:temp])

        if len(entry_text.get()) > 15:
            entry_text.set(entry_text.get()[:15])

    def update_screen(self, update):
        width = self.winfo_width()
        height = self.winfo_height()

        if update and (self.width != width or self.height != height):
            self.width = width
            self.height = height

            if round(width * 9 / 16) > height:
                gap = (round(width * 9 / 16) - height) / 2
                self.margin_width = round(10 / 100 * height * 16 / 9 + gap)
                self.margin_height = round(10 / 100 * height)
                self.main_layout = [round(width - 2 * self.margin_width),
                                    round(height - 2 * self.margin_height)]
            elif round(width * 9 / 16) < height:
                gap = (height - round(width * 9 / 16)) / 2
                self.margin_width = round(10 / 100 * width)
                self.margin_height = round(10 / 100 * width * 9 / 16 + gap)
                self.main_layout = [round(width - 2 * self.margin_width),
                                    round(height - 2 * self.margin_height)]
            else:
                self.margin_width = round(10 / 100 * width)
                self.margin_height = round(10 / 100 * height)
                self.main_layout = [round(width - 2 * self.margin_width),
                                    round(height - 2 * self.margin_height)]

            """
            self.top_frame.config(width=width, height=self.margin_height)
            # self.mid_frame.config(width=self.main_layout[0], height=self.main_layout[1])
            self.bot_frame.config(width=width, height=self.margin_height)
            self.midleft_frame.config(width=self.margin_width, height=self.main_layout[1])
            self.midright_frame.config(width=self.margin_width, height=self.main_layout[1])
            """

            # self.canvas.config(width=width, height=height)

            """
            coords = [self.canvas.bbox(self.id_enter),
                      self.canvas.bbox(self.id_exit)]
            offset = [
                # 0 = enter text
                [(50 / 100 * self.main_layout[0] / 2),
                 (10 / 100 * self.main_layout[1] / 2)],
                # 2 = exit text
                [(50 / 100 * self.main_layout[0] / 2),
                 (50 / 100 * self.main_layout[1]) + (10 / 100 * self.main_layout[1] / 2)]
            ]
            """
            # self.canvas.move(self.id_enter, offset[0][0] - self.offset[0][0], offset[0][1] - self.offset[0][1])
            # self.canvas.move(self.id_exit, offset[1][0] - self.offset[2][0], offset[1][1] - self.offset[2][1])

            self.font_size = round(self.main_layout[1] / self.FONTSIZE_RATIO)

            self.login_canvas.update_res(self)  # self.width, self.height, self.font_size

            font_setting = self.font_style + " " + str(self.font_size) + " bold"
            self.canvas.itemconfig(self.id_enter, font=font_setting)
            self.canvas.itemconfig(self.id_exit, font=font_setting)

            enter_coords = (self.margin_width + (50 / 100 * self.main_layout[0] / 2),
                            self.margin_height + (10 / 100 * self.main_layout[1] / 2))
            exit_coords = (self.margin_width + (50 / 100 * self.main_layout[0] / 2),
                           self.margin_height + (self.main_layout[1] / 2) + (10 / 100 * self.main_layout[1] / 2))
            self.canvas.coords(self.id_enter, enter_coords)
            self.canvas.coords(self.id_exit, exit_coords)

            self.left_layout.configure(width=self.main_layout[0] / 2 - 50,
                                       height=self.main_layout[1] - round(self.margin_height / 1.6))
            self.left_layout.place(x=width / 2 + 50, y=self.margin_height)

            self.frame_result.configure(width=self.main_layout[0] / 2 - 50,
                                        height=self.main_layout[1] - round(self.margin_height / 1.6))
            # width=self.main_layout[0] / 2 - 50, height=self.main_layout[1]-round(self.margin_height/1.6)
            self.frame_hist.configure(width=self.main_layout[0] / 2 - 50,
                                      height=self.main_layout[1] - round(self.margin_height / 1.6))

            width_tab = round((self.main_layout[0] / 25))  # = 65
            font_setting = self.font_style + " " + str(self.font_size)
            self.frame_hist.label_date.configure(font=font_setting)
            self.frame_hist.label_date.place(x=self.winfo_width(), y=self.winfo_height())
            self.frame_hist.label_date.update()
            font_setting = self.font_style + " " + str(round(self.font_size + self.font_size / 4)) + " bold"
            self.frame_hist.label_date_prev.configure(font=font_setting)
            self.frame_hist.label_date_next.configure(font=font_setting)
            self.frame_hist.label_date_prev.place(x=self.winfo_width(), y=self.winfo_height())
            self.frame_hist.label_date_next.place(x=self.winfo_width(), y=self.winfo_height())
            self.frame_hist.label_date_prev.update()
            self.frame_hist.label_date_next.update()
            self.s.theme_settings("MyStyle", settings={
                "TNotebook.Tab": {"configure": {"padding": [width_tab, 5],
                                                "font": (self.font_style, str(self.font_size - 2))
                                                }}})

            tab_size = [self.main_layout[0] / 2 - 50, self.main_layout[1] - round(self.margin_height / 1.6)]
            self.frame_prof.update_res(self, tab_size)
            self.frame_result.update_res(self, tab_size)
            self.frame_hist.update_res(self, tab_size)
            # HERE PROBLEM
            # self.frame_hist.label_date.place(x=tab_size[0] / 2 - self.frame_hist.label_date.winfo_width() / 2,
            #                                  y=round(5 / 100 * tab_size[1]) +
            #                                    (self.frame_hist.label_date_prev.winfo_height() -
            #                                     self.frame_hist.label_date.winfo_height()) / 2)
            # self.frame_hist.label_date_prev.place(x=tab_size[0] / 2 - self.frame_hist.label_date.winfo_width() / 2 -
            #                                         self.frame_hist.label_date_prev.winfo_width(),
            #                                       y=round(5 / 100 * tab_size[1]))
            # self.frame_hist.frame_hist.label_date_next.place(x=tab_size[0] / 2 + self.frame_hist.label_date.winfo_width() / 2,
            #                                       y=round(5 / 100 * tab_size[1]))
            # SOLUTION
            self.frame_hist.label_date_prev.place(x=tab_size[0] / 2 - self.frame_hist.label_date.winfo_width() / 2 -
                                                    self.frame_hist.label_date_prev.winfo_width(), y=0)
            self.frame_hist.label_date_next.place(x=tab_size[0] / 2 + self.frame_hist.label_date.winfo_width() / 2, y=0)
            self.frame_hist.label_date.place(x=tab_size[0] / 2 - self.frame_hist.label_date.winfo_width() / 2,
                                             y=self.frame_hist.label_date_prev.winfo_height() / 2 -
                                               self.frame_hist.label_date.winfo_height() / 2)

            self.tabs.configure(width=round(tab_size[0]), height=round(tab_size[1]))
            self.tabs.update()
            if self.frame_hist.calendar_visib:
                self.frame_hist.calendar.place(
                    x=self.tabs.winfo_width() / 2 - self.frame_hist.calendar.winfo_width() / 2,
                    y=5 / 100 * self.tabs.winfo_width() + self.frame_hist.label_date.winfo_height())

            font_setting = "Calibri " + str(round(self.font_size * 0.73))
            self.logout_btn.configure(font=font_setting)
            self.logout_btn.place(x=self.width, y=0)
            self.logout_btn.update()
            self.logout_btn.place(x=self.width - (self.margin_width / 2 + self.logout_btn.winfo_width() / 2),
                                  y=self.margin_height / 2 - self.logout_btn.winfo_height() / 2)

            # self.offset[0] = offset[0]
            # self.offset[2] = offset[1]

            if not self.cam_enter:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[0])

                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                self.msg = "Video Output is Unavailable.\nClick Here to Set Up Camera"
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_enter.configure(image=self.frame_enter_tk)

            if not self.cam_exit:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[1])
                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_exit.configure(image=self.frame_exit_tk)

            self.label_enter.place(x=self.margin_width +
                                     (50 / 100 * self.main_layout[0] - self.frame_enter_tk.width()) / 2,
                                   y=round(10 / 100 * self.main_layout[1]) + self.margin_height)
            self.label_exit.place(x=self.margin_width +
                                    (50 / 100 * self.main_layout[0] - self.frame_exit_tk.width()) / 2,
                                  y=round(60 / 100 * self.main_layout[1]) + self.margin_height)

        elif not update:
            if not self.cam_enter:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[0])

                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                self.msg = "Video Output is Unavailable.\nClick Here to Set Up Camera"
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_enter.configure(image=self.frame_enter_tk)

            if not self.cam_exit:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[1])
                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
                self.label_exit.configure(image=self.frame_exit_tk)

            self.label_enter.place(x=self.margin_width +
                                     (50 / 100 * self.main_layout[0] - self.frame_enter_tk.width()) / 2,
                                   y=round(10 / 100 * self.main_layout[1]) + self.margin_height)
            self.label_exit.place(x=self.margin_width +
                                    (50 / 100 * self.main_layout[0] - self.frame_exit_tk.width()) / 2,
                                  y=round(60 / 100 * self.main_layout[1]) + self.margin_height)

    def setup_camera(self, camera, camera_enter):
        if camera_enter:
            self.cam_enter = cv2.VideoCapture(camera)
        else:
            self.cam_exit = cv2.VideoCapture(camera)

    def update_camera_frame(self):
        if self.update_frame_mode == 0:
            """
            if self.cam_enter:
                camera, frame = self.cam_enter.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.frame_enter = Image.fromarray(cv2image)
                ratio = self.cam_enter_res[0] / self.cam_enter_res[1]
                self.frame_enter = self.frame_enter.resize((round(40 / 100 * self.main_layout[1] * ratio),
                                                            round(40 / 100 * self.main_layout[1])))
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_enter)
            else:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[0])
                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_enter = self.frame_unavailable
                self.frame_exit = self.frame_unavailable
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
                # self.frame_enter = self.frame_enter.resize((round(50 / 100 * self.main_layout[0]),
                #                                             round(40 / 100 * self.main_layout[1])))
                # self.frame_enter_tk = ImageTk.PhotoImage(self.frame_enter)

            if self.cam_exit:
                camera, frame = self.cam_exit.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.frame_exit = Image.fromarray(cv2image)
                ratio = self.cam_exit_res[0] / self.cam_exit_res[1]
                self.frame_exit = self.frame_exit.resize((round(40 / 100 * self.main_layout[1] * ratio),
                                                          round(40 / 100 * self.main_layout[1])))
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_exit)
            else:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[1])
                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_enter = self.frame_unavailable
                self.frame_exit = self.frame_unavailable
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
                # self.frame_exit = self.frame_exit.resize((round(50 / 100 * self.main_layout[0]),
                #                                           round(40 / 100 * self.main_layout[1])))
                # self.frame_exit_tk = ImageTk.PhotoImage(self.frame_exit)
            """
            if self.cam_enter:
                camera, frame = self.cam_enter.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.frame_enter = Image.fromarray(cv2image)
                ratio = self.cam_enter_res[0] / self.cam_enter_res[1]
                self.frame_enter = self.frame_enter.resize((round(40 / 100 * self.main_layout[1] * ratio),
                                                            round(40 / 100 * self.main_layout[1])))
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_enter)
                self.label_enter.configure(image=self.frame_enter_tk)
                self.label_enter.configure(image=self.frame_enter_tk)
                self.label_enter.place(x=self.margin_width +
                                         (50 / 100 * self.main_layout[0] - self.frame_enter_tk.width()) / 2,
                                       y=round(10 / 100 * self.main_layout[1]) + self.margin_height)

                vehicle, LpImg, cor = self.ai_enter.get_plate(frame, resize=False)
                self.plt_num_enter = self.ai_enter.read_plate(LpImg)
                # print(self.plt_num_enter)
            """
            else:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[0])
                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_enter = self.frame_unavailable
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_unavailable)
            """

            if self.cam_exit:
                camera, frame = self.cam_exit.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.frame_exit = Image.fromarray(cv2image)
                ratio = self.cam_exit_res[0] / self.cam_exit_res[1]
                self.frame_exit = self.frame_exit.resize((round(40 / 100 * self.main_layout[1] * ratio),
                                                          round(40 / 100 * self.main_layout[1])))
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_exit)
                self.label_exit.configure(image=self.frame_exit_tk)
                self.label_exit.configure(image=self.frame_exit_tk)
                self.label_exit.place(x=self.margin_width +
                                        (50 / 100 * self.main_layout[0] - self.frame_exit_tk.width()) / 2,
                                      y=round(60 / 100 * self.main_layout[1]) + self.margin_height)

                vehicle, LpImg, cor = self.ai_enter.get_plate(frame)
                self.plt_num_exit = self.ai_enter.read_plate(LpImg)
            """
            else:
                self.frame_unavailable = Image.new('RGB', (round(50 / 100 * self.main_layout[0]),
                                                           round(40 / 100 * self.main_layout[1])),
                                                   color=self.color_unavailable[1])
                self.font = ImageFont.truetype("arial.ttf", round(self.font_size * 1.07))
                draw = ImageDraw.Draw(self.frame_unavailable)
                w, h = draw.textsize(self.msg, font=self.font)
                draw.text((round((self.frame_unavailable.width / 2 - w / 2)),
                           round(self.frame_unavailable.height / 2 - h / 2)),
                          self.msg, "#EEEEEE", font=self.font, align=CENTER)
                self.frame_exit = self.frame_unavailable
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_unavailable)
            """
            # self.canvas.itemconfig(self.id_frame_enter, image=self.frame_enter_tk)
            # self.canvas.itemconfig(self.id_frame_exit, image=self.frame_exit_tk)

            """offset = [
                        # 0 = enter frame
                        [(50 / 100 * self.main_layout[0] / 2),
                         (10 / 100 * self.main_layout[1]) + (40 / 100 * self.main_layout[1] / 2)],
                        # 1 = exit frame
                        [(50 / 100 * self.main_layout[0] / 2),
                         (60 / 100 * self.main_layout[1]) + (40 / 100 * self.main_layout[1] / 2)]
                    ]"""

            # self.canvas.move(self.id_frame_enter, offset[0][0] - self.offset[1][0],
            #                  offset[0][1] - self.offset[1][1])
            # self.canvas.move(self.id_frame_exit, offset[1][0] - self.offset[3][0],
            #                  offset[1][1] - self.offset[3][1])

            """self.offset[1] = offset[0]
            self.offset[3] = offset[1]"""

        elif self.update_frame_mode == 1:
            if self.cam_prev and not self.update_setting:
                camera, frame = self.cam_prev.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                frame_prev = Image.fromarray(cv2image)
                ratio = self.cam_prev_res[0] / self.cam_prev_res[1]
                frame_prev = frame_prev.resize((round(self.PREVIEW_MAXHEIGHT * ratio), self.PREVIEW_MAXHEIGHT))
                self.preview_tk = ImageTk.PhotoImage(frame_prev)
                self.label_prev.place(x=(514 / 2 - self.PREVIEW_MAXHEIGHT *
                                         (self.cam_prev_res[0] / self.cam_prev_res[1]) / 2)
                                      , y=48.2)
                self.label_prev.configure(image=self.preview_tk)
            """
            else:
                # self.preview_tk = self.no_preview
                self.label_prev.place(x=(514 / 2 - self.PREVIEW_MAXHEIGHT *
                                         (self.cam_prev_res[0] / self.cam_prev_res[1]) / 2)
                                      , y=48.2)
                self.label_prev.configure(image=self.no_preview)
                # self.frame_exit = self.frame_exit.resize((round(50 / 100 * self.main_layout[0]),
                #                                           round(40 / 100 * self.main_layout[1])))
                # self.frame_exit_tk = ImageTk.PhotoImage(self.frame_exit)
            """

            # width=514, marhin_height=48.2
            # self.label_enter.place(x=self.margin_width, y=round(10 / 100 * self.main_layout[1]) + self.margin_height)

    def config_event(self, event):
        # while True:
        #     if gui.width != gui.root.winfo_width() or gui.height != gui.root.winfo_height():
        #         update = True
        #     else:
        #         update = False

        # self.width = event.width
        # self.height = event.height
        self.time_called = time.time()

        if self.update_frame_mode == 0:
            if self.cam_enter:
                camera, frame = self.cam_enter.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.frame_enter = Image.fromarray(cv2image)
                ratio = self.cam_enter_res[0] / self.cam_enter_res[1]
                self.frame_enter = self.frame_enter.resize((round(40 / 100 * self.main_layout[1] * ratio),
                                                            round(40 / 100 * self.main_layout[1])))
                self.frame_enter_tk = ImageTk.PhotoImage(self.frame_enter)
                self.label_enter.configure(image=self.frame_enter_tk)

            if self.cam_exit:
                camera, frame = self.cam_exit.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.frame_exit = Image.fromarray(cv2image)
                ratio = self.cam_exit_res[0] / self.cam_exit_res[1]
                self.frame_exit = self.frame_exit.resize((round(40 / 100 * self.main_layout[1] * ratio),
                                                          round(40 / 100 * self.main_layout[1])))
                self.frame_exit_tk = ImageTk.PhotoImage(self.frame_exit)
                self.label_exit.configure(image=self.frame_exit_tk)
        elif self.update_frame_mode == 1:
            if self.cam_prev and not self.update_setting:
                camera, frame = self.cam_prev.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                preview = Image.fromarray(cv2image)
                ratio = self.cam_prev_res[0] / self.cam_prev_res[1]
                preview = preview.resize((round(self.PREVIEW_MAXHEIGHT * ratio), self.PREVIEW_MAXHEIGHT))
                self.preview_tk = ImageTk.PhotoImage(preview)
                self.label_prev.configure(image=self.preview_tk)

        # self.update_screen(True)
        # self.update_camera_frame()

        # self.update()
        # time.sleep(0.01)

    def update_frame_sched(self):
        if self.update_frame_mode == 1 and self.canvas_index == 1:
            temp = time.time() - self.time_stats_1
            if 5 < temp < 6:
                self.time_stats_1 = time.time()
                self.status_text_1.configure(text="")

            temp = time.time() - self.time_stats_2
            if 5 < temp < 6:
                self.time_stats_2 = time.time()
                self.status_text_2.configure(text="")

        if time.time() - self.time_called > 0.1:
            self.today = datetime.date.today()
            # print(self.today)
            self.update_camera_frame()
            self.update_screen(True)
            self.update()

        self.after(10, self.update_frame_sched)

    def set_canvas_index(self, ci):
        self.canvas_index = ci

    def set_canvas(self):
        if self.canvas_index == 0:
            self.login_canvas.update_res(self.frame_hist.winfo_width(), self.frame_hist.winfo_height(), self.font_size)
        elif self.canvas_index == 1:
            self.login_canvas.place_forget()
            self.canvas.place(x=0, y=0)
            self.setting.entryconfig(self.setting.index("Camera Enter"), state=NORMAL)
            self.setting.entryconfig(self.setting.index("Camera Exit"), state=NORMAL)


def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    get_setting()
    gui = SentsGui()
    # thread = threading.Thread(target=threadfunc, daemon=True)
    # thread.start()

    gui.after(10, gui.update_frame_sched)
    gui.mainloop()


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
        text += "\ngate=\n"
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
            elif line.find("gate=") == 0:
                server_setting[6] = line.split('=')[1].replace("\n", "")
    db = MySQL(server_setting[0], server_setting[2], server_setting[3])
    fl = Filezilla(host=server_setting[0], user=server_setting[4], password=server_setting[5])


if __name__ == '__main__':
    main()
