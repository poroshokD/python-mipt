import pygame, math, os, json
from pygame.draw import *
from random import randint, uniform


pygame.init()



class Ball():
    '''
    Ball class.
    '''
    def __init__(self):
        '''
        Creates a new ball with random position, color, speed and radius.
        '''
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.vx = randint(-10, 10)
        self.vy = randint(-10, 10)
        self.r = randint(20, 100)

    def draw(self):
        '''
        Draws ball on the screen. Uses resources/face.png
        '''
        global hitboxEnabled
        if hitboxEnabled:
            circle(screen, (255, 255, 255), (self.x, self.y), self.r)
        face_path = os.path.join('resources', 'face.png')

        texture_surface = pygame.image.load(face_path)

        width = texture_surface.get_width()
        height = texture_surface.get_height()
        new_size = (self.r * 2,
                    (self.r * 2 * 594) // 504)

        texture_surface = pygame.transform.scale(texture_surface, new_size)
        screen.blit(texture_surface, (self.x - self.r,
                                      self.y - self.r / 2 - new_size[1] / 4))
                
        
        

    def processClick(self, event):
        '''
        Checks if position of click is in radius of a ball
        '''
        x, y = event.pos
        return (self.x - x) ** 2 + (self.y - y) ** 2 < self.r ** 2

    def move(self):
        '''
        Moves ball within screen
        '''
        self.x += self.vx
        self.y += self.vy

    def stayOnScreen(self):
        '''
        Checks if ball is in screen. If not, brings it back.
        '''
        if self.x + self.r >= X_BORDER:
            self.x -= 2 * (self.x + self.r - X_BORDER)
            self.vx *= -1
        if self.y + self.r >= Y_BORDER:
            self.y -= 2 * (self.y + self.r - Y_BORDER)
            self.vy *= -1
        if self.x - self.r <= 0:
            self.x += 2 * (self.r - self.x)
            self.vx *= -1
        if self.y - self.r <= 0:
            self.y += 2 * (self.r - self.y)
            self.vy *= -1

class Targeter():
    '''
    Objects of this class will spin around ball with speed depenging on a size
    of a ball. 
    '''

    def __init__(self, ball):
        '''
        Creates targeter with random angle, radius from ball. It's speed
        depends on size of a ball, the bigger - the faster.
        TO DO: Set more interesting color
        '''
        self.angle = uniform(-math.pi, math.pi)
        self.angleSpeed = uniform(-0.2 * ball.r / 500,
                                  0.2 * ball.r / 500)
        self.r = randint(ball.r + 20, ball.r + 100)
        self.rSpeed = uniform(0.1 * ball.r ** 2 / 1000,
                              1 * ball.r ** 2 / 1000)
        self.x, self.y = ball.x, ball.y
        self.width, self.height = 0, 0
        self.texture = ['squid1.png', 'squid2.png'][randint(0,1)]

    def move(self):
        '''
        Updates angle and radius of targeter.
        '''
        self.angle += self.angleSpeed
        self.r -= self.rSpeed

    def draw(self, ball):
        '''
        Draws targeter.
        ball - connected ball.
        '''
        self.x, self.y = ball.x, ball.y
        
        texture_path = os.path.join('resources', self.texture)

        texture_surface = pygame.image.load(texture_path)

        width = texture_surface.get_width() // 2
        height = texture_surface.get_height() // 2
        self.width = width
        self.height = height
        new_size = (width, height)

        if hitboxEnabled:
            rect(screen, (255, 255, 255), (self.x + self.r * math.sin(self.angle) - width / 2,
                                        self.y + self.r * math.cos(self.angle) - height / 2,
                                           width, height)
                   )

        texture_surface = pygame.transform.scale(texture_surface, new_size)
        screen.blit(texture_surface, (self.x  + self.r * math.sin(self.angle) - width / 2,
                                      self.y + self.r * math.cos(self.angle) - height / 2))
         

    def readyForDestruction(self, ball):
        '''
        Checks whether connected ball can be destroyed comparing it's radius
        with targeter radius.
        ball - connected ball.
        '''
        return self.r < ball.r

    def processClick(self, event):
        '''
        Checks if position of click is in targeter
        '''
        x, y = event.pos
        isOnXAxis = (x >= self.x + self.r * math.sin(self.angle) - self.width / 2
                     and x <= self.x + self.r * math.sin(self.angle) + self.width / 2
                     )
        isOnYAxis = (y >= self.y + self.r * math.cos(self.angle) - self.height / 2
                     and y <= self.y + self.r * math.cos(self.angle) + self.height / 2
                     )
        
        
        return isOnXAxis and isOnYAxis

class ClickedBall():
    '''
    Gets drawn when click on the ball has been succesful at the same place
    as the ball. It only gets drawn 10 times before destruction.
    '''
    
    
    def __init__(self, ball, FPS):
        '''
        Creates object in position of a ball with the same radius as the
        ball.
        ball - the clicked ball;
        FPS - FPS of the mainloop.
        '''
        self.x, self.y = ball.x, ball.y
        self.r = ball.r

        #Time to live is for how many frames will ClickedBall be drawn.
        self.timeToLive = FPS // 3
        
    def draw(self):
        '''
        Draws ClickedBall. Uses resources/face_clicked.png
        '''
        
        face_path = os.path.join('resources', 'face_clicked.png')

        texture_surface = pygame.image.load(face_path)

        width = texture_surface.get_width()
        height = texture_surface.get_height()
        new_size = (self.r * 2,
                    (self.r * 2 * 594) // 504)

        texture_surface = pygame.transform.scale(texture_surface, new_size)
        screen.blit(texture_surface, (self.x - self.r,
                                      self.y - self.r / 2 - new_size[1] / 4))
         

    def isAlive(self):
        '''
        Checks whether ball can be drawn again. If yes, reduces it's timer
        of being drawn by 1 and returns True; returns False otherwise.
        '''
        if self.timeToLive > 0:
            self.timeToLive -= 1
            return True
        else:
            return False

class DestroyedBall(ClickedBall):
    def draw(self):
        '''
        Draws DestroyedBall. Uses resources/face_destroyed.png
        '''
        
        face_path = os.path.join('resources', 'face_destroyed.png')

        texture_surface = pygame.image.load(face_path)

        width = texture_surface.get_width()
        height = texture_surface.get_height()
        new_size = (self.r * 2,
                    (self.r * 2 * height) // width)

        texture_surface = pygame.transform.scale(texture_surface, new_size)
        screen.blit(texture_surface, (self.x - self.r,
                                      self.y - self.r / 2 - new_size[1] / 4))

def drawScore():
    '''
    Draws score. Takes score as global variable.
    '''
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 30)
    textSurface = myFont.render('Score: ' + str(score), False, (255, 255, 255))
    screen.blit(textSurface, (0, 10))

def drawEscapeText():
    '''
    Draws text ESC - меню
    '''
    pygame.font.init()
    myFont = pygame.font.SysFont('Comic Sans MS', 30)
    textSurface = myFont.render('ESC - меню', False, (255, 255, 255))
    screen.blit(textSurface, (0, 40))

def saveData(name):
    '''
    Saves data to leaderboard.json
    name - name that will be written in file
    '''
    global score
    data = {}
    try:
        with open('leaderboard.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if name in data:
        print('Вы уверены, что хотите сохранить очки под этим именем? \n')
        if int(data[name]) > score:
            print('Если вы впишете очки под этим именем, то понизите рекорд.\n')
        print('Если Вы уверены, то введите Y. Иначе данные не сохранятся\n')
        print('Сохранить данные?')
        answer = input()
        if answer != 'Y':
            return
        
    data[name] = score
    with open('leaderboard.json', 'w') as f:
        json.dump(data, f)

def menuLoop():
    '''
    Function that will show game menu.
    '''
    def drawMenu():
        '''
        Draws text "Меню"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 40)
        textSurface = myFont.render('Меню', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 180))

    def drawLeaderboardMenu():
        '''
        Draws text "Таблица лидеров"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Таблица лидеров', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 20))
        
    def drawSettingsMenu():
        '''
        Draws text "Настройки"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Настройки', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 60))

    def drawTutorialMenu():
        '''
        Draws text "Обучение"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Обучение', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) + 20))

    def drawQuitMenu():
        '''
        Draws text "Выйти"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Выйти', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) + 60))

    def drawQuitAndSaveMenu():
        '''
        Draws text "Выйти"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Выйти и сохранить', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) + 100))
    def drawContinueMenu():
        '''
        Draws text "Продолжить"
        '''
        pygame.font.init()
        myFont = pygame.font.SysFont('Comic Sans MS', 29)
        textSurface = myFont.render('Продолжить', False, (255, 255, 255))
        width = textSurface.get_width()
        screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                  (Y_BORDER // 2) - 100))

    def processClick(event):
        '''
        Checks whether click position was in one of the menu buttons
        event - event of click
        '''
        x, y = event.pos

        nonlocal menuFinished
        global finished
        global doASave

        isOnXAxis = False
        isOnYAxis = False

        #Processing X position of click
        if  not (x >= (X_BORDER // 2) - (270 // 2) and
            x <= (X_BORDER // 2) + (270 // 2)):
            return

        #Processing Продолжить button
        if (y >= (Y_BORDER // 2) - 100 and
            y <= (Y_BORDER // 2) - 61 ):
            menuFinished = True
            return

        #Processing Настройки button
        if (y >= (Y_BORDER // 2) - 60 and
            y <= (Y_BORDER // 2) - 21):
            settingsLoop()
            return

        #Processing Таблица лидеров button
        if (y >= (Y_BORDER // 2) - 20 and
            y <= (Y_BORDER // 2) + 19):
            leaderboardLoop()
            return

        #Processing Обучение button
        if (y >= (Y_BORDER // 2) + 20 and
            y <= (Y_BORDER // 2) + 59):
            tutorialLoop()
            return

        #Processing Выход button
        if (y >= (Y_BORDER // 2) + 60 and
            y <= (Y_BORDER // 2) + 99):
            finished = True
            menuFinished = True
            return

        #Processing Выйти и сохранить
        if (y >= (Y_BORDER // 2) + 100 and
            y <= (Y_BORDER // 2) + 139):
            finished = True
            menuFinished = True
            doASave = True
            return
            
        

    global FPS
    global clock
    global finished
    global screen
    
    menuFinished = False

    #Menu Loop
    while (not menuFinished) and (not finished):
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                processClick(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished == True
                    return

        #Drawing menu elements
        drawMenu()

        drawContinueMenu()
        drawSettingsMenu()
        drawLeaderboardMenu()
        drawTutorialMenu()
        drawQuitMenu()
        drawQuitAndSaveMenu()

        pygame.display.update()

        screen.fill((0, 0, 0))
        drawBackground()

def settingsLoop():
    '''
    Settings menu
    '''

    def drawSettings():
        '''
        Draw text
        '''
        global hitboxEnabled
        def drawHitboxOption():
            '''
            Draws text for hitbox option in settings menu
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 29)
            textSurface = myFont.render('Рисовать хитбоксы', False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2) - 200,
                                      (Y_BORDER // 2) - 100))

        def drawHitboxValue():
            '''
            Draws value of hitboxEnabled in settings menu
            '''
            global hitboxEnabled
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 29)
            textSurface = myFont.render(str(hitboxEnabled), False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2) + 200,
                                      (Y_BORDER // 2) - 100))

        #Calling functions to draw text
        drawHitboxOption()
        drawHitboxValue()

    def processClick(event):
        '''
        Checkes whether click was on value of hitboxEnabled
        event - event of click
        '''
        global hitboxEnabled
        
        x, y = event.pos

        isOnXAxis = False
        isOnYAxis = False

        if not (x >= (X_BORDER // 2) - (71 // 2) + 200 and
                x <= (X_BORDER // 2) + (71 // 2) + 200):
            return

        if (y >= ((Y_BORDER // 2) - 100) and
            y <= (Y_BORDER // 2) - 61):
            hitboxEnabled = not hitboxEnabled    
        
    global FPS
    global clock
    global finished
    global screen
    
    settingsFinished = False

    #Settings Loop
    while not settingsFinished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                processClick(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settingsFinished == True
                    return
                
        #Draw settings text
        drawSettings()
        
        pygame.display.update()

        screen.fill((0, 0, 0))
    
def tutorialLoop():
    '''
    Starts the tutorial menu.
    '''
    def drawTutorial():
        '''
        Draws all the text of tutorial
        '''
        def drawTextTutorial():
            '''
            Draws Обучение
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 40)
            textSurface = myFont.render('Обучение', False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                      (Y_BORDER // 2) - 180))

        
        def drawText(text, height):
            '''
            Draws given text at the given height relative to
            y = (Y_BORDER // 2) - 120
            text - given text;
            height - given height.
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 29)
            textSurface = myFont.render(text, False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - 400,
                                      (Y_BORDER // 2) - 120 + height))

        drawTextTutorial()
        
        textArray = ['Цель игры:',
                     '  Спасите Сон Ки Хунов от нападающих на на них кальмаров!',
                     ' Нажимайте на них и получайте очки (+1 за Сон Ки Хуна,',
                     ' +3 за кальмара)',
                     'Управление:',
                     '  ESC - выйти в меню.']

        for i in range(len(textArray)):
            drawText(textArray[i], i * 40)

        
        
        
    global FPS
    global clock
    global finished
    global screen
    
    tutorialFinished = False

    #Tutorial Loop
    while not tutorialFinished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tutorialFinished == True
                    return
                
        #Draw settings text
        drawTutorial()
        
        pygame.display.update()

        screen.fill((0, 0, 0))
    
def leaderboardLoop():
    '''
    Leaderboard menu
    '''
    def drawLeaderboard():
        '''
        Draw text for leaderboard
        '''

        def drawTextLeaderboard():
            '''
            Draws Таблица лидеров
            '''
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 40)
            textSurface = myFont.render('Таблица лидеров', False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2),
                                      (Y_BORDER // 2) - 180))

        def drawName(number, name, height):
            '''
            Draws given name and number in leaderboard at the left part
            of the screen at the given height relative to
            y = (Y_BORDER // 2) - 120.
            text - given text;
            height - given height.
            '''
            text = str(number) + '. ' + str(name)
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 29)
            textSurface = myFont.render(text, False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - 500,
                                      (Y_BORDER // 2) - 120 + height))
            
        def drawScore(score, height):
            '''
            Draws given score in leaderboard at the right part
            of the screen at the given height relative to
            y = (Y_BORDER // 2) - 120.
            text - given text;
            height - given height.
            '''
            text = str(score) + ' pts.'
            pygame.font.init()
            myFont = pygame.font.SysFont('Comic Sans MS', 29)
            textSurface = myFont.render(text, False, (255, 255, 255))
            width = textSurface.get_width()
            screen.blit(textSurface, ((X_BORDER // 2) - (width // 2) + 400,
                                      (Y_BORDER // 2) - 120 + height))
        
        nonlocal data

        drawTextLeaderboard()

        number = 1
        
        for w in sorted(data, key=data.get, reverse=True):
            drawName(number, w, number * 40)
            drawScore(data[w], number * 40)
            number +=1
            if number > 10:
                break
        
    
    try:
        with open('leaderboard.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}


    leaderboardFinished = False
    
    #Leaderboard loop
    while not leaderboardFinished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leaderboardFinished == True
                    return
                
        #Draw leaderboard text
        drawLeaderboard()
        
        pygame.display.update()

        screen.fill((0, 0, 0))

def drawBackground():
    '''
    Draws menu background. Used resources/background.png
    '''
    global screen
    
    background_path = os.path.join('resources', 'background.png')
    background_surface = pygame.image.load(background_path)
    screen.blit(background_surface, (0,0))

#Setting up a screen
FPS = 30
X_BORDER = 1200
Y_BORDER = 900
screen = pygame.display.set_mode((X_BORDER, Y_BORDER))

#Setting up a path to game directory
dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
resources_path = dir_path + '/resources'
print(resources_path)

#Setting up a pygame mainloop
pygame.display.update()
clock = pygame.time.Clock()
finished = False

#Settings
hitboxEnabled = False #Determines whether game should draw hitboxes
N = 5 #Number of balls

#Set some important variables:
score = 0
doASave = False

#Arrays for balls, targeters and clicked balls.
ballObjects = [0] * N
for i in range(N):
    ballObjects[i] = Ball()
    ballObjects[i].draw()

targeterObjects = [0] * N
for i in range(N):
    targeterObjects[i] = Targeter(ballObjects[i])
    targeterObjects[i].draw(ballObjects[i])

clickedObjects = []

destroyedObjects = []

#Main loop
while not finished:
    clock.tick(FPS)
    succesfullyClicked = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not succesfullyClicked:
            #Checks if event is mouse click and if there was no succesful
            #click already in this frame.
            #Then checks if this click is succesful (if there was click on a
            #ball or on a tageter).
            #If yes:
            #-Updates score (+1 for ball, +3 for targeter);
            #-Creates new ball;
            #-Marks this frame as the one with succesful click;
            #-Breaks cycle
            #-Creates "clicked ball" (object of ClickedBall class).
            for i in range(len(ballObjects)):
                if ballObjects[i].processClick(event):
                    clickedObjects.append(ClickedBall(ballObjects[i], FPS))
                    score += 1
                    succesfullyClicked = True
                    ballObjects[i] = Ball()
                    break
                if targeterObjects[i].processClick(event):
                    clickedObjects.append(ClickedBall(ballObjects[i], FPS))
                    score += 3
                    succesfullyClicked = True
                    ballObjects[i] = Ball()
                    break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menuLoop()
    #Moves and draws balls
    for i in ballObjects:
        i.move()
        i.stayOnScreen()
        i.draw()

    #Draws Destroyed Balls
    for i in destroyedObjects:
        i.draw()
        if not i.isAlive():
            destroyedObjects.remove(i)

    #Moves and draws targeters; destroys ball and targeter and creates
    #destroyed ball object if targeter is in radius of a connected ball
    for i in range(N):
        targeterObjects[i].move()
        targeterObjects[i].draw(ballObjects[i])

        if targeterObjects[i].readyForDestruction(ballObjects[i]):
            destroyedObjects.append(DestroyedBall(ballObjects[i], FPS))
            ballObjects[i] = Ball()
            targeterObjects[i] = Targeter(ballObjects[i])
        

    #Draws Clicked Balls
    for i in clickedObjects:
        i.draw()
        if not i.isAlive():
            clickedObjects.remove(i)

    #Draws score
    drawScore()
    drawEscapeText()

    
    pygame.display.update()

    screen.fill((0, 0, 0))
    drawBackground()

pygame.quit()

#Saving data
if doASave:
    saveData(input('Введите имя\n'))
