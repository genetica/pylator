from socket import *
from threading import Thread

from colorama import init,deinit

from termcolor import colored
import threading
import yaml
import subprocess
import time
import numpy as np
import warnings
import sys

from contextlib import redirect_stderr

#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_Tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
#import matplotlib.animation as animation
#from matplotlib import style

import tkinter as Tk
import tkinter as Tk
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)
#style.use("ggplot")

#f = Figure(figsize=(5,5), dpi=100)
#a = f.add_subplot(231)
#b = f.add_subplot(232)
##c = f.add_subplot(233)
#d = f.add_subplot(234)
#e = f.add_subplot(236)

AppActive = True
ThreadContinue = True
InputTextReady = False
PlottingGraphs = False
TextToSend = ""

kics_execute_command = ""
kics_cwd = ""
simple_execute_command = ""
simple_cwd = ""

tsd_temp=[]
proxy_v=[]
proxy_c=[]
cooler_v=[]
cooler_c=[]

warnings.filterwarnings("ignore",".*GUI is implemented.*")



class KedaApp(Tk.Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.Tk.__init__(self, *args, **kwargs)

        # Tk.Tk.iconbitmap(self, default="clienticon.ico")
        Tk.Tk.wm_title(self, "Kenis 1280 Network Terminal")
        
        
        container = Tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (TerminalPage,):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.terminalFrame = self.frames[TerminalPage]
        self.show_frame(TerminalPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def write_to_terminal(self,text):
        self.frames[TerminalPage].write_text(text)

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.insert(Tk.END,string)
        self.widget.see(Tk.END)

class TerminalPage(Tk.Frame):

    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        label = Tk.Label(self, text="Terminal Feedback", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Menu",
                            command=lambda: controller.show_frame(MenuPage))
        button1.pack() 

        self.T = Tk.Text(self, borderwidth=3, relief="sunken", height=50, width=120)

        #sys.stdout = Std_redirector(self.T)

        self.T.config(bg='black',font=("consolas", 12), undo=True, wrap='word')
        # T.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scrollb=Tk.Scrollbar(self,command=self.T.yview)
        # scrollb.grid(row=0, column=1, sticky='nsew')
        self.T['yscrollcommand'] = scrollb.set
        self.T.pack()

        self.T.tag_add('INFO', '1.0', 'end')
        self.T.tag_add('ERR', '1.0', 'end')
        self.T.tag_add('DEBUG', '1.0', 'end')
        self.T.tag_configure('INFO',foreground="yellow")
        self.T.tag_configure('ERR',foreground="red")
        self.T.tag_configure('DEBUG',foreground="cyan")
        self.T.tag_configure('LOG_DATA',foreground="green")

    def write_text(self, text):
        # if (chr(text[0][0])=='I'):            
        #     self.T.insert(Tk.END, text[0][2:].decode("utf-8"),('INFO'))
        #     self.T.see(Tk.END)
        # if (chr(text[0][0])=='E'):            
        #     self.T.insert(Tk.END, text[0][2:].decode("utf-8"), ('ERR'))
        #     self.T.see(Tk.END)
        # if (chr(text[0][0])=='D'):            
        #     self.T.insert(Tk.END, text[0][2:].decode("utf-8"), ('DEBUG'))
        #     self.T.see(Tk.END)
        if (text[0] == 'C'):            
            self.T.insert(Tk.END, text[1:],('LOG_DATA'))
            self.T.see(Tk.END)
        else:
            self.T.insert(Tk.END, text, ('DEBUG'))
            self.T.see(Tk.END)




def GetInput():
    global ThreadContinue
    global image_show
    global app

    while ThreadContinue:        
        TextToSend = input('>')
        # first make sure we have actually typed something
        if (len(TextToSend)>0):        
            if (TextToSend == "exit"):
                ThreadContinue = False
                AppActive = False
                deinit()
                app.destroy()
                return
            # if it starts with a ! -> we want to execute something locally
            app.write_to_terminal('C' + TextToSend)
            print('C' + TextToSend)
            # if (TextToSend[0] == '!'):
            #     if (TextToSend=='!kics'):
            #         s.sendto('pil restart\0'.encode('utf-8'), (UDP_IP, 1988))
            #         time.sleep(5)                
            #         p=subprocess.Popen(['python',kics_execute_command],cwd=kics_cwd,creationflags = subprocess.CREATE_NEW_CONSOLE)                
            #     if (TextToSend=='!simple_vid'):
            #         s.sendto('pil restart\0'.encode('utf-8'), (UDP_IP, 1988))
            #         time.sleep(5)              
            #         p=subprocess.Popen(['python',simple_execute_command],cwd=simple_cwd,creationflags = subprocess.CREATE_NEW_CONSOLE)  
            #     if (TextToSend=='!test'):
            #         app.write_to_terminal("Hello")
            # else:
            #     TextToSend = TextToSend + '\0'
            #     s.sendto(TextToSend.encode('utf-8'), (UDP_IP, 1988))


if __name__ == "__main__":
    init()

    text = colored("Kenis 1280 Network Terminal", 'yellow', attrs=['reverse', 'blink'])
    print (text)

    app = KedaApp()

    #output_t = Thread(target=GetUDPData,args=())
    #output_t.start()

    
    sys.stdout = Std_redirector(app.terminalFrame.T)

    app.terminalFrame.write_text("YIP")

    input_t = Thread(target=GetInput,args=())
    input_t.start()

    #ani = animation.FuncAnimation(f, animate, interval=1000)
    app.mainloop()