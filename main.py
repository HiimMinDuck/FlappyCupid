import pygame, sys, time, math, colorsys, random
from pygame.math import Vector2
from pygame.locals import *
from background import Background
from button import Button
from heart import Heart
from cupid import Cupid
from other import checkHitBox
from other import clamp

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

    #font 
    fontOpen1= pygame.font.Font('./media/font/fontOpen.ttf', 100)
    fontOpen2= pygame.font.Font('./media/font/fontOpen2.ttf', 30)
    fontSmall=pygame.font.Font('./media/font/fontOpen2.ttf', 20)
    fontGame=pygame.font.Font('./media/font/fontGame.ttf',20)
    
    #image
    shop = pygame.image.load('./media/img/shop.png')
    shop_bg = pygame.image.load('./media/img/shop_bg.png')
    button1=pygame.image.load('./media/img/button1.png')
    logo = pygame.image.load('./media/img/logo.png')
    logo_below = pygame.image.load('./media/img/logo_below.png')
    logo_hide = pygame.image.load('./media/img/logo_hide.png')
    title_bg = pygame.image.load('./media/img/bg.png')
    title_bg.fill((242, 50, 0), special_flags=pygame.BLEND_ADD)

    #sound
    flapfx = pygame.mixer.Sound("./media/sound/flap.wav")
    upgradefx = pygame.mixer.Sound("./media/sound/upgrade.wav")
    heartfx = pygame.mixer.Sound("./media/sound/heart.wav")
    deadfx = pygame.mixer.Sound("./media/sound/dead.wav")

    #variables
    rotOffset = -5
    a=120

    #create object
    player=Cupid()
    hearts=[]
    buttons=[]

    #add 3 buttons
    for i in range(3): 
        buttons.append(Button())

    buttons[0].typeIndicatorSprite = pygame.image.load('./media/img/flap_indicator.png')
    buttons[0].price = 5   
    buttons[1].typeIndicatorSprite = pygame.image.load('./media/img/speed_indicator.png')
    buttons[1].price = 5 
    buttons[2].typeIndicatorSprite = pygame.image.load('./media/img/heartup_indicator.png')
    buttons[2].price = 30

    #add 5 heart
    for i in range(5):
        hearts.append(Heart())

    for heart in hearts:
        heart.position.xy = random.randrange(0, DISPLAY.get_width() - heart.img.get_width()), hearts.index(heart)*-200 - player.position.y
    
    #background
    bg = [Background(), Background(), Background()]

    # some variables that we need
    heartCount = 0
    startingHeight = player.position.y
    height = 0
    health = 100
    flapForce = 3
    heartMultiplier = 5
    dead = False

    presentScreenTimer = 0
    while presentScreenTimer < 100:
        dt = time.time() - last_Time
        dt *= FPS
        presentScreenTimer += dt
        #so the loop presentScreenTimer will run 100>200 times
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((242, 167, 135))
        # fill the start message on the top of the game
        presentMessageColor=(217,119,77)
        presentMessage = fontOpen1.render("HiimDuck", True, presentMessageColor)
        presentMessage2= fontOpen2.render("PRESENTS", True, presentMessageColor)
        DISPLAY.blit(presentMessage, (DISPLAY.get_width()/2 - presentMessage.get_width()/2, DISPLAY.get_height()/2 - presentMessage.get_height()))
        DISPLAY.blit(presentMessage2, (DISPLAY.get_width()/2 - presentMessage2.get_width()/2, DISPLAY.get_height()/2))    
        # update display
        pygame.display.update()
        # wait
        pygame.time.delay(1000)
        

    
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
    while True:
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
            if event.type==pygame.KEYDOWN and event.key==K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            #quit the console
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

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

        DISPLAY.blit(pygame.transform.rotate(player.currentDirection, clamp(player.velocity.y, -10, 5)*rotOffset), (player.position.x,player.position.y + camOffset))
        
        DISPLAY.blit(shop_bg, (0, a))
        pygame.draw.rect(DISPLAY,(81,48,20),(21,437+a,150*(health/100),25+a))
       
        DISPLAY.blit(shop, (0, 0))

        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (buttons.index(button)*125), 393+a))

            priceDisplay = fontGame.render(str(button.price), True, (0,0,0))
            DISPLAY.blit(priceDisplay, (292 + (buttons.index(button)*125), 403+a))

            levelDisplay = fontGame.render('Lvl. ' + str(button.level), True, (200,200,200))
            DISPLAY.blit(levelDisplay, (234 + (buttons.index(button)*125), 441+a))

            DISPLAY.blit(button.typeIndicatorSprite, (202 + (buttons.index(button)*125), 377+a))

        heartCountDisplay = fontGame.render(str(heartCount).zfill(7), True, (0,0,0))
        DISPLAY.blit(heartCountDisplay, (72, 397+a))

        if dead:
            DISPLAY.blit(button1, (4, 4))
            deathMessage = fontOpen2.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))

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

        for heart in hearts:
            if heart.position.y + camOffset  > DISPLAY.get_height():

                heart.position.y = -(DISPLAY.get_height()/2)
                heart.position.x = random.randrange(0, DISPLAY.get_width() - heart.img.get_width())

            if (checkHitBox(player.position.x, player.position.y, player.currentDirection.get_width(), player.currentDirection.get_height(), heart.position.x, heart.position.y, heart.img.get_width(), heart.img.get_height())):
                dead = False
                pygame.mixer.Sound.play(heartfx)
                heartCount += 1
                health = 100
                heart.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                heart.position.x = random.randrange(0, DISPLAY.get_width() - heart.img.get_width())
        
        for button in buttons:
            buttonX,buttonY = 220 + (buttons.index(button)*125), 393
            if clicked and not dead and checkHitBox(mouseX, mouseY, 3, 3, buttonX, buttonY, button.sprite.get_width(), button.sprite.get_height()):
                if (heartCount >= button.price):
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    heartCount -= button.price
                    button.price = round(button.price*2.5)
                    if (buttons.index(button) == 0):
                        flapForce *= 1.5
                    if (buttons.index(button) == 1):
                        player.velocity.x *= 1.5
                    if (buttons.index(button) == 2):
                        heartMultiplier += 10
                        for i in range(heartMultiplier):
                            hearts.append(Heart())
                            hearts[-1].position.xy = random.randrange(0, DISPLAY.get_width() - heart.img.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(0, 200)
                    

            if dead and clicked and checkHitBox(mouseX, mouseY, 3, 3, 4, 4, button1.get_width(), button1.get_height()):
                health = 100
                player.velocity.xy = 3, 0
                player.position.xy = 295, 100
                player.currentDirection = player.rightDirection
                heartCount = 0
                height = 0
                flapForce = 3
                heartMultiplier = 5
                buttons = []
                for i in range(3): buttons.append(Button())
                buttons[0].typeIndicatorSprite = pygame.image.load('./media/img/flap_indicator.png')
                buttons[0].price = 5   
                buttons[1].typeIndicatorSprite = pygame.image.load('./media/img/speed_indicator.png')
                buttons[1].price = 5 
                buttons[2].typeIndicatorSprite = pygame.image.load('./media/img/heartup_indicator.png')
                buttons[2].price = 30
                hearts = []
                for i in range(5): hearts.append(Heart())
                for heart in hearts:
                    heart.position.xy = random.randrange(0, DISPLAY.get_width() - heart.img.get_width()), hearts.index(heart)*-200 - player.position.y
                pygame.mixer.Sound.play(upgradefx)
                dead = False         

            
            bg[0].position = camOffset + round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
            bg[1].position = bg[0].position + DISPLAY.get_height() 
            bg[2].position = bg[0].position - DISPLAY.get_height()

        pygame.display.update()
        pygame.time.delay(10)

if __name__ == "__main__":
    main()