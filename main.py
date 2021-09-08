from other import checkHitBox
import pygame, sys, time, math

from pygame import display
from heart import Heart
from pygame.constants import QUIT
from cupid import Cupid

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
    #font of word
    fontOpen1= pygame.font.Font('./media/font/fontOpen.ttf', 100)
    fontOpen2= pygame.font.Font('./media/font/fontOpen2.ttf', 30)
    fontSmall=pygame.font.Font('./media/font/fontOpen2.ttf', 20)
    button1=pygame.image.load('./media/img/button1.png')
    logo = pygame.image.load('./media/img/logo.png')
    logo_below = pygame.image.load('./media/img/logo_below.png')
    logo_hide = pygame.image.load('./media/img/logo_hide.png')
    title_bg = pygame.image.load('./media/img/bg.png')
    title_bg.fill((242, 50, 0), special_flags=pygame.BLEND_ADD)

    last_time = time.time()
    presentScreenTimer = 0

    while presentScreenTimer < 100:
        dt = time.time() - last_Time
        dt *= FPS
        last_Time = time.time()
        presentScreenTimer += dt
        #so the loop presentScreenTimer will run 100>200 times
        for event in pygame.event.get():
            # if the user clicks the button
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
    while running:
        #lock max fps is 60
        clock.tick(FPS)

        DISPLAY.fill(WHITE)
        for event in pygame.event.get():
            #quit the console
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
        pass

if __name__ == "__main__":
    main()