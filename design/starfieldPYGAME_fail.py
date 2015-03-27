import sys, pygame
from eventBasedAnimationClass import EventBasedAnimationClass
import random, math


class Stars(object):
    def __init__(self, x, y, screen):
        self.screen = screen
        self.white = (255, 255, 255)
        self.x = x
        self.y = y
        self.r = random.uniform(1.1, 4)
        self.dx = random.randint(-15, 15)
        self.dy = random.randint(-15, 15)
        #repicks if dx and dy is 0 (meaning itll grow uncontrollably)
        while self.dy == 0 or self.dx == 0:
            self.dx = random.randint(-5, 5)
            self.dy = random.randint(-5, 5)
        #chooses whether it should spawn in the small circle or big circle
        random.choice([self.smallCenterCircle(), self.bigCenterCircle()])

    def smallCenterCircle(self):
        #spawns stars on the smaller circle area in center of screen
        self.cx = self.x + self.dx * 5
        self.cy = self.y + self.dy * 5

    def bigCenterCircle(self):
        #spawns stars on the bigger circle, and makes the star go slower
        self.cx = self.x + self.dx * 15
        self.cy = self.y + self.dy * 15
        self.dx /= 2
        self.dy /= 2

    def draw(self, canvas):
        x, y, r = self.cx, self.cy, self.r
        pygame.draw.circle(self.screen, self.white, (x, y), r)

class StarField(EventBasedAnimationClass):
    def __init__(self):
        super(StarField, self).__init__(1000, 600)
        self.screen = pygame.display.set_mode((self.width, self.height))


    def sizeChanged(self, event):
        # self.canvas = event.widget.canvas
        self.width = event.width
        self.height = event.height
        self.redrawAll()

    def shiftUp(self):
        #gives illusion of travelling up
        for selectStar in self.starList:
            #makes sure the star isn't moving too slow
            if math.fabs(selectStar.dy) > 5:
                if selectStar.dy > 1:
                    selectStar.dy /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed
                if selectStar.dy < -1:
                    selectStar.dy *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed

    def shiftDown(self):
        #gives illusion of travelling down
        for selectStar in self.starList:
            #makes sure the star isn't moving too slow
            if math.fabs(selectStar.dy) > 5:
                if selectStar.dy > -1:
                    selectStar.dy *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed
                if selectStar.dy < 1:
                    selectStar.dy /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed

    def shiftRight(self):
        #gives illusion of travelling right
        for selectStar in self.starList:
            if math.fabs(selectStar.dx) > 5:
                #makes sure the star isn't moving too slow
                if selectStar.dx > -1:
                    selectStar.dx *= self.dArrowSpeed
                    selectStar.r *= self.dRadSpeed
                if selectStar.dx < 1:
                    selectStar.dx /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed

    def shiftLeft(self):
        #gives illusion of travelling left
        for selectStar in self.starList:
            if math.fabs(selectStar.dx) > 5:
                #makes sure the star isn't moving too slow
                if selectStar.dx > 1:
                    selectStar.dx /= self.dArrowSpeed
                    selectStar.r /= self.dRadSpeed
                if selectStar.dx < -1:
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

    def onKeyPressed(self,event):
        #arrows shifts the perspective of the stars by moving some stars slower
        #and some stars faster
        for event in pygame.event.get():
            if event.key == pygame.K_UP:
                self.shiftUp()
            if event.key == pygame.K_DOWN:
                self.shiftDown()
            if event.key == pygame.K_RIGHT:
                self.shiftRight()
            if event.key == pygame.K_LEFT:
                self.shiftLeft()
            if event.key == K_W: #speeds up
                self.speedUp()
            if event.key == K_S: #slows down
                self.slowDown()

    def onMousePressed(self,event):
        self.x,self.y=event.x,event.y

    def onTimerFired(self):
        #creates 6 stars every timerfired
        for i in xrange(6):
            newStar=Stars(self.x, self.y, self.screen)
            self.starList.append(newStar)
        #loops through stars and gives illusion of zooming in
        for selectStar in self.starList:
            #moves the star
            selectStar.cx += selectStar.dx
            selectStar.cy += selectStar.dy
            selectStar.dy *= self.speedChange
            selectStar.dx *= self.speedChange
            if selectStar.r > self.maxStarSize:
                selectStar.r *= self.rChange
        self.removeStars()


    def removeStars(self):
        #takes star out of list if it goes off the screen
        self.newStarList = []
        while len(self.starList) > 0:
            stillOnBoard = self.starList.pop()
            if 0 < stillOnBoard.x < self.width or 0 < stillOnBoard.y < self.height:
                self.newStarList.append(stillOnBoard)
        self.starList = self.newStarList

    def initAnimation(self):
        #x,y is the center of field
        self.x = self.width/2  
        self.y = self.height/2
        self.starList = []
        self.maxStarSize = 15
        #how fast stars change without any keypresses
        self.speedChange = 1.1
        self.rChange = 1.22
        #how fast stars change speed/radius when arrows are pressed
        self.dArrowSpeed = 1.15
        self.dRadSpeed = 1.05
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)


    def drawStars(self):
        for selectStar in self.starList:
            selectStar.draw(self.canvas)

    def redrawAll(self):
        #draws the background
        self.screen.fill((self.black))
        self.drawStars()
        # self.canvas.create_oval(self.x-20,self.y-20,self.x+20,self.y+20,fill="",outline="Red")

    def run(self):
        self.initAnimation


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 

    clock = pygame.time.Clock()
    StarField.run

    clock.tick(40)


