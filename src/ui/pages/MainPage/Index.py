import customtkinter
import os
import sys
import time
import threading
from tkinter import Tk
from dotenv import load_dotenv
from functools import partial
from tkinter.font import Font
import queue

from cairosvg import svg2png
from PIL import Image, ImageTk
import io

# load env variables
# PyInstaller temp folder
# https://pyinstaller.org/en/stable/runtime-information.html
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    load_dotenv(dotenv_path=os.path.join(sys._MEIPASS, os.path.join("configs", ".env")))
else:
    load_dotenv(dotenv_path=f'configs/.env')


# manual access to schema directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# restore parent directory path
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
from ui.pages.WelcomePage.Index import Index as WelcomePage

# Load the Font Awesome OTF font
fontFile    =   os.path.abspath(os.path.join(dir_path, '../../../assets/fonts/fontawesome/svgs/solid/database.svg'))

class Index:
    def __init__(self, root):
        self.status = f"Dreaming"
        self.customer = None
        self.processing = True
        self.timerTreshold = 1
        self.maximumCustomers = 3
        self.customerQueue = queue.Queue(maxsize=self.maximumCustomers)
        self.mainFrame = customtkinter.CTkFrame(master=root, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.mainFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.mainFrame.grid_rowconfigure(2, weight=1)
        self.mainFrame.grid_columnconfigure (0, weight=1)

        # top section
        self.topFrame = customtkinter.CTkFrame(master=self.mainFrame, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.topFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.topFrame.grid_rowconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure (0, weight=1)

        self.bannerFrame = customtkinter.CTkFrame(master=self.mainFrame, corner_radius=0, bg_color="orange", fg_color="transparent")
        self.bannerFrame.grid(row=1 , column=0, padx=0, pady=0, sticky="nsew")
        self.bannerFrame.grid_rowconfigure(0, weight=1)
        self.bannerFrame.grid_columnconfigure (1, weight=1)

        self.midFrame = customtkinter.CTkFrame(master=self.mainFrame, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.midFrame.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        self.midFrame.grid_rowconfigure(0, weight=1)
        self.midFrame.grid_columnconfigure (1, weight=1)

        self.logoSection = customtkinter.CTkFrame(self.topFrame, height=50, bg_color="transparent", fg_color="transparent")
        self.logoSection.pack(pady=10, padx=10, fill="both") # Pack the button with vertical padding
        self.logoLabel = customtkinter.CTkLabel(self.logoSection, text="BARBER SHOP", fg_color="#484849", compound="center", corner_radius=10, font=("Arial", 20, "bold"))
        self.logoLabel.pack (fill="both", ipadx=20, ipady=10)

        self.barbersArea = customtkinter.CTkFrame(master=self.bannerFrame, corner_radius=0, bg_color="orange", fg_color="transparent")
        self.barbersArea.grid(row=0, column=0, padx=0, pady=0, sticky="new")
        self.barbersArea.grid_rowconfigure(0, weight=1)
        self.barbersArea.grid_columnconfigure (0, weight=1)

        self.statusLabel = customtkinter.CTkLabel(self.barbersArea, text=f"{self.status}", fg_color="#484849", compound="center", corner_radius=0)
        self.statusLabel.pack (fill="both", ipadx=20, ipady=10)

        self.waitingArea = customtkinter.CTkFrame(master=self.bannerFrame, corner_radius=0, bg_color="blue", fg_color="transparent")
        self.waitingArea.grid(row=0, column=1, padx=0, pady=0, sticky="new")
        self.waitingArea.grid_rowconfigure(0, weight=1)
        self.waitingArea.grid_columnconfigure (0, weight=1)

        self.waitingLabel = customtkinter.CTkLabel(self.waitingArea, text=f"{self.customerQueue.qsize()}", fg_color="#484849", compound="center", corner_radius=0)
        self.waitingLabel.pack (fill="both", ipadx=20, ipady=10)

        self.customerButtonArea = customtkinter.CTkFrame(master=self.midFrame, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.customerButtonArea.grid(row=0, column=0, padx=0, pady=0, sticky="new")
        self.customerButtonArea.grid_rowconfigure(0, weight=0)
        self.customerButtonArea.grid_columnconfigure (0, weight=0)

        self.custButton = customtkinter.CTkButton(master=self.customerButtonArea, text="ADD CUSTOMER +", bg_color="transparent", fg_color="#39BA06", command=partial(self.__addCustomer))
        self.custButton.grid(row=0, column=0, pady=50, padx=30, sticky="nsew")

        threading.Thread(target=partial(self.__readQueue), daemon=True).start ()

        return None
    
    def __renderUIforQueueSize (self):
        self.waitingLabel.configure(text=f"{self.customerQueue.qsize()}  -- Waiting Chairs Available: ( {self.maximumCustomers})")
        self.statusLabel.configure(text=f"{self.status}")
        return self
    
    def __addCustomer (self):
        __thread = threading.Thread(target=partial(self.__addQueue,"test"))
        __thread.start ()
        return self
    
    def __readQueue (self):
        while True:
            # prevent infinite ui rendering
            if self.processing:
                if self.customerQueue.qsize() == 0:
                    self.status = "Dreaming . . ."
                    self.__renderUIforQueueSize ()
                    self.processing = False

                else:
                    self.customer = self.customerQueue.get()
                    self.status = "Cutting . . ."
                    self.__renderUIforQueueSize ()

                    # process for n seconds each customer
                    time.sleep(self.timerTreshold)
                    self.status = "Dreaming . . ."
                    self.__renderUIforQueueSize ()

    
    def __addQueue (self, threadName):
        self.processing = True
        __customer = f"{threadName}"

        # prevent locking the main thread (ui)
        if self.customerQueue.qsize () >= self.maximumCustomers:
            return self
        
        try:
            self.customerQueue.put(__customer)
            # get number of customers
            self.__renderUIforQueueSize ()
        except Exception:
            print('full')

        return self
    
    