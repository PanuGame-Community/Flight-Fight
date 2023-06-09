import requests as rq
from tkinter.messagebox import showinfo,showerror
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
import os
import threading as th
import time
class Window(Tk):
    def __init__(self,version,newversion=None):
        super().__init__()
        self.process = 0
        self.old_process = None
        self.filesize = 0
        self.old_filesize = 0
        self.l = 0
        self.old_l = 0
        self.title("更新中")
        self.geometry("400x100")
        self.resizable(False,False)
        self.progress = Progressbar(self)
        self.progress.place(relx=0.1,rely=0.2,relwidth=0.8,relheight=0.3)
        font = Font(size=8)
        self.pt = Label(self,font=font)
        self.pt.place(relx=0.1,rely=0.6,relwidth=0.2,relheight=0.2)
        self.ft = Label(self,font=font)
        self.ft.place(relx=0.3,rely=0.6,relwidth=0.3,relheight=0.2)
        self.lt = Label(self,font=font)
        self.lt.place(relx=0.6,rely=0.6,relwidth=0.3,relheight=0.2)
        self.thread_it(self.update_progress)
        self.thread_it(self.upgrade,version,newversion)
        self.mainloop()
    def thread_it(self,target,*args):
        t = th.Thread(target=target,args=args)
        t.start()
    def update_progress(self):
        while True:
            if self.process != self.old_process:
                self.progress["value"] = self.process
                self.old_process = self.process
                self.pt.config(text=f"进度:{self.process}%")
            if self.filesize != self.old_filesize:
                self.ft.config(text=f"总共:{round(self.filesize/1024,2)}kB")
            if self.l != self.old_l:
                self.lt.config(text=f"已下载:{round(self.l/1024,2)}kB")
            time.sleep(0.05)
    def upgrade(self,version,newversion=None):
        if not newversion:
            newversion = float(rq.get("https://553o7g9239.oicp.vip/static/Flight-Fight/Version.txt").text.strip("\n"))
            if newversion <= version:
                showinfo("Update",f"已经是最新版本  版本号:{version}")
                os._exit(0)
        response = rq.get(f"https://553o7g9239.oicp.vip/static/Flight-Fight/UpdateInstaller{newversion}.exe",stream=True)
        self.filesize = int(response.headers["content-length"])
        with open("upgrade.exe","wb") as file:
            for recv in response.iter_content(chunk_size=8192):
                self.l += len(recv)
                self.process = round(self.l / self.filesize * 100,2)
                file.write(recv)
        os.system("start upgrade.exe")
        os._exit(0)
