import os.path
import random
import tkinter
import tkinter.filedialog
import customtkinter as c
from PIL import Image
import webbrowser
from typing import Union
from os import listdir
import json
import threading
from bot import *
from text import *
from queue import *
from credential_management import *
from download import start_direct_download


c.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
c.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

products = dict()
try:
    file = open("prods.json","r")
    products = json.load(file)
except:
    pass

languages = list(LAN_dict.keys())
try:
    LAN = LAN_dict[products.pop("language")]
except:
    LAN = 1

all_products = list()
for (key,value) in products.items():
    all_products.append(f"{key} - {value}")


EN_SCALE = 0
notif_cnt = 0
how_many_countries = 0
file_ok = ""
chrome_ok = ""
download_finished_status = 0

current_path = os.path.realpath(os.path.dirname(__file__))
current_path = current_path.replace("\\","/")
media_path = current_path + "/media/"

log_pipe = Queue()
bot_pipe = Queue()

def check_chromedriver():
    global chrome_ok
    if "chromedriver.exe" in listdir(current_path):
        chrome_ok = "green"
    else:
        chrome_ok = "#565B5E"

def chrome_open():
    webbrowser.open(chromedriver_link)

def discord_open():
    webbrowser.open(discord_link)

def telegram_open():
    webbrowser.open(telegram_link)

def support():
    webbrowser.open(support_link)

def direct_download_chromedriver() -> int:
    return start_direct_download(current_path)

def get_centered_geometry_string(window: c.CTk, w: int, h: int) -> str:
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = int(ws/2) - int(w/2)
    y = int(hs/2) - int(h/2)
    return "%dx%d+%d+%d" % (w, h, x, y)


class Management(c.CTkToplevel):
    def __init__(self):
        super().__init__()
        self._upd: Union[int, None] = None
        self._upd = 0
        self.geometry(get_centered_geometry_string(self,w=400,h=270))
        self.grab_set()
        self.resizable(False, False)
        self.title(Gestisci[LAN])
        self.frame = c.CTkFrame(self, width=170, corner_radius=20)
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.grid_rowconfigure((0,2,4,6), weight=1)

        self.code_label = c.CTkLabel(self, text=Codice[LAN], font=c.CTkFont(family="arial", size=15, weight="bold"))
        self.code_label.place(relx=0.17+EN_SCALE, rely=0.06)
        self.code = c.CTkEntry(self, width=220)
        self.code.place(relx=0.045, rely=0.15)

        self.name_label = c.CTkLabel(self, text=Nome[LAN], font=c.CTkFont(family="arial", size=15, weight="bold"))
        self.name_label.place(relx=0.26, rely=0.28)
        self.name = c.CTkEntry(self, width=220)
        self.name.place(relx=0.045, rely=0.37)

        self.add_button = c.CTkButton(self, height=30, width=100, text=Aggiungi[LAN], font=c.CTkFont(family="arial", size=15, weight="bold"), fg_color="green", hover_color="dark green", command=self.add_event)
        self.add_button.place(relx=0.67, rely=0.26)

        self.code_menu = c.CTkOptionMenu(self, values=all_products, width=220, dynamic_resizing=False)
        self.code_menu.place(relx=0.045, rely=0.6)
        if len(all_products) > 0:
            self.code_menu.set(all_products[0])
        else:
            self.code_menu.set(Nessun_prodotto[LAN])

        self.remove_button = c.CTkButton(self, height=30, width=100, text=Elimina[LAN], font=c.CTkFont(family="arial", size=15, weight="bold"), fg_color="#C41D1D", hover_color="dark red", command=self.remove_event)
        self.remove_button.place(relx=0.67, rely=0.598)

        self.info = c.CTkLabel(self, text=INFO_MNG[LAN])
        self.info.grid(row=7,column=1, columnspan=6)

    def add_event(self):
        success = 1
        c_entry = self.code.get()
        n_entry = self.name.get()
        if len(c_entry) != 10:
            self.code.configure(border_color="red", border_width=2)
            success = 0
        else:
            self.code.configure(border_color="#565B5E")
        if len(n_entry) < 1:
            self.name.configure(border_color="red", border_width=2)
            success = 0
        else:
            self.name.configure(border_color="#565B5E")

        if success == 0:
            self.error_window(Formato_dati[LAN])
            return

        for product in all_products:
            if c_entry == product[:10]:
                self.error_window(Prodotto_esistente[LAN])
                return
        products[c_entry] = n_entry
        all_products.append(f"{c_entry} - {n_entry}")
        file1 = open(r"prods.json", "w+")
        json.dump(products, file1)
        file1.close()
        self.exit_window()
        self._upd = 1
        return

    def remove_event(self):
        entry = self.code_menu.get()[:10]
        if entry[0] == 'N':
            self.error_window(Nessun_prodotto[LAN])
            return
        for product in all_products:
            if entry == product[:10]:
                all_products.remove(product)
                products.pop(entry)
                file1 = open(r"prods.json", "w")
                json.dump(products, file1)
                file1.close()
                self.exit_window()
                self._upd = 1
                return
        self.error_window(Prodotto_inesistente[LAN])

    def error_window(self,msg):
        error_window = c.CTkToplevel(self)
        error_window.geometry(get_centered_geometry_string(error_window,w=300,h=100))
        error_window.resizable(False, False)
        error_window.grab_set()
        error_window.title(Errore[LAN])
        error_window.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        error_window.grid_columnconfigure((0,1,2,3,4,5), weight=0)
        error_window.label = c.CTkLabel(error_window,text=msg, height=10)
        error_window.label.grid(row=0, column=0, padx=(20,0), pady=(25,0))
        error_window.button = c.CTkButton(error_window, text="OK", command=error_window.destroy)
        error_window.button.grid(row=1, column=0, padx=(50,0), pady=(20,0))
        pic = c.CTkImage(dark_image=Image.open(f"{media_path}exclamation.png"), size=(60,60))
        error_window.pic = c.CTkButton(error_window, image=pic, width=50, text="", fg_color="transparent", hover=False)
        error_window.pic.place(relx=0.7, rely=0.13)

    def exit_window(self):
        self.grab_release()
        self.destroy()

    def get_upd(self):
        self.master.wait_window(self)
        return self._upd


