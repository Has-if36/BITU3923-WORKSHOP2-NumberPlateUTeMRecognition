from tkinter import *
import tkinter.ttk as ttk
import tkcalendar as cal
import cv2
from PIL import Image, ImageTk, ImageFont, ImageDraw
import urllib.request
import ssl
import threading
import time
import datetime
import sys
import wmi
import re

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
CP = [['#E1D89F', 'black', '#EEEEEE', None, None, '#EEB76B', 'black', '#EEEEEE', '#E1D89F', 'black', '#FFD369'],
      ['#2B2B2B', '#EEEEEE', '#5C527F', None, None, '#261C2C', '#EEEEEE', '#5C527F', '#5C527F', '#EEEEEE', '#FFD369']]

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


# url = "https://192.168.1.17:8080/video"
# sys.setrecursionlimit(1000)

# Fetch Database
def fetch_history_owner(date):
    pass


def fetch_plate_owner(plate_number):
    pass


class SentsGui:
    class LoginCanvas(Canvas):
        def __init__(self, root, theme, screen_width, screen_height, width, height, font_size,
                     canvas_index):
            super().__init__(width=screen_width, height=screen_height, bg=CP[theme][0], highlightthickness=0)
            self.canvas_index = canvas_index
            self.root = root.root
            self.root_2 = root
            self.place(x=width, y=height)

            self.ori_logo = Image.open("./tom.png")
            self.resized_logo = self.ori_logo.resize((round(25 / 100 * height), round(25 / 100 * height)),
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
            """
            # Input
                self.login_user_strvar.get()
                self.login_pass_strvar.get()
            """

            if self.login_user_strvar.get() and self.login_pass_strvar.get():
                # Database Connection
                match_account = False
                privilege = None

                """
                # Output
                    match_account
                    privilege
                """

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
            self.resized_logo = self.ori_logo.resize((round(25 / 100 * height), round(25 / 100 * height)),
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
            self.configure(bg=CP[theme][0])
            self.login_logo_label.configure(bg=CP[theme][0])
            self.login_title_text.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.login_user_frame.configure(bg=CP[theme][0])
            self.login_user_text.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.login_pass_text.configure(bg=CP[theme][0], fg=CP[theme][1])
            self.login_btn.configure(bg=CP[theme][5], fg=CP[theme][6],
                                     activebackground=CP[theme][8], activeforeground=CP[theme][9])
            self.update()

    class LogFrame(Frame):
        def __init__(self, root, tab_size):
            self.sub_frame = []
            self.list_log = []

            super().__init__(root.tabs, width=tab_size[0], height=tab_size[1], bg=CP[root.theme][5])
            self.place(x=0, y=0)
            self.update()

            font_setting = root.font_style + " " + str(round(root.font_size + root.font_size / 4)) + " bold"
            self.label_date_prev = Label(self, text='<', font=font_setting, padx=5,
                                         bg=CP[root.theme][5], fg=CP[root.theme][6])
            self.label_date_next = Label(self, text='>', font=font_setting, padx=5,
                                         bg=CP[root.theme][5], fg=CP[root.theme][6])
            self.label_date_prev.place(x=self.winfo_width(), y=self.winfo_height())
            self.label_date_next.place(x=self.winfo_width(), y=self.winfo_height())
            self.label_date_prev.update()
            self.label_date_next.update()

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

            temp = str(root.today).split('-')
            font_setting = root.font_style + " " + str(root.font_size)
            text_date = str(temp[2]) + " " + MONTH[temp[1]] + " " + str(temp[0])
            self.label_date = Label(self, text=text_date, font=font_setting, padx=7, pady=3,
                                    bg=CP[root.theme][5], fg=CP[root.theme][6])
            self.label_date.place(x=self.winfo_width(), y=self.winfo_height())
            self.label_date.update()
            self.calendar = cal.Calendar(self, year=int(temp[0]),
                                         month=int(temp[1]), day=int(temp[2]))  # selectmode="day"

            """self.label_date.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2,
                                  y=round(5 / 100 * tab_size[1]) +
                                    (self.label_date_prev.winfo_height() - self.label_date.winfo_height()) / 2)
            self.label_date_prev.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2 -
                                         self.label_date_prev.winfo_width(), y=round(5 / 100 * tab_size[1]))
            self.label_date_next.place(x=tab_size[0] / 2 + self.label_date.winfo_width() / 2,
                                       y=round(5 / 100 * tab_size[1]))"""

            self.label_date_prev.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2 -
                                         self.label_date_prev.winfo_width(), y=0)
            self.label_date_next.place(x=tab_size[0] / 2 + self.label_date.winfo_width() / 2, y=0)
            self.label_date.place(x=tab_size[0] / 2 - self.label_date.winfo_width() / 2,
                                  y=self.label_date_prev.winfo_height() / 2 - self.label_date.winfo_height() / 2)

            self.calendar_visib = False
            self.calendar.place(x=root.tabs.winfo_width(), y=root.tabs.winfo_height())
            self.calendar.update()
            self.calendar.place_forget()

            self.label_date.bind("<ButtonPress>", lambda event, a=2: root.on_press(event, a))
            self.label_date_prev.bind("<ButtonPress>", lambda event, a=3: root.on_press(event, a))
            self.label_date_next.bind("<ButtonPress>", lambda event, a=4: root.on_press(event, a))
            root.tabs.bind("<ButtonRelease>", lambda event, a=5: root.on_release(event, a))
            self.label_date.bind("<ButtonRelease>", lambda event, a=2: root.on_release(event, a))
            self.label_date_prev.bind("<ButtonRelease>", lambda event, a=3: root.on_release(event, a))
            self.label_date_next.bind("<ButtonRelease>", lambda event, a=4: root.on_release(event, a))
            root.tabs.bind("<ButtonRelease>", lambda event, a=5: root.on_release(event, a))
            self.calendar.bind("<<CalendarSelected>>", lambda event: root.select_date(event))

    def __init__(self):
        self.cam_enter = None  # cv2.VideoCapture(0)
        self.cam_exit = None  # cv2.VideoCapture(url)
        self.cam_prev = None
        self.url = ""
        self.theme = 1
        self.canvas_index = 0
        self.font_color = ['black', "#EEEEEE"]
        # [border, bg, bg2, selectbg]
        self.color_root = [["#171010", "#E1D89F", "#D89216", "#EEB76B"], ["#171010", "#261C2C", "#2B2B2B", "#3E2C41"]]
        self.color_bg = ["#6E85B2", "#2B2B2B"]
        self.color_bg_2 = ["#EEB76B", "#261C2C"]
        self.color_unavailable = ["#171010", "#171010"]
        # [bg, fg, selectorcolor, activebackground, activeforeground]
        self.color_radiobutton = [[self.color_bg_2[0], self.font_color[0], "#EEEEEE", "#E1D89F", self.font_color[0]],
                                  [self.color_bg_2[1], self.font_color[1], "#5C527F", "#3E2C41", self.font_color[1]]]
        # [bg, fg, activebackground, activeforeground]
        self.color_optionmenu = ["#261C2C", "#6E85B2", "#3E2C41", "#EEEEEE", "#916BBF"]
        # [bg, fg, activebackground, activeforeground]
        self.color_button = ["#6E85B2", "#171010", "#5C527F", "#171010"]
        # [bg, fg, activebackground, activeforeground]
        self.color_menu = [["#EEEEEE", self.font_color[0], "#EEEEEE", self.font_color[0]],
                           ["#261C2C", self.font_color[1], "#5C527F", self.font_color[1]]]
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

        self.root = Tk()
        self.width = round(67 / 100 * self.root.winfo_screenwidth())
        self.height = round(67 / 100 * self.root.winfo_screenheight())
        self.margin_width = round(10 / 100 * self.width)
        self.margin_height = round(10 / 100 * self.height)
        self.main_layout = [round(self.width - 2 * self.margin_width), round(self.height - 2 * self.margin_height)]
        self.font_size = round(self.main_layout[1] / self.FONTSIZE_RATIO)
        # print(self.main_layout[1])

        self.today = datetime.date.today()
        self.date = datetime.date.today()

        self.root.title("UTeM SEntS Security")
        self.root.geometry('{}x{}'.format(self.width, self.height))
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)

        # self.root.resizable(False, False)
        # self.root.attributes('-fullscreen', True)

        self.root.update()
        self.login_canvas = self.LoginCanvas(self, self.theme, self.root.winfo_screenwidth(),
                                             self.root.winfo_screenheight(),
                                             self.root.winfo_width(), self.root.winfo_height(), self.font_size,
                                             self.canvas_index)
        self.canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(),
                             bg=self.color_bg[self.theme], borderwidth=0, highlightthickness=0)

        self.canvas.place(x=self.root.winfo_width(), y=self.root.winfo_width())

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
                                 bg=CP[self.theme][5], fg=CP[self.theme][6],
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
            self.root.after(1000, state_enable)

        self.menubar = Menu(self.root, background=self.color_menu[self.theme][0],
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
        self.setting.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="Setting", menu=self.setting)
        self.root.config(menu=self.menubar)
        self.root.after(1500, state_enable)

        """
        self.top_frame = Frame(self.root, bg=self.color_bg[self.theme], width=self.width, height=self.margin_height, pady=3,
                               borderwidth=0, highlightthickness=0)
        self.top_frame.grid(row=0, columnspan=3)
        # self.mid_frame = Frame(self.root, bg='white', width=self.main_layout[0], height=self.main_layout[1], pady=3)
        # self.mid_frame.grid(row=1, column=1, columnspan=1)
        self.bot_frame = Frame(self.root, bg=self.color_bg[self.theme], width=self.width, height=self.margin_height, pady=3,
                               borderwidth=0, highlightthickness=0)
        self.bot_frame.grid(row=2, columnspan=3)

        self.midleft_frame = Frame(self.root, bg=self.color_bg[self.theme], width=self.margin_width,
                                   height=self.main_layout[1], pady=0, borderwidth=0, highlightthickness=0)
        self.midleft_frame.grid(row=1, column=0, rowspan=1)
        self.midright_frame = Frame(self.root, bg=self.color_bg[self.theme], width=self.margin_width,
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
                                                fill=self.font_color[self.theme], font=font_setting, text="Enter")
        self.label_enter = Label(self.canvas, bg=self.color_bg[self.theme], borderwidth=0, highlightthickness=0)
        self.id_exit = self.canvas.create_text(self.margin_width, self.margin_height, anchor=CENTER,
                                               fill=self.font_color[self.theme], font=font_setting, text="Exit")
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
        self.text_enter = Text(self.root)
        self.text_enter.grid(row=1, column=1, columnspan=1)
        self.text_enter.config(font=('Arial', 8, 'bold'))
        self.text_enter.tag_configure("Enter", foreground="black", underline=False)
        self.text_enter.bind("<Enter>", click_text)
        self.text_enter.bind("<Leave>", hover_text)
        self.label_enter = Label(self.root, text=self.text_enter)
        """
        self.root.bind("<Configure>", self.config)
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
        width_tab = round((self.main_layout[0] / 12.7))  # = 65
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
        self.frame_result = Frame(self.tabs, width=tab_size[0], height=tab_size[1],
                                  bg=self.color_root[self.theme][1])
        # width=self.main_layout[0] / 2 - 50, height=self.main_layout[1]-round(self.margin_height/1.6)
        self.frame_hist = self.LogFrame(self, tab_size)
        # width=self.main_layout[0] / 2 - 50, height=self.main_layout[1]-round(self.margin_height/1.6)

        self.tabs.add(self.frame_result, text=f'{"Result": ^5s}')
        self.tabs.add(self.frame_hist, text=f'{"History": ^5s}')
        self.tabs.pack(expand=1, fill="both")

        # self.calendar.place(x=self.margin_width * 6, y=self.margin_height * 3)
        self.canvas.place_forget()

        def change_layout():
            self.menubar.configure(background=self.color_menu[self.theme][0], foreground=self.color_menu[self.theme][1],
                                   activebackground=self.color_menu[self.theme][2],
                                   activeforeground=self.color_menu[self.theme][3])
            self.setting.configure(background=self.color_menu[self.theme][0], foreground=self.color_menu[self.theme][1],
                                   selectcolor=self.color_menu[self.theme][3])
            self.root.config(menu=self.menubar)

            self.canvas.configure(bg=self.color_bg[self.theme])
            self.canvas.itemconfig(self.id_enter, fill=self.font_color[self.theme])
            self.label_enter.configure(bg=self.color_bg[self.theme])
            self.canvas.itemconfig(self.id_exit, fill=self.font_color[self.theme])
            self.label_exit.configure(bg=self.color_bg[self.theme])

            self.left_layout.configure(highlightbackground=self.color_root[self.theme][0],
                                       highlightcolor=self.color_root[self.theme][0])

            # Theme
            width_tab = round((self.main_layout[0] / 12.7))  # = 65
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
                                            }}
            })

            self.frame_result.configure(bg=self.color_root[self.theme][1])
            self.frame_hist.configure(bg=self.color_root[self.theme][1])

            self.frame_hist.label_date.configure(bg=self.color_root[self.theme][1], fg=self.font_color[self.theme])

            self.frame_hist.label_date_prev.configure(bg=self.color_root[self.theme][1], fg=self.font_color[self.theme])
            self.frame_hist.label_date_next.configure(bg=self.color_root[self.theme][1], fg=self.font_color[self.theme])
            self.logout_btn.configure(bg=CP[self.theme][5], fg=CP[self.theme][6],
                                      activebackground=CP[self.theme][8], activeforeground=CP[self.theme][9])

        self.root.update()

        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
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
            self.frame_hist.label_date.configure(bg=self.color_root[self.theme][1])
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
        elif layout == 3:
            self.frame_hist.label_date_prev.configure(bg=self.color_root[self.theme][1])
            self.date = self.date - datetime.timedelta(days=1)
            temp = str(self.date).split('-')
            temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
            self.frame_hist.label_date.configure(text=temp)
            self.frame_hist.calendar.selection_set(self.date)
            # self.label_date.

            # Database Stuff
        elif layout == 4:
            self.frame_hist.label_date_next.configure(bg=self.color_root[self.theme][1])
            self.date = self.date + datetime.timedelta(days=1)
            temp = str(self.date).split('-')
            temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
            self.frame_hist.label_date.configure(text=temp)
            self.frame_hist.calendar.selection_set(self.date)
            # self.label_date.
            # Database Stuff
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
        temp = str(temp).split(' ')[0].split('-')
        temp = temp[2] + ' ' + MONTH[temp[1]] + ' ' + temp[0]
        self.frame_hist.label_date.configure(text=temp)

    def setup_cam(self, camera):
        title = "Camera Setting "
        width = 514  # round(self.root.winfo_width() / 2)
        height = 530  # round(self.root.winfo_height() / 1.2)
        # print(width, height)
        x = round(self.root.winfo_width() / 2 - width / 2) + self.root.winfo_x()
        y = round(self.root.winfo_height() / 2 - height / 2) + self.root.winfo_y()
        self.update_frame_mode = 1  # Remember to set back to 0

        if camera == 0:
            title = title + "Enter"
        elif camera == 1:
            title = title + "Exit"

        child_camera = Toplevel(self.root)
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
        # self.mid_frame = Frame(self.root, bg='white', width=main_layout[0], height=main_layout[1], pady=3)
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
        child_camera.bind("<Configure>", self.config)

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
        width = self.root.winfo_width()
        height = self.root.winfo_height()

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

            self.login_canvas.update_res(self.width, self.height, self.font_size)

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

            width_tab = round((self.main_layout[0] / 12.7))  # = 65
            font_setting = self.font_style + " " + str(self.font_size)
            self.frame_hist.label_date.configure(font=font_setting)
            self.frame_hist.label_date.place(x=self.root.winfo_width(), y=self.root.winfo_height())
            self.frame_hist.label_date.update()
            font_setting = self.font_style + " " + str(round(self.font_size + self.font_size / 4)) + " bold"
            self.frame_hist.label_date_prev.configure(font=font_setting)
            self.frame_hist.label_date_next.configure(font=font_setting)
            self.frame_hist.label_date_prev.place(x=self.root.winfo_width(), y=self.root.winfo_height())
            self.frame_hist.label_date_next.place(x=self.root.winfo_width(), y=self.root.winfo_height())
            self.frame_hist.label_date_prev.update()
            self.frame_hist.label_date_next.update()
            self.s.theme_settings("MyStyle", settings={
                "TNotebook.Tab": {"configure": {"padding": [width_tab, 5],
                                                "font": (self.font_style, str(self.font_size - 2))
                                                }}})

            tab_size = [self.main_layout[0] / 2 - 50, self.main_layout[1] - round(self.margin_height / 1.6)]
            self.frame_hist.label_date.place(x=tab_size[0] / 2 - self.frame_hist.label_date.winfo_width() / 2,
                                             y=round(5 / 100 * tab_size[1]) +
                                               (self.frame_hist.label_date_prev.winfo_height() -
                                                self.frame_hist.label_date.winfo_height()) / 2)
            self.frame_hist.label_date_prev.place(x=tab_size[0] / 2 - self.frame_hist.label_date.winfo_width() / 2 -
                                                    self.frame_hist.label_date_prev.winfo_width(),
                                                  y=round(5 / 100 * tab_size[1]))
            self.frame_hist.label_date_next.place(x=tab_size[0] / 2 + self.frame_hist.label_date.winfo_width() / 2,
                                                  y=round(5 / 100 * tab_size[1]))

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

    def config(self, event):
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

        # self.root.update()
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
            self.root.update()

        self.root.after(10, self.update_frame_sched)

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
    gui = SentsGui()
    # thread = threading.Thread(target=threadfunc, daemon=True)
    # thread.start()

    gui.root.after(10, gui.update_frame_sched)
    gui.root.mainloop()


if __name__ == '__main__':
    main()