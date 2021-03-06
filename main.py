
import pygame, sys, time, math, colorsys, random

from pygame.math import Vector2, disable_swizzling
from pygame.locals import *
from pygame.mixer import stop

from background import Background
from button import Button
from heart import Heart
from cupid import Cupid
from monster import Monster
from other import checkHitBox
from other import clamp
from other import calcu
from other import calcuDegree

from arrow import Arrow
def main():
    #intialize the pygame
    pygame.init()
    #create the screen width 800 heigh 600
    DISPLAY = pygame.display.set_mode((800,600))
    #set caption of the screen
    pygame.display.set_caption('Flappy Cupid - When will i find love?')
    #set icon of the game is the hearh
    pygame.display.set_icon(pygame.image.load('./media/img/broke_heart.png'))

    #lock fps is 60
    FPS=60
    last_Time=time.time()
    #color
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    PINK = (199,21,133)
    DEEPPINK=(255,105,180)
    YELLOW=(255,255,0)
    #font
    fontGame2=pygame.font.Font('./media/font/fontGame2.ttf',20)
    fontOpen1= pygame.font.Font('./media/font/fontOpen.ttf', 100)
    fontOpen2= pygame.font.Font('./media/font/fontOpen2.ttf', 30)
    fontSmall=pygame.font.Font('./media/font/fontOpen2.ttf', 20)
    fontGame=pygame.font.Font('./media/font/fontGame.ttf',20)
    
    #image
    dead_bg=pygame.image.load('./media/img/dead_bg.png')
    retry_button= pygame.image.load('./media/img/retry_button.png')
    shop = pygame.image.load('./media/img/shop.png')
    shop_bg = pygame.image.load('./media/img/shop_bg.png')
    button1=pygame.image.load('./media/img/button1.png')
    logo = pygame.image.load('./media/img/logo.png')
    logo_below = pygame.image.load('./media/img/logo_below.png')
    logo_hide = pygame.image.load('./media/img/logo_hide.png')
    title_bg = pygame.image.load('./media/img/bg.png')
    title_bg.fill((242, 50, 0), special_flags=pygame.BLEND_ADD)

    #sound
    shotfx = pygame.mixer.Sound('./media/sound/shot.wav')
    introfx = pygame.mixer.Sound('./media/sound/intro.wav')
    flapfx = pygame.mixer.Sound("./media/sound/flap.wav")
    upgradefx = pygame.mixer.Sound("./media/sound/upgrade.wav")
    heartfx = pygame.mixer.Sound("./media/sound/heart.wav")
    deadfx = pygame.mixer.Sound("./media/sound/dead.wav")
    hitfx = pygame.mixer.Sound('./media/sound/hit.wav')

    #variables
    rotOffset = -5
    a=120

    #create object
    player=Cupid()
    hearts=[]
    buttons=[]
    monsters=[]
    arrows=[]

    #add 4 buttons
    for i in range(4): 
        buttons.append(Button())

    buttons[0].typeIndicatorSprite = pygame.image.load('./media/img/flap_indicator.png')
    buttons[0].price = 10   
    buttons[1].typeIndicatorSprite = pygame.image.load('./media/img/speed_indicator.png')
    buttons[1].price = 10 
    buttons[2].typeIndicatorSprite = pygame.image.load('./media/img/heartup_indicator.png')
    buttons[2].price = 30
    buttons[3].typeIndicatorSprite = pygame.image.load('./media/img/powerup_indicator.png')
    buttons[3].price = 50

    #add 5 heart
    for i in range(5):
        hearts.append(Heart())

    for heart in hearts:
        heart.position.xy = random.randrange(0, DISPLAY.get_width() - heart.img.get_width()), hearts.index(heart)*(-200) - player.position.y
    
    #add monster
    for i in range(1):
        monsters.append(Monster())

    for monster in monsters:
        monster.position.xy = random.randrange(0,DISPLAY.get_width() - monster.img.get_width()), -1000
    
    #add arrow
    for i in range(1):
        arrows.append(Arrow())

    for arrow in arrows:
        arrow.position.xy = 1000,1000
    #background
    bg = [Background(), Background(), Background()]

    # some variables other
    heartCount = 0
    startingHeight = player.position.y
    height = 0
    health = 100
    flapForce = 3
    heartMultiplier = 5
    dead = False
    monsterdead= 1
    aim= False
    fire=False
    powerhold=0
    min = DISPLAY.get_height()
    id = 0.1
    kc = 0
    degree = 0
    arrowpower = 0
    arrowvelx = 0
    arrowvely = 0



    presentScreenTimer = 0
    while presentScreenTimer < 100:
        if presentScreenTimer == 0:
            pygame.mixer.Sound.play(introfx)
        dt = time.time() - last_Time
        dt *= FPS
        presentScreenTimer += dt
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((242, 167, 135))
        presentMessageColor=(217,119,77)
        presentMessage = fontOpen1.render("HiimDuck", True, presentMessageColor)
        presentMessage2= fontOpen2.render("PRESENTS", True, presentMessageColor)
        DISPLAY.blit(presentMessage, (DISPLAY.get_width()/2 - presentMessage.get_width()/2, DISPLAY.get_height()/2 - presentMessage.get_height()))
        DISPLAY.blit(presentMessage2, (DISPLAY.get_width()/2 - presentMessage2.get_width()/2, DISPLAY.get_height()/2))    
        # update display
        pygame.display.update()
        # wait
        pygame.time.delay(3000)
        

    
    titleScreen = True
    while titleScreen:
        dt = time.time() - last_Time
        dt *= FPS
        last_Time = time.time()

        mouseX,mouseY = pygame.mouse.get_pos()

        clicked = False
        keys = pygame.key.get_pressed()
        # get events
        for event in pygame.event.get():
            #if user press the left mouse
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #if user click and click into the button start the game
        if (clicked and checkHitBox(mouseX, mouseY, 3, 3, DISPLAY.get_width()/2 - button1.get_width()/2, 398, button1.get_width(), button1.get_height())):
            clicked = False
            pygame.mixer.Sound.play(upgradefx)
            titleScreen = False
            

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0,0))
        DISPLAY.blit(logo_hide, (0,0))  
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2, DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))
        DISPLAY.blit(logo_below, (DISPLAY.get_width()/2 - logo_below.get_width()/2, DISPLAY.get_height()/2 + logo_below.get_height() )) 
        DISPLAY.blit(button1, (DISPLAY.get_width()/2 - button1.get_width()/2, 398))
        startMessage = fontSmall.render("START", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, 409))

        pygame.display.update()
        pygame.time.delay(10)
        
    clock=pygame.time.Clock()
    running= True
    #main loop of game
    while running:
        #lock max fps is 60
        clock.tick(FPS)
        dt = time.time() - last_Time
        dt *= 60
        last_Time = time.time()
        # again, get the position
        mouseX,mouseY = pygame.mouse.get_pos()
        
        jump = False
        clicked = False
        keys = pygame.key.get_pressed()
        # get events
        for event in pygame.event.get():
            #if user press the left mouse
            if event.type==pygame.KEYDOWN and event.key==K_w:
                jump = True
            if event.type==pygame.KEYDOWN:
                if event.key==K_SPACE:
                    aim = True
            if event.type==pygame.KEYUP and event.key==K_SPACE:
                aim = False
                fire=True
                arrowpower=powerhold
                powerhold = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            #quit the console
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        if aim == True:
            powerhold=powerhold+0.2*dt
        



        camOffset = -player.position.y + DISPLAY.get_height()/2 - player.currentDirection.get_size()[1]/2
        DISPLAY.fill(WHITE)

        for o in bg:
            o.setSprite(((player.position.y/50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((player.position.y/50) % 100) / 100,0.5,0.5)
        currentHeightMarker = fontOpen1.render(str(height), True, (color[0]*255, color[1]*255, color[2]*255, 50 ))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width()/2 - currentHeightMarker.get_width()/2, camOffset + round((player.position.y - startingHeight)/DISPLAY.get_height())*DISPLAY.get_height() + player.currentDirection.get_height() - 40))

        for heart in hearts:
            DISPLAY.blit(heart.img, (heart.position.x, heart.position.y + camOffset))
        
        for monster in monsters:
            DISPLAY.blit(monster.img, (monster.position.x, monster.position.y + camOffset))
            healthMonDisplay = fontGame2.render(str(monster.health) + ' HP', True, (0,0,0))
            DISPLAY.blit(healthMonDisplay,(monster.position.x + (monster.img.get_size()[0]/2) - (healthMonDisplay.get_width()/2), monster.position.y + camOffset + monster.img.get_size()[1]))

        if monsterdead % 5 == 0 and monsterdead != 0:
            if monsterdead %10 == 0:
                monsters.append(Monster())
                monsters[-1].checkTarget('untarget')
                monsters[-1].position.x = random.randrange(0,DISPLAY.get_width() - monster.img.get_width())
                monsters[-1].position.y = monsters[0].position.y - random.randrange(2, 5) *  DISPLAY.get_height()
            for monster in monsters:
                monster.maxhealth += 1
                monster.health += 1
            monsterdead += 1
            
        if fire == True and heartCount > 0:
            fire = False
            arrows.append(Arrow())
            heartCount-=1
            pygame.mixer.Sound.play(shotfx)
            for monster in monsters:
                
                if monsters.index(monster) == id:
                    degree = calcuDegree(monster.position.x + (monster.img.get_size()[0]/2), monster.position.y + (monster.img.get_size()[1]/2) , player.position.x + (player.currentDirection.get_size()[0]/2), player.position.y + (player.currentDirection.get_size()[1]/2))
                    arrowvelx = abs((monster.position.x +(monster.img.get_size()[0]/2) - (player.position.x + player.currentDirection.get_size()[0]/2)))
                    arrowvely = -abs(monster.position.y + (monster.img.get_size()[1]/2) - (player.position.y+ (player.currentDirection.get_size()[1]/2)))
                    if player.velocity.x > 0:
                        degree = -abs(degree)
                        arrowvelx = abs(arrowvelx)
                    else: 
                        degree= abs(degree)
                        arrowvelx = -abs(arrowvelx)
                    break
                else:
                    degree = 0
                    arrowvelx = 0
                    arrowvely = 0
            
            
            for arrow in arrows:
                arrows[-1].position.x = player.position.x + (player.currentDirection.get_size()[0]/2)
                arrows[-1].position.y = player.position.y+ (player.currentDirection.get_size()[1]/2)
                arrows[-1].degree = degree
                arrows[-1].power = clamp((round( player.maxpower * (arrowpower/50) )), player.minpower, player.maxpower)
                arrows[-1].velocity.x = arrowvelx/60
                arrows[-1].velocity.y = arrowvely/60
        
            
        for arrow in arrows:
            if arrow.velocity.x == 0 and arrow.velocity.y == 0 and arrow.degree == 0:
                arrow.degree = 180
                arrow.velocity.y = 5
            arrow.position.x += arrow.velocity.x *dt
            arrow.position.y += arrow.velocity.y *dt
            DISPLAY.blit(pygame.transform.rotate(arrow.img , arrow.degree), (arrow.position.x , arrow.position.y + camOffset))     


        DISPLAY.blit(pygame.transform.rotate(player.currentDirection, clamp(player.velocity.y, -10, 5)*rotOffset), (player.position.x,player.position.y + camOffset))
        
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY,DEEPPINK,(21,437+a,150*(health/100),25))

        pygame.draw.rect(DISPLAY,YELLOW,(716,437+a,71*(powerhold/50),27))
        DISPLAY.blit(shop, (0, 0))

        minpowerDisplay= fontGame.render(str(player.minpower),True,(0,0,0))
        DISPLAY.blit(minpowerDisplay, (710,530))
        maxpowerDisplay= fontGame.render(str(player.maxpower),True,(0,0,0))
        DISPLAY.blit(maxpowerDisplay, (780,530))

        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (buttons.index(button)*125), 393+a))

            priceDisplay = fontGame2.render(str(button.price), True, (0,0,0))
            DISPLAY.blit(priceDisplay, (292 + (buttons.index(button)*125), 403+a))

            levelDisplay = fontGame2.render('Lvl. ' + str(button.level), True, PINK)
            DISPLAY.blit(levelDisplay, (234 + (buttons.index(button)*125), 441+a))

            DISPLAY.blit(button.typeIndicatorSprite, (202 + (buttons.index(button)*125), 377+a))
            
            

        heartCountDisplay = fontGame.render(str(heartCount).zfill(7), True, (0,0,0))
        DISPLAY.blit(heartCountDisplay, (72, 397+a))



        if dead:
            hearts.clear()
            monsters.clear()
            DISPLAY.blit(dead_bg, (0, 0))
            DISPLAY.blit(retry_button, ((DISPLAY.get_width()/2 - retry_button.get_width()/2), (DISPLAY.get_height()/2 -50)))
            deathMessage = fontOpen2.render("RETRY", True, BLACK)
            DISPLAY.blit(deathMessage, (20+(DISPLAY.get_width()/2 - retry_button.get_width()/2), 8+(DISPLAY.get_height()/2 -50)))

        height = round(-(player.position.y - startingHeight)/DISPLAY.get_height())

        player.position.x += player.velocity.x*dt

        if player.position.x + player.currentDirection.get_size()[0] > DISPLAY.get_width():
            player.velocity.x = -abs(player.velocity.x)
            player.currentDirection = player.leftDirection
            rotOffset = 5

        if player.position.x < 0:
            player.velocity.x = abs(player.velocity.x)
            player.currentDirection = player.rightDirection
            rotOffset = -5

        if jump and not dead:
            player.velocity.y = -flapForce
            pygame.mixer.Sound.play(flapfx)

        player.position.y += player.velocity.y*dt
        player.velocity.y = clamp(player.velocity.y + player.acceleration*dt, -99999999999, 50)

        health -= 0.2*dt

        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(deadfx)

        for arrow in arrows:
            if arrow.position.y + camOffset > DISPLAY.get_height():
                arrows.pop(arrows.index(arrow))
                
            for monster in monsters:    
                if (checkHitBox(arrow.position.x, arrow.position.y, arrow.img.get_width(), arrow.img.get_height(), monster.position.x, monster.position.y, monster.img.get_width(), monster.img.get_height())):
                    pygame.mixer.Sound.play(hitfx)
                    if monster.health > arrow.power:
                        arrow.position.y= 1000
                        monster.health -= arrow.power
                        break
                    if monster.health <= arrow.power:
                        arrow.power -= monster.health
                        monster.health = 0
                    if arrow.power == 0:
                        arrow.position.y=1000

                    if monster.health <= 0:
                        monsterdead+=1
                        monster.checkTarget('untarget')
                        monster.position.x = random.randrange(0, DISPLAY.get_width() - monster.img.get_width())
                        monster.position.y = monster.position.y - DISPLAY.get_height()*random.randrange(5 - (height % 5) , 6)
                        monster.health = monster.maxhealth
                    
        
        for heart in hearts:
            if heart.position.y + camOffset  > DISPLAY.get_height():
                heart.position.y -= DISPLAY.get_height()*2
                heart.position.x = random.randrange(0, DISPLAY.get_width() - heart.img.get_width())

            if (checkHitBox(player.position.x, player.position.y, player.currentDirection.get_width(), player.currentDirection.get_height(), heart.position.x, heart.position.y, heart.img.get_width(), heart.img.get_height())):
                pygame.mixer.Sound.play(heartfx)
                heartCount += 1
                health = 100
                heart.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                heart.position.x = random.randrange(0, DISPLAY.get_width() - heart.img.get_width())

        for monster in monsters:
            if monster.position.y + camOffset > DISPLAY.get_height():
                monsterdead += 1
                monster.position.x = random.randrange(0, DISPLAY.get_width() - monster.img.get_width())
                monster.position.y = monster.position.y - DISPLAY.get_height()*random.randrange(5 - (height % 5) , 6)
            
            if (checkHitBox(player.position.x, player.position.y, player.currentDirection.get_width(), player.currentDirection.get_height(),monster.position.x, monster.position.y, monster.img.get_width(),monster.img.get_height())):
                dead = True
                pygame.mixer.Sound.play(deadfx)
                


            if player.velocity.x > 0:
                if monster.position.x > player.position.x:
                    kc = calcu(monster.position.x + (monster.img.get_size()[0]/2),monster.position.y + (monster.img.get_size()[1]/2) ,player.position.x + (player.currentDirection.get_size()[0]/2),player.position.y + (player.currentDirection.get_size()[1]/2))
                    if min >= kc:
                        min = kc
                        id = monsters.index(monster)
                    else:
                        monster.checkTarget('untarget')

                if monsters.index(monster) == id:
                    monster.checkTarget('target')
                    if monster.position.x < player.position.x or player.position.y < monster.position.y:
                        monster.checkTarget('untarget')
                        id = 0.1
                        min = DISPLAY.get_height()
            
            if player.velocity.x < 0:
                if monster.position.x < player.position.x:
                    kc = calcu(monster.position.x + (monster.img.get_size()[0]/2),monster.position.y + (monster.img.get_size()[1]/2) ,player.position.x + (player.currentDirection.get_size()[0]/2),player.position.y + (player.currentDirection.get_size()[1]/2))
                    if min > kc:
                        min = kc
                        id = monsters.index(monster)
                    else:
                        monster.checkTarget('untarget')

                if monsters.index(monster) == id:
                    monster.checkTarget('target')
                    if monster.position.x > player.position.x or player.position.y < monster.position.y:
                        monster.checkTarget('untarget')
                        id = 0.1    
                        min = DISPLAY.get_height()


       
            


        for button in buttons:
            buttonX,buttonY = 220 + (buttons.index(button)*125), 393+a
            
            if clicked and not dead and checkHitBox(mouseX, mouseY, 3, 3, buttonX, buttonY, button.sprite.get_width(), button.sprite.get_height()):
                if (heartCount >= button.price):
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    heartCount -= button.price
                    button.price = round(button.price*3)
                    if (buttons.index(button) == 0):
                        flapForce *= 1.1
                    if (buttons.index(button) == 1):
                        player.velocity.x *= 1.1
                    if (buttons.index(button) == 2):
                        heartMultiplier += 1
                        for i in range(heartMultiplier):
                            hearts.append(Heart())
                            hearts[-1].position.xy = random.randrange(0, DISPLAY.get_width() - heart.img.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(0, 200)
                    if (buttons.index(button) == 3):
                        player.minpower = player.minpower+1
                        player.maxpower = round(player.minpower*2.5) + 1
            


        if dead == True and clicked and checkHitBox(mouseX, mouseY, 3, 3, ((DISPLAY.get_width()/2 - retry_button.get_width()/2)), (DISPLAY.get_height()/2 - 50), retry_button.get_width(), retry_button.get_height()):
            health = 100
            player.velocity.xy = 3, 0
            player.position.xy = 295, 100
            player.currentDirection = player.rightDirection
            heartCount = 0
            height = 0
            flapForce = 3
            heartMultiplier = 5
            player.minpower = 1
            player.maxpower = 2
            monsterdead = 1
            buttons = []
            for i in range(4): buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load('./media/img/flap_indicator.png')
            buttons[0].price = 10  
            buttons[1].typeIndicatorSprite = pygame.image.load('./media/img/speed_indicator.png')
            buttons[1].price = 10 
            buttons[2].typeIndicatorSprite = pygame.image.load('./media/img/heartup_indicator.png')
            buttons[2].price = 30
            buttons[3].typeIndicatorSprite = pygame.image.load('./media/img/powerup_indicator.png')
            buttons[3].price = 50
            hearts = []
            for i in range(5): hearts.append(Heart())
            for heart in hearts:
                heart.position.xy = random.randrange(0, DISPLAY.get_width() - heart.img.get_width()), hearts.index(heart)*-200 - player.position.y
            monsters = []
            for i in range(1):
                monsters.append(Monster())
            for monster in monsters:
                monster.position.xy = random.randrange(0,DISPLAY.get_width() - monster.img.get_width()), -1000

            pygame.mixer.Sound.play(upgradefx)
            dead = False         

            
        bg[0].position = camOffset + round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height() 
        bg[2].position = bg[0].position - DISPLAY.get_height()

        pygame.display.update()
        pygame.time.delay(10)
if __name__ == "__main__":
    main()