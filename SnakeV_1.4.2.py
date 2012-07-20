#coding: latin1

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, math, datetime
from pygame.locals import *

class Snake(object):
    '''
    represents a snake in our snake game
    '''
    NOCOLLISION =  0
    COLLISION   = -1
    EATAPPLE    = -2
    PASSEXIT    = -3

    def __init__(self, playground):
        self.playground = playground
        self.expansion = 0
        
    def move(self, direction):
        x, y = self.playground.snakePosition[0]
        dx, dy = direction
        newHeadPosition = (x + dx, y + dy)
        
        collisionEvent = self.playground.collisionDetection(newHeadPosition)
        if collisionEvent == Snake.EATAPPLE:
            self.expansion += 4
    
        self.playground.snakePosition.insert(0, newHeadPosition)    
        if self.expansion == 0:
            self.playground.snakePosition.pop()
        else:
            self.expansion -= 1
            
        return collisionEvent

class Playground(object):
    '''
    represents the playground in our snake game
    '''

    def __init__(self):
        self.width          = 0
        self.height         = 0
        self.applePositions = []
        self.barPositions   = []
        self.exitPosition   = []
        self.snakePosition  = []
    
    def loadLevel(self, fileName):
        global datei
        datei = open(fileName, "r")
        y = -1
        for zeile in datei:
            x = -1
            y += 1
            for zeichen in zeile:
                if zeichen != '\n':
                    x += 1
                    if zeichen == 'A':
                        self.applePositions.append((x, y))
                    elif zeichen == 'S':
                        self.snakePosition.append((x, y))
                    elif zeichen == 's':
                        self.snakePosition.insert(0, (x, y))
                    elif zeichen == 'H':
                        self.barPositions.append((x,y))
                    elif zeichen == 'E':
                        self.exitPosition.append((x,y))
            
        self.width  = x
        self.height = y
        print self.width, " -> ", self.height

    def collisionDetection(self, newHeadPosition):
        if newHeadPosition in self.exitPosition:
            print "exit collision"
            return Snake.PASSEXIT
        
        elif newHeadPosition in self.snakePosition:
            print "self collision"
            return Snake.COLLISION
        
        elif newHeadPosition in self.barPositions:
            print "bar collision"
            return Snake.COLLISION
        
        elif newHeadPosition in self.applePositions:
            print "apple collision"
            self.applePositions.remove(newHeadPosition)
            return Snake.EATAPPLE
        
        return Snake.NOCOLLISION

gameCycle       = 0
currentLevel    = 1
direction       = (0, 0)
commands        = []
playground      = Playground()
snake           = Snake(playground)

def resize((width, height)):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10.0, playground.width * 10.0 + 20.0, playground.height * 10.0 + 20.0, -10.0, -6.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
                      
def clearScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, 3.0)
                        
def drawElement(element, color):
    r, g, b = color
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    if element == playground.barPositions:
        for part in element:
            x, y    = part
            x       = x * 10.0 + 1
            y       = y * 10.0 + 1
            glVertex3f(x, y, 0.0)
            glVertex3f(9.0 + x, y, 0.0)
            glVertex3f(9.0 + x, 9.0 + y, 0.0)
            glVertex3f(x, 9.0 + y, 0.0)
            glEnd()
    else:
        for part in element:
            x, y    = part
            x       = x * 10.0
            y       = y * 10.0
            glVertex3f(x, y, 1.0)
            glVertex3f(9.0 + x, y, 1.0)
            glVertex3f(9.0 + x, 9.0 + y, 1.0)
            glVertex3f(x, 9.0 + y, 1.0)
            glEnd()

def handleEvent(event):            
    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        return False
    
    global commands
    if event.type == KEYDOWN:
        if event.key == K_RIGHT:
            commands.append(( +1,  0))
        if event.key == K_LEFT:
            commands.append(( -1,  0))
        if event.key == K_UP:
            commands.append((  0, -1))
        if event.key == K_DOWN:
            commands.append((  0, +1))
    
    return True
        
def showASCIIArt(fileName, delay):
    datei = open(fileName, "r")
    asciiArt = []
    y = -1
    for zeile in datei:
        x = -1
        y += 1
        for zeichen in zeile:
            if zeichen != '\n':
                x += 1
                if zeichen == 'X':
                    asciiArt.append((x, y))

    clearScreen()
    drawElement(asciiArt, (1.0, 0.0, 0.0))
    pygame.display.flip()
    pygame.time.delay(delay)
        
def showGameOver():
    print "GAMEOVER"
    showASCIIArt("GameOver.txt", 3000)
    global currentLevel
    global NEXT_LEVEL
    currentLevel = 1
    NEXT_LEVEL = 3
    del currentLevel
    del NEXT_LEVEL
    restartGame()
        
def showYouWon():
    print "WINNER"
    global currentLevel
    global NEXT_LEVEL
    global VERSUCH
    currentlevel = 1
    try:
        print "TRY 1"
        NEXT_LEVEL += 1
        print "LEVAELANEXT", NEXT_LEVEL
    except:
        print "EXCEPT1"
        NEXT_LEVEL = 2
        print "ZEILE 182 ist der Fehler"
    showASCIIArt("YouWon.txt", 5000)
    loadNextLevel(NEXT_LEVEL)

def resetGameState():
    # reinitialize the game (restart)
    global direction, commands, playground, snake
    playground  = Playground()
    snake       = Snake(playground)    
    direction   = (0, 0)
    commands    = []
    currentLevel= 1
    NEXT_LEVEL  = 2
    pygame.event.clear()

def loadNextLevel(nextLevel):
    resetGameState()
    playground.loadLevel("Level\level%d.txt" % nextLevel)

def restartGame():
    currentLevel = 1
    loadNextLevel(currentLevel)
        
def main():
    pygame.init()
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF
    
    playground.loadLevel("Level\level1.txt")    
    screenSize = (playground.width * 20, playground.height * 20)    
    pygame.display.set_mode(screenSize, video_flags)
    resize(screenSize)
    
    init()
    while True:
        if not handleEvent(pygame.event.poll()):
            break
        
        global gameCycle
        gameCycle += 1
        gameCycle %= 4
        if gameCycle == 0:
            global direction
            if commands:
                validCommand = False
                while not validCommand and commands:
                    new_x, new_y = commands.pop(0)
                    old_x, old_y = direction
                    if not ((abs(new_x) == abs(old_x)) and (abs(new_y) == abs(old_y))):
                        validCommand  = True
                
                if validCommand:
                    direction = (new_x, new_y)
            
            if direction != (0, 0):
                collisionEvent = snake.move(direction)
                if collisionEvent == Snake.COLLISION:
                    showGameOver()
                if collisionEvent == Snake.PASSEXIT:
                    if not playground.applePositions:
                        showYouWon()

            clearScreen()
            drawElement(playground.barPositions,    (0.5, 0.5, 0.5))
            drawElement(playground.applePositions,  (1.0, 0.0, 0.0))
            drawElement(playground.snakePosition,   (0.0, 1.0, 0.0))
            if not playground.applePositions:
                drawElement(playground.exitPosition,    (0.0, 0.0, 1.0))
            
                
            pygame.display.flip()
        
        pygame.time.delay(50)
        
if __name__ == '__main__':
    main()