class Logger(c.CTk):
    def __init__(self):
        super().__init__()

        self._no_of_reports: int
        self._no_of_reports = 0
        self._res: int
        self._res = -1
        default_font = c.CTkFont(family="arial", size=15, weight="bold")

        # configure window
        self.title("Logger")
        self.geometry(get_centered_geometry_string(self,w=500,h=600))
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        self.logger = c.CTkTextbox(self, width=350, height=500, corner_radius=20, font=c.CTkFont(family="arial", size=14, weight="bold"), state="disabled")
        self.logger.grid(row=1, column=1, columnspan=4, pady=15)

        self.reports = c.CTkLabel(self, width=40, font=c.CTkFont(family="arial", size=13, weight="bold"), text=Segnalazioni[LAN] + '0')
        self.reports.place(relx=0.08, rely=0.913)

        self.exit_button = c.CTkButton(self, height=40, text=Esci[LAN], font=default_font, fg_color="#C41D1D", hover_color="dark red", command=self.kill)
        self.exit_button.grid(row=4, column=2, columnspan=2, padx=30, pady=10)

        self.delete_history = c.CTkButton(self, height=30, width=50, text=Cronologia[LAN], font=c.CTkFont(family="arial", size=12, weight="bold"), command=self.delete_history)
        self.delete_history.place(relx=0.75, rely=0.905)

    def kill(self):
        if self._res == -1:
            bot_pipe.put(False)
        self.grab_release()
        self.destroy()

    def delete_history(self):
        self.logger.configure(state="normal")
        self.logger.delete("0.0","end")
        self.logger.configure(state="disabled")
        self.reports.configure(text=Segnalazioni[LAN] + "0")
        self._no_of_reports = 1

    def log_write(self):
        title_is_not_arrived = 1
        cnt = 0
        while True:
            if not bot_pipe.empty():
                exit()
            self.logger.configure(state="disabled")
            log = log_pipe.get(block=True)
            self.logger.configure(state="normal")
            if isinstance(log, str):
                if log[0:3] == "#@$" and title_is_not_arrived:
                    title_is_not_arrived = 0
                    if len(log) < 40:
                        self.title(log[3:40])
                    else:
                        self.title(log[3:40] + "...")

                elif log[0:3] == "&&&":             # messages
                    if log[3] not in ['R','C','S','❌']:
                        cnt += 1
                        self._no_of_reports += 1
                    self.logger.insert("end", text=log[3:])
                    self.reports.configure(text=Segnalazioni[LAN] + f"{self._no_of_reports}")
                    if cnt == how_many_countries and how_many_countries > 1:
                        self.logger.insert("end",61*"-"+"\n")
                        cnt = 0

            else:
                self.logger.insert("end", text="Wrong pipe format")
            self.logger.configure(state="disabled")


