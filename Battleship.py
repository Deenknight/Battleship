# pygame template - skeleton for new games
#everything is based on the dimensions of the screen so it may be ugly to read.

import pygame, sys
import random
import os
from pygame import draw

class Ship(pygame.sprite.Sprite): #Object for all the ships
    def __init__(self,length,up,xPos,yPos):
        self.up = up #if the ship is facing upwards then True
        self.length = length
        pygame.sprite.Sprite.__init__(self)

        #This part just makes the actual image of the ship
        if self.up:
            self.image = pygame.Surface((WIDTH/(3*lengthX),self.length*(HEIGHT/(2*lengthY))-HEIGHT/50)) 
        else:
            self.image = pygame.Surface((self.length*(WIDTH/(2*lengthX))-WIDTH/50, HEIGHT/(3*lengthY)))
        self.image.fill((105,105,105))
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
        #Starting position is saved for when you reset
        self.startX = xPos
        self.startY = yPos
        #This is needed to change the ship's position data
        self.oldX = -1
        self.oldY = -1
        self.oldUp = True
        
        self.hits = 0
        self.sunk = False
        
    def update(self):
        if self.up:
            self.image = pygame.Surface((WIDTH/(3*lengthX),self.length*(HEIGHT/(2*lengthY))-HEIGHT/50))
        else:
            self.image = pygame.Surface((self.length*(WIDTH/(2*lengthX))-WIDTH/50, HEIGHT/(3*lengthY)))
        xPos = self.rect.x
        yPos = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos
        self.image.fill((105,105,105))
        
        self.shipInfo = []
        #This part just updates the ship's position data
        if self.oldX > -1:
            for i in range(self.length):
                if self.up:
                    for j in range(self.length):
                        index = (self.oldY+j)*lengthX+self.oldX
                        self.shipInfo.append(index)
                else:
                    for j in range(self.length):
                        index = (self.oldY)*lengthX+self.oldX+j
                        
                        self.shipInfo.append(index)
        
    def reset(self): #resets the position of the ship
        self.rect.x = self.startX
        self.rect.y = self.startY
        self.up = True
        self.oldX = -1
        self.oldY = -1
    

class Computer(): #this is the AI
    def __init__(self,ships):
        self.square = [] #This is the info of the ships
        for i in range(lengthX*lengthY):
            self.square.append(False)
        self.shipInfo = []
        self.shipLength = []
        
        
        
        for i in range(len(ships)): #This part "places" the computer ships
            
            helpfulList = []
            self.shipLength.append(ships[i])
            #If the ship is facing up or sideways. 1 is upwards, and 2 is sideways.
            direction = random.randint(1,2)
            again = True
            if direction == 1:
                limit = (lengthX*lengthY)-(lengthY*self.shipLength[i]) #This stops the ship from going off screen
                location = random.randint(1,limit)
                while again: #This part tests whether the 
                    again = False
                    location = random.randint(1,limit)
                    for j in range(self.shipLength[i]):
                        index = location+j*lengthX
                        if self.square[index]:
                            
                            again = True
                for j in range(self.shipLength[i]):
                    index = location+j*lengthX
                    
                        
                    self.square[index] = True
                    helpfulList.append(index)
                
            else:
                limit = lengthX*lengthY-self.shipLength[i]
                location = random.randint(1,limit)
                while again:
                    again = False
                    location = random.randint(1,limit)
                    for j in range(self.shipLength[i]):
                        index = location+j
                        if self.square[index]:
                            again = True
                    for j in range(self.shipLength[i]):
                        index = location+j
                        
                        if int(location / lengthX) != int(index/lengthX):
                            again = True
                for j in range(self.shipLength[i]):
                    index = location+j
                    self.square[index] = True
                    helpfulList.append(index)
            self.shipInfo.append(helpfulList)
            # print(i,self.shipInfo[i])
        self.guessed = []
        self.directGuessed = []
        self.shipHits = [0 for i in range(len(ships))]
        self.idea = 0
        self.lastHit = -1
        self.backupGuess = 0
    def guessIt(self):
        # print(computerMarker,self.idea)
        
                
        if self.idea == 1:
            
            while True:
                self.direct = self.resetIdea()
                if self.direct == 1:
                    if self.mainGuess-lengthX < 0 or self.mainGuess-lengthX in self.guessed:
                        self.resetIdea()
                    else:
                        self.guess = self.mainGuess-lengthX
                        break
                if self.direct == 2:
                    if self.mainGuess%lengthX == 0 or self.mainGuess-1 in self.guessed:
                        self.resetIdea()
                    else:
                        self.guess = self.mainGuess-1
                        break
                if self.direct == 3:
                    if self.mainGuess+lengthX > len(self.square) or self.mainGuess+lengthX in self.guessed:
                        self.resetIdea()
                    else:
                        self.guess = self.mainGuess+lengthX
                        break
                else:
                    if self.mainGuess+1%lengthX == 0 or self.mainGuess+1 in self.guessed:
                        self.resetIdea()
                    else:
                        self.guess = self.mainGuess+1
                        break
            
            return self.guess
            if self.check(False, self.guess):
                self.idea += 1
                self.mainGuess = self.guess    
                

            
        elif self.idea >= 2:
            if self.direct == 1:
                
                    self.guess = self.mainGuess-lengthX
                    
            elif self.direct == 2:
                
                    self.guess = self.mainGuess-1
                    
            elif self.direct == 3:
                    self.guess = self.mainGuess+lengthX
                    
            elif self.direct == 4:
                
                    self.guess = self.mainGuess+1

                

            return self.guess
            
            
        else:
            while True:
                self.guess = random.randint(0,len(self.square)-1)
                if not self.guess in self.guessed:
                    self.guessed.append(self.guess)
                    
                    
                    self.mainGuess = self.guess
                    self.backupGuess = self.guess
                    return self.guess
                    break
    def resetIdea(self):
        while True:
            direct = random.randint(1,4)
            if not direct in self.directGuessed:
                self.directGuessed.append(direct)
                return direct
                break
    def check(self,CompChoosing,guessed):
        if CompChoosing:
            return square[guessed]
            # print('square[guessed] = ',square[guessed])
                
        else:
            return self.square[guessed]
    


