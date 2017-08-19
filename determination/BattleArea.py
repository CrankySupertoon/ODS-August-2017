# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.determination.BattleArea
from panda3d.core import LineSegs, Vec3
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from DrawnSquare import DrawnSquare
import math, random
ALL_KEYS = ('forward', 'reverse', 'turnLeft', 'turnRight', 'jump')

class BattleArea(DrawnSquare):
    MUSIC_FILE = None
    HEART_COLOR = (1, 0, 0, 1)
    ENEMY_COLOR = (1, 0, 0, 1)
    INIT_SPEED = 0.5
    PLAYER_SPEED = 0.8
    ENEMY_HURT_TIME = 0.4
    GAME_LENGTH = 10
    LEFT_X = -0.3
    RIGHT_X = 1.3
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, shakeCallback = None, endCallback = None, stopCallback = None, **kwargs):
        DrawnSquare.__init__(self, **kwargs)
        self.keys = {k:False for k in ALL_KEYS}
        self.shakeCallback = shakeCallback
        self.endCallback = endCallback
        self.stopCallback = stopCallback
        self.shakeSequence = None
        self.music = None
        self.seq = None
        self.nextEnemyHurt = 0
        self.hits = 0
        self.enemies = []
        self.heart = OnscreenImage(parent=self.card, image='phase_3/maps/heart.png', color=self.HEART_COLOR, scale=(0.04, 0, 0.05))
        self.heart.setTransparency(1)
        return

    def destroy(self):
        if not DrawnSquare.destroy(self):
            return
        if self.seq and self.seq.isPlaying():
            self.seq.pause()
        if self.music:
            self.music.stop()
        self.stopGame()
        del self.heart
        del self.enemies
        del self.music
        del self.seq

    def doShakeCallback(self):
        if self.shakeCallback:
            self.shakeCallback()

    def doEndCallback(self):
        if self.endCallback:
            self.endCallback()

    def doStopCallback(self):
        if self.stopCallback:
            self.stopCallback()

    def getLineXtoZ(self, fromX, toX, z):
        return ((fromX, 0, z), (toX, 0, z))

    def getRandomDirection(self):
        return random.choice([self.UP,
         self.DOWN,
         self.LEFT,
         self.RIGHT])

    def calculateVelocity(self, fromPos, toPos, speed):
        radians = math.atan2(toPos.getX() - fromPos.getX(), toPos.getZ() - fromPos.getZ())
        return Vec3(math.sin(radians), 0, math.cos(radians)) * speed

    def destroyEnemies(self):
        for enemy in self.enemies:
            enemy.removeNode()

        self.enemies = []

    def createEnemy(self, pos):
        enemy = OnscreenImage(parent=self.card, image='phase_3/maps/gear.png', color=self.ENEMY_COLOR, scale=(0.04, 0, 0.05), pos=pos)
        enemy.setTransparency(1)
        self.enemies.append(enemy)
        return enemy

    def createStationaryEnemies(self, positions):
        for pos in positions:
            self.createEnemy(pos)

    def gameLoop(self, task):
        pass

    def checkGameFinish(self, task):
        if not hasattr(self, 'heart') or not self.heart:
            return
        if task.time > self.GAME_LENGTH:
            self.stopGameSequence()
            return
        self.gameLoop(task)
        return task.cont

    def startGame(self):
        self.accept('InputState-forward', lambda pressed: self.keyPressed('forward', pressed))
        self.accept('InputState-reverse', lambda pressed: self.keyPressed('reverse', pressed))
        self.accept('InputState-turnLeft', lambda pressed: self.keyPressed('turnLeft', pressed))
        self.accept('InputState-turnRight', lambda pressed: self.keyPressed('turnRight', pressed))
        self.accept('InputState-jump', lambda pressed: self.keyPressed('jump', pressed))
        taskMgr.add(self.checkGameFinish, self.uniqueName('gameLoop'))

    def stopGame(self):
        if self.shakeSequence and self.shakeSequence.isPlaying():
            self.shakeSequence.finish()
        self.shakeSequence = None
        taskMgr.remove(self.uniqueName('gameLoop'))
        self.ignoreAll()
        return

    def startMusic(self):
        if self.MUSIC_FILE:
            self.music = loader.loadMusic(self.MUSIC_FILE)
            base.playMusic(self.music, looping=1, volume=0.9)

    def initGameSequence(self):
        self.seq = Sequence(Func(self.startMusic), self.card.scaleInterval(self.INIT_SPEED, (self.scale[0], 0, 0)), self.card.scaleInterval(self.INIT_SPEED, self.scale), Wait(0.5), Func(self.startGame))
        self.seq.start()

    def stopGameSequence(self):
        self.seq = Sequence(Func(self.stopGame), Func(self.doStopCallback), self.card.scaleInterval(self.INIT_SPEED, (self.scale[0], 0, 0)), self.card.scaleInterval(self.INIT_SPEED, 0), Func(self.destroy), Func(self.doEndCallback))
        self.seq.start()

    def shakeScreen(self):
        if self.shakeSequence and self.shakeSequence.isPlaying():
            return
        origPos = self.card.getPos()
        self.shakeSequence = Sequence(self.card.posInterval(0.1, origPos + 0.1), self.card.posInterval(0.1, origPos - 0.1), self.card.posInterval(0.1, origPos)).start()

    def moveEnemies(self, dt):
        for enemy in self.enemies:
            if not enemy.velocity:
                continue
            newPos = enemy.getPos() + enemy.velocity * dt
            if newPos.getX() > self.RIGHT_X or newPos.getX() < self.LEFT_X or newPos.getZ() > self.RIGHT_X or newPos.getZ() < self.LEFT_X:
                enemy.removeNode()
                self.enemies.remove(enemy)
            else:
                enemy.setPos(newPos)

    def checkCollision(self, time):
        if time <= self.nextEnemyHurt:
            return
        heartSize = self.heart.getScale().getX()
        for enemy in self.enemies:
            if not enemy:
                continue
            if (self.heart.getPos() - enemy.getPos()).lengthSquared() < ((heartSize + enemy.getScale().getX()) * 0.5) ** 2:
                self.hits += 1
                self.doShakeCallback()
                self.shakeScreen()
                self.nextEnemyHurt = time + self.ENEMY_HURT_TIME
                return

    def movePlayerGeneral(self, minKey, maxKey, origPos, setterFunc, dt):
        if self.keys[minKey] and self.keys[maxKey]:
            return
        if self.keys[minKey]:
            pos = origPos - self.PLAYER_SPEED * dt
        elif self.keys[maxKey]:
            pos = origPos + self.PLAYER_SPEED * dt
        else:
            return
        setterFunc(min(0.95, max(0.05, pos)))

    def keyPressed(self, id, pressed):
        self.keys[id] = pressed