class App(c.CTk):
    def __init__(self):
        super().__init__()

        self._conditions = tkinter.IntVar(value=0)
        self._sellers: list = []
        self._sellers_string: str = ""
        self._notif: int
        self._notif = 0
        self._stores = []
        self._guide_window = None
        default_font = c.CTkFont(family="arial", size=15, weight="bold")
        telegram = c.CTkImage(dark_image=Image.open(f"{media_path}telegram.png"), size=(39, 32))
        discord = c.CTkImage(dark_image=Image.open(f"{media_path}discord.png"), size=(38, 28))
        support_img = c.CTkImage(dark_image=Image.open(f"{media_path}support.png"), size=(30, 30))
        mng = c.CTkImage(dark_image=Image.open(f"{media_path}mng.png"), size=(30, 30))
        fld = c.CTkImage(dark_image=Image.open(f"{media_path}folder.png"), size=(31, 25))
        stg = c.CTkImage(dark_image=Image.open(f"{media_path}stg.png"), size=(30, 30))

        mail, password = get_credentials()

        # configure window
        self.title("Amazon Bot © @swordsman210")
        self.geometry(get_centered_geometry_string(self,w=830,h=486))
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)

# -----------------------------------------------          SIDEBAR        ------------------------------------------------------------

        self.sidebar_frame = c.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure((0,1,2), weight=2)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = c.CTkLabel(self.sidebar_frame, text="Amazon\nBot", font=c.CTkFont(family="arial",size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 6))
        self.sidebar_start_button = c.CTkButton(self.sidebar_frame, height=40, text=Avvia[LAN], font=default_font, fg_color="green", hover_color="dark green", command=self.start_event)
        self.sidebar_start_button.grid(row=1, column=0, columnspan=3, padx=30, pady=10)
        self.sidebar_exit_button = c.CTkButton(self.sidebar_frame, height=40, text=Esci[LAN], font=default_font, fg_color="#C41D1D", hover_color="dark red", command=self.destroy)
        self.sidebar_exit_button.grid(row=2, column=0, columnspan=3, padx=20, pady=10)
        self.sidebar_language_label = c.CTkLabel(self.sidebar_frame, text=Select_lan[LAN])
        self.sidebar_language_label.place(relx=0.25,rely=0.65)
        self.sidebar_language_selection = c.CTkOptionMenu(self.sidebar_frame, width=100, values=languages)
        self.sidebar_language_selection.place(relx=0.25, rely=0.73)
        self.sidebar_language_selection.set(languages[LAN])
        self.sidebar_guide_button = c.CTkButton(self.sidebar_frame, height=30, text=Guida[LAN], font=default_font, text_color="black", fg_color="#ffd900", hover_color="#b8ab02", command=self.guide_open)
        self.sidebar_guide_button.grid(row=6, column=0, columnspan=3, padx=20, pady=(188, 10))
        self.sidebar_discord_button = c.CTkButton(self.sidebar_frame, width=9, height=10, image=discord,  text='', fg_color="transparent", command=discord_open)
        self.sidebar_discord_button.grid(row=8, column=0, pady=0)
        self.sidebar_telegram_button = c.CTkButton(self.sidebar_frame, width=9, height=10, image=telegram, text='', fg_color="transparent", command=telegram_open)
        self.sidebar_telegram_button.grid(row=8, column=1, pady=1)
        self.sidebar_support_button = c.CTkButton(self.sidebar_frame, width=10, height=10, image=support_img, text='', fg_color="transparent", hover_color="green", command=support)
        self.sidebar_support_button.grid(row=8, column=2,  pady=1)

