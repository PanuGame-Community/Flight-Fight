from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
import check
import pygame
root = None
def update():
    root.destroy()
    root.quit()
    win = Tk()
    win.title("版本更迭")
    win.geometry("1000x618")
    ft = Font(size=20)
    text = Text(win,font=ft)
    with open("版本更迭.txt",encoding="UTF-8") as file:
        text.insert("insert",file.read())
    text.config(state="disable")
    text.place(relx=0,rely=0,relwidth=1,relheight=1)
    win.mainloop()
    mainwindow()
def startgame():
    root.destroy()
    root.quit()
    import game
def story():
    root.destroy()
    root.quit()
    pygame.init()
    screen = pygame.display.set_mode([480,300])
    pygame.display.set_caption("飞机大战介绍")
    keepgoing = True
    clock = pygame.time.Clock()
    ys = 0
    y = 0
    my = -560
    rgb = 5
    rgbs = 5
    text = """请按↑↓键浏览
飞机大战  版本号:2.3
你是B国的空军将领，强大的A国想要
攻打弱小的B国,你需要驾驶唯一一艘
战斗机与A国的轰炸机对抗,你不可以
放过轰炸机，因为它会去轰炸基地！
游戏规则
1.按下↑↓←→键操控战斗机移动
2.按下空格键发射子弹，击中敌机血
量加1，子弹加5
3.当满足40分时，按下1键释放小招
击中敌机分数加5，血量减1，子弹加
5
4.当满足85分时，按下2键释放大招
击中敌机分数加15，血量减1，子弹
加5
5.当满足200分时，按下3键回满血
6.按"-"减速，按"="加速
7.开局600个子弹

图片来源：西瓜创客"""
    ls = text.split("\n")
    font = pygame.font.Font("楷体.ttf",30)
    font2 = pygame.font.Font("楷体.ttf",25)
    while keepgoing:
        screen.fill([255,255,255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if y <= -3:
                        ys = 3
                    else:
                        ys = 0
                if event.key == pygame.K_DOWN:
                    if y >= my:
                        ys = -3
                    else:
                        ys = 0
                if event.key == pygame.K_SPACE:
                    keepgoing = False
            if event.type == pygame.KEYUP:
                ys = 0
        if y >= -3 and ys == 3:
            ys = 0
        if y <= my and ys == -3:
            ys = 0
        y += ys
        if rgb >= 250:
            rgbs = -5
        if rgb <= 5:
            rgbs = 5
        rgb += rgbs
        for i in range(len(ls)):
            surf = font.render(ls[i],1,(0,0,0)).convert_alpha()
            if y+40*i > 270:
                break
            if y+40*i > -40:
                screen.blit(surf,[0,y+40*i])
        pygame.draw.rect(screen,(255,255,255),(0,275,480,25),0)
        surf2 = font2.render("按下空格键继续",1,(rgb,rgb,rgb)).convert_alpha()
        screen.blit(surf2,[(screen.get_width()-surf2.get_width())/2,screen.get_height()-30])
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    mainwindow()
def mainwindow():
    global root
    root = Tk()
    root.geometry("400x200")
    root.resizable(False,False)
    root.title("飞机大战启动器")
    title = Font(size=40)
    bbh = Font(size=8)
    Label(root,text="飞机大战",font=title).pack(pady=20)
    Label(root,text="版本号:2.3",font=bbh).pack(side="right",anchor="s",padx=5,pady=5)
    Button(root,text="版本更迭",command=update).place(relx=0.1,rely=0.5,relwidth=3/15,relheight=0.2)
    Button(root,text="开始游戏",command=startgame).place(relx=0.4,rely=0.5,relwidth=3/15,relheight=0.2)
    Button(root,text="游戏说明",command=story).place(relx=0.7,rely=0.5,relwidth=3/15,relheight=0.2)
    root.mainloop()
mainwindow()