class RegularBattleArea(BattleArea):

    def __init__(self, **kwargs):
        BattleArea.__init__(self, **kwargs)
        self.lockX = False
        self.lockY = False
        self.heart.setPos(0.5, 0, 0.5)

    def setLockX(self, lockX):
        self.lockX = lockX

    def setLockY(self, lockY):
        self.lockY = lockY

    def gameLoop(self, task):
        self.movePlayer(globalClock.getDt())

    def movePlayer(self, dt):
        if not self.lockX:
            self.movePlayerGeneral('turnLeft', 'turnRight', self.heart.getX(), self.heart.setX, dt)
        if not self.lockY:
            self.movePlayerGeneral('reverse', 'forward', self.heart.getZ(), self.heart.setZ, dt)


class ThrowBattleArea(RegularBattleArea):
    MUSIC_FILE = 'phase_3.5/audio/bgm/MG_throw.ogg'
    HEART_COLOR = (1, 1, 0, 1)
    WAIT_STAGE = 0
    THROW_STAGE = 1
    ENEMY_STAGE = 2
    WAIT_STAGE_TIME = 1.0
    THROW_STAGE_TIME = 0.6
    NUM_ENEMIES = 8
    DIRECTIONS = {BattleArea.UP: [ (0.065 + x * 0.125, 0, 0.925) for x in xrange(NUM_ENEMIES) ],
     BattleArea.DOWN: [ (0.065 + x * 0.125, 0, 0.065) for x in xrange(NUM_ENEMIES) ],
     BattleArea.LEFT: [ (0.05, 0, 0.065 + z * 0.125) for z in xrange(NUM_ENEMIES) ],
     BattleArea.RIGHT: [ (0.95, 0, 0.065 + z * 0.125) for z in xrange(NUM_ENEMIES) ]}

    def __init__(self, **kwargs):
        RegularBattleArea.__init__(self, **kwargs)
        self.stage = self.THROW_STAGE
        self.nextStage = 0
        self.lastDirection = -1
        self.throwSequence = None
        return

    def getName(self):
        return TTLocalizer.MinigameThrow

    def stopGame(self):
        if self.throwSequence and self.throwSequence.isPlaying():
            self.throwSequence.finish()
        self.throwSequence = None
        BattleArea.stopGame(self)
        return

    def approxEqual(self, a, b, tolerance):
        return abs(a - b) < tolerance

    def getRandomDirection(self):
        directions = [self.UP,
         self.DOWN,
         self.LEFT,
         self.RIGHT]
        x, y, z = self.heart.getPos()
        if self.approxEqual(x, 0.05, 0.01):
            directions.remove(self.LEFT)
        elif self.approxEqual(x, 0.95, 0.01):
            directions.remove(self.RIGHT)
        if self.approxEqual(z, 0.05, 0.01):
            directions.remove(self.DOWN)
        elif self.approxEqual(z, 0.95, 0.01):
            directions.remove(self.UP)
        if self.lastDirection in directions:
            directions.remove(self.lastDirection)
        return random.choice(directions)

    def gameLoop(self, task):
        dt = globalClock.getDt()
        self.movePlayer(dt)
        self.handleStages(task.time)
        self.checkCollision(task.time)

    def unlockRequired(self):
        if self.lastDirection in (self.UP, self.DOWN):
            self.lockX, self.lockY = True, False
        else:
            self.lockX, self.lockY = False, True

    def handleStages(self, taskTime):
        if taskTime < self.nextStage:
            return
        if self.stage > self.ENEMY_STAGE:
            self.stage = self.WAIT_STAGE
        if self.stage == self.WAIT_STAGE:
            self.destroyEnemies()
            self.nextStage = taskTime + self.WAIT_STAGE_TIME
        elif self.stage == self.THROW_STAGE:
            self.lastDirection = self.getRandomDirection()
            self.lockX, self.lockY = True, True
            x, y, z = self.heart.getPos()
            cX, cY, cZ = self.card.getPos()
            if self.lastDirection == self.UP:
                heartPos, cardPos1, cardPos2, cardPos3 = ((x, 0, 0.95),
                 (cX, 0, cZ + 0.1),
                 (cX, 0, cZ - 0.1),
                 self.card.getPos())
            elif self.lastDirection == self.DOWN:
                heartPos, cardPos1, cardPos2, cardPos3 = ((x, 0, 0.05),
                 (cX, 0, cZ - 0.1),
                 (cX, 0, cZ + 0.1),
                 self.card.getPos())
            elif self.lastDirection == self.LEFT:
                heartPos, cardPos1, cardPos2, cardPos3 = ((0.05, 0, z),
                 (cX + 0.1, 0, cZ),
                 (cX - 0.1, 0, cZ),
                 self.card.getPos())
            elif self.lastDirection == self.RIGHT:
                heartPos, cardPos1, cardPos2, cardPos3 = ((0.95, 0, z),
                 (cX - 0.1, 0, cZ),
                 (cX + 0.1, 0, cZ),
                 self.card.getPos())
            self.throwSequence = Sequence(self.heart.posInterval(0.1, heartPos), self.card.posInterval(0.075, cardPos1), self.card.posInterval(0.075, cardPos2), self.card.posInterval(0.075, cardPos3), Func(self.unlockRequired))
            self.throwSequence.start()
            self.nextStage = taskTime + self.THROW_STAGE_TIME
        else:
            self.createStationaryEnemies(self.DIRECTIONS[self.lastDirection])
            self.nextStage = taskTime + self.THROW_STAGE_TIME
        self.stage += 1


