import socket
from tkinter.messagebox import showinfo,showerror
import os
try:
    con = socket.create_connection(("553o7g9239.oicp.vip",32145))
    con.send(b"ver")
    ver = con.recv(10)
    if ver == b"2.4":
        showinfo("提示","已经是最新版本")
        con.send(b"exit")
        os._exit(0)
    con.send(b"get")
    filesize = int(con.recv(1024).decode())
    print(filesize)
    s = con.recv(1024)
    with open("upgrade.exe","wb") as file:
        file.write(s)
        l = len(s)
        while l < filesize:
            if filesize - l >= 1024:
                s = con.recv(1024)
                l += len(s)
            else:
                s = con.recv(filesize - l)
                l = filesize
            file.write(s)
    con.send(b"exit")
except:
    showerror("错误","服务器未就绪")
    os._exit(0)
os.system("start upgrade.exe")
os._exit(0)
