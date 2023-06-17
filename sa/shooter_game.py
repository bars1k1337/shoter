#Створи власний Шутер!
from pygame import *
from random import *

window=display.set_mode((700,500))
backround=transform.scale(image.load("galaxy.jpg"),(700,500))
clock=time.Clock()
display.set_caption("шутер")
font.init()
font2=font.Font(None,36)
win_width=700
win_height=500
lost=0
score=0
font.init()
font2=font.Font(None,40)
win=font2.render("YOU WIN",True,(255,255,255))
lose=font2.render("YOU LOSE",True,(180,0,0))
 
mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()
fire_sound =mixer.Sound("fire.ogg")
class gameSprite(sprite.Sprite):
    def __init__(self,sprite_image,sprite_x,sprite_y,size_x,size_y,sprite_speed):
        super().__init__()
        self.image=transform.scale(image.load(sprite_image),(size_x,size_y))
        self.speed=sprite_speed
        self.rect=self.image.get_rect()
        self.rect.x=sprite_x
        self.rect.y=sprite_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(gameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet=Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(gameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
finish=False
player=Player("rocket.png",300,350,65,65,15)
run=True
class Bullet(gameSprite):
    def update(self):
        self.rect.y+= self.speed
        if self.rect.y<0:
            self.kill()


img_monsters=("ufo.png")
monsters=sprite.Group()
for m in range(1,6):
    monster=Enemy(img_monsters, randint(
        80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
bullets=sprite.Group()

while run:
    
    
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:    
                fire_sound.play()
                player.fire()   
                     
    if not finish:
        window.blit(backround,(0,0))    
        text=font2.render("Пропуски:"+str(lost),1,(255,255,255))
        window.blit(text,(10,20))

        text2=font2.render("Попадання:"+str(score),1,(255,255,255))
        window.blit(text2,(10,50))
        
        
        player.update()
        player.reset()
        monsters.update()
         
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()       
        collidergroup=sprite.groupcollide(bullets,monsters,True,True)
        for c in collidergroup:
            score=score+1
            monster=Enemy(img_monsters,randint(
                    80,win_width-80),-40,80,50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(player,monsters,False)or lost>=3:
            finish=True
            window.blit(lose,(250,250))    
        if score==10:
            finish=True
            window.blit(win,(250,250))    
    display.update()
    clock.tick(60)