class LaserBattleArea(RegularBattleArea):
    MUSIC_FILE = 'phase_3.5/audio/bgm/MG_laser.ogg'
    WAIT_STAGE = 0
    WARN_APPEAR_STAGE = 1
    ATTACK_STAGE = 7
    WAIT_STAGE_TIME = 1.0
    WAIT_TILL_NEXT_WARN = 0.5
    WAIT_TILL_NEXT_RUN = 1.0
    BULLET_SPEED = 2.0
    X_DIFFERENCES = (0.1, 0.2, 0, -0.1, -0.2)
    GAME_LENGTH = 9.2
    SOURCES = (Vec3(1, 0, 1), Vec3(0, 0, 1))
    WARNING_COLOR = (1, 0.64, 0, 1)
    HEART_COLOR = (1, 0.64, 0, 1)

    def __init__(self, **kwargs):
        RegularBattleArea.__init__(self, **kwargs)
        self.warningLines = None
        self.warningLinesNp = None
        self.stage = self.WARN_APPEAR_STAGE
        self.nextStage = 0
        self.selectNewSource()
        return

    def getName(self):
        return TTLocalizer.MinigameLaser

    def destroy(self):
        if not RegularBattleArea.destroy(self):
            return
        del self.warningLines
        del self.warningLinesNp

    def selectNewSource(self):
        self.fromPos = random.choice(self.SOURCES)

    def gameLoop(self, task):
        dt = globalClock.getDt()
        self.movePlayer(dt)
        self.moveEnemies(dt)
        self.checkCollision(task.time)
        self.handleStages(task.time)

    def handleStages(self, taskTime):
        if taskTime < self.nextStage:
            return
        if self.stage > self.ATTACK_STAGE:
            self.selectNewSource()
            self.stage = self.WAIT_STAGE
        if self.stage == self.WAIT_STAGE:
            self.nextStage = taskTime + self.WAIT_STAGE_TIME
        elif self.stage == self.ATTACK_STAGE:
            self.warningLinesNp.removeNode()
            self.nextStage = taskTime + self.WAIT_TILL_NEXT_RUN
            x, y, z = self.heart.getPos()
            for target in [ Vec3(x - x2, 0, z) for x2 in self.X_DIFFERENCES ]:
                enemy = self.createEnemy(self.fromPos)
                enemy.velocity = self.calculateVelocity(self.fromPos, target, self.BULLET_SPEED)

        elif self.stage % 2 == 0:
            self.warningLinesNp.removeNode()
            self.nextStage = taskTime + self.WAIT_TILL_NEXT_WARN
        else:
            self.warningLines = LineSegs()
            self.warningLines.setThickness(3)
            self.warningLines.setColor(*self.WARNING_COLOR)
            x, y, z = self.heart.getPos()
            self.drawLines(self.warningLines, [ [self.fromPos, (x - x2, 0, z)] for x2 in self.X_DIFFERENCES ])
            self.warningLinesNp = self.card.attachNewNode(self.warningLines.create())
            self.nextStage = taskTime + self.WAIT_TILL_NEXT_WARN
        self.stage += 1


