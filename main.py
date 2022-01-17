import sys

import pygame

elementSize = 25
snake = [[13,13],[13,14]]   # [13,13] is the head of the snake. [13,14] is the first body part of the snake
clock = pygame.time.Clock()

green = (0, 255, 0)     # RGB value
lightGreen = (0, 102, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (180, 0, 0)

pygame.init()
screen = pygame.display.set_mode([700,700]) # 700 is the size of the gamefield


"""
This method draws the snake and the apples (white boxes) on the playground and fills the background in black color.
"""
def draw():
    screen.fill(black)
    drawSnake()


"""
This method draws the snake on the playground. The coordination for the head spawn can be interpreted as follows: 
coordinate[0] = x-coordinates for the snake bodypart. coordinate[1] = y-coordinates for the snake bodypart. The 1 at the 
end of the pygame.draw.rect method makes, that the white boxes are only outlined but not filled out.
"""
def drawSnake():
    head = True
    for bodypart in snake:
        coordinate = [bodypart[0] * elementSize, bodypart[1] * elementSize]
        if head:
            pygame.draw.rect(screen, red, (coordinate[0], coordinate[1], elementSize, elementSize), 0)
            head = False
        else:
            pygame.draw.rect(screen, green, (coordinate[0], coordinate[1], elementSize, elementSize), 1)

"""
This is the main loop of the game and it keeps the game running as long as the go variable is True.
"""
def mainLoop():
    go = True
    snakeAttachment = None
    appleIndex = -1  # ???
    end = False
    score = 0
    direction = 0  # 0 = up, 1 = right, 2 = down, 3 = left

    while go:
        direction = buttonActions(direction)
        snakeMovement()
        snakeDirections(direction)
        #end = snakeCollusion(end)
        #appleIndex, score, snakeAttachment = bodyIncreasing(appleIndex, score, snakeAttachment)
        #snakeAttachment = snakeAttachementProof(appleIndex, snakeAttachment)
        #appleFrequency()
        #startEndGame(end, score)

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


"""
This method defines the movement of the body parts of the snake by iterating through the snake with the starting 
point at the first body block directly behind the head of the snake. Within the iteration, the body parts of the snake 
are moved by one element to the front to the place where the penultimate element was. A copy of the snake list has to be 
created, because otherwise both lists would change if one is changed
"""
def snakeMovement():
    number = len(snake) - 1
    for i in range(1, len(snake)):
        snake[number] = snake[number - 1].copy()
        number -= 1


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
This method draws the snake, the apples appearing on the playground and the text box that counts the score at the top of
the playground. The pygame.display.update() method will print all the changes of the screen
"""
def showPlayground(score):
    draw()
    #textGround, textBox = textObject("Score: " + str(score), font)
    #textBox.center = ((350, 40))
    #screen.blit(textGround, textBox)
    pygame.display.update()

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
    clock.tick(10)


# To start the program, the main loop has to be called!
mainLoop()