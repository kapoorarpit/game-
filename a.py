import pygame
pygame.init()

win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = [pygame.image.load('standing.png'),pygame.image.load('standing2.png')]

clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,height, width):
        self.x = x
        self.y = y
        self.height=height
        self.width=width
        self.vel = 10
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 15
        self.standing=True
        self.hitbox= (self.x+30, self.y+30, 300,300)
        self.power=100

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(char[0], (self.x,self.y))
            else:
                win.blit(char[1], (self.x, self.y))
        self.hitbox= (self.x-30, self.y-30, 300,500)
#        pygame.draw.rect(win, (255,0,0), self.hitbox,1)
        pygame.draw.rect(win,(0,0,255),(30,10,100,10))
        if self.power>0:
            pygame.draw.rect(win,(0,255,0),(30,10, self.power,10))



class enemy(object):
    def __init__(self, x ,y,width, height):
        self.x= x
        self.y= y
        self.width= width
        self.height= height
        self.vel= 10
        self.right =False
        self.left =False
        self.walkCount = 0
        self.start= 10
        self.end= 1100
        self.walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png')]
        self.walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png')]
        self.hitbox= (self.x, self.y, 300,500)
        self.power=100

    def draw(self,win):
        self.move()
        if self.walkCount+1 >= 27:
            self.walkCount=0

        if self.vel>0:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
            self.walkCount +=1
        self.hitbox= (self.x+70, self.y+40, 400,500)
#        pygame.draw.rect(win, (255,0,0), self.hitbox,1)
        pygame.draw.rect(win, (0,0,255),(1000,10,100,10))
        if self.power>0:
            pygame.draw.rect(win, (0,255,0),(1000,10,self.power,10))

    def move(self):
        if self.vel >0:
            if self.x + self.vel < self.end:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount =0
        else:
            if self.x - self.vel >self.start:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount =0


class projectile():
    def  __init__(self, x, y, radius, color, facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel= 10* self.facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    en.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

#mainloop
man = player(100, 320,1,1)
run = True
en = enemy(10,250,1,1)
bullets=[]
bshoot=0
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if bshoot >0:
        bshoot+=1
    if bshoot >3:
        bshoot=0
    
    if man.x==en.x:
        man.power-=30

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    for bullet in bullets:
        if bullet.x > en.x+ 30 and bullet.x< en.x + en.hitbox[2]:
            if bullet.y > en.y+30 and bullet.y < en.y + en.hitbox[3]:
                bullets.pop(bullets.index(bullet))
                en.power-=10

        if bullet.x<1200 and bullet.x>0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
      
    if keys[pygame.K_a] and bshoot==0:
        if man.left:
            facing =-1
        else:
            facing = 1
        if len(bullets) <25:
            bullets.append(projectile(round(man.x+man.width//2), round(man.y+man.height//2) , 6, (0,0,0), facing))
        bshoot=1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing= False
    elif keys[pygame.K_RIGHT] and man.x < 1200 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing= False
    else:
        man.standing=True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -15:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 15
            
    redrawGameWindow()

pygame.quit()
