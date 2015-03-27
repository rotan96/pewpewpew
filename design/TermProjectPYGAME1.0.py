import sys, pygame, random, math
clock = pygame.time.Clock()

class Stars(object):
    def __init__(self, x, y, screen):
        self.white = (255, 255, 255)
        self.screen = screen
        self.x = x
        self.y = y
        # self.r = random.uniform(1.1, 4)
        self.r = random.randint(1, 4)
        self.dx = random.randint(-15, 15)
        self.dy = random.randint(-15, 15)
        #repicks if dx or dy is 0 (meaning itll grow uncontrollably)
        while self.dy == 0 or self.dx == 0:
            self.dx = random.randint(-5, 5)
            self.dy = random.randint(-5, 5)
        #chooses whether it should spawn in the small circle or big circle
        random.choice([self.smallCenterCircle(), self.bigCenterCircle()])

    def smallCenterCircle(self):
        #spawns stars on the smaller circle area in center of self.screen
        self.cx = self.x + self.dx * 5
        self.cy = self.y + self.dy * 5

    def bigCenterCircle(self):
        #spawns stars on the bigger circle, and makes the star go slower
        self.cx = self.x + self.dx * 15
        self.cy = self.y + self.dy * 15
        self.dx /= 2
        self.dy /= 2

    def draw(self):
        cx, cy, r = int(self.cx), int(self.cy), int(self.r)
        pygame.draw.circle(self.screen, self.white, (cx, cy), r, 0)

class StarField(object):
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

    def initAnimation(self):
        #x,y is the center of field
        self.x = self.width/2  
        self.y = self.height/2
        self.starList = []
        self.maxStarSize = 15
        #how fast stars change without any keypresses
        self.speedChange = 1.1
        self.rChange = 1.3
        #how fast stars change speed/radius when arrows are pressed
        self.dArrowSpeed = 1.15
        self.dRadSpeed = 1.05
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

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
        self.redrawAll()

    def removeStars(self):
        #takes star out of list if it goes off the self.screen
        self.newStarList = []
        while len(self.starList) > 0:
            stillOnBoard = self.starList.pop()
            if 0 < stillOnBoard.cx < self.width and 0 < stillOnBoard.cy < self.height:
                self.newStarList.append(stillOnBoard)
        self.starList = self.newStarList

    def drawStars(self):
        for selectStar in self.starList:
            selectStar.draw()

    def redrawAll(self):
        self.screen.fill(self.black)
        self.drawStars()

def run():
    width = 1000
    height = 600
    screen = pygame.display.set_mode((width, height))
    curRun = StarField(width, height, screen)
    curRun.initAnimation()

    while True:
        for event in pygame.event.get():
            #the quit function
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #tests for mousepressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                curRun.onMousePressed(event.pos)

        #tests for keypressed
        keyState = pygame.key.get_pressed()
        curRun.onKeyPressed(keyState)
        curRun.onTimerFired()    
       
        clock.tick(30)


        pygame.display.flip()


run()