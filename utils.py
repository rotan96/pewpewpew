import pygame, random, math, variables

#these are general functions that all classes can use
def writeText(text, loc, color, size, screen):
    #Taken with minor adjustments from
    #https://www.pygame.org/docs/tut/tom/games2.html
    font = pygame.font.SysFont("Verdana", size)
    text = font.render(text, True, color)
    textpos = text.get_rect()
    textpos.center = loc
    screen.blit(text, textpos)
    return textpos

#almost the exact same code used for starfield game
class StarsForBackground(object):
    def __init__(self, x, y, screen):
        self.color = (80, 80, 80)
        self.screen = screen
        self.screen.set_colorkey((0, 0, 0))
        self.x = x
        self.y = y
        self.r = random.randint(1, 4)
        self.dx = self.dy = 0
        #repicks if dx or dy is 0 (meaning itll grow uncontrollably)
        while self.dy == 0 or self.dx == 0:
            self.dx = random.randint(-20, 20)
            self.dy = random.randint(-20, 20)
        self.smallCenterCircle()

    def smallCenterCircle(self):
        #spawns stars on the smaller circle area in center of self.screen
        self.cx = self.x + self.dx * 5
        self.cy = self.y + self.dy * 5
        self.dx *= 0.3
        self.dy *= 0.3

    def draw(self):
        cx, cy, r = int(self.cx), int(self.cy), int(self.r)
        pygame.draw.circle(self.screen, self.color, (cx, cy), r, 0)

#non-interactive background
class StarFieldBackground(object):
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.initAnimation()
        self.screen.set_colorkey((0, 0, 0))


    def initAnimation(self):
        #x,y is the center of field
        self.x = self.width/2  
        self.y = self.height/2
        self.starList = []
        self.maxStarSize = 6
        #how fast stars change without any keypresses
        self.speedChange = 1.1
        self.rChange = 1.04
        self.black = (0, 0, 0)


    def onTimerFired(self):
        #creates 4 stars every timerfired
        for i in xrange(4):
            newStar=StarsForBackground(self.x, self.y, self.screen)
            self.starList.append(newStar)
        #loops through stars and gives illusion of zooming in
        for selectStar in self.starList:
            #moves the star
            selectStar.cx += selectStar.dx
            selectStar.cy += selectStar.dy
            selectStar.dy *= self.speedChange
            selectStar.dx *= self.speedChange
            if selectStar.r < self.maxStarSize:
                selectStar.r *= self.rChange
        self.removeStars()
        self.redrawAll()

    def removeStars(self):
        #takes star out of list if it goes off the screen
        newStarList = []
        while len(self.starList) > 0:
            #removes bullets from the list
            stillOnBoard = self.starList.pop()
            #tests to see if it is still on the screen
            if (0 < stillOnBoard.cx < self.width and
                0 < stillOnBoard.cy < self.height):
                #if it is append to new list, if not move on
                newStarList.append(stillOnBoard)
        self.starList = newStarList

    def drawStars(self):
        for selectStar in self.starList:
            selectStar.draw()

    def redrawAll(self):
        self.screen.fill(self.black)
        self.drawStars()