class ChaseBattleArea(RegularBattleArea):
    MUSIC_FILE = 'phase_3.5/audio/bgm/MG_chase.ogg'
    ENEMY_SPAWN_TIME = 0.4
    BULLET_SPEED = 0.95

    def __init__(self, **kwargs):
        RegularBattleArea.__init__(self, **kwargs)
        self.nextEnemySpawn = 0

    def getName(self):
        return TTLocalizer.MinigameChase

    def gameLoop(self, task):
        dt = globalClock.getDt()
        self.movePlayer(dt)
        self.spawnEnemies(task.time)
        self.moveEnemies(dt)
        self.checkCollision(task.time)

    def spawnEnemies(self, taskTime):
        if taskTime < self.nextEnemySpawn:
            return
        direction = self.getRandomDirection()
        if direction == self.UP:
            x, z = random.uniform(self.LEFT_X, self.RIGHT_X), self.RIGHT_X
        elif direction == self.DOWN:
            x, z = random.uniform(self.LEFT_X, self.RIGHT_X), self.LEFT_X
        elif direction == self.LEFT:
            x, z = self.LEFT_X, random.uniform(self.LEFT_X, self.RIGHT_X)
        elif direction == self.RIGHT:
            x, z = self.RIGHT_X, random.uniform(self.LEFT_X, self.RIGHT_X)
        pos = Vec3(x, 0, z)
        enemy = self.createEnemy(pos)
        enemy.velocity = self.calculateVelocity(pos, self.heart.getPos(), self.BULLET_SPEED)
        self.nextEnemySpawn = taskTime + self.ENEMY_SPAWN_TIME


