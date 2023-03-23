import pygame
import random
pygame.init()
class bg(pygame.sprite.Sprite):
    def __init__(self,image,y,sp):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
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
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [475,650]
        self.list = []
        self.crdlist = []

    def move(self,x,y,screen,aco_l):
        global crdlist
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
            i.move(screen)
            for j in aco_l:
                if i.touch(j):
                    self.list.remove(i)
                    crdlist.append(Destroyed(j.get_point(),0))
                    boom.play()
        screen.blit(self.image,self.rect)

    def create(self):
        self.list.append(Zidan(5,"Missile.png",self.rect.center))

    def touch(self,point):
        return self.rect.collidepoint(point)

    def get_center(self):
        return self.rect.center

class Zidan(pygame.sprite.Sprite):
    def __init__(self,speed,image,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.y_speed = speed

    def move(self,screen):
        self.rect.centery -= self.y_speed
        screen.blit(self.image,self.rect)

    def touch(self,aco):
        global score
        if aco.rect.collidepoint(self.rect.center):
            aco.kill()
            score += 10
            return True
        return False

class Aircraft_other(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
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
        for i in range(1,13):
            image = pygame.image.load("./Attack1/Attack"+str(i)+".png")
            image = pygame.transform.scale2x(image)
            for j in range(3):
                self.images.append(image)
                self.rects.append(image.get_rect())
                self.rects[cnt].center = [475,360]
                cnt += 1
        self.index = 0

    def next_page(self,screen):
        screen.blit(self.images[self.index%36],self.rects[self.index%36])
        self.index += 1
        return self.index % 36 == 0

class Attack2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rects = []
        self.images = []
        cnt = 0
        for i in range(27):
            image = pygame.image.load("./Attack2/Attack"+str(i)+".png")
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
            image = pygame.image.load("./Destroyed/Destroyed"+str(i)+".png")
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

screen = pygame.display.set_mode([950,720])
bg1 = bg("Space Fight.png",-720,4)
bg2 = bg("Space Fight.png",0,4)

pygame.display.set_caption("飞机大战1.6")

ac = Aircraft_me("Aircraft.png")
acs = [0,0]
crdlist = []
HP = 100
score = 0
done = False
des = Destroyed(ac.get_center(),0)
type_attack1 = False
atk1 = Attack1()
type_attack2 = False
atk2 = Attack2()

aco_l = []
bl = [True,]
for i in range(150):
    bl.append(False)

bgm1 = pygame.mixer.Sound("Movie.wav")
bgm1.play(-1)
bgm2 = pygame.mixer.Sound("win.wav")
boom = pygame.mixer.Sound("crash.wav")

clock = pygame.time.Clock()
count = 0

keep_going = True
keepgoing = True
while keepgoing and keep_going:
    if not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    acs = [-3,0]
                if event.key == pygame.K_RIGHT:
                    acs = [3,0]
                if event.key == pygame.K_UP:
                    acs = [0,-3]
                if event.key == pygame.K_DOWN:
                    acs = [0,3]
                if event.key == pygame.K_SPACE:
                    ac.create()
                if event.key == pygame.K_1:
                    if not type_attack1 and score >= 40:
                        score -= 40
                        type_attack1 = True
                if event.key == pygame.K_2:
                    if not type_attack2 and score >= 85:
                        score -= 85
                        type_attack2 = True

            if event.type == pygame.KEYUP:
                acs = [0,0]

        if random.choice(bl):
            aco = Aircraft_other("Aircraft2.png")
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

        if type_attack1:
            type_attack1 = not atk1.next_page(screen)
            for i in aco_l:
                crdlist.append(Destroyed(i.get_point(),0))
                boom.play()
                i.kill()
                score += 5

        if type_attack2:
            type_attack2 = not atk2.next_page(screen)
            for i in aco_l:
                crdlist.append(Destroyed(i.get_point(),0))
                boom.play()
                i.kill()
                score += 15
        for i in crdlist:
            if i.next_page(screen):
                crdlist.remove(i)

        t_HP = "HP:" + str(HP)
        t_score = "Score:" + str(score)
        HP_font = pygame.font.Font(None,60)
        HP_surf = HP_font.render(t_HP,1,(255,255,255))
        score_font = pygame.font.Font(None,60)
        score_surf = score_font.render(t_score,1,(255,255,255))
        screen.blit(HP_surf,[0,0])
        screen.blit(score_surf,[screen.get_width()-score_surf.get_width(),0])

        pygame.display.update()

        clock.tick(60)
        count += 1
    else:
        if des.get_index() == 0:
            bgm1.stop()
            boom.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False
        bg1.move(screen)
        bg2.move(screen)
        des = Destroyed(ac.get_center(),des.get_index())
        keep_going = not des.next_page(screen)
        pygame.display.update()
        clock.tick(60)

pygame.time.delay(890)
boom.stop()
if keep_going:
    pygame.quit()
else:
    pygame.display.set_caption("Game Over")
    final_text1 = 'Game Over'
    final_text2 = 'Your final score is: ' + str(score)
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
        ft1_font = pygame.font.Font(None,100)
        ft1_surf = ft1_font.render(final_text1,1,(255-r,255-b,255-g))
        ft2_font = pygame.font.Font(None,60)
        ft2_surf = ft2_font.render(final_text2,1,(255-r,255-b,255-g))
        screen.blit(ft1_surf,[screen.get_width()//2 - \
                              ft1_surf.get_width()//2,350])
        screen.blit(ft2_surf,[screen.get_width()//2 - \
                              ft2_surf.get_width()//2,450])
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
