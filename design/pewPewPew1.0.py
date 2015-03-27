import sys, pygame, random, math, utils
#learned about sprites from
#http://programarcadegames.com/index.php?chapter=introduction_to_sprites



class PewShip(pygame.sprite.Sprite):
    def __init__(self, width, height, screen):
        super(PewShip, self).__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.white = (255, 255, 255)
        self.shipWidth = 75
        self.shipHeight = 45
        #x and y are based on the point of the ship
        self.shipX = self.width / 2
        self.shipY = self.height / 2
        self.screen = screen
        #how fast the arrows move the ship
        self.shipSpeed = 15
        #the speed at which the height/width changes for directional views
        self.dSize = .97
        self.theta = 0

    def editShipShape(self, direct):
        #changes shape for 2.5D perspective
        if direct == "right":
            self.theta += math.pi / 100
        elif direct == "left":
            self.theta -= math.pi / 100
        elif direct == "up":
            self.shipHeight *= self.dSize
        elif direct == "down":
            self.shipHeight *= (1 + (1 - self.dSize))

    def moveShip(self, key):
        #moves the ship based on arrows
        if key[pygame.K_UP]:
            #keeps the ship on the screen
            if self.shipY > 0:
                self.shipY -= self.shipSpeed
                self.editShipShape("up")
        if key[pygame.K_DOWN]:
            if self.shipY < self.height - self.shipHeight:
                self.shipY += self.shipSpeed
                self.editShipShape("down")
        if key[pygame.K_RIGHT]:
            if self.shipX < self.width - self.shipWidth / 2:
                self.shipX += self.shipSpeed
                self.editShipShape("right")
        if key[pygame.K_LEFT]:
            if self.shipX > 0 + self.shipWidth / 2 :
                self.shipX -= self.shipSpeed
                self.editShipShape("left")


    def drawShip(self):
        x, y, w, h = self.shipX, self.shipY, self.shipWidth, self.shipHeight
        theta = self.theta
        # pygame.draw.polygon(self.screen, self.white, ((x, y),
        #     (x - w / 2, y + h), (x, y + 2 * h / 3), (x + w / 2, y + h)), 0)
        leftWingX, leftWingY = x - w / 2, y + h
        centerX, centerY = x, y + 2 * h / 3
        rightWingX, rightWingY = x + w / 2, y + h
        dx = 15 * math.sin(theta)
        dy = 15 * math.cos(theta)
        #draws ship
        pygame.draw.polygon(self.screen, self.white, ((x, y), 
            (leftWingX + dx, leftWingY - dy), (centerX + dx, centerY - dy), 
            (rightWingX + dx, rightWingY - dy)), 0)


class PewBullet(pygame.sprite.Sprite):
    #bullet implementation modified from
    #http://programarcadegames.com/python_examples/f.php?file=bulletList.py
    def __init__(self, x, y, cx, cy, screen):
        super(PewBullet, self).__init__()
        self.bulletSize = 5
        self.image = pygame.Surface([self.bulletSize, self.bulletSize])
        self.color = (0, 255, 100)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.cx, self.cy = cx, cy
        self.bulletSpeed = 20
        self.screen = screen
        self.dx, self.dy = (self.cx - self.rect.x), (self.cy - self.rect.y)
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

    def move(self):
        self.dx, self.dy = (self.cx - self.rect.x), (self.cy - self.rect.y)
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if self.distance != 0:
            self.rect.x += (self.dx / self.distance) * self.bulletSpeed
            self.rect.y += (self.dy / self.distance) * self.bulletSpeed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0)

    def almostCenter(self):
        #checks if the bulletList are almost in the middle of the screen
        #by seeing if it's moving away from the center
        #velTheta is velocity angle, dirTheta is direction angle
        #derived with help from jvanbure 

        #As dotP(dir, direction) = ||a||*||b||*cos(theta)
        dirx = self.rect.x - self.cx
        diry = self.rect.y - self.cy
        if dirx ** 2 + diry ** 2 == 0:
            return True
        dotP = (self.dx*dirx + self.dy*diry)
        dotP /= ((self.dx**2 + self.dy**2) * (dirx**2 + diry**2))**0.5
        theta = math.acos(dotP)
        return abs(theta) < math.pi/2