class ShooterBattleArea(RegularBattleArea):
    MUSIC_FILE = 'phase_3.5/audio/bgm/MG_shooter.ogg'
    HEART_COLOR = (0, 1, 1, 1)
    ENEMY_SPAWN_TIME = 0.4
    BULLET_DELAY_TIME = 0.2
    LAUNCH_TIME = 3.5
    GEAR_BULLET_SPEED = 0.95
    BULLET_SPEED = 2.0
    NUM_ENEMIES = 8

    def __init__(self, **kwargs):
        RegularBattleArea.__init__(self, **kwargs)
        self.enemySpots = [False] * self.NUM_ENEMIES
        self.nextEnemySpawn = 0
        self.nextBullet = 0
        self.bullets = []

    def getName(self):
        return TTLocalizer.MinigameShooter

    def destroy(self):
        if not RegularBattleArea.destroy(self):
            return
        del self.enemySpots
        del self.bullets

    def getFreeIndex(self):
        indexes = []
        for i, element in enumerate(self.enemySpots):
            if not element:
                indexes.append(i)

        if not indexes:
            return -1
        return random.choice(indexes)

    def gameLoop(self, task):
        dt = globalClock.getDt()
        self.movePlayer(dt)
        self.spawnEnemies(task.time)
        self.moveEnemies(dt)
        self.checkCollision(task.time)
        self.shootBullet(task.time)
        self.moveBullets(dt)

    def shootBullet(self, taskTime):
        if taskTime < self.nextBullet or not self.keys['jump']:
            return
        bullet = OnscreenImage(parent=self.card, image='phase_3/maps/bullet.png', scale=(0.04, 0, 0.05), color=(1, 1, 1, 1), pos=self.heart.getPos())
        bullet.velocity = Vec3(0, 0, self.BULLET_SPEED)
        bullet.setTransparency(1)
        self.bullets.append(bullet)
        self.nextBullet = taskTime + self.BULLET_DELAY_TIME

    def moveBullets(self, dt):
        for bullet in self.bullets:
            newPos = bullet.getPos() + bullet.velocity * dt
            if newPos.getX() > self.RIGHT_X or newPos.getX() < self.LEFT_X or newPos.getZ() > self.RIGHT_X or newPos.getZ() < self.LEFT_X:
                bullet.removeNode()
                self.bullets.remove(bullet)
                return
            for i in xrange(len(self.enemies) - 1, -1, -1):
                enemy = self.enemies[i]
                if (bullet.getPos() - enemy.getPos()).lengthSquared() < ((bullet.getScale().getX() + enemy.getScale().getX()) * 0.5) ** 2:
                    bullet.removeNode()
                    enemy.removeNode()
                    if enemy.spawnSlot != -1:
                        self.enemySpots[enemy.spawnSlot] = False
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    return

            bullet.setPos(newPos)

    def spawnEnemies(self, taskTime):
        if taskTime < self.nextEnemySpawn:
            return
        else:
            for enemy in self.enemies:
                if enemy.spawnSlot != -1 and taskTime >= enemy.launchTime:
                    enemy.velocity = self.calculateVelocity(enemy.getPos(), self.heart.getPos(), self.GEAR_BULLET_SPEED)
                    self.enemySpots[enemy.spawnSlot] = False
                    enemy.spawnSlot = -1

            self.nextEnemySpawn = taskTime + self.ENEMY_SPAWN_TIME
            spawnSlot = self.getFreeIndex()
            if spawnSlot == -1:
                return
            enemy = self.createEnemy((0.065 + spawnSlot * 0.125, 0, 0.925))
            enemy.spawnSlot = spawnSlot
            enemy.launchTime = taskTime + self.LAUNCH_TIME
            enemy.velocity = None
            self.enemySpots[spawnSlot] = True
            return