class Marker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(markerWhite, ((int((WIDTH/(3*lengthX))), int((HEIGHT/(3*lengthY)))))) #scale image
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        
        self.rect.x = WIDTH/3-WIDTH/6
        self.rect.y = HEIGHT/2
        self.mode = 1
    def align(self):
        squareX = -1
        squareY = -1
        if self.rect.x > WIDTH/4 and self.rect.x < WIDTH/4*3:
            for i in range(lengthX):
                if self.rect.x  > WIDTH/4+i*(WIDTH/(2*lengthX)): 
                        squareX = i
        if self.rect.y > HEIGHT/4 and self.rect.y < HEIGHT/4*3:
            for i in range(lengthY):
                if self.rect.y  > HEIGHT/4+i*(HEIGHT/(2*lengthY)):
                        squareY = i
        if squareX != -1 and squareY != -1:      
            self.rect.x = WIDTH/4+squareX*(WIDTH/(2*lengthX))+ WIDTH/(10*lengthX)#WIDTH/100
            self.rect.y = HEIGHT/4+squareY*(HEIGHT/(2*lengthY))+ HEIGHT/(10*lengthY)#HEIGHT/100
            self.index = (squareY)*lengthX+squareX
        else:
            self.rect.x = WIDTH/3-WIDTH/6
            self.rect.y = HEIGHT/2
            self.index = -1
    def update(self):
        if self.mode == 1:
                self.image = pygame.transform.scale(markerWhite, ((int(WIDTH/(3*lengthX)), int((HEIGHT/(3*lengthY))))))
                self.image.set_colorkey(BLACK)
        elif self.mode == 2:
                self.image = pygame.transform.scale(markerRed, ((int(WIDTH/(3*lengthX)), int((HEIGHT/(3*lengthY))))))
                self.image.set_colorkey(BLACK)

    

