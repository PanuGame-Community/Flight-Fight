import os
from tkinter import messagebox as mb
tp = True
tp = tp and os.path.isfile("./Aircraft.png")
tp = tp and os.path.isfile("./game.py")
tp = tp and os.path.isfile("./main.py")
tp = tp and os.path.isfile("./Missile.png")
tp = tp and os.path.isfile("./Movie.wav")
tp = tp and os.path.isfile("./Space Fight.png")
tp = tp and os.path.isfile("./win.wav")
tp = tp and os.path.isfile("./check.py")
tp = tp and os.path.isfile("./upgrade.py")
tp = tp and os.path.isfile("./crash.wav")
tp = tp and os.path.isfile("./版本更迭.txt")

tp = tp and os.path.isdir("./Attack1")
if os.path.isdir("./Attack1"):
    for i in range(1,12):
        tp = tp and os.path.isfile("./Attack1/Attack"+str(i)+".png")

tp = tp and os.path.isdir("./Attack2")
if os.path.isdir("./Attack2"):
    for i in range(27):
        tp = tp and os.path.isfile("./Attack2/Attack"+str(i)+".png")

tp = tp and os.path.isdir("./Destroyed")
if os.path.isdir("./Destroyed"):
    for i in range(1,9):
        tp = tp and os.path.isfile("./Destroyed/Destroyed"+str(i)+".png")

if not tp:
    mb.showerror("","File Not Found")
    os._exit(-1)
