import sys, pygame, random, math, utils, variables
from starField import StarField
from pewPewPew import PewPewPew
from menuClass import Menu
from utils import StarFieldBackground

clock = pygame.time.Clock()
# I used http://lorenzod8n.wordpress.com/category/pygame-tutorial/ to learn the
# basics of pygame
# I used various pages from http://pygame.org/docs/ as a reference


def runStarField(starFieldRun):
    #starts the starfield game
    for event in pygame.event.get():
        #tests for mousepressed for starfield
        if event.type == pygame.MOUSEBUTTONDOWN:
            starFieldRun.onMousePressed(event.pos)
    starFieldRun.onTimerFired() 
    #tests for keypressed for starfield
    starFieldKeyState = pygame.key.get_pressed()
    starFieldRun.onKeyPressed(starFieldKeyState)

def runPewPewPew(pewPewPewRun):
    #starts pewpewpew game
    pewPewKeyState = pygame.key.get_pressed()
    pewPewPewRun.onKeyPressed(pewPewKeyState)
    pewPewPewRun.onTimerFired()


def run():
    width = 1200
    height = 700
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    starFieldRun = StarField(width, height, screen)
    pewPewPewRun = PewPewPew(width, height, screen)
    menuRun = Menu(width, height, screen)

    #initialization statement taken from 
    #http://lorenzod8n.wordpress.com/category/pygame-tutorial/
    while True:
        for event in pygame.event.get():
            #the quit function
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #end of copied code

        #only draws if neither game is playing
        if not variables.playSF and not variables.playPPP:
            menuRun.drawMenu()
        elif variables.playSF:
            runStarField(starFieldRun)
        elif variables.playPPP:
            runPewPewPew(pewPewPewRun)

      
        clock.tick(20)


        pygame.display.flip()


run()