# -----------------------------------------------          PRODUCT        ------------------------------------------------------------

        self.product_frame = c.CTkFrame(self,width=100,corner_radius=20)
        self.product_frame.grid(row=0, column=0, columnspan=8, padx=(65,17),pady=17)
        self.product_frame.grid_columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.product_label = c.CTkLabel(self.product_frame, text=Dettagli_prod[LAN], font=c.CTkFont(family="arial",size=17, weight="bold"))
        self.product_label.grid(row=0, column=4, padx=0, pady=20)
        self.code_label = c.CTkLabel(self.product_frame, text=Codice[LAN], font=default_font)
        self.code_label.grid(row=1, column=4, pady=0)
        self.code = c.CTkOptionMenu(self.product_frame,values=all_products,width=220,dynamic_resizing=False)
        self.code.grid(row=2, columnspan=6,  padx=(20, 0), pady=(0,20), sticky="w")
        if len(all_products) > 0:
            self.code.set(all_products[0])
        else:
            self.code.set(Nessun_prodotto[LAN])
        self.product_mng_button = c.CTkButton(self.product_frame, width=1, height=1, image=mng, text='', fg_color="transparent", hover=False, command=self.open_management)
        self.product_mng_button.place(relx=0.835,rely=0.415)
        self.price_label = c.CTkLabel(self.product_frame, text=Prezzo_max[LAN], font=default_font)
        self.price_label.grid(row=4, column=4)
        self.price = c.CTkEntry(self.product_frame, width=255)
        self.price.grid(row=5, columnspan=8, padx=(20, 20), pady=(0, 20), sticky="nsew")