def grid(x,y):
    if square == []:
        for i in range(x*y):
            square.append(False)
        
    draw.rect(screen,(128,128,128),(WIDTH/4,HEIGHT/4,WIDTH/2,HEIGHT/2))
    for i in range(1,x):
        draw.line(screen, WHITE, (WIDTH/4+i*(WIDTH/(2*x)),HEIGHT/4), (WIDTH/4+i*(WIDTH/(2*x)),HEIGHT/4*3))
    for i in range(1,y):
        draw.line(screen, WHITE, (WIDTH/4,HEIGHT/4+i*(HEIGHT/(2*y))), (WIDTH/4*3,HEIGHT/4+i*(HEIGHT/(2*y))))




    

def align(num):
    squareX = -1
    squareY = -1
    if ship[num].rect.x > WIDTH/4 and ship[num].rect.x < WIDTH/4*3:
        for i in range(lengthX):
            if ship[num].rect.x > WIDTH/4+i*(WIDTH/(2*lengthX)):
                squareX = i
    if ship[num].rect.y > HEIGHT/4 and ship[num].rect.y < HEIGHT/4*3:
        for i in range(lengthY):
            if ship[num].rect.y > HEIGHT/4+i*(HEIGHT/(2*lengthY)):
                squareY = i

    
    if ship[num].oldX != -1:
            if ship[num].oldUp:
                for i in range(ship[num].length):
                    index = (ship[num].oldY+i)*lengthX+ship[num].oldX
                    square[index] = False
            else:
                for i in range(ship[num].length):
                    index = (ship[num].oldY)*lengthX+ship[num].oldX+i
                    square[index] = False
    if squareX != -1 and squareY != -1:
        
        if ship[num].up:
            ship[num].rect.x = WIDTH/4+squareX*(WIDTH/(2*lengthX)) + WIDTH/(12*lengthX) #(WIDTH/(6*lengthX))
            ship[num].rect.y = HEIGHT/4+squareY*(HEIGHT/(2*lengthY)) + (ship[num].length*(HEIGHT/(2*lengthY))-HEIGHT/50)/20
            
            ship[num].oldX = squareX
            ship[num].oldY = squareY
            ship[num].oldUp = ship[num].up 
            for i in range(ship[num].length):
                index = (squareY+i)*lengthX+squareX
                if index > len(square):
                    for j in range(i+1):
                        
                        index = (squareY+j-1)*lengthX+squareX
                        square[index] = False
                    ship[num].reset()
                    break
               
                
                else:
                    square[index] = True
                
            
             
        elif not ship[num].up:
            ship[num].rect.x = WIDTH/4+squareX*(WIDTH/(2*lengthX)) + (ship[num].length*(WIDTH/(2*lengthX))-WIDTH/50)/20
            ship[num].rect.y = HEIGHT/4+squareY*(HEIGHT/(2*lengthY)) + HEIGHT/(12*lengthY)

            ship[num].oldX = squareX
            ship[num].oldY = squareY
            ship[num].oldUp = ship[num].up
            for i in range(ship[num].length):
                index = (squareY)*lengthX+squareX+i
                if index > len(square):
                    for j in range(i+1):
                        index = (squareY)*lengthX+squareX+j-1
                        square[index] = False
                    ship[num].reset()
                    
                
                elif index-squareY*lengthX >= lengthX:
                    for j in range(i+1):
                        index = (squareY)*lengthX+squareX+j
                        square[index] = False
                    ship[num].reset()
                    
                else:
                    square[index] = True
                
    
    else:
        ship[num].reset()


  
def check(player_choosing,guessed):
    if not player_choosing:
        return square[guessed]
        # print('square[guessed] = ',square[guessed])
            
    else:
        return computer.square[guessed]  


# initialization
FPS = 60
img_dir = os.path.join(os.getcwd(), 'img') #add the file path for our images
#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()

# set game window specifications
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
settings = pygame.display.Info()
WIDTH = settings.current_w
HEIGHT = settings.current_h
pygame.display.set_caption("Battleship")
clock = pygame.time.Clock()

# load the marker images
markerRed = pygame.image.load(os.path.join(img_dir, 'markerRed.png')).convert()
markerWhite = pygame.image.load(os.path.join(img_dir, "markerWhite.png")).convert()
# initialize the marker objects
player_markers = pygame.sprite.Group()
computer_markers = pygame.sprite.Group()
current_markers = pygame.sprite.Group()
marker = []
compmarker = []
currentMarker = -1
computerMarker = -1


lengthX = 10
lengthY = 10

