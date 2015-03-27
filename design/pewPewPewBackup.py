import sys, pygame, random, math, utils
#learned about sprites from
#http://programarcadegames.com/index.php?chapter=introduction_to_sprites

#TWO TRIANGLES FOR PEWSHIP FOR SHADING FOR PERSPECTIVE

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
    def __init__(self, x, y, cx, cy, screen, color):
        #x, y is inital, cx, cy is final
        super(PewBullet, self).__init__()
        self.bulletSize = 7
        self.color = color
        self.image = pygame.Surface([self.bulletSize, self.bulletSize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.cx, self.cy = cx, cy
        self.bulletSpeed = 20
        self.screen = screen
        self.dx, self.dy = (self.cx - self.rect.x), (self.cy - self.rect.y)

    def move(self):
        self.dx, self.dy = (self.cx - self.rect.x), (self.cy - self.rect.y)
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if self.distance != 0:
            self.rect.x += (self.dx / self.distance) * self.bulletSpeed
            self.rect.y += (self.dy / self.distance) * self.bulletSpeed
            self.rect.size = (self.bulletSize / 1.1, self.bulletSize / 1.1)
            # print self.rect.size

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

    def onScreen(self):
        #for enemy bullets
        return 0 < self.x < 




class PewEnemy(pygame.sprite.Sprite):
    def __init__(self, screen, cx, cy, path, i, level, shipX, shipY):
        super(PewEnemy, self).__init__()
        self.color = (100, 100, 255)
        self.enemySize = 0
        self.screen = screen
        #center of the screen
        self.cx, self.cy = cx, cy
        #location of the ship
        self.shipX, self.shipY = shipX, shipY
        self.image = pygame.Surface([self.enemySize, self.enemySize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.rect.x, self.rect.y)
        self.startTime = pygame.time.get_ticks()
        self.path = path
        self.offset = i * self.enemySize
        self.level = level
        self.bulletList = pygame.sprite.Group()

    def update(self):
        self.pos()
        distance = math.sqrt((self.rect.x - self.cx) ** 2 + (self.rect.y - self.cy) ** 2)
        self.rect.size = (distance / 10, distance / 10)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0)
        for bullet in self.bulletList:
            bullet.draw()

    def OB(self):
        #removes enemy when it goes too close to center
        if (math.sqrt((self.rect.x - self.cx) ** 2 + (self.rect.y - self.cy) ** 2) < 64):
            return True

    def controlBullets(self):
        width, height = self.cx * 2, self.cy * 2
        newBulletList = pygame.sprite.Group()
        for bullet in self.bulletList:
            #moves bullets
            bullet.move()
            #removes bullets
            if 0 < bullet.x < width or 0 < bullet.y < height:
                newBulletList.add(bullet)
        self.bulletList = newBulletList


    def shoot(self):
        #randomly lets the enemies shoot
        if self.level >= 3:  #enemies don't shoot back till level 
            if random.randint(0, 50) == 5:
                #1/50 chance for enemy to shoot
                print "enemy is at", self.rect.x, self.rect.y
                newBullet = PewBullet(self.rect.x, self.rect.y, self.shipX,
                                      self.shipY, self.screen, (100, 50, 200))
                self.bulletList.add(newBullet)

    def doStuff(self):
        #controls everything the enemy does
        self.update()
        self.shoot()
        self.controlBullets()


    def pos(self):
        #get time in seconds
        #different paths the enemies can follow
        #idea of partials from jvanbure
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
#        print (self.rect.x, self.rect.y)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, shipX, shipY):
        super(EnemyBullet, self).__init__()
        self.screen = screen
        self.x, self.y = x, y
        self.shipX, self.shipY = shipX, shipY
        self.color = (255, 0, 100)
        self.bulletSize = 7
        self.image = pygame.Surface([self.bulletSize, self.bulletSize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.bulletSpeed = 20
        self.dx, self.dy = (self.shipX - self.rect.x), (self.shipY - self.rect.y)


    def update(self):
        #moves the bullet
        self.dx, self.dy = (self.shipX - self.rect.x), (self.shipY - self.rect.y)
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if self.distance != 0:
            self.rect.x += (self.dx / self.distance) * self.bulletSpeed
            self.rect.y += (self.dy / self.distance) * self.bulletSpeed

    def draw(self):
        print "bullet is at", self.rect.x, self.rect.y
        pygame.draw.rect(self.screen, self.color, self.rect, 0)


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen, level, cx, cy):
        super(Boss, self).__init__()
        self.screen = screen
        self.color = (100, 200, 70)
        self.size = 200
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.health = level * 10
        self.rect.move_ip(cx, cy)

    def move(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0)


class PewPewPew(object):
    #controls the game
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.initAnimation()
        self.backgroundRun = utils.StarFieldBackground(self.width, self.height, self.screen)

    def initAnimation(self):
        self.ship = PewShip(self.width, self.height, self.screen)
        self.black = (0, 0, 0)
        self.shipSpeed = 10
        self.score = 300#############################################################################
        self.level = 3###############################################################################
        self.health = 100
        self.bulletList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.numOfPaths = 4
        self.levelUpDisplay = 0  #displays "level up" for 5 clock ticks

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
                                  self.screen, (0, 255, 100))
            self.bulletList.add(newBullet)
        #resets
        if key[pygame.K_r]:
            self.initAnimation()

    def testCollision(self):
        #player bullets colliding with enemy
        if pygame.sprite.groupcollide(self.bulletList, self.enemyList, True, True, collided = None):
            #points gained goes up as the level goes up
            self.score += 10 * self.level
        #player colliding with enemy
        # print pygame.sprite.spritecollideany(self.ship, self.enemyList, collided = None)
        # print pygame.sprite.spritecollideany(self.ship, self.enemyList)
        if pygame.sprite.spritecollideany(self.ship, self.enemyList) != None:
            print "owwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"

    def shoot(self):
        #moves the bullets
        for bullet in self.bulletList:
            bullet.move()
        self.removeBullets()

    def bossFight(self):
        self.boss = Boss(self.screen, self.level, self.width / 2, self.height / 2)
        print "MUAHAHAHAHAHAHA"

    def enemyControl(self):
        path = random.randint(0, self.numOfPaths)
#        path = 5
        #if it's not a boss level
        if self.level % 5 != 0:
            #only adds new enemies if there are no enemies on screen... 10 at a time
            if len(self.enemyList) == 0:
                for i in xrange(10):
                    newEnemy = PewEnemy(self.screen, self.width / 2, self.height / 2, path, i, self.level, self.ship.shipX, self.ship.shipY)
                    self.enemyList.add(newEnemy)
#               print "I MAED A NEW LIST", path
            for enemy in self.enemyList:
                enemy.doStuff()
                #checks if enemy is out of bounds
                if enemy.OB():
                    self.enemyList.remove(enemy)



    def checkLevel(self):
        #levels up
        oldLevel = self.level
        if 200 > self.score >= 100:
            self.level = 2
        elif 400 > self.score >= 200:
            self.level = 3
        elif 800 > self.score >= 400:
            self.level = 4
        #boss level
        elif 900 > self.score >= 800:
            self.level = 5
        elif 900 > self.score >= 1400:
            self.level = 6
        elif 1400 > self.score >= 2000:
            self.level = 7
        #checks to see if level up happened
        if oldLevel != self.level:
            #shows the "level up" message
            self.levelUpDisplay = 10
            #clears the screen every level up
            self.enemyList = pygame.sprite.Group()
            self.enemyBullets = pygame.sprite.Group()



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
        self.testCollision()
        self.checkStats()
        if self.level % 5 == 0:
            self.bossFight()
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
        if self.level % 5 == 0:
            self.boss.draw()
        self.drawInfo()
        self.ship.drawShip()