# -----------------------------------------------          ACCOUNT        ------------------------------------------------------------

        self.account_frame = c.CTkFrame(self, width=300, corner_radius=20)
        self.account_frame.grid(row=0, column=0, columnspan=10, padx=(515,0), pady=(17,17))
        self.account_frame.grid_columnconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.account_label = c.CTkLabel(self.account_frame, text=Dettagli_acc[LAN], font=c.CTkFont(family="arial", size=17, weight="bold"))
        self.account_label.grid(row=0, column=0, columnspan=8, pady=20)
        self.mail_label = c.CTkLabel(self.account_frame, text="Mail", font=default_font)
        self.mail_label.grid(row=1, column=0, columnspan=8)
        self.mail = c.CTkEntry(self.account_frame, width=255)
        self.mail.insert(0,mail)
        self.mail.grid(row=2, columnspan=8, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.password_label = c.CTkLabel(self.account_frame, text="Password", font=default_font)
        self.password_label.grid(row=4, column=0, columnspan=5)
        self.password = c.CTkEntry(self.account_frame, width=155, show='●', font=c.CTkFont(size=10))
        self.password.insert(0,password)
        self.password.grid(row=5, columnspan=5, padx=(20, 20), pady=(0, 20), sticky="nsew")
        self.save_credentials = c.CTkCheckBox(master=self.account_frame, text=Salva_credenziali[LAN])
        self.save_credentials.select()
        self.save_credentials.place(relx=0.65, rely=0.77)

# -----------------------------------------------          SETTINGS        ------------------------------------------------------------

        self.settings_frame = c.CTkFrame(self, width=400, corner_radius=20)
        self.settings_frame.grid(row=1, column=0, columnspan=8, rowspan=5, padx=(151-EN_SCALE*1100,17-EN_SCALE*850), pady=(0,30))
        self.settings_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.settings_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.chromedriver_label = c.CTkLabel(self.settings_frame, text="Chromedriver", font=default_font)
        self.chromedriver_label.grid(row=1, column=0, padx=(40,0), pady=(20,0))
        self.chromedriver = c.CTkEntry(self.settings_frame, width=217, border_color=chrome_ok)
        self.chromedriver.insert(0,File_trovato[chrome_ok])
        self.chromedriver.grid(row=2, columnspan=5, padx=(20, 0), pady=(0, 20), sticky="w")
        self.chromedriver_button = c.CTkButton(self.settings_frame, width=1, height=1, image=fld, text='', fg_color="transparent", hover=False, command=self.file_browse)
        self.chromedriver_button.place(relx=0.64+EN_SCALE, rely=0.205)
        self.telegram_label = c.CTkLabel(self.settings_frame, text=Telegram_Username[LAN], font=default_font)
        self.telegram_label.grid(row=4, column=0, padx=(70,0), pady=(10,0))
        self.telegram = c.CTkEntry(self.settings_frame, placeholder_text=Opzionale[LAN], width=250)
        self.telegram.grid(row=5, columnspan=5,rowspan=8, padx=(20, EN_SCALE*500), pady=(0, 60))
        self.notif = c.CTkCheckBox(master=self.settings_frame, text=Modalita_notif[LAN], command=self.notif_activate)
        self.notif.place(relx=0.058, rely=0.83)
        self.time = c.CTkSlider(self.settings_frame, height=150, from_=30, to=300, number_of_steps=270, orientation="vertical", command=self.read_slider)
        self.time.place(relx=0.835+EN_SCALE*0.8, rely=0.05)
        self.time.set(120)
        self.time_label = c.CTkLabel(self.settings_frame, text=f"{Aggiornamento[LAN]}:\n 120s")
        self.time_label.grid(row=6, column=8, columnspan=6, padx=(10, 10), pady=(15, 0), sticky="se")

# -----------------------------------------------          DETAILS        ------------------------------------------------------------

        self.details_frame = c.CTkFrame(self, width=208, corner_radius=20)
        self.details_frame.place(relx=0.73-EN_SCALE*0.25, rely=0.518)
        self.details_frame.grid_columnconfigure((0,1), weight=1)
        self.details_frame.grid_rowconfigure((0,1), weight=1)
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = c.CTkLabel(master=self.details_frame, text=Acquistare[LAN])
        self.label_radio_group.grid(row=0, column=0, padx=(20,50+EN_SCALE*500), pady=(10,185))
        self.it = c.CTkCheckBox(master=self.details_frame, text="IT")
        self.it.place(relx=0.1, rely=0.2)
        self.it.select()
        self.uk = c.CTkCheckBox(master=self.details_frame, text="UK")
        self.uk.place(relx=0.4, rely=0.2)
        self.de = c.CTkCheckBox(master=self.details_frame, text="DE")
        self.de.place(relx=0.7, rely=0.2)
        self.fr = c.CTkCheckBox(master=self.details_frame, text="FR")
        self.fr.place(relx=0.1, rely=0.4)
        self.es = c.CTkCheckBox(master=self.details_frame, text="ES")
        self.es.place(relx=0.4, rely=0.4)
        self._stores.append(self.it)
        self._stores.append(self.uk)
        self._stores.append(self.de)
        self._stores.append(self.fr)
        self._stores.append(self.es)
        self.headless = c.CTkCheckBox(master=self.details_frame, text="Headless mode")
        self.headless.place(relx=0.1, rely=0.6)
        #self.headless.select()
        self.settings_button = c.CTkButton(self.details_frame, width=50, height=30, image=stg, text=Opzioni[LAN], corner_radius=100, hover=True, command=self.other_options)
        self.settings_button.place(relx=0.068, rely=0.77)

    def other_options(self):
        other_options = c.CTkToplevel(self)
        other_options.geometry(get_centered_geometry_string(other_options,w=400,h=300))
        other_options.grab_set()
        other_options.resizable(False, False)
        other_options.title(Opzioni[LAN])

        def save_event():
            self._sellers_string = ''
            for seller in other_options.sellers_entry.get().split(','):
                self._sellers.append(seller)
                self._sellers_string += seller+','
            self._sellers_string = self._sellers_string[:-1]
            other_options.grab_release()
            other_options.destroy()

        def discard_event():
            self._conditions = tkinter.IntVar(value=0)
            self._sellers_string = ''
            other_options.sellers_entry.delete('0','end')
            other_options.grab_release()
            other_options.destroy()

        other_options.product_conditions_label = c.CTkLabel(other_options,text=Condizioni["title"][LAN], font=c.CTkFont(family="arial", size=16, weight="bold"))
        other_options.product_conditions_label.place(relx=0.08, rely=0.06)
        other_options.all_conditions = c.CTkRadioButton(other_options, text=Condizioni["any"][LAN], variable=self._conditions, value=0)
        other_options.all_conditions.place(relx=0.08, rely=0.2)
        other_options.only_new = c.CTkRadioButton(other_options, text=Condizioni["new"][LAN], variable=self._conditions, value=1)
        other_options.only_new.place(relx=0.38, rely=0.2)
        other_options.only_used = c.CTkRadioButton(other_options, text=Condizioni["used"][LAN], variable=self._conditions, value=2)
        other_options.only_used.place(relx=0.68, rely=0.2)

        other_options.sellers_label = c.CTkLabel(other_options, text=Venditori[LAN], font=c.CTkFont(family="arial", size=16, weight="bold"))
        other_options.sellers_label.place(relx=0.08, rely=0.35)
        other_options.sellers_entry = c.CTkEntry(other_options, width=245)
        other_options.sellers_entry.insert('0',self._sellers_string)
        other_options.sellers_entry.place(relx=0.3, rely=0.35)
        other_options.sellers_description = c.CTkLabel(other_options, text=INFO_SLR[LAN],justify="left")
        other_options.sellers_description.place(relx=0.08, rely=0.5)

        other_options.remove_button = c.CTkButton(other_options, height=30, width=100, text=Annulla[LAN],
                                         font=c.CTkFont(family="arial", size=15, weight="bold"), fg_color="#C41D1D",
                                         hover_color="dark red", command=discard_event)
        other_options.remove_button.place(relx=0.13, rely=0.82)
        other_options.save_button = c.CTkButton(other_options, height=30, width=100, text=Salva[LAN],
                                      font=c.CTkFont(family="arial", size=15, weight="bold"), fg_color="green",
                                      hover_color="dark green", command=save_event)
        other_options.save_button.place(relx=0.65, rely=0.82)


    def error_window(self,msg):
        error_window = c.CTkToplevel(self)
        error_window.geometry(get_centered_geometry_string(error_window,w=300,h=100))
        error_window.resizable(False, False)
        error_window.grab_set()
        error_window.title(Errore[LAN])
        error_window.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        error_window.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=0)
        error_window.label = c.CTkLabel(error_window, text=msg, height=10)
        error_window.label.grid(row=0, column=0, padx=(20, 0), pady=(25, 0))
        error_window.button = c.CTkButton(error_window, text="OK", command=error_window.destroy)
        error_window.button.grid(row=1, column=0, padx=(50, 0), pady=(20, 0))
        pic = c.CTkImage(dark_image=Image.open(f"{media_path}exclamation.png"), size=(60, 60))
        error_window.pic = c.CTkButton(error_window, image=pic, width=50, text="", fg_color="transparent", hover=False)
        error_window.pic.place(relx=0.7, rely=0.13)

    def file_browse(self):
        path = tkinter.filedialog.askopenfilename(initialdir=media_path[:-6],title="Select Chromedriver", filetypes=(("", ""), ("", ".exe")))
        self.chromedriver.insert(0,path)

    def read_slider(self,value):
        self.time_label.configure(text=f"{Aggiornamento[LAN]}:\n {int(value)}s")

    def notif_activate(self):
        if self._notif % 2:
            self.mail_label.configure(text_color='white')
            self.mail.configure(state='normal',text_color='white')
            self.password_label.configure(text_color='white')
            self.password.configure(state='normal',text_color='white')
            self.telegram.configure(placeholder_text=Opzionale[LAN])
        else:
            self.mail_label.configure(text_color='grey')
            self.mail.configure(state='disabled',text_color='grey',border_color="#565B5E")
            self.password_label.configure(text_color='grey')
            self.password.configure(state='disabled',text_color='grey',border_color="#565B5E")
            self.telegram.configure(placeholder_text='',text_color='white')
        self._notif += 1

    def destroy(self):
        tkinter.Tk.destroy(self)
        products["language"] = self.sidebar_language_selection.get()
        file = open("prods.json", "w+")
        json.dump(products, file)
        file.close()
        exit()

    def guide_open(self):
        guide_window = c.CTkToplevel(self)
        self._guide_window = guide_window
        guide_window.geometry(get_centered_geometry_string(guide_window,w=700,h=700-EN_SCALE*4000))
        guide_window.grab_set()
        guide_window.resizable(False,False)
        guide_window.title(Guida_utilizzo[LAN])
        guide_window.grid_columnconfigure((0,1),weight=5)
        guide_window.grid_rowconfigure(1, weight=1)

        guide_window.guide = c.CTkLabel(master=guide_window, text=GUIDE_TEXT[LAN])
        guide_window.guide.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        guide_window.download_button = c.CTkButton(guide_window, height=30, text=Download_manuale[LAN], command=chrome_open)
        guide_window.download_button.grid(row=1, column=0, padx=20, pady=10)
        guide_window.direct_download_button = c.CTkButton(guide_window, height=30, text=Download_diretto[LAN], command=self.attempt_chromedriver_download)
        guide_window.direct_download_button.grid(row=1, column=1, padx=20, pady=10)

    def attempt_chromedriver_download(self):
        popup = self.open_confirmation_popup()
        popup.master.wait_window(popup)
        choice = popup._choice
        if not choice:
            return
        pb_thread = threading.Thread(target=self.open_progressbar)
        pb_thread.start()
        result = direct_download_chromedriver()
        global download_finished_status
        download_finished_status = result
    
    def open_confirmation_popup(self):
        conf_popup = c.CTkToplevel(self._guide_window)
        conf_popup.geometry(get_centered_geometry_string(conf_popup,w=300,h=100))
        conf_popup.title('')
        conf_popup.grab_set()
        conf_popup.resizable(False,False)
        conf_popup.grid_columnconfigure((0,1),weight=5)
        conf_popup.grid_rowconfigure(1, weight=1)
        conf_popup._choice = False

        conf_popup.guide = c.CTkLabel(master=conf_popup, text=Download_diretto_exp[LAN])
        conf_popup.guide.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        def close_popup():
            conf_popup.destroy()
        conf_popup.close_button = c.CTkButton(conf_popup, height=30, text=Annulla[LAN], command=close_popup)
        conf_popup.close_button.grid(row=1, column=0, padx=20, pady=10)

        def send_confirm():
            conf_popup._choice = True
            conf_popup.destroy()
        conf_popup.confirm_button = c.CTkButton(conf_popup, height=30, text=Conferma[LAN], command=send_confirm)
        conf_popup.confirm_button.grid(row=1, column=1, padx=20, pady=10)

        return conf_popup
    
    def open_progressbar(self):
        pb = self.progressbar()
        global download_finished_status
        time.sleep(1+random.randint(1,3))
        global chrome_ok
        while True:
            if download_finished_status > 0:
                pb._close()
                try:
                    chrome_ok = "green"
                    self.chromedriver.delete(0,"end")
                    self.chromedriver.insert(0,File_trovato[chrome_ok])
                    SuccessWindow(type="success").mainloop()
                except: pass
                break
            elif download_finished_status < 0:
                pb._close()
                try:
                    chrome_ok = "#565B5E"
                    self.chromedriver.delete(0,"end")
                    SuccessWindow(type="error").mainloop()
                except: pass
                break
        self.chromedriver.configure(border_color=chrome_ok)
        return

    def progressbar(self):
        pb = c.CTkToplevel(self._guide_window)
        pb._result = -1
        pb.geometry(get_centered_geometry_string(pb,w=300,h=100))
        pb.resizable(False, False)
        pb.grab_set()
        pb.title('')
        pb.frame = c.CTkFrame(pb, width=170, corner_radius=20)
        pb.grid_columnconfigure(0, weight=1)
        pb.grid_rowconfigure(0, weight=1)

        pb.progress_bar = c.CTkProgressBar(pb, orientation="horizontal", mode="indeterminate")
        pb.progress_bar.grid(row=0, column=0)
        pb.progress_bar.start()

        def close():
            pb.progress_bar.stop()
            pb.destroy()

        pb._close = close
        return pb

    def open_management(self):
        upd = Management().get_upd()
        if upd == 1:
            self.code.configure(values=all_products)
            if len(all_products) > 0:
                self.code.set(all_products[0])
                self.product_mng_button.configure(border_color="", border_width=0)
            else:
                self.code.set(Nessun_prodotto[LAN])
            self.code.update()

    def start_event(self):
        success = 1

        # PRODUCT DETAILS
        notif = self.notif.get()
        code = self.code.get()[:10]
        if code[6].isspace() or code[6] == 'e':
            self.product_mng_button.configure(border_color="red", border_width=1)
            success = 0
        else:
            self.product_mng_button.configure(border_color="", border_width=0)
        price = self.price.get()
        if not price.isdigit():
            self.price.configure(border_color="red", border_width=2)
            success = 0
        else:
            self.price.configure(border_color="#565B5E")
            price = int(price)

        # ACCOUNT DETAILS
        mail = self.mail.get()
        password = self.password.get()
        if ("@" not in mail or len(mail) == 0) and notif == 0:
            self.mail.configure(border_color="red", border_width=2)
            success = 0
        else:
            self.mail.configure(border_color="#565B5E")
        if len(password) == 0 and notif == 0:
            self.password.configure(border_color="red", border_width=2)
            success = 0
        else:
            self.password.configure(border_color="#565B5E")
        save = self.save_credentials.get()
        if save == 1:
            store_credentials(mail, password)
        else:
            delete_credentials()

        # CONFIG DETAILS
        if chrome_ok == "#565B5E":
            chromedriver = self.chromedriver.get()
            if len(chromedriver) == 0:
                self.chromedriver.configure(border_color="red", border_width=2)
                success = 0
            else:
                self.chromedriver.configure(border_color="#565B5E")
        else:
            chromedriver = media_path[:-6] + "chromedriver.exe"
        telegram = self.telegram.get()
        if (len(telegram) != 0 and telegram[0] != '@') or (len(telegram) == 0 and notif):
            self.telegram.configure(border_color="red", border_width=2)
            success = 0
        if len(telegram) > 1 and telegram[0] == '@':
            self.telegram.configure(border_color="#565B5E")
        refresh = int(self.time.get())

        # AMAZON SETTINGS
        stores = []
        i = -1
        global how_many_countries
        for store in self._stores:
            i += 1
            if store.get():
                stores.append(COUNTRIES[i])
                how_many_countries += 1
        if how_many_countries == 0:
            success = 0
            for store in self._stores:
                store.configure(border_color="red", border_width=2)
        else:
            for store in self._stores:
                store.configure(border_color="#949A9F", border_width=3)
        headless = bool(self.headless.get())
        conditions = self._conditions.get()
        sellers = self._sellers_string

        if success:
            self.withdraw()
            for country in stores:
                short_url = f"https://www.amazon.{country}/dp/{code}"
                url = short_url + "/ref=olp-opf-redir?aod=1&ie=UTF8&condition=ALL"
                bot_thread = threading.Thread(target=bot, args=(LAN, price, mail, password, country, telegram, chromedriver, url, short_url, refresh, notif, headless, conditions, sellers, log_pipe, bot_pipe))
                bot_thread.start()
            l = LogThread()
            l.logger = Logger()
            l.start()
            l.logger.mainloop()
            exit()