# create ship objects
all_ships = pygame.sprite.Group()
ship = []
ship.append(Ship(2,True,WIDTH/3-WIDTH/5,HEIGHT/3))
ship.append(Ship(3,True,WIDTH/3-WIDTH/7,HEIGHT/3))
ship.append(Ship(3,True,WIDTH/3-WIDTH/6,HEIGHT/3+HEIGHT/3))
ship.append(Ship(4,True,WIDTH/3-WIDTH/7,HEIGHT/3+HEIGHT/7))
ship.append(Ship(5,True,WIDTH/3-WIDTH/5,HEIGHT/3+HEIGHT/10))
numberOfShips = 5

compShip = []
computer = Computer([2,3,3,4,5])
compShip.append(Ship(2,True,WIDTH/3-WIDTH/5,HEIGHT/3))
compShip.append(Ship(3,True,WIDTH/3-WIDTH/7,HEIGHT/3))
compShip.append(Ship(3,True,WIDTH/3-WIDTH/6,HEIGHT/3+HEIGHT/3))
compShip.append(Ship(4,True,WIDTH/3-WIDTH/7,HEIGHT/3+HEIGHT/7))
compShip.append(Ship(5,True,WIDTH/3-WIDTH/5,HEIGHT/3+HEIGHT/10))
all_computer = pygame.sprite.Group()

for i in range(numberOfShips):
    all_ships.add(ship[i])
    
    
    helpingY = int(computer.shipInfo[i][0]/lengthX)
    helpingX = computer.shipInfo[i][0] - lengthX*helpingY
    if computer.shipInfo[i][0]+1 == computer.shipInfo[i][1]:
        compShip[i].up = False
        
        compShip[i].rect.x = WIDTH/4+helpingX*(WIDTH/(2*lengthX)) + (compShip[i].length*(WIDTH/(2*lengthX))-WIDTH/50)/20
        compShip[i].rect.y = HEIGHT/4+helpingY*(HEIGHT/(2*lengthY)) + HEIGHT/(12*lengthY)
        # print(i,'side')
    else:
        compShip[i].up = True
        compShip[i].rect.x = WIDTH/4+helpingX*(WIDTH/(2*lengthX)) + WIDTH/(12*lengthX)
        compShip[i].rect.y = HEIGHT/4+helpingY*(HEIGHT/(2*lengthY)) + (compShip[i].length*(HEIGHT/(2*lengthY))-HEIGHT/50)/20
        # print(i,'up')



background = pygame.image.load(os.path.join(img_dir, "Battleship.jpg")).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/15790.08))
text = [0 for i in range(20)]
text[0] = font.render("Play", True, BLACK)
text[1] = font.render("ALLIES", True, BLUE)
text[2] = font.render("AXIS", True, RED)
text[3] = font.render("Exit Game", True, BLACK)
text[4] = font.render("Back", True, BLACK)
text[5] = font.render("Next", True, YELLOW)
text[6] = font.render("Fire!", True, YELLOW)
text[7] = font.render("Miss", True, WHITE)
text[8] = font.render("Hit!", True, YELLOW)
text[9] = font.render("Sunk!", True, RED)
font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/4000))
text[12] = font.render("BATTLESHIP", True, BLUE)
mode = 0
minimode = 0
num = 0
moving_piece = False
square = []
shipNumber = 0
counter = 0

#Game Loop
running = True



