import pygame
import sys
import numpy as np

elementSize = 25
snake = [[13,13],[13,14]]   # [13,13] is the head of the snake. [13,14] is the first body part of the snake
appleCoordination = []

green = (0, 255, 0)     # RGB value
lightGreen = (0, 102, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (180, 0, 0)

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('arialblack', 35)
screen = pygame.display.set_mode([700,700]) # 700 is the size of the gamefield

"""
This method generates the textfield on the top of the playground, which shows the score of the game.
"""
def textObject(text, font):
    textArea = font.render(text, True, (255, 255, 255))
    return textArea, textArea.get_rect()


"""
This method draws the the snake and the apples (white boxes) on the playground and fills the background in black color.
"""
def draw():
    screen.fill(black)
    drawApple()
    drawSnake()


"""
This method draws the snake on the playground. The coordination for the head spawn can be interpreted as follows: 
coordinate[0] = x-coordinates for the snake bodypart. coordinate[1] = y-coordinates for the snake bodypart. The 1 at the 
end of the pygame.draw.rect method makes, that the white boxes are only outlined but not filled out.
"""
def drawSnake():
    head = True
    for bodypart in snake:
        coordinate = [bodypart[0] * elementSize, bodypart[1] * elementSize]  # To identify at which point on the screen the head of the snake is. x[0] represents the x coordinate and equals 13 whereas x[1] represents the y coordinate and equals 14
        if head:
            pygame.draw.rect(screen, red, (coordinate[0], coordinate[1], elementSize, elementSize), 0)  # rect is a square. (0,0,0) is the color black. coordinate[0] = x coordinate, coordinate[1] = y coordinate. (left, top, width, height). 0 = square is filled out
            head = False
        else:
            pygame.draw.rect(screen, green, (coordinate[0], coordinate[1], elementSize, elementSize), 1)


"""
This method draws the apples on the playground. The coordination for the apple spawn can be interpreted as follows: 
apple[0] = x-coordinate. apple[1] = y-coordinate. Therefore, the coordination[0] is the first element in the nested 
array and represents the x-coordinate of the apple spawn. The coordination[1] is the second element in the nested array 
and represents the y-coordinate of the apple spawn. The 1 at the end of the pygame.draw.rect method makes, that the 
white boxes are only outlined but not filled out.
"""
def drawApple():
    for apple in appleCoordination:
        coordination = [apple[0] * elementSize, apple[1] * elementSize]
        pygame.draw.rect(screen, white, (coordination[0], coordination[1], elementSize, elementSize), 1)


def mainLoop():
    # Main Loop
    go = True  # The game runs as long as the go variable is True
    snakeAttachment = None
    appleIndex = -1  # ???
    end = False
    score = 0
    direction = 0  # 0 = up, 1 = right, 2 = down, 3 = left

    while go:
        direction = buttonActions(direction)
        snakeMovement()
        snakeDirections(direction)
        end = snakeCollusion(end)
        appleIndex, score, snakeAttachment = bodyIncreasing(appleIndex, score, snakeAttachment)
        snakeAttachment = snakeAttachementProof(appleIndex, snakeAttachment)
        appleFrequency()
        startEndGame(end, score)


"""
This method checks for collision with a wall or the snake itself. If so, the game will be ended with the achieved score 
printed on the console. If not, the playground will be showed.
"""
def startEndGame(end, score):
    if end == False:  # check for collision with a wall or the snake itself
        showPlayground(score)
    else:
        print("You achieved " + str(score) + " points")
        sys.exit()
    clock.tick(0.5)


"""
This method draws the snake, the apples appearing on the playground and the text box that counts the score at the top of
the playground. The pygame.display.update() method will print all the changes of the screen
"""
def showPlayground(score):
    draw()
    #textGround, textBox = textObject("Score: " + str(score), font)
    #textBox.center = ((350, 40))
    #screen.blit(textGround, textBox)
    pygame.display.update()


# This method avoids that an apple can be generated on another apple or on any part of the snake
def appleCoordinateGenerator():
    notOK = True
    while notOK:
        coordinate = [np.random.randint(0, 28), np.random.randint(0, 28)]     # generates random numbers for the x and y coordinate from 0 to 27
        change = False
        for x in snake:
            if coordinate == x:         # If coordinate is not ok, change will be True
                change = True
        for x in appleCoordination:     # to check if the apple is already spawn on a space with an apple
            if coordinate == x:
                change = True
        if change == False:             # If coordinate is ok, the coordinate will be returned
            return coordinate


"""
This method defines the amount and the frequency of the apples that are shown on the playground. There is a minimum of
one apple that has to be on the playground and a maximum of four apples that can be on the playground. 
len(appleCoordination) == 0 means that if there is no apple on the field one has to be spawned!
"""
def appleFrequency():
    random = np.random.randint(0, 100)
    if random <= 1 and len(appleCoordination) < 4 or len(appleCoordination) == 0:
        appleCoordination.append(appleCoordinateGenerator())


"""
This method checks, if the apple coordination is the same as the snake head coordination, then the body of the snake 
will be increased by one and the score will be increased by one as well.
"""
def bodyIncreasing(appleIndex, score, snakeAttachment):
    for x in range(0, len(appleCoordination)):
        if appleCoordination[x] == snake[0]:
            snakeAttachment = snake[-1].copy()
            appleIndex = x  # apple index will be destroyed (?)
            score += 1
    return appleIndex, score, snakeAttachment


"""
This method is highly connected to the bodyIncreasing method. It checks if there is a attachment of the snake and if so, 
a copy of it will be attached to the rest of the snake (which consist of one body block and one head block).
"""
def snakeAttachementProof(appleIndex, snakeAttachment):
    if snakeAttachment != None:
        snake.append(snakeAttachment.copy())
        snakeAttachment = None
        appleCoordination.pop(appleIndex)  # apple will be deleted from the apple list
    return snakeAttachment


"""
This method checks, if the snake is collided either with itself or with one of the four boundaries. Therefore the 
method checks:

if the head of the snake has the same position with one of the body parts of the snake
if the x-coordinate of the snake is on the left (0) or on the right (27) side out of the playground
if the snake y-coordinate of the snake is on the upper (0) or on the lower (27) side out of the playground
"""
def snakeCollusion(end):
    for x in range(1, len(snake)):
        if snake[0] == snake[x]:
            end = True
    if snake[0][0] < 0 or snake[0][0] > 27:
        end = True
    if snake[0][1] < 0 or snake[0][1] > 27:
        end = True
    return end


"""
This method defines, in what directions the snake should move given certain directions.

if direction = 0 (up) then the y coordinate of the head should be decreased by one
if direction = 1 (right) then the x coordinate of the head should be increased by one
if direction = 2 (down) then the y coordinate of the head should be increased by one
if direction = 3 (left) then the x coordinate of the head should be decreased by one
"""
def snakeDirections(direction):
    if direction == 0:
        snake[0][1] -= 1
    if direction == 1:
        snake[0][0] += 1
    if direction == 2:
        snake[0][1] += 1
    if direction == 3:
        snake[0][0] -= 1


"""
This method defines the movement of the body parts of the snake by iterating through the snake but with the starting 
point at the first body block directly behind the head of the snake. Within the iteration, the body parts of the snake 
are moved by one element to the front to the place where the penultimate element was
"""
def snakeMovement():
    number = len(snake) - 1
    for i in range(1, len(snake)):
        snake[number] = snake[number - 1].copy()
        number -= 1


"""
This method defines all the actions that will happen after certain button presses. Therefore the pygame.event.get() 
method is used to iterate through all the button presses events that can occur. It is only allowed to move the snake in 
a certain direction, if it is not moving in the opposite direction at the moment

following events should occur:
If the game window gets close by the red cross at the upper left corner, the game will be closed.
It is forbidden to move the snake upwards if it is moving downwards. It first have to move left or right
It is forbidden to move the snake to the left if it is moving to the right. It first have to move up or down
It is forbidden to move the snake downwards if it is moving upwards. It first have to move left or right
It is forbidden to move the snake to the right if it is moving to the left. It first have to move up or down

The directions are defined by the w, a, s, d buttons but can be changed to the arrow buttons be replacing:
K_w with K_UP
K_d with K_RIGHT
K_s with K_DOWN
K_a with K_LEFT
"""
def buttonActions(direction):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != 2:
                direction = 0
            if event.key == pygame.K_d and direction != 3:
                direction = 1
            if event.key == pygame.K_s and direction != 0:
                direction = 2
            if event.key == pygame.K_a and direction != 1:
                direction = 3
    return direction

# To start the program, the main loop has to be called!
mainLoop()
