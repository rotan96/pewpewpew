import utils, pygame


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
        self.backgroundRun = utils.StarFieldBackground(self.width, self.height, self.screen)

    def drawMainTitle(self):
        #title
        #location of the text
        titleLoc = (self.width / 2, self.height / 5)
        title = "Temp title"
        utils.writeText(title, titleLoc, self.textColor, 100, self.screen)

    def drawMainPlay(self):
        #play button
        playLoc = (self.width / 2, self.height * 3 / 7)
        playRectLoc = utils.writeText("Play", (playLoc), self.textColor, 50, self.screen)
        #changes color when the mouse is hovered over it
        if playRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Play", playLoc, self.hilightColor, 50, self.screen)
            #changes screen to show "play" menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 1
        
    def drawMainHelp(self):
        #help button
        helpLoc = (self.width / 2, self.height * 4 / 7)
        helpRectLoc = utils.writeText("Help", (helpLoc), self.textColor, 50, self.screen)
        if helpRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Help", helpLoc, self.hilightColor, 50, self.screen)
        
    def drawMainHS(self):
        #high score button
        hsLoc = (self.width / 2, self.height * 5 / 7)
        hsRectLoc = utils.writeText("High Score", (hsLoc), self.textColor, 50, self.screen)
        if hsRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("High Score", hsLoc, self.hilightColor, 50, self.screen)
 
    def drawMainScreen(self):
        #draws the title screen
        self.drawMainTitle()
        self.drawMainPlay()
        self.drawMainHelp()
        self.drawMainHS()

    def drawPlayStarfield(self):
        starfieldLoc = (self.width / 2, self.height * 2 / 5)
        starFieldRectLoc = utils.writeText("Starfield", (starfieldLoc), self.textColor, 50, self.screen)
        if starFieldRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Starfield", starfieldLoc, self.hilightColor, 50, self.screen)
            #sees if the starfield button has been pressed
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #starts the game
                    self.playSF = True


    def drawPlayPewPewPew(self):
        pewLoc = (self.width / 2, self.height * 3 / 5)
        starFieldRectLoc = utils.writeText("PewPewPew", (pewLoc), self.textColor, 50, self.screen)
        if starFieldRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("PewPewPew", pewLoc, self.hilightColor, 50, self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #starts the game
                    self.playPPP = True


    def drawPlayScreen(self):
        self.drawPlayStarfield()
        self.drawPlayPewPewPew()


    def drawMenu(self):
        self.backgroundRun.onTimerFired()
        if self.state == 0:
            self.drawMainScreen()
        if self.state == 1:
            self.drawPlayScreen()
        return (self.playSF, self.playPPP)

