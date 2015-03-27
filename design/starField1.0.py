import random, math, pygame, sys

class Stars(object):
    def __init__(self, x, y, screen):
        self.white = (255, 255, 255)
        self.screen = screen
        self.x = x
        self.y = y
        self.r = random.uniform(2.1, 2.2)
        # self.r = random.randint(1, 4)
        self.dx = self.dy = 0
        #repicks if dx or dy is 0 (meaning itll grow uncontrollably)
        while self.dy == 0 and self.dx == 0:
            self.dx = random.uniform(-20, 20)
            self.dy = random.uniform(-20, 20)
        #chooses whether it should spawn in the small circle or big circle
        if random.getrandbits(1):
            self.smallCenterCircle()
        else:
            self.bigCenterCircle()

    def smallCenterCircle(self):
        #spawns stars on the smaller circle area in center of self.screen
        self.cx = self.x + self.dx * 5
        self.cy = self.y + self.dy * 5
        self.dx *= 0.2
        self.dy *= 0.2

    def bigCenterCircle(self):
        #spawns stars on the bigger circle, and makes the star go slower
        self.cx = self.x + self.dx * 10
        self.cy = self.y + self.dy * 10
        self.dx *= 0.15
        self.dy *= 0.15

    def draw(self):
        cx, cy, r = int(self.cx), int(self.cy), int(self.r)
        pygame.draw.circle(self.screen, self.white, (cx, cy), r, 0)

class StarField(object):
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.initAnimation()

    def initAnimation(self):
        #x,y is the center of field
        self.x = self.width/2  
        self.y = self.height/2
        self.starList = []
        self.maxStarSize = 3
        #how fast stars change without any keypresses
        self.speedChange = 1.1
        self.rChange = 1.03
        #how fast stars change speed/radius when arrows are pressed
        self.dArrowSpeed = 1.1
        self.dRadSpeed = 1.05
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def shiftUp(self):
        #gives illusion of travelling up
        for selectStar in self.starList:
            #makes sure the star isn't moving too slow
            if math.fabs(selectStar.dy) > 5:
                if selectStar.dy > 0:
                    selectStar.dy /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed
                if selectStar.dy < 0:
                    selectStar.dy *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed

    def shiftDown(self):
        #gives illusion of travelling down
        for selectStar in self.starList:
            #makes sure the star isn't moving too slow
            if math.fabs(selectStar.dy) > 5:
                if selectStar.dy > 0:
                    selectStar.dy *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed
                if selectStar.dy < 0:
                    selectStar.dy /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed

    def shiftRight(self):
        #gives illusion of travelling right
        for selectStar in self.starList:
            if math.fabs(selectStar.dx) > 5:
                #makes sure the star isn't moving too slow
                if selectStar.dx > 0:
                    selectStar.dx *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed
                if selectStar.dx < 0:
                    selectStar.dx /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed

    def shiftLeft(self):
        #gives illusion of travelling left
        for selectStar in self.starList:
            if math.fabs(selectStar.dx) > 5:
                #makes sure the star isn't moving too slow
                if selectStar.dx > 0:
                    selectStar.dx /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed
                if selectStar.dx < 0:
                    selectStar.dx *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed

    def speedUp(self):
        for selectStar in self.starList:
            selectStar.dx *= self.dArrowSpeed
        selectStar.r *= self.dRadSpeed

    def slowDown(self):
        for selectStar in self.starList:
            #makes sure the stars don't stop
            if math.fabs(selectStar.dx) > 1:
                selectStar.dx /= self.dArrowSpeed
            if math.fabs(selectStar.dy) > 1:
                selectStar.dy /= self.dArrowSpeed
            selectStar.r /= self.dRadSpeed

    def onKeyPressed(self, key):
        #arrows shifts the perspective of the stars by moving some stars slower
        #and some stars faster
        if key[pygame.K_UP]:
            self.shiftUp()
        if key[pygame.K_DOWN]:
            self.shiftDown()
        if key[pygame.K_RIGHT]:
            self.shiftRight()
        if key[pygame.K_LEFT]:
            self.shiftLeft()
        if key[pygame.K_w]: #speeds up
            self.speedUp()
        if key[pygame.K_s]: #slows down
            self.slowDown()

    def onMousePressed(self, event):
        #changes center of starfield
        self.x,self.y = event

    def onTimerFired(self):
        #creates 4 stars every timerfired
        for i in xrange(4):
            newStar=Stars(self.x, self.y, self.screen)
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