class HeadOnBattleArea(BattleArea):
    MUSIC_FILE = 'phase_3.5/audio/bgm/MG_headon.ogg'
    HEART_COLOR = (0, 1, 0, 1)
    WAIT_STAGE_TIME = 1.0
    SPAWN_STAGE_TIME = 0.3
    MIN_ENEMIES = 2
    MAX_ENEMIES = 6
    BULLET_SPEED = 1.65
    DIRECTIONS = {BattleArea.UP: [(0.5, 0, BattleArea.RIGHT_X), Vec3(0, 0, -BULLET_SPEED)],
     BattleArea.DOWN: [(0.5, 0, BattleArea.LEFT_X), Vec3(0, 0, BULLET_SPEED)],
     BattleArea.LEFT: [(BattleArea.LEFT_X, 0, 0.5), Vec3(BULLET_SPEED, 0, 0)],
     BattleArea.RIGHT: [(BattleArea.RIGHT_X, 0, 0.5), Vec3(-BULLET_SPEED, 0, 0)]}

    def __init__(self, **kwargs):
        BattleArea.__init__(self, **kwargs)
        self.waiting = False
        self.nextStage = 0
        self.spawned = 0
        self.required = 0
        self.direction = -1
        self.heart.setPos(0.5, 0, 0.5)
        self.protectorNp = OnscreenImage(parent=self.card, image='phase_3/maps/bullet.png', scale=(0.04, 0, 0.05), color=(1, 1, 1, 1), pos=(0.5, 0, 0.65), hpr=(0, 0, -90))

    def getName(self):
        return TTLocalizer.MinigameHeadOn

    def destroy(self):
        if not BattleArea.destroy(self):
            return
        del self.protectorNp

    def gameLoop(self, task):
        dt = globalClock.getDt()
        self.spawnEnemies(task.time)
        self.moveEnemies(dt)
        self.checkCollision(task.time)
        self.checkProtectorColl()

    def keyPressed(self, id, pressed):
        if not pressed:
            return
        if id == 'forward':
            self.protectorNp.setPosHpr(0.5, 0, 0.65, 0, 0, -90)
        elif id == 'reverse':
            self.protectorNp.setPosHpr(0.5, 0, 0.35, 0, 0, 90)
        elif id == 'turnLeft':
            self.protectorNp.setPosHpr(0.375, 0, 0.5, 0, 0, 180)
        elif id == 'turnRight':
            self.protectorNp.setPosHpr(0.625, 0, 0.5, 0, 0, 180)

    def spawnEnemies(self, taskTime):
        if taskTime < self.nextStage:
            return
        if self.waiting:
            self.nextStage = taskTime + self.WAIT_STAGE_TIME
            self.waiting = False
            return
        if not self.required:
            self.spawned = 0
            self.direction = self.getRandomDirection()
            self.required = random.randint(self.MIN_ENEMIES, self.MAX_ENEMIES)
        if self.spawned == self.required:
            self.waiting = True
            self.required = 0
            return
        startPos, velocity = self.DIRECTIONS[self.direction]
        enemy = self.createEnemy(startPos)
        enemy.velocity = velocity
        self.spawned += 1
        self.nextStage = taskTime + self.SPAWN_STAGE_TIME

    def checkProtectorColl(self):
        for i in xrange(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[i]
            if (self.protectorNp.getPos() - enemy.getPos()).lengthSquared() < ((self.protectorNp.getScale().getX() + enemy.getScale().getX()) * 0.5) ** 2:
                enemy.removeNode()
                self.enemies.remove(enemy)
                return


class GearsBattleArea(BattleArea):
    MUSIC_FILE = 'phase_3.5/audio/bgm/MG_gears.ogg'
    HEART_COLOR = (0.5, 0, 0.5, 1)
    LINE_NUM = 3
    LINE_MAX_Z = 0.78
    LINE_DIFFERENCE = LINE_MAX_Z / LINE_NUM
    ENEMY_POOL = range(LINE_NUM)
    LINE_SPEED = 2
    PLAYER_SPEED = 0.75
    ENEMY_SPEED = 1.0
    ENEMY_SPAWN_TIME = 0.85
    ENEMY_SPAWN_MIDDLE_START = 0.3
    SIMPLE_GAME = 0
    MIDDLE_GAME = 1
    RANDOM_GAME = 2
    LEFT = 0
    RIGHT = 1

    def __init__(self, gameType = RANDOM_GAME, **kwargs):
        BattleArea.__init__(self, **kwargs)
        self.nextLineSwitch = 0
        self.nextEnemySpawn = 0
        self.nextEnemySpawnMid = self.ENEMY_SPAWN_MIDDLE_START
        self.lineTarget = 0
        self.middleLine = int(math.floor(self.LINE_NUM / 2.0))
        self.currentLine = self.middleLine
        self.heart.setPos(0.5, 0, self.getZForLine(self.currentLine))
        if gameType == self.RANDOM_GAME:
            self.gameType = random.choice([self.SIMPLE_GAME, self.MIDDLE_GAME])
        else:
            self.gameType = gameType

    def getName(self):
        return TTLocalizer.MinigameGears

    def getZForLine(self, line):
        return self.LINE_MAX_Z - self.LINE_DIFFERENCE * line

    def initLines(self):
        BattleArea.initLines(self)
        self.lines.setColor(*self.HEART_COLOR)
        self.drawLines(self.lines, [ self.getLineXtoZ(0, 1, self.getZForLine(i)) for i in xrange(self.LINE_NUM) ])

    def switchLine(self, offset):
        newLine = self.currentLine + offset
        if newLine < 0 or newLine >= self.LINE_NUM:
            return
        self.currentLine = newLine
        self.lineTarget = self.getZForLine(newLine)

    def gameLoop(self, task):
        dt = globalClock.getDt()
        self.movePlayer(dt)
        self.spawnEnemies(task.time)
        self.moveEnemies(dt)
        self.checkCollision(task.time)

    def spawnEnemy(self, direction, line):
        enemy = self.createEnemy((self.RIGHT_X if direction == self.LEFT else self.LEFT_X, 0, self.getZForLine(line)))
        enemy.velocity = Vec3(self.ENEMY_SPEED if direction == self.RIGHT else -self.ENEMY_SPEED, 0, 0)

    def spawnEnemies(self, time):
        if self.gameType == self.SIMPLE_GAME:
            self.spawnSimpleEnemies(time)
        else:
            self.spawnMiddleEnemies(time)

    def spawnMiddleEnemies(self, time):
        if time > self.nextEnemySpawn:
            for i in self.ENEMY_POOL:
                if i != self.middleLine:
                    self.spawnEnemy(self.LEFT, i)

            self.nextEnemySpawn = time + self.ENEMY_SPAWN_TIME
        if time > self.nextEnemySpawnMid:
            self.spawnEnemy(self.RIGHT, self.middleLine)
            self.nextEnemySpawnMid = time + self.ENEMY_SPAWN_TIME

    def spawnSimpleEnemies(self, time):
        if time <= self.nextEnemySpawn:
            return
        emptySpot = random.choice(self.ENEMY_POOL)
        for i in self.ENEMY_POOL:
            if i != emptySpot:
                self.spawnEnemy(self.LEFT, i)

        self.nextEnemySpawn = time + self.ENEMY_SPAWN_TIME

    def movePlayer(self, dt):
        if not self.lineTarget:
            if not (self.keys['forward'] and self.keys['reverse']):
                if self.keys['forward']:
                    self.switchLine(-1)
                elif self.keys['reverse']:
                    self.switchLine(1)
        else:
            if self.lineTarget >= self.heart.getZ():
                newZ = min(self.lineTarget, self.heart.getZ() + self.LINE_SPEED * dt)
            else:
                newZ = max(self.lineTarget, self.heart.getZ() - self.LINE_SPEED * dt)
            self.heart.setZ(newZ)
            if newZ == self.lineTarget:
                self.lineTarget = 0
        self.movePlayerGeneral('turnLeft', 'turnRight', self.heart.getX(), self.heart.setX, dt)


ALL_GAMES = [ThrowBattleArea,
 LaserBattleArea,
 ShooterBattleArea,
 ChaseBattleArea,
 GearsBattleArea,
 HeadOnBattleArea]

def getRandomGame():
    return random.choice(ALL_GAMES)