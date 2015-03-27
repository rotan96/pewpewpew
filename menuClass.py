import utils, pygame, highScores, variables
#this file draws in the menu

class Menu(object):
    #Idea adapted from http://www.pygame.org/project-MenuClass-1260-.html
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.backgroundColor = (0, 0, 0)
        self.textColor = (20, 10, 200)
        self.subtextColor = (20, 80, 255)
        self.hilightColor = (150, 150, 250)
        #the menu currently on
        self.state = 0
        #returns if the trigger to play the game is pressed
        self.backgroundRun = utils.StarFieldBackground(self.width, self.height,
                                                       self.screen)

    def drawMainTitle(self):
        #title
        #location of the text
        titleLoc = (self.width / 2, self.height / 5)
        title = "PewPewPew"
        utils.writeText(title, titleLoc, self.textColor, 100, self.screen)

    def drawMainPlay(self):
        #play button
        playLoc = (self.width / 2, self.height * 3 / 7)
        playRectLoc = utils.writeText("Play", (playLoc), self.textColor, 50,
                                      self.screen)
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
        helpRectLoc = utils.writeText("Help", (helpLoc), self.textColor, 50,
                                      self.screen)
        if helpRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Help", helpLoc, self.hilightColor, 50, self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 2
        
    def drawMainHS(self):
        #high score button
        hsLoc = (self.width / 2, self.height * 5 / 7)
        hsRectLoc = utils.writeText("High Score", (hsLoc), self.textColor, 50,
                                    self.screen)
        if hsRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("High Score", hsLoc, self.hilightColor, 50,
                            self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 4
 
    def drawMainScreen(self):
        #draws the title screen
        self.drawMainTitle()
        self.drawMainPlay()
        self.drawMainHelp()
        self.drawMainHS()

    def drawBackButton(self):
        backLoc = (50, self.height - 30)
        backRectLoc = utils.writeText("Back", backLoc, self.textColor, 30,
                                      self.screen)
        if backRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Back", backLoc, self.hilightColor, 30, self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 0


    def drawPlayStarfield(self):
        starfieldLoc = (self.width / 2, self.height * 2 / 5)
        starFieldRectLoc = utils.writeText("Starfield", starfieldLoc,
                                           self.textColor, 50, self.screen)
        if starFieldRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Starfield", starfieldLoc, self.hilightColor, 50,
                            self.screen)
            #sees if the starfield button has been pressed
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #starts the game
                    variables.playSF = True


    def drawPlayPewPewPew(self):
        pewLoc = (self.width / 2, self.height * 3 / 5)
        starFieldRectLoc = utils.writeText("PewPewPew", (pewLoc),
                                           self.textColor, 50, self.screen)
        if starFieldRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("PewPewPew", pewLoc, self.hilightColor, 50,
                            self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #starts the game
                    variables.playPPP = True


    def drawPlayScreen(self):
        self.drawPlayStarfield()
        self.drawPlayPewPewPew()
        self.drawBackButton()

    def drawStarHelpIcon(self):
        starLoc = (self.width / 4, 75)
        starHelpRectLoc = utils.writeText("Starfield", (starLoc),
                                          self.textColor, 50, self.screen)
        if starHelpRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("Starfield", starLoc, self.hilightColor, 50,
                            self.screen)
            #changes screen to show "play" menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 2
        if self.state == 2:
            utils.writeText("Starfield", starLoc, self.hilightColor, 50,
                            self.screen)


    def drawPewHelpIcon(self):
        pewLoc = (self.width * 3 / 4, 75)
        pewHelpRectLoc = utils.writeText("PewPewPew", (pewLoc), self.textColor,
                                         50, self.screen)
        if pewHelpRectLoc.collidepoint(pygame.mouse.get_pos()):
            utils.writeText("PewPewPew", pewLoc, self.hilightColor, 50,
                            self.screen)
            #changes screen to show "play" menu
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 3
        if self.state == 3:
            utils.writeText("PewPewPew", pewLoc, self.hilightColor, 50,
                            self.screen)


    def drawInst(self):
        #draws instructions for whatever game is selected
        if self.state == 2:
            text = open("starInstruction.txt", "r")
        elif self.state == 3:
            text = open("pewInstruction.txt", "r")
        #splits instructions into new lines
        textX, textY = self.width / 2, self.height / 4
        #writes line by line

        for line in text.readlines():
            utils.writeText(line.strip(), (textX, textY), self.subtextColor, 20,
                            self.screen)
            textY += 25

    def drawStarHelpScreen(self):
        self.drawStarHelpIcon()
        self.drawPewHelpIcon()
        self.drawInst()
        self.drawBackButton()

    def drawPewHelpScreen(self):
        self.drawStarHelpIcon()
        self.drawPewHelpIcon()
        self.drawInst()
        self.drawBackButton()

    def drawScores(self):
        #draws the text into the high score score
        scores = highScores.load()
        nameX, scoreX = self.width / 4, self.width * 3 / 4
        y = self.height * 3 / 7
        for score in scores:
            utils.writeText(score.name, (nameX, y), self.textColor, 40,
                            self.screen)
            utils.writeText(str(score.score), (scoreX, y), self.textColor, 40,
                            self.screen)
            y += 60

    def drawHighScoreScreen(self):
        title = "High Scores"
        titleLoc = (self.width / 2, self.height / 7)
        utils.writeText(title, titleLoc, self.textColor, 100, self.screen)
        self.drawScores()
        self.drawBackButton()


    def drawMenu(self):
        self.backgroundRun.onTimerFired()
        if self.state == 0:
            self.drawMainScreen()
        elif self.state == 1:
            self.drawPlayScreen()
        elif self.state == 2:
            self.drawStarHelpScreen()
        elif self.state == 3:
            self.drawPewHelpScreen()
        elif self.state == 4:
            self.drawHighScoreScreen()

