import sys, pygame, random, math, utils, highScores, eztext, variables

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
        self.shipHeight = abs(self.rect.y - self.height / 2) / 7
        #x and y are based on the point of the ship
        self.rect.move_ip(self.width / 2, self.height / 2)
        self.screen = screen
        #how fast the arrows move the ship
        self.shipSpeed = 25
        #the speed at which the height/width changes for directional views
        self.dSize = .97
        self.theta = 0
        self.maxSize = 50.0

    def editShipShape(self, direct):
        #changes shape for 2.5D perspective
        if direct == "right":
            self.theta += math.pi / 100
        elif direct == "left":
            self.theta -= math.pi / 100
        elif direct == "up" or direct == "down":
            sizeRatio = (self.maxSize / self.height / 2.0)
            self.shipHeight = abs(self.rect.y - (self.height / 2.0)) * sizeRatio
            self.shipHeight += 50

    def moveShip(self, key):
        #moves the ship based on arrows
        if key[pygame.K_UP]:
            #keeps the ship on the screen
            if self.rect.y > self.shipHeight:
                self.rect.y -= self.shipSpeed
                self.editShipShape("up")
        if key[pygame.K_DOWN]:
            if self.rect.y < self.height - self.shipHeight:
                self.rect.y += self.shipSpeed
                self.editShipShape("down")
        if key[pygame.K_RIGHT]:
            if self.rect.x < self.width - self.shipWidth / 2:
                self.rect.x += self.shipSpeed
                self.editShipShape("right")
        if key[pygame.K_LEFT]:
            if self.rect.x > 0 + self.shipWidth / 2 :
                self.rect.x -= self.shipSpeed
                self.editShipShape("left")

    def drawShip(self):
        x, y, w, h = self.rect.x, self.rect.y, self.shipWidth, self.shipHeight
        dx = 35 * math.sin(self.theta)
        dy = 35 * math.cos(self.theta)
        if self.rect.y - self.height / 2 > 0: #bottom half of screen
            leftWingX, leftWingY = x - w / 2, y + h
            centerX, centerY = x, y + 3 * h / 4
            rightWingX, rightWingY = x + w / 2, y + h
            dy *= -1
        else:
            leftWingX, leftWingY = x - w / 2, y - h
            centerX, centerY = x, y - 3 * h / 4
            rightWingX, rightWingY = x + w / 2, y - h
        #draws ship
        pygame.draw.polygon(self.screen, self.white, ((x, y), 
        (leftWingX + dx, leftWingY + dy), (centerX + dx, centerY + dy), 
        (rightWingX + dx, rightWingY + dy)), 0)

class PewBullet(pygame.sprite.Sprite, pygame.Rect):
    #bullet implementation modified from
    #http://programarcadegames.com/python_examples/f.php?file=bulletList.py
    def __init__(self, x, y, cx, cy, screen, color, size):
        #x, y is inital loc, cx, cy is final loc
        pygame.sprite.Sprite.__init__(self)
        self.bulletSize = size
        self.color = color
        self.image = pygame.Surface([self.bulletSize, self.bulletSize])
        self.image.fill(self.color)
        pygame.Rect.__init__(self, self.image.get_rect())
        self.rect = self
        self.move_ip(x, y)
        self.cx, self.cy = cx, cy
        self.bulletSpeed = 20
        self.screen = screen
        self.dx, self.dy = (self.cx - self.x), (self.cy - self.y)

    def update(self):
        self.dx, self.dy = (self.cx - self.x), (self.cy - self.y)
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)
        if self.distance != 0:
            self.x += (self.dx / self.distance) * self.bulletSpeed
            self.y += (self.dy / self.distance) * self.bulletSpeed
            self.size = (self.bulletSize / 1.1, self.bulletSize / 1.1)
            # print self.rect.size

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self, 0)

    def almostCenter(self):
        #checks if the bulletList are almost in the middle of the screen
        #by seeing if it's moving away from the center
        #velTheta is velocity angle, dirTheta is direction angle
        #derived with help from jvanbure 
        #As dotP(dir, direction) = ||a||*||b||*cos(theta)
        dirx = self.x - self.cx
        diry = self.y - self.cy
        if dirx ** 2 + diry ** 2 == 0:
            return True
        dotP = (self.dx*dirx + self.dy*diry)
        dotP /= ((self.dx**2 + self.dy**2) * (dirx**2 + diry**2))**0.5
        theta = math.acos(dotP)
        return abs(theta) < math.pi/2

