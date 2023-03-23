import pygame
import random
from pygame.locals import DOUBLEBUF
from pickle import load,dump
pygame.init()
class bg(pygame.sprite.Sprite):
    def __init__(self,image,y,sp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = -5
        self.rect.top = 0
        self.y_speed = sp
        self.y = y

    def move(self,screen):
        self.y += self.y_speed
        self.rect.top = (self.y+720)%1440-720
        screen.blit(self.image,self.rect)

class Aircraft_me(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [475,650]
        self.list = []
        self.crdlist = []

    def move(self,x,y,screen,aco_l):
        global crdlist,HP,missile
        self.rect.centerx += x
        self.rect.centery += y
        if self.rect.centery > screen.get_height():
            self.rect.centery = screen.get_height()

        if self.rect.centerx > screen.get_width():
            self.rect.centerx = screen.get_width()

        if self.rect.centery < 0:
            self.rect.centery = 0

        if self.rect.centerx < 0:
            self.rect.centerx = 0

        for i in self.list:
            i.move(screen,self.list)
            for j in aco_l:
                if i.touch(j):
                    if i.type == 0:
                        self.list.remove(i)
                    elif i.type == 2:
                        if not i.showing:
                            i.y_speed = 0
                            i.show()
                    crdlist.append(Destroyed(j.get_point(),0))
                    missile += 5
                    boom.play()
                    if HP < 100:
                        HP += 1
        screen.blit(self.image,self.rect)

    def create(self):
        img = random.choice(missile_type)
        if img == "FasterMissile.png":
            tp = 1
        elif img == "LightningMissile.png":
            tp = 2
        else:
            tp = 0
        if img == "FasterMissile.png":
            speed = 7
        elif img == "LightningMissile.png":
            speed = 3
        else:
            speed = 5
        self.list.append(Zidan(speed,img,self.rect.center,tp))

    def touch(self,point):
        return self.rect.collidepoint(point)

    def get_center(self):
        return self.rect.center

class Zidan(pygame.sprite.Sprite):
    def __init__(self,speed,image,pos,tp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.y_speed = speed
        self.type = tp
        self.angle = 0
        self.showing = False

    def move(self,screen,zl):
        self.rect.centery -= self.y_speed
        if self.type == 2:
            img = pygame.transform.rotate(self.image,self.angle)
            self.angle += 3
            rct = img.get_rect()
            rct.center = self.rect.center
            if self.showing:
                if self.cnt > 120:
                    zl.remove(self)
                    del self
                else:
                    self.cnt += 1
                    drawLightning(screen,self.rect.center,20)
        else:
            img = self.image
            rct = self.rect
        screen.blit(img,rct)

    def touch(self,aco):
        global score
        if self.type != 2 or self.showing == False:
            if aco.rect.collidepoint(self.rect.center):
                aco.kill()
                score += 10
                return True
            else:
                return False
        else:
            if aco.rect.centery > self.rect.centery - 20 and aco.rect.centery < self.rect.centery + 20:
                aco.kill()
                score += 10
                return True
            else:
                return False
    def show(self):
        self.cnt = 0
        self.showing = True

class Aircraft_other(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load(image).convert_alpha(),180)
        self.rect = self.image.get_rect()
        self.rect.center = [random.randint(50,900),-100]

    def move(self,screen):
        global HP
        self.rect.centery += 3

        if self.rect.centery > screen.get_height():
            HP -= 10
            self.kill()

        screen.blit(self.image,self.rect)
    
    def get_point(self):
        return self.rect.center

    def kill(self):
        global aco_l
        aco_l.remove(self)

class Attack1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rects = []
        self.images = []
        cnt = 0
        for i in range(1,12):
            image = pygame.image.load("./Attack1/Attack"+str(i)+".png").convert_alpha()
            image = pygame.transform.scale2x(image)
            for j in range(3):
                self.images.append(image)
                self.rects.append(image.get_rect())
                self.rects[cnt].center = [475,360]
                cnt += 1
        self.index = 0

    def next_page(self,screen):
        screen.blit(self.images[self.index%33],self.rects[self.index%33])
        self.index += 1
        return self.index % 33 == 0

class Attack2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rects = []
        self.images = []
        cnt = 0
        for i in range(27):
            image = pygame.image.load("./Attack2/Attack"+str(i)+".png").convert_alpha()
            image = pygame.transform.scale2x(image)
            for j in range(3):
                self.images.append(image)
                self.rects.append(image.get_rect())
                self.rects[cnt].center = [475,360]
                cnt += 1
        self.index = 0

    def next_page(self,screen):
        screen.blit(self.images[self.index%81],self.rects[self.index%81])
        self.index += 1
        return self.index % 81 == 0

class Destroyed(pygame.sprite.Sprite):
    def __init__(self,point,index):
        pygame.sprite.Sprite.__init__(self)
        self.rects = []
        self.images = []
        cnt = 0
        for i in range(1,9):
            image = pygame.image.load("./Destroyed/Destroyed"+str(i)+".png").convert_alpha()
            image = pygame.transform.scale2x(image)
            for j in range(6):
                self.images.append(image)
                self.rects.append(image.get_rect())
                self.rects[cnt].center = point
                cnt += 1
        self.index = index

    def next_page(self,screen):
        screen.blit(self.images[self.index%48],self.rects[self.index%48])
        self.index += 1
        return self.index % 48 == 0

    def get_index(self):
        return self.index
    
def drawLightning(screen,point,value):
    for i in range(3):
        x = point[0]
        ls = []
        r = random.randint(10,30)
        while x + r < screensize[0]:
            ls.append(x + r)
            x += r
            r = random.randint(10,30)
        ls.append(x + r)
        ls = [point] + [[i,point[1] + random.randint(-value,value)] for i in ls]
        w = random.randint(1,2)
        pygame.draw.lines(screen,[0,0,255],False,ls,w + 2)
        pygame.draw.lines(screen,[255,255,255],False,ls,w)
        x = point[0]
        ls = []
        r = random.randint(10,30)
        while x - r > 0:
            ls.append(x - r)
            x -= r
            r = random.randint(10,30)
        ls.append(x - r)
        ls = [point] + [[i,point[1] + random.randint(-value,value)] for i in ls]
        w = random.randint(1,2)
        pygame.draw.lines(screen,[0,0,255],False,ls,w + 2)
        pygame.draw.lines(screen,[255,255,255],False,ls,w)

screensize = [950,720]
screen = pygame.display.set_mode(screensize,DOUBLEBUF)
screen.set_alpha(None)
pygame.event.set_allowed([pygame.QUIT,pygame.KEYDOWN,pygame.KEYUP])

bg1 = bg("Space Fight.png",-720,4)
bg2 = bg("Space Fight.png",0,4)

pygame.display.set_caption("飞机大战")

ac = Aircraft_me("Aircraft.png")
acs = [0,0]
type_fire = 0
missile = 600
old_missile = None
missile_type = ["Missile.png" for i in range(10)] + ["FasterMissile.png" for i in range(2)] + ["LightningMissile.png"]
movespeed = 3
old_movespeed = None
crdlist = []
HP = 100
old_HP = None
score = 0
old_score = None
done = False
type_attack1 = False
atk1 = Attack1()
type_attack2 = False
atk2 = Attack2()
font = pygame.font.Font(None,60)

aco_l = []
bl = [True] + [False for i in range(150)]

bgm1 = pygame.mixer.Sound("Movie.wav")
bgm1.play(-1)
bgm2 = pygame.mixer.Sound("win.wav")
boom = pygame.mixer.Sound("crash.wav")
boom.set_volume(0.4)
boom2 = pygame.mixer.Sound("crash.wav")
boom2.set_volume(0.6)

clock = pygame.time.Clock()
count = 0
cnt = 0

keep_going = True
keepgoing = True
while keepgoing and keep_going:
    if not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    acs[0] -= movespeed
                elif event.key == pygame.K_RIGHT:
                    acs[0] += movespeed
                elif event.key == pygame.K_UP:
                    acs[1] -= movespeed
                elif event.key == pygame.K_DOWN:
                    acs[1] += movespeed
                elif event.key == pygame.K_SPACE:
                    type_fire = 2
                elif event.key == pygame.K_EQUALS:
                    if movespeed < 10:
                        movespeed += 1
                        if acs[0] > 0:
                            acs[0] += 1
                        elif acs[0] < 0:
                            acs[0] -= 1
                        if acs[1] > 0:
                            acs += 1
                        elif acs[1] < 0:
                            acs[1] -= 1
                elif event.key == pygame.K_MINUS:
                    if movespeed > 1:
                        movespeed -= 1
                        if acs[0] > 0:
                            acs[0] -= 1
                        elif acs[0] < 0:
                            acs[0] += 1
                        if acs[1] > 0:
                            acs -= 1
                        elif acs[1] < 0:
                            acs[1] += 1
                elif event.key == pygame.K_1:
                    if not type_attack1 and score >= 40:
                        score -= 40
                        type_attack1 = True
                        r = False
                        while len(aco_l) != 0:
                            crdlist.append(Destroyed(aco_l[0].get_point(),0))
                            r = True
                            aco_l[0].kill()
                            score += 5
                            missile += 5
                            HP -= 1
                        if r:
                            boom2.play()
                elif event.key == pygame.K_2:
                    if not type_attack2 and score >= 85:
                        score -= 85
                        type_attack2 = True
                        r = False
                        while len(aco_l) != 0:
                            crdlist.append(Destroyed(aco_l[0].get_point(),0))
                            r = True
                            aco_l[0].kill()
                            score += 15
                            missile += 5
                            HP -= 1
                        if r:
                            boom2.play()
                elif event.key == pygame.K_3:
                    if score >= 200:
                        score -= 200
                        HP = 100

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    acs[0] += movespeed
                if event.key == pygame.K_RIGHT:
                    acs[0] -= movespeed
                if event.key == pygame.K_UP:
                    acs[1] += movespeed
                if event.key == pygame.K_DOWN:
                    acs[1] -= movespeed
                if event.key == pygame.K_SPACE:
                    type_fire = 0

        if random.choice(bl):
            aco = Aircraft_other("Aircraft.png")
            aco_l.append(aco)
            if len(bl) > 20:
                bl.pop()
        count = 0
        
        bg1.move(screen)
        bg2.move(screen)

        ac.move(acs[0],acs[1],screen,aco_l)
        
        for i in aco_l:
            i.move(screen)
            count += ac.touch(i.get_point())
        done = not (count == 0 and HP > 0)
        if done:
            des = Destroyed(ac.get_center(),0)
        if type_fire == 2 and missile > 0:
            ac.create()
            type_fire = 1
            cnt = 0
            missile -= 1
        elif type_fire == 1 and cnt % 10 == 0 and missile > 0:
            ac.create()
            missile -= 1
        cnt += 1
            
        if type_attack1:
            type_attack1 = not atk1.next_page(screen)

        if type_attack2:
            type_attack2 = not atk2.next_page(screen)

        for i in crdlist:
            if i.next_page(screen):
                crdlist.remove(i)

        if HP != old_HP:
            old_HP = HP
            t_HP = "HP:" + str(HP)
            HP_surf = font.render(t_HP,1,(255,255,255))
        if score != old_score:
            t_score = "Score:" + str(score)
            score_surf = font.render(t_score,1,(255,255,255))
        if movespeed != old_movespeed:
            t_speed = "Speed:" + str(movespeed)
            speed_surf = font.render(t_speed,1,(255,255,255))
        if missile != old_missile:
            t_missile = "Missile:" + str(missile)
            missile_surf = font.render(t_missile,1,(255,255,255))
        screen.blit(HP_surf,[0,0])
        screen.blit(score_surf,[screen.get_width()-score_surf.get_width(),0])
        screen.blit(speed_surf,[(screen.get_width()-speed_surf.get_width())/3,0])
        screen.blit(missile_surf,[(screen.get_width()-missile_surf.get_width())/1.5,0])

        pygame.display.update()

        clock.tick(60)
    else:
        if des.get_index() == 0:
            bgm1.stop()
            boom2.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False
        bg1.move(screen)
        bg2.move(screen)
        keep_going = not des.next_page(screen)
        pygame.display.update()
        clock.tick(50)

pygame.time.delay(890)
boom.stop()
if keep_going:
    pygame.quit()
else:
    ft1_font = pygame.font.Font(None,100)
    ft2_3_font = pygame.font.Font(None,60)
    pygame.display.set_caption("Game Over")
    try:
        with open("best.pkl","rb") as file:
            best = load(file)
        if best < score:
            best = score
            with open("best.pkl","wb") as file:
                dump(best,file)
    except:
        best = score
        with open("best.pkl","wb") as file:
            dump(best,file)
    final_text1 = 'Game Over'
    final_text2 = 'Your final score is: ' + str(score)
    final_text3 = 'Your best score is: ' + str(best)
    bgm2.play(-1)
    keepgoing = True
    r = random.randint(5,250)
    rs = 1
    g = random.randint(5,250)
    gs = 2
    b = random.randint(5,250)
    bs = 3
    while keepgoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False
        screen.fill([r,g,b])
        ft1_surf = ft1_font.render(final_text1,1,(255-r,255-b,255-g))
        ft2_surf = ft2_3_font.render(final_text2,1,(255-r,255-b,255-g))
        ft3_surf = ft2_3_font.render(final_text3,1,(255-r,255-b,255-g))
        screen.blit(ft1_surf,[screen.get_width()//2 - \
                              ft1_surf.get_width()//2,300])
        screen.blit(ft2_surf,[screen.get_width()//2 - \
                              ft2_surf.get_width()//2,400])
        screen.blit(ft3_surf,[screen.get_width()//2 - \
                              ft3_surf.get_width()//2,450])
        pygame.display.update()
        if r > 250:
            rs = -2
        if g > 250:
            gs = -1
        if b > 250:
            bs = -3
        
        if r < 5:
            rs = 1
        if g < 5:
            gs = 2
        if b < 5:
            bs = 3
        r += rs
        g += gs
        b += bs
        clock.tick(50)
    pygame.quit()