class SuccessWindow(c.CTkToplevel):
    def __init__(self, type: str):
        super().__init__()
        self.geometry(get_centered_geometry_string(self,w=300,h=150))
        self.grab_set()
        self.resizable(False, False)
        self.title("")
        self.frame = c.CTkFrame(self, width=170, corner_radius=20)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        self.grid_columnconfigure((0,1), weight=0)

        match type:
            case "success":
                self.message = Chromedriver_success[LAN]
                self.media = f"{media_path}success.png"
            case "error":
                self.message = Qualcosa[LAN]
                self.media = f"{media_path}exclamation.png"

        self.label = c.CTkLabel(self, text=self.message, height=10)
        self.label.grid(row=0, column=0, padx=(20, 0), pady=(25, 0))
        self.button = c.CTkButton(self, text="OK", width=75, command=self.close)
        self.button.grid(row=1, column=0, padx=(20, 0))
        pic = c.CTkImage(dark_image=Image.open(self.media), size=(60, 60))
        self.pic = c.CTkButton(self, image=pic, width=50, text="", fg_color="transparent", hover=False)
        self.pic.grid(row=0, rowspan=2, column=1, padx=(20,0))
    
    def close(self):
        self.destroy()

class LogThread(threading.Thread):
    logger: Logger

    def run(self):
        time.sleep(3)
        threading.Thread(target=self.logger.log_write).start()


if __name__ == "__main__":
    if LAN == 1:
        EN_SCALE = 0.02
    check_chromedriver()
    File_trovato['green'] = ft[LAN]
    App().mainloop()