class PewEnemy(pygame.sprite.Sprite):
    def __init__(self, screen, path, i, level):
        super(PewEnemy, self).__init__()
        self.color = (100, 100, 255)
        self.enemySize = 0
        self.screen = screen
        #center of the screen
        self.cx, self.cy = screen.get_width() / 2, screen.get_height() / 2
        #location of the ship
        self.image = pygame.Surface([self.enemySize, self.enemySize])
        self.image.fill(self.color)
        # self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.rect.x, self.rect.y)
        self.startTime = pygame.time.get_ticks()
        self.path = path
        self.i = i
        self.level = level
        self.update()
        self.bulletList = pygame.sprite.Group()

    def update(self):
        distance = math.sqrt((self.rect.x - self.cx) ** 2 +
                             (self.rect.y - self.cy) ** 2)
        self.rect.size = (distance / 10, distance / 10)
        self.offset = self.i * (self.rect.size[0] * 3)
        self.pos()

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 1)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bulletList:
            bullet.draw()

    def OB(self):
        #removes enemy when it goes too close to center
        if (math.sqrt((self.rect.x - self.cx) ** 2 +
            (self.rect.y - self.cy) ** 2) < 64):
            return True

    def moveBullets(self):
        width, height = self.cx * 2, self.cy * 2
        newBulletList = pygame.sprite.Group()
        for bullet in self.bulletList:
            #moves bullets
            bullet.update()
            #removes bullets
            if not bullet.almostCenter():
                newBulletList.add(bullet)
        self.bulletList = newBulletList

    def shoot(self, shipLoc):
        #randomly lets the enemies shoot
        x, y = shipLoc
        if self.level >= 2:  #enemies don't shoot back till level 2
            if random.randint(0, 125) == 42:
                # makes the shooting more sparse 
                newBullet = PewBullet(self.rect.x, self.rect.y, x,
                                      y, self.screen, (250, 170, 100), 10)
                self.bulletList.add(newBullet)

    def doStuff(self, shipLoc):
        #controls everything the enemy does
        self.update()
        self.shoot(shipLoc)
        self.moveBullets()

    def pos(self):
        #get time in seconds
        #different paths the enemies can follow
        #idea of partials from jvanbure
        #prevents from dividing by 0
        t = max(0.001, pygame.time.get_ticks() - self.startTime) + self.offset
        #z is the time scaled to fit the function
        if self.path == 0:  #spiral
            #spirally path
            z = (t / 5000.0) + 0.2
            self.rect.x = (100 * math.cos(z * 10)) / z + self.cx
            self.rect.y = (100 * math.sin(z * 10)) / z + self.cy
        elif self.path == 1:  #vertical wave from top
            z = t / 1000.0
            self.rect.x =(self.cx - 300) * (math.cos(z) - math.sin(z)) + self.cx
            self.rect.y = 30 * z + 40
        elif self.path == 2:  #horizontal wave from left
            z = t / 1000.0
            self.rect.x = 50 * z + 40
            self.rect.y =(self.cy - 140) * (math.cos(z) - math.sin(z)) + self.cy
        elif self.path == 3:  #diagonal wave from upper left coner
            z = t / 200.0
            self.rect.x = 18 * z
            self.rect.y = 100 * math.cos(z) + 10 * z
        elif self.path == 4:  #diagonal wave from lower right coner
            z = t / 200.0
            self.rect.x = self.screen.get_width() - 18 * z
            self.rect.y = self.screen.get_height() - 100 * math.cos(z) + 10 * z

