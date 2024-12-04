import pygame, sys, random
pygame.init()

canClick = True
gameEnded = False

playerHP = 5;

silkClock = pygame.time.Clock()
startWorms = pygame.time.get_ticks() / 1000


def displayCountdown(worms, maxTime, gameClass):
    global canClick
    global gameEnded

    if worms > 0:
        currTime = maxTime - pygame.time.get_ticks() / 1000
        if currTime < 0:
            currTime = 0;
            canClick = False
            lose_surf = font1.render('YOU LOSE!', False, 'dark red')
            lose_rect = lose_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            gameClass.window.blit(lose_surf, lose_rect)
            lose2_surf = font1.render('One more burned hand and broken wrist', False, 'dark red')
            lose2_rect = lose_surf.get_rect(center=(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 75))
            gameClass.window.blit(lose2_surf, lose2_rect)
        else:
            time_surf = font1.render('Time Remaining: %0.2f' % currTime, False, 'red')
            time_rect = time_surf.get_rect(topleft=(SCREEN_WIDTH / 20, 25))
            gameClass.window.blit(time_surf, time_rect)

    else:
        endWorms = pygame.time.get_ticks() / 1000;
        newDay = font1.render('You made it big! Well done... Day 1/???', True, 'green')
        newDay_rect = newDay.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT/2))
        gameClass.window.blit(newDay, newDay_rect)


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SEA_BLUE = (62, 155, 247)

start = 6000

font1 = pygame.font.SysFont('helvetica', 30)


class Collectible(object):
    def __init__(self, value):
        self.value = value
# End Collectible Initialization
    def getValue(self):
        return self.value
# End Collectible class
class SilkWorm (Collectible):
    def __init__(self, x, y):
        Collectible.__init__(self, 30)
        self.wormX = x
        self.wormY = y
        self.clicked = False
        self.wormDim = (self.wormX, self.wormY, 45, 23)

        self.numSpots = random.randint(1, 4)
        self.spotLocX = random.randint(self.wormX, self.wormX+45)
        self.spotLocY = random.randint(self.wormY, self.wormY+23)

        # print('This SilkWorm will have %d spots, which are @ (%d, %d).' % (self.numSpots, self.spotLocX, self.spotLocY))
    # END Silk Worm Initialization
    def draw(self, playerClass, gameClass):
        self.worm = pygame.draw.ellipse(gameClass.window, 'light gray', self.wormDim, 0) # Make into Ellipse Later
        self.wormDot = pygame.draw.circle(gameClass.window, 'black', (self.spotLocX, self.spotLocY), 2.5)

        # Mouse Position and Clicking
        pos = pygame.mouse.get_pos()
        if self.worm.collidepoint(pos) and canClick:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                # print("Clicked")
                playerClass.score += self.value
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    # END Draw Method for SilkWorm
# End Silk Worm class
class Player(object):
    def __init__(self):
        self.score = 0
    # End Player Initialization
# End Player class
class Game(object):
    def __init__(self):
        self.playerHP = 5;
        self.gamePlay = True;
        ## Set up the screen and make the game world
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Silkworm Micro-Game')

    def playSilk(self):
        pass;

    def loseHP(self, loss):
        self.playerHP -= loss;

    def toggleGame(self):
        if self.gamePlay:
            self.gamePlay = False;
        else:
            self.gamePlay = True;

# END GAME

silkCoords = []
silkWormArray = []

## Generate List of Silkworms in the game
wormTotal = random.randint(1, 8)
for i in range(wormTotal):
    silkCoords.append((random.randint(162, 338), random.randint(162, 338)))
    # print("\tHow Many Silk Worms Appended %i: (%d, %d)" % (i, silkCoords[i][0], silkCoords[i][1]))
    silkWormArray.append(SilkWorm(silkCoords[i][0], silkCoords[i][1]))

secret = Player()

def redrawGameWindow(gameClass):
    global gameEnded

    gameClass.window.fill('white')
    basin = pygame.draw.circle(gameClass.window, 'dark gray', (250, 250), 150)
    water = pygame.draw.circle(gameClass.window, SEA_BLUE, (250, 250), 125)
    text = font1.render('Score: %d' % secret.score, 1, (0, 0, 0))
    gameClass.window.blit(text, (350, 25))
    displayCountdown(len(silkWormArray), wormTotal*1.5, gameClass)

    health_surface = font1.render('Health: %d' % playerHP, 1, 'blue')
    health_rect = health_surface.get_rect(center=(50, 450));
    gameClass.window.blit(health_surface, health_rect)

    for worm in range(len(silkWormArray)):
        silkWormArray[worm].draw(secret, gameClass)
    # End FOR Loop
    if len(silkWormArray) == 0:
        gameEnded = True
    pygame.display.update()
# End Function

def main():
    game = Game();
    gameRun = True

    while gameRun:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRun = False
                pygame.quit()
                sys.exit()
        # End FOR

        for worms in silkWormArray:
            if worms.clicked:
                silkWormArray.pop(silkWormArray.index(worms))

        redrawGameWindow(game)
    silkClock.tick(120)
    # End Game Loop

main()