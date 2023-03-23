import pygame
import check
pygame.init()
screen = pygame.display.set_mode([480,300])
pygame.display.set_caption("飞机大战1.1介绍")
keepgoing = True
keep_going = True
clock = pygame.time.Clock()
ys = 0
y = 0
rgb = 5
rgbs = 5
text = """请按↑↓键浏览
飞机大战1.1
你是B国的空军将领，强大的A国想要
攻打弱小的B国，你需要驾驶唯一一
艘战斗机与A国的轰炸机对抗，你不
可以放过轰炸机，因为它会去轰炸基
地！
游戏规则
1.按下↑↓←→键操控战斗机移动
2.按下空格键发射子弹
3.当满足40分时，按下1键释放小招
4.当满足85分时，按下2键释放大招

图片来源：西瓜创客"""
ls = text.split("\n")
fonts = []
surfs = []
while keepgoing and keep_going:
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
                if y >= -283:
                    ys = -3
                else:
                    ys = 0
            if event.key == pygame.K_SPACE:
                keep_going = False
        if event.type == pygame.KEYUP:
            ys = 0
    if y >= -3 and ys == 3:
        ys = 0
    if y <= -283 and ys == -3:
        ys = 0
    y += ys
    if rgb >= 250:
        rgbs = -5
    if rgb <= 5:
        rgbs = 5
    rgb += rgbs
    text2 = "按下空格键继续"
    font2 = pygame.font.Font("楷体.ttf",25)
    surf2 = font2.render(text2,1,(rgb,rgb,rgb))
    screen.blit(surf2,[(screen.get_width()-surf2.get_width())/2,screen.get_height()-30])
    for i in range(len(ls)):
        font = pygame.font.Font("楷体.ttf",30)
        surf = font.render(ls[i],1,(0,0,0))
        if y+40*i > 240:
            break
        if y+40*i > -40:
            screen.blit(surf,[(screen.get_width()-surf.get_width())/2,y+40*i])
    pygame.display.update()
    clock.tick(60)
pygame.quit()
if keepgoing:
    import game
