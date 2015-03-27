import sys, pygame, random, math, utils
from starField import StarField
from pewPewPew import PewPewPew

clock = pygame.time.Clock()
# I used http://lorenzod8n.wordpress.com/category/pygame-tutorial/ to learn the
# basics of pygame


class Menu(object):
    #Idea adapted from http://www.pygame.org/project-MenuClass-1260-.html
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.backgroundColor = (0, 0, 0)
        self.textColor = (20, 10, 200)
        self.hilightColor = (150, 150, 250)
        #the menu currently on
        self.state = 0
        #returns if the trigger to play the game is pressed
        self.playSF = False
        self.playPPP = False

    def drawMainTitle(self):
        #title
        #location of the text
        titleX, titleY = self.width / 2, self.height / 5
        title = "Temp title"
        utils.writeText(title, (titleX, titleY), self.textColor, 100, self.screen)

    def drawMainPlay(self):
        #play button
        playX, playY = self.width / 2, self.height * 3 / 7
        playRectLoc = utils.writeText("Play", (playX, playY), self.textColor, 50, self.screen)
        #changes color when the mouse is hovered over it
        if playRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Play", (playX, playY), self.hilightColor, 50, self.screen)
            #changes screen to show "play" menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 1
        
    def drawMainHelp(self):
        #help button
        helpX, helpY = self.width / 2, self.height * 4 / 7
        helpRectLoc = utils.writeText("Help", (helpX, helpY), self.textColor, 50, self.screen)
        if helpRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Help", (helpX, helpY), self.hilightColor, 50, self.screen)
        
    def drawMainHS(self):
        #high score button
        hsX, hsY = self.width / 2, self.height * 5 / 7
        hsRectLoc = utils.writeText("High Score", (hsX, hsY), self.textColor, 50, self.screen)
        if hsRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("High Score", (hsX, hsY), self.hilightColor, 50, self.screen)
 
    def drawMainScreen(self):
        #draws the title screen
        self.drawMainTitle()
        self.drawMainPlay()
        self.drawMainHelp()
        self.drawMainHS()

    def drawPlayStarfield(self):
        starfieldX, starFieldY = self.width / 2, self.height * 2 / 5
        starFieldRectLoc = utils.writeText("Starfield", (starfieldX, starFieldY), self.textColor, 50, self.screen)
        if starFieldRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Starfield", (starfieldX, starFieldY), self.hilightColor, 50, self.screen)
            #sees if the starfield button has been pressed
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #starts the game
                    self.playSF = True


    def drawPlayPewPewPew(self):
        pewX, pewY = self.width / 2, self.height * 3 / 5
        starFieldRectLoc = utils.writeText("PewPewPew", (pewX, pewY), self.textColor, 50, self.screen)
        if starFieldRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("PewPewPew", (pewX, pewY), self.hilightColor, 50, self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #starts the game
                    self.playPPP = True


    def drawPlayScreen(self):
        self.drawPlayStarfield()
        self.drawPlayPewPewPew()


    def drawMenu(self):
        self.screen.fill(self.backgroundColor)
        if self.state == 0:
            self.drawMainScreen()
        if self.state == 1:
            self.drawPlayScreen()
        return (self.playSF, self.playPPP)



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
    pewPewPewRun.onTimerFired()
    pewPewKeyState = pygame.key.get_pressed()
    pewPewPewRun.onKeyPressed(pewPewKeyState)



def run():
    width = 1000
    height = 600
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    starFieldRun = StarField(width, height, screen)
    starFieldRun.initAnimation()
    pewPewPewRun = PewPewPew(width, height, screen)
    pewPewPewRun.initAnimation()
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


        playSF, playPPP = menuRun.drawMenu()[0], menuRun.drawMenu()[1]
        if playSF:
            runStarField(starFieldRun)
        if playPPP:
            runPewPewPew(pewPewPewRun)







      
        clock.tick(30)


        pygame.display.flip()


run()