class Boss(pygame.sprite.Sprite):
    def __init__(self, screen, level, cx, cy):
        super(Boss, self).__init__()
        self.screen = screen
        self.color = (100, 200, 70)
        self.size = 200
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.health = self.maxHealth = level * 10.0
        self.rect.move_ip(cx, cy)
        self.startTime = pygame.time.get_ticks()
        self.cx, self.cy = cx, cy
        self.bulletList = pygame.sprite.Group()

    def updateBullets(self, shipLoc):
        (x, y) = shipLoc
        if random.randint(0, 20) == 20:
            newBullet = PewBullet(self.rect.x, self.rect.y, x, y, self.screen,
                                  (250, 170, 100), 10)
            self.bulletList.add(newBullet)

    def update(self, shipLoc):
        distance = math.sqrt((self.rect.x - self.screen.get_width() / 2) ** 2 +
                             (self.rect.y - self.screen.get_height() / 2) ** 2)
        self.rect.size = (distance, distance)
        t = (pygame.time.get_ticks() - self.startTime) / (500 * math.pi)
        self.rect.x = self.screen.get_width() / 4 * math.cos(t) + self.cx
        self.rect.y = self.screen.get_height() / 4 * math.sin(t) + self.cy
        self.updateBullets(shipLoc)

    def removeBullets(self):
        #same bullet removal as star removal from starfield
        newBulletList = pygame.sprite.Group()
        for bullet in self.bulletList:
            #if it's not close to the center, keep it
            if not bullet.almostCenter():
                newBulletList.add(bullet)
            bullet.update()
        self.bulletList = newBulletList

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0)
        for bullet in self.bulletList:
            bullet.draw()
        self.removeBullets()
        #health
        hx, hy= (self.rect.x, self.rect.y - 5)
        hHeight = 10
        hWidth = self.rect.size[0] * (self.health / self.maxHealth)
        healthLoc = (hx, hy, hWidth, hHeight)
        pygame.draw.rect(self.screen, (255, 0, 0), healthLoc, 0)
        healthNum = str(int(self.health))
        utils.writeText(healthNum, (self.rect.x + self.rect.size[0] / 2,
                        self.rect.y), (255, 255, 255), 20, self.screen)

class MiscBox(pygame.sprite.Sprite):
    def __init__(self, screen, color):
        super(MiscBox, self).__init__()
        self.screen = screen
        self.size = 30
        self.color = color
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.rect.move_ip(x, y)

    def update(self):
        #distance from the center of screen
        distance = math.sqrt((self.rect.x - self.screen.get_width() / 2) ** 2 +
                             (self.rect.y - self.screen.get_height() / 2) ** 2)
        maxDistance = math.sqrt(self.cx ** 2 + self.cy ** 2)
        newSize = (distance / maxDistance) * self.size
        self.rect.size = (newSize, newSize)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, 0)