while running:
    while mode == 0:
        font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/15790.08))
        clock.tick(FPS)
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        draw.rect(screen,(128,0,0),(WIDTH/2-WIDTH/10,HEIGHT/3+HEIGHT/25,WIDTH/4,HEIGHT/5))

        PLAY_BUTTON_X = WIDTH/2-WIDTH/30
        PLAY_BUTTON_Y = HEIGHT/3+HEIGHT/20

        EXIT_BUTTON_X = WIDTH/3+WIDTH/11
        EXIT_BUTTON_Y = HEIGHT/2

        TITLE_X = WIDTH/30
        TITLE_Y = HEIGHT/8
            
        screen.blit(text[0],(PLAY_BUTTON_X, PLAY_BUTTON_Y))
        screen.blit(text[3],(EXIT_BUTTON_X, EXIT_BUTTON_Y))
        screen.blit(text[12],(TITLE_X,TITLE_Y))
        for event in pygame.event.get():
            mouseButton = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if mouseButton[0] == 1:
                mouse_pos = pygame.mouse.get_pos()
                print(WIDTH/mouse_pos[0],HEIGHT/mouse_pos[1])
            
                if text[3].get_rect(topleft=(EXIT_BUTTON_X, EXIT_BUTTON_Y)).collidepoint(mouse_pos):
                    
                    pygame.quit()
                    sys.exit()
                elif text[0].get_rect(topleft=(PLAY_BUTTON_X, PLAY_BUTTON_Y)).collidepoint(mouse_pos):
                    
                    mode = 1
                 
        pygame.display.flip()
    while mode == 1:
        clock.tick(FPS)
        screen.fill((51,153,255))

        NEXT_BUTTON_X = WIDTH-WIDTH/5
        NEXT_BUTTON_Y = HEIGHT/4*3

        for event in pygame.event.get():

            mouseButton = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if mouseButton[2] == 1 and moving_piece:
                #print(num)
                if ship[num].up:

                    ship[num].up = False
                elif not ship[num].up:
                    ship[num].up = True
            if moving_piece:
                if ship[num].up:
                    ship[num].rect.x = mouse_pos[0] - WIDTH/(6*lengthX)
                    ship[num].rect.y = mouse_pos[1] - ship[num].length*(HEIGHT/(4*lengthY))+HEIGHT/50
                else:
                    ship[num].rect.x = mouse_pos[0] - ship[num].length*(WIDTH/(4*lengthX))+WIDTH/50
                    ship[num].rect.y = mouse_pos[1] - HEIGHT/(6*lengthY)
            if mouseButton[0] == 0 and moving_piece:
                    moving_piece = False
                    align(num)
                    for i in range(numberOfShips):
                        if i == num:
                            continue
                        elif pygame.sprite.collide_rect(ship[num],ship[i]):
                            #print('ok')
                            ship[num].reset()
                    
                    #print(mouse_pos[0],mouse_pos[1])
            if mouseButton[0] == 1 and not moving_piece:
                for i in range(numberOfShips):
                    if ship[i].rect.collidepoint(mouse_pos):
                        moving_piece = True
                        num = i

                if text[5].get_rect(topleft=(NEXT_BUTTON_X, NEXT_BUTTON_Y)).collidepoint(mouse_pos):
                    if thisCounter == numberOfShips:
                        mode = 2
                        fired = 0
                            
            
                
        

        grid(lengthX,lengthY)
        all_ships.update()
        thisCounter = 0
        for i in range(numberOfShips):
            if ship[i].rect.x>WIDTH/4:
                thisCounter +=1
        if thisCounter == numberOfShips:
            screen.blit(text[5],(NEXT_BUTTON_X,NEXT_BUTTON_Y))
        all_ships.draw(screen)
        pygame.display.flip()

    while mode == 2:
        clock.tick(FPS)
        screen.fill((51,153,255))
        grid(lengthX,lengthY)
        counter += 1
        text[6] = font.render("Fire!", True, YELLOW)

        FIRE_BUTTON_X = WIDTH-WIDTH/5
        FIRE_BUTTON_Y = HEIGHT/4

        if counter == 1:
            marker.append(Marker())
            currentMarker += 1
            if currentMarker > 0:
                player_markers.add(marker[currentMarker-1])
            current_markers.add(marker[currentMarker])
            fireClicked = False
            marker[currentMarker].index = -1
			
        mouse_pos = pygame.mouse.get_pos()
		
        for event in pygame.event.get():
            mouseButton = pygame.mouse.get_pressed()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if moving_piece: 
                            
                marker[currentMarker].rect.x = mouse_pos[0] - (WIDTH/(2*lengthX)-WIDTH/50)/2
                marker[currentMarker].rect.y = mouse_pos[1] - (HEIGHT/(2*lengthY)-HEIGHT/50)/2
            if mouseButton[0] == 0 and moving_piece:
                moving_piece = False
                
                
                marker[currentMarker].align()
                
                hits = pygame.sprite.spritecollide(marker[currentMarker],player_markers,False)
                if hits:
                    # print('collided bish')
                    current_markers.remove(marker[currentMarker])
                    marker.remove(marker[currentMarker])
                    marker.append(Marker())
                    
                    current_markers.add(marker[currentMarker])
                    marker[currentMarker].index = -1
                
                    
                                
                    mouse_pos = pygame.mouse.get_pos()
                    # print(mouse_pos[0],mouse_pos[1])
            if mouseButton[0] == 1 and not moving_piece:
                if not fireClicked and marker[currentMarker].rect.collidepoint(mouse_pos):
                    moving_piece = True
                elif marker[currentMarker].index != -1 and text[6].get_rect(topleft=(FIRE_BUTTON_X, FIRE_BUTTON_Y)).collidepoint(mouse_pos):
                    if not fireClicked:
                        winCheck = 0
                        
                        fireClicked = True
                        
                        if check(True, marker[currentMarker].index):
                            fired = 1
                            
                            marker[currentMarker].mode = 2
                            for i in range(5):
                                if marker[currentMarker].index in computer.shipInfo[i]:
                                    computer.shipHits[i] += 1
                                    if computer.shipHits[i] >= len(computer.shipInfo[i]):
                                        compShip[i].sunk = True
                                        fired = 2
                                         
                                        all_computer.add(compShip[i])
                                        
                                if compShip[i].sunk:
                                    winCheck += 1
                                    if winCheck >= numberOfShips:
                                        mode = 4
                elif fireClicked and text[5].get_rect(topleft=(NEXT_BUTTON_X, NEXT_BUTTON_Y)).collidepoint(mouse_pos):
                    mode = 3
                    current_markers.remove(marker[currentMarker])
                    counter = 0
                    fired = 0



        if marker[currentMarker].index != -1 and not fireClicked and text[6].get_rect(topleft=(FIRE_BUTTON_X, FIRE_BUTTON_Y)).collidepoint(mouse_pos):
            text[6] = font.render("Fire!", True, RED)

        

        marker[currentMarker].update()

        
        text[7] = font.render("Miss", True, WHITE)
        text[8] = font.render("Hit!", True, YELLOW)
        text[9] = font.render("Sunk!", True, RED)
        if not fireClicked:
            screen.blit(text[6],(FIRE_BUTTON_X, FIRE_BUTTON_Y))
        else:
            screen.blit(text[5],(NEXT_BUTTON_X,NEXT_BUTTON_Y))

            if fired == 0:
                screen.blit(text[7],(WIDTH/2,HEIGHT/6))
            elif fired == 1:
                screen.blit(text[8],(WIDTH/2,HEIGHT/6))
            else:
                screen.blit(text[9],(WIDTH/2,HEIGHT/6))
                
        all_computer.update()
        all_computer.draw(screen)
        current_markers.draw(screen)
        player_markers.update()
        player_markers.draw(screen)
        
        pygame.display.flip()
    while mode == 3:
        clock.tick(FPS)
        screen.fill((51,153,255))
        grid(lengthX,lengthY)
        counter += 1
        if counter == 1:
            compmarker.append(Marker())
            computerMarker += 1
            computer_markers.add(compmarker[computerMarker])

            computerGuess = computer.guessIt()

        
            squareY = int(computerGuess / lengthX)
            squareX = computerGuess - squareY*lengthX
            
            compmarker[computerMarker].rect.x = WIDTH/4+squareX*(WIDTH/(2*lengthX))+WIDTH/100
            compmarker[computerMarker].rect.y = HEIGHT/4+squareY*(HEIGHT/(2*lengthY))+HEIGHT/100
            compmarker[computerMarker].index = computerGuess
            
            winCheck = 0
            if check(False, compmarker[computerMarker].index):
                fired = 1
                
                for i in range(numberOfShips):
                    
                    if compmarker[computerMarker].index in ship[i].shipInfo:
                        ship[i].hits += 1
                        
                        if ship[i].hits >= ship[i].length:
                            fired = 2
                            
                            ship[i].sunk = True
                            computer.idea = -1
                            computer.guess = 0
                            computer.mainGuess = 0
                            computer.direct = 0
                            computer.directGuessed = []
                    if ship[i].sunk:
                        
                        winCheck += 1
                        if winCheck >= numberOfShips:
                            mode = 5
            
                compmarker[computerMarker].mode = 2
                computer.idea += 1
                computer.mainGuess = computerGuess
                
            elif computer.idea >= 2:
                computer.direct -= 2
                if computer.direct <= 0:
                    computer.direct+=4
                computer.mainGuess = computer.backupGuess




                
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouseButton = pygame.mouse.get_pressed()
            if mouseButton[0] == 1 and mouse_pos[0] > int(WIDTH/1.24574209) and mouse_pos[0] < int(WIDTH/1.1352549) and mouse_pos[1] > int(HEIGHT/4) and mouse_pos[1] < int(HEIGHT/3.49090909):
                mode = 2
                counter = 0
                fired = 0
                    
                
        text[7] = font.render("Miss", True, WHITE)
        text[8] = font.render("Hit!", True, YELLOW)
        text[9] = font.render("Sunk!", True, RED)
        screen.blit(text[5],(WIDTH-WIDTH/5,HEIGHT/4))

        if fired == 0:
            screen.blit(text[7],(WIDTH/2,HEIGHT/6))
        elif fired == 1:
            screen.blit(text[8],(WIDTH/2,HEIGHT/6))
        else:
            screen.blit(text[9],(WIDTH/2,HEIGHT/6))
        all_ships.draw(screen)
        computer_markers.update()
        computer_markers.draw(screen)
        
        pygame.display.flip()
    while mode == 4:
        clock.tick(FPS)
        screen.fill((41,122,204))
        for i in range(numberOfShips):
            ship[i].image.fill((84,84,84))
            compShip[i].image.fill((84,84,84))
        grid(lengthX,lengthY)
        all_computer.update()
        all_computer.draw(screen)
        player_markers.update()
        player_markers.draw(screen)
        counter += 1
        font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/7895.04))
        text[10] = font.render("VICTORY", True, WHITE)
        font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/15790.08))
        text[11] = font.render("Press anywhere to continue", True, YELLOW)
        screen.blit(text[10],(WIDTH/3,HEIGHT/2))
        if counter >= 180:        
            screen.blit(text[11],(WIDTH/3,HEIGHT/4*3))
            for event in pygame.event.get():
                mouseButton = pygame.mouse.get_pressed()
                if mouseButton[0] == 1:
                    mode = 0
                    counter = 0
                    fired = 0
                    
                    compShip = []
                    computer = Computer([2,3,3,4,5])
                    compShip.append(Ship(2,True,WIDTH/3-WIDTH/5,HEIGHT/3))
                    compShip.append(Ship(3,True,WIDTH/3-WIDTH/7,HEIGHT/3))
                    compShip.append(Ship(3,True,WIDTH/3-WIDTH/6,HEIGHT/3+HEIGHT/3))
                    compShip.append(Ship(4,True,WIDTH/3-WIDTH/7,HEIGHT/3+HEIGHT/7))
                    compShip.append(Ship(5,True,WIDTH/3-WIDTH/5,HEIGHT/3+HEIGHT/10))

                    player_markers = pygame.sprite.Group()
                    computer_markers = pygame.sprite.Group()
                    current_markers = pygame.sprite.Group()
                    marker = []
                    compmarker = []
                    currentMarker = -1
                    computerMarker = -1
                    all_computer = pygame.sprite.Group()
                    for i in range(numberOfShips):
                        all_ships.add(ship[i])
                        
                        
                        helpingY = int(computer.shipInfo[i][0]/lengthX)
                        helpingX = computer.shipInfo[i][0] - lengthX*helpingY

                        if computer.shipInfo[i][0]+1 == computer.shipInfo[i][1]:
                            compShip[i].up = False
                            
                            compShip[i].rect.x = WIDTH/4+helpingX*(WIDTH/(2*lengthX)) + (compShip[i].length*(WIDTH/(2*lengthX))-WIDTH/50)/20
                            compShip[i].rect.y = HEIGHT/4+helpingY*(HEIGHT/(2*lengthY)) + HEIGHT/(12*lengthY)
                            # print(i,'side')
                        else:
                            compShip[i].up = True
                            compShip[i].rect.x = WIDTH/4+helpingX*(WIDTH/(2*lengthX)) + WIDTH/(12*lengthX)
                            compShip[i].rect.y = HEIGHT/4+helpingY*(HEIGHT/(2*lengthY)) + (compShip[i].length*(HEIGHT/(2*lengthY))-HEIGHT/50)/20
                            # print(i,'up')
                            0.
        pygame.display.flip()
    while mode == 5:
        clock.tick(FPS)
        screen.fill((41,122,204))
        
        grid(lengthX,lengthY)
        for i in range(numberOfShips):
            ship[i].image.fill((84,84,84))
            compShip[i].image.fill((84,84,84))
        all_ships.draw(screen)
        computer_markers.update()
        computer_markers.draw(screen)

        counter += 1
        font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/7895.04))
        text[10] = font.render("DEFEAT", True, RED)
        font = pygame.font.SysFont("fixedsys regular", int((WIDTH*HEIGHT)/15790.08))
        text[11] = font.render("Press anywhere to continue", True, YELLOW)
        screen.blit(text[10],(WIDTH/3,HEIGHT/2))
        screen.blit(text[11],(WIDTH/3,HEIGHT/4*3))
        if counter >= 180:        
            screen.blit(text[11],(WIDTH/3,HEIGHT/4*3))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                mouseButton = pygame.mouse.get_pressed()
                if mouseButton[0] == 1:
                    mode = 0
                    counter = 0
                    fired = 0
                    
                    compShip = []
                    ship.append(Ship(2,True,WIDTH/3-WIDTH/5,HEIGHT/3))
                    ship.append(Ship(3,True,WIDTH/3-WIDTH/7,HEIGHT/3))
                    ship.append(Ship(3,True,WIDTH/3-WIDTH/6,HEIGHT/3+HEIGHT/3))
                    ship.append(Ship(4,True,WIDTH/3-WIDTH/7,HEIGHT/3+HEIGHT/7))
                    ship.append(Ship(5,True,WIDTH/3-WIDTH/5,HEIGHT/3+HEIGHT/10))
                    
                    computer = Computer([2,3,3,4,5])
                    compShip.append(Ship(2,True,WIDTH/3-WIDTH/5,HEIGHT/3))
                    compShip.append(Ship(3,True,WIDTH/3-WIDTH/7,HEIGHT/3))
                    compShip.append(Ship(3,True,WIDTH/3-WIDTH/6,HEIGHT/3+HEIGHT/3))
                    compShip.append(Ship(4,True,WIDTH/3-WIDTH/7,HEIGHT/3+HEIGHT/7))
                    compShip.append(Ship(5,True,WIDTH/3-WIDTH/5,HEIGHT/3+HEIGHT/10))

                    player_markers = pygame.sprite.Group()
                    computer_markers = pygame.sprite.Group()
                    current_markers = pygame.sprite.Group()
                    marker = []
                    compmarker = []
                    currentMarker = -1
                    computerMarker = -1
                    all_computer = pygame.sprite.Group()
                    for i in range(numberOfShips):
                        all_ships.add(ship[i])
                        
                        
                        helpingY = int(computer.shipInfo[i][0]/lengthX)
                        helpingX = computer.shipInfo[i][0] - lengthX*helpingY

                        if computer.shipInfo[i][0]+1 == computer.shipInfo[i][1]:
                            compShip[i].up = False
                            
                            compShip[i].rect.x = WIDTH/4+helpingX*(WIDTH/(2*lengthX)) + (compShip[i].length*(WIDTH/(2*lengthX))-WIDTH/50)/20
                            compShip[i].rect.y = HEIGHT/4+helpingY*(HEIGHT/(2*lengthY)) + HEIGHT/(12*lengthY)
                            # print(i,'side')
                        else:
                            compShip[i].up = True
                            compShip[i].rect.x = WIDTH/4+helpingX*(WIDTH/(2*lengthX)) + WIDTH/(12*lengthX)
                            compShip[i].rect.y = HEIGHT/4+helpingY*(HEIGHT/(2*lengthY)) + (compShip[i].length*(HEIGHT/(2*lengthY))-HEIGHT/50)/20
                            # print(i,'up')

        pygame.display.flip()

pygame.quit()
sys.exit()