class PewEnemy(pygame.sprite.Sprite):
    def __init__(self, screen, cx, cy, path):
        super(PewEnemy, self).__init__()
        self.color = (100, 100, 255)
        self.enemySize = 0
        self.screen = screen
        #center of the screen
        self.cx, self.cy = cx, cy
        self.image = pygame.Surface([self.enemySize, self.enemySize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.rect.x, self.rect.y)
        self.startTime = pygame.time.get_ticks()
        self.path = path

    def update(self):
        self.pos()
        distance = math.sqrt((self.rect.x - self.cx) ** 2 + (self.rect.y - self.cy) ** 2)
        self.rect.size = (distance / 10, distance / 10)

    def draw(self):
        self.update()
        pygame.draw.rect(self.screen, self.color, self.rect, 0)

    def OB(self):
        #removes enemy when it goes too close to center
        if (math.sqrt((self.rect.x - self.cx) ** 2 + (self.rect.y - self.cy) ** 2) < 64):
            return True

    def pos(self):
        #get time in seconds
        #different paths the enemies can follow
        #idea of partials with help from jvanbure
        t = max(0.001, pygame.time.get_ticks() - self.startTime)
        #z is the time scaled to fit the function
        if self.path == 0:  #line
            z = t / 10.0
            self.rect.x = z
            self.rect.y = z
        elif self.path == 1:  #spiral
            #spirally path
            #prevents from dividing by 0
            z = (t / 5000.0) + 0.2
            self.rect.x = (100 * math.cos(z * 10)) / z + self.cx
            self.rect.y = (100 * math.sin(z * 10)) / z + self.cy
        elif self.path == 2:  #vertical wave from top
            z = t / 1000.0
            self.rect.x = (self.cx - 300) * (math.cos(z) - math.sin(z)) + self.cx
            self.rect.y = 30 * z
        elif self.path == 3:  #horizontal wave from bottom
            z = t / 1000.0
            self.rect.x = 50 * z
            self.rect.y = (self.cy - 150) * (math.cos(z) - math.sin(z)) + self.cy
        elif self.path == 4:  #diagonal wave from upper left coner
            z = t / 200.0
            self.rect.x = 18 * z
            self.rect.y = 100 * math.cos(z) + 10 * z
        elif self.path == 5:  #FIX THIS to be diagonal from a different corner
            z = t / 200
            self.rect.x = 100 * math.sin(z) + 10 * z
            self.rect.y = 18 * z
        print (self.rect.x, self.rect.y)


class PewPewPew(object):
    #controls the game
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.bulletList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.score = 90
        self.level = 1
        self.health = 100
        self.numOfPaths = 4
        self.levelUpDisplay = 0  #displays "level up" for 5 clock ticks
        self.initAnimation()
        self.backgroundRun = utils.StarFieldBackground(self.width, self.height, self.screen)

    def initAnimation(self):
        self.ship = PewShip(self.width, self.height, self.screen)
        self.black = (0, 0, 0)
        self.shipSpeed = 10

    def removeBullets(self):
        #same bullet removal as star removal from starfield
        newBulletList = pygame.sprite.Group()
        for bullet in self.bulletList:
            #if it's not close to the center, keep it
            if not bullet.almostCenter():
                newBulletList.add(bullet)
        self.bulletList = newBulletList

    def onKeyPressed(self, key):
        #key is entire list of the state of keys
        self.ship.moveShip(key)
        if key[pygame.K_SPACE]:
            x, y = self.ship.shipX, self.ship.shipY
            newBullet = PewBullet(x, y, self.width / 2, self.height / 2,
                                  self.screen)
            self.bulletList.add(newBullet)
        if key[pygame.K_s]:
            self.spawnEnemy()

    def testCollision(self):
        #player bullets colliding with enemy
        if pygame.sprite.groupcollide(self.bulletList, self.enemyList, True, True, collided = None):
            #points gained goes up as the level goes up
            self.score += 10 * self.level

    def shoot(self):
        #moves the enemy
        for bullet in self.bulletList:
            bullet.move()
        self.removeBullets()

    def enemyControl(self):
        path = random.randint(0, self.numOfPaths)
        # path = 5
        #only adds new enemies if there are no enemies on screen... 10 at a time
        if len(self.enemyList) == 0:
            for i in xrange(10):
                newEnemy = PewEnemy(self.screen, self.width / 2, self.height / 2, path)
                self.enemyList.add(newEnemy)
            print "I MAED A NEW LIST", path
        for enemy in self.enemyList:
            #if the enemy is "out of bounds"
            if enemy.OB():
                self.enemyList.remove(enemy)

    def enemyShoot(self):
        #enemies don't shoot back until level 3
        if self.level >= 3:
            for enemy in self.enemyList:
                pass

    def checkLevel(self):
        #levels up
        oldLevel = self.level
        if 300 > self.score >= 100:
            self.level = 2
        elif 600 > self.score >= 300:
            self.level = 3
        #checks to see if level up should be displayed
        if oldLevel != self.level:
            self.levelUpDisplay = 10


    def gameOver(self):
        #displays the game over screen
        pass

    def checkStats(self):
        #checks the numbers to see if settings of the game should change
        self.checkLevel()
        if self.health <= 0:
            self.gameOver()


    def onTimerFired(self):
        self.enemyControl()
        self.shoot()
        self.enemyShoot()
        self.testCollision()
        self.checkStats()
        self.backgroundRun.onTimerFired()
        self.redrawAll()

    def drawInfo(self):
        #draws all text on screen
        infoColor = (50, 200, 150)
        #score
        scoreLoc = (50, 20)
        utils.writeText("Score: %d"%self.score, scoreLoc, infoColor, 20, self.screen)
        #level
        levelLoc = (self.width - 45, 20)
        utils.writeText("Level: %d"%self.level, levelLoc, infoColor, 20, self.screen)
        #health

    def drawLevelUp(self):
        #every level up, levelUpDisplay becomes nonzero, and it's displayed for
        #as long as levelUpDisplay is not zero
        levelLoc = (self.width / 2, self.height / 2)
        levelColor = (100, 200, 100)
        utils.writeText("Level Up!", levelLoc, levelColor, 50, self.screen)
        self.levelUpDisplay -= 1

    def redrawAll(self):
        #modifying the bullets
        for bullet in self.bulletList:
            bullet.draw()
        for enemy in self.enemyList:
            enemy.draw()
        if self.levelUpDisplay > 0:
            self.drawLevelUp()
        self.drawInfo()
        self.ship.drawShip()