class PewPewPew(object):
    #controls the game
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.initAnimation()
        self.backgroundRun = utils.StarFieldBackground(self.width, self.height,
                                                       self.screen)
        self.hs = highScores.load()

    def initAnimation(self):
        self.ship = PewShip(self.width, self.height, self.screen)
        self.black = (0, 0, 0)
        self.shipSpeed = 10
        self.score = 0
        self.level = 1
        self.health = 100
        #level up is based on how many enemies killed
        self.enemiesKilled = 0
        self.bulletList = pygame.sprite.Group()
        self.ammo = 250
        self.ammoBoxList = pygame.sprite.Group()
        self.healthBoxList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.bossList = pygame.sprite.Group()
        self.numOfPaths = 3
        self.levelUpDisplay = 0  #displays "level up" for 5 clock ticks
        self.isGameOver = False

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
            if self.ammo > 0:
                x, y = self.ship.rect.x, self.ship.rect.y
                newBullet = PewBullet(x, y, self.width / 2, self.height / 2,
                                      self.screen, (0, 255, 100), 7)
                self.bulletList.add(newBullet)
                self.ammo -= 1
        #resets
        if key[pygame.K_r]:
            self.initAnimation()
        #quits
        if key[pygame.K_q]:
            self.initAnimation()
            variables.playPPP = False
        ################################################################################
        if key[pygame.K_o]:
            self.score += 3000

    def testBossCollision(self):
        if self.ship.rect.colliderect(self.boss):
            self.health -= self.level / 5
        for bullet in self.boss.bulletList:
            if self.ship.rect.colliderect(bullet):
                self.health -= self.level
        if pygame.sprite.groupcollide(self.bossList, self.bulletList, False,
                                      True, collided = None):
            self.boss.health -= 1
        #if the boss is killed
        if self.boss.health <= 0:
            self.score += 100 * (self.level / 5)
            self.level += 1

    def testCollision(self):
        #player bullets colliding with enemy
        if pygame.sprite.groupcollide(self.bulletList, self.enemyList, True,
                                      True, collided = None):
            #points gained goes up as the level goes up
            self.score += 5 * self.level
            self.enemiesKilled += 1
        #player colliding with enemy bullets
        for enemy in self.enemyList:
            for bullet in enemy.bulletList:
                if self.ship.rect.colliderect(bullet):
                    bullet.remove(enemy.bulletList)
                    self.health -= self.level
        #player colliding with ammo boxes
        for ammoBox in self.ammoBoxList:
            if self.ship.rect.colliderect(ammoBox):
                self.ammo += 100
                ammoBox.remove(self.ammoBoxList)
        #player colliding with health boxes
        for healthBox in self.healthBoxList:
            if self.ship.rect.colliderect(healthBox):
                #restoreos a random amount
                self.health += random.randint(5, 10)
                healthBox.remove(self.healthBoxList)
        #only if its on a boss level and the boss hasn't died
        if self.level % 5 == 0 and len(self.bossList) > 0:
            self.testBossCollision()

    def shoot(self):
        #moves the bullets
        for bullet in self.bulletList:
            bullet.update()
        self.removeBullets()

    def bossFight(self):
        #creates a new boss
        if len(self.bossList) == 0:
            cx = random.randint(self.screen.get_width() / 3,
                                self.screen.get_width() * 2 / 3)
            cy = random.randint(self.screen.get_height() / 3,
                                self.screen.get_height() * 2 / 3)
            self.boss = Boss(self.screen, self.level, cx, cy)
            self.bossList.add(self.boss)
        self.boss.update((self.ship.rect.x, self.ship.rect.y))

    def enemyControl(self):
        path = random.randint(0, self.numOfPaths)
        # path = 4
        #if it's not a boss level
        if self.level % 5 != 0:
            #only adds (10) new enemies if there are no enemies on screen
            if len(self.enemyList) == 0:
                for i in xrange(10):
                    newEnemy = PewEnemy(self.screen, path, i, self.level)
                    self.enemyList.add(newEnemy)
            for enemy in self.enemyList:
                enemy.doStuff((self.ship.rect.x, self.ship.rect.y))
                #checks if enemy is out of bounds
                if enemy.OB():
                    self.enemyList.remove(enemy)

    def checkLevel(self):
        #levels up
        oldLevel = self.level
        if self.enemiesKilled == (self.level + 1) * 10:
            self.level += 1
            self.enemiesKilled = 0
        #checks to see if level up happened
        if oldLevel != self.level:
            #shows the "level up" message
            self.levelUpDisplay = 15
            #clears the screen every level up
            self.enemyList = pygame.sprite.Group()
            self.enemyBullets = pygame.sprite.Group()

    def gameOver(self):
        #what to do when the game is over
        #record high score
        #taken from http://www.pygame.org/project-EzText-920-.html
        name = ""
        name = eztext.Input(maxlength=10, color=(255,0,0), 
            prompt='Enter your name: ', x = self.width / 4, y = self.height / 2)
        #a is just a trigger
        a = True
        while a:
            events = pygame.event.get()
            # process other events
            for event in events:
                # close it x button is pressed while recording the name
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    a = False
            # update name
            name.update(events)
            self.backgroundRun.onTimerFired()
            # blit name on the sceen
            name.draw(self.screen)
            # refresh the display
            pygame.display.flip()
        #end of copied code
        self.hs.append(highScores.Score(name.value, self.score))
        self.hs.sort(reverse = True)
        #max of 5 high scores on the list
        if len(self.hs) > 5:
            #removes the lowest score after sorted
            self.hs.pop()
        highScores.save(self.hs)

    def checkStats(self):
        #checks the numbers to see if settings of the game should change
        self.checkLevel()
        if self.health <= 0:
            self.isGameOver = True
            self.gameOver()

    def spawnAmmoBox(self):
        #spawns an ammo box at a random time when there is less than 75 bullets
        if random.randint(0, 50) == 42:
            newAmmoBox = MiscBox(self.screen, (0, 255, 100))
            self.ammoBoxList.add(newAmmoBox)

    def spawnHealthBox(self):
        #same idea as ammo box
        if random.randint(0, 500) == 42:
            newHealthBox = MiscBox(self.screen, (255, 87, 87))
            self.healthBoxList.add(newHealthBox)

    def onTimerFired(self):
        if self.health > 0:
            if self.level % 5 == 0:
                self.bossFight()
            self.enemyControl()
            self.shoot()
            self.testCollision()
            self.checkStats()
            #only allows one ammo box on screen at one time
            if self.ammo < 75 and len(self.ammoBoxList) == 0:
                self.spawnAmmoBox()
            if self.health < 50 and len(self.healthBoxList) == 0:
                self.spawnHealthBox()
        #draws the background
        self.backgroundRun.onTimerFired()
        self.redrawAll()

    def drawInfo(self):
        #draws all text on screen
        infoColor = (50, 200, 150)
        #score
        scoreLoc = (75, 20)
        utils.writeText("Score: %d"%self.score, scoreLoc, infoColor, 20,
                        self.screen)
        #level
        levelLoc = (self.width - 75, 20)
        utils.writeText("Level: %d"%self.level, levelLoc, infoColor, 20,
                        self.screen)
        #health bar
        hx, hy= (self.width / 4, 20)
        hHeight = 10
        hWidth = (self.width / 2) * (self.health / 100.0)
        healthLoc = (hx, hy, hWidth, hHeight)
        pygame.draw.rect(self.screen, (255, 0, 0), healthLoc, 0)
        utils.writeText("Health: %d"%self.health, (self.width / 2, 25),
                        (255, 255, 255), 20, self.screen)
        #ammo amt
        ammoLoc = (self.width - 75, self.height - 20)
        utils.writeText("Ammo: %d"%self.ammo, ammoLoc, infoColor,20,self.screen)
        if self.ammo <= 0:
            self.drawOutOfAmmo()

    def drawOutOfAmmo(self):
        #draws out of ammo text
        print "OUT OF AMMO"
        ooaLoc = (self.width / 2, self.height / 2)
        utils.writeText("OUT OF AMMO", ooaLoc, (100, 100, 0), 50, self.screen)

    def drawLevelUp(self):
        #every level up, levelUpDisplay becomes nonzero, and it's displayed for
        #as long as levelUpDisplay is not zero
        levelLoc = (self.width / 2, self.height / 2)
        levelColor = (100, 200, 100)
        utils.writeText("Level Up!", levelLoc, levelColor, 50, self.screen)
        self.levelUpDisplay -= 1

    def drawGameOver(self):
        gameOverLoc = (self.width / 2, 60)
        textColor = (200, 0, 200)
        utils.writeText("Game Over", gameOverLoc, textColor, 70, self.screen)
        restartLoc = (self.width / 2, 150)
        utils.writeText("Press r to restart", restartLoc, textColor, 40,
                        self.screen)
        quitLoc = (self.width / 2, 200)
        utils.writeText("Press q to quit", quitLoc, textColor, 40, self.screen)

    def redrawAll(self):
        if not self.isGameOver:
            #modifying the bullets
            for bullet in self.bulletList:
                bullet.draw()
            for enemy in self.enemyList:
                enemy.draw()
            if self.levelUpDisplay > 0:
                self.drawLevelUp()
            if self.level % 5 == 0 and len(self.bossList) != 0:
                self.boss.draw()
            for ammoBox in self.ammoBoxList:
                ammoBox.draw()
            for healthBox in self.healthBoxList:
                healthBox.draw()
            self.drawInfo()
            self.ship.drawShip()
        else:
            self.drawGameOver()

