import pygame
import sys
import numpy as np

elementSize = 25
snake = [[13,13],[13,14]]   # [13,13] is the head of the snake. [13,14] is the first body part of the snake
appleCoordination = []
direction = 0   # 0 = up, 1 = right, 2 = down, 3 = left

green = (0, 255, 0)
lightGreen = (0, 102, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (180, 0, 0)

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('arialblack', 35)
screen = pygame.display.set_mode([700,700]) # 700 is the size of the gamefield

def textObject(text, font):
    textArea = font.render(text, True, (255, 255, 255))
    return textArea, textArea.get_rect()

def draw():
    screen.fill(black)

    for apple in appleCoordination:
        coordination = [apple[0] * elementSize, apple[1] * elementSize]     # The coordinates for the apple spawn. apple[0] = x coordinate. apple[1] = y coordinate.
        pygame.draw.rect(screen, white, (coordination[0], coordination[1], elementSize, elementSize), 1)      # spawn the apple

    head = True
    for x in snake:
        coordinate = [x[0] * elementSize, x[1] * elementSize] # To identify at which point on the screen the head of the snake is. x[0] represents the x coordinate and equals 13 whereas x[1] represents the y coordinate and equals 14
        if head:
            pygame.draw.rect(screen, red, (coordinate[0], coordinate[1], elementSize, elementSize),0) # rect is a square. (0,0,0) is the color black. coordinate[0] = x coordinate, coordinate[1] = y coordinate. elementSize = width and height of the square. 0 = square is filled out
            head = False
        else:
            pygame.draw.rect(screen, green, (coordinate[0], coordinate[1], elementSize, elementSize), 1) # (47, 79, 79) is a grey color body


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


appleCoordination.append(appleCoordinateGenerator())        # one coordinate for the appleCoordination will be append


# Main Loop
go = True   # The game runs as long as the go variable is True
snakeAttachment = None
appleIndex = -1     #???
end = False
score = 0

while go:
    for event in pygame.event.get():    # all the reactions to the different types of events like button presses are defined in the for loop
        if event.type == pygame.QUIT: sys.exit()    # If the game window gets close, the game will be closed
        if event.type == pygame.KEYDOWN:                        # the following if cases will only allow to move the snake in a certain direkction, if it is not moving in the opposite direction at the moment
            if event.key == pygame.K_w and direction != 2:     # K_UP it is forbidden to move the snake upwards if it is moving downwards. It first have to move left or right
                direction = 0                                   # If direction is not up, the snake can be moved up (direction 0)
            if event.key == pygame.K_d and direction != 3:  # K_RIGHT
                direction = 1
            if event.key == pygame.K_s and direction != 0:   # K_DOWN
                direction = 2
            if event.key == pygame.K_a and direction != 1:   # K_LEFT
                direction = 3

    if snakeAttachment != None:
        snake.append(snakeAttachment.copy())
        snakeAttachment = None
        appleCoordination.pop(appleIndex)       # apple will be deleted from the apple list

    number = len(snake) - 1
    for i in range(1, len(snake)):                  # iterate through the snake but with the starting point at the first body point directly behind the head of the snake
        snake[number] = snake[number - 1].copy()    # body parts of the snake are moved by one element to the front to the place where the penultimate element was
        number -= 1

    if direction == 0:          # if direction = 0 (up) then the y coordinate of the head should be decreased by one
        snake[0][1] -= 1
    if direction == 1:          # if direction = 1 (right) then the x coordinate of the head should be increased by one
        snake[0][0] += 1
    if direction == 2:          # if direction = 2 (down) then the y coordinate of the head should be increased by one
        snake[0][1] += 1
    if direction == 3:          # if direction = 3 (left) then the x coordinate of the head should be decreased by one
        snake[0][0] -= 1

    for x in range(1, len(snake)):
        if snake[0] == snake[x]:
            end = True

    if snake[0][0] < 0 or snake[0][0] > 27:
        end = True

    if snake[0][1] < 0 or snake[0][1] > 27:
        end = True

    for x in range(0, len(appleCoordination)):      # if the apple coordination = snake head coordination, then the body of the snake will be increased by one and the score will be increased by one as well
        if appleCoordination[x] == snake[0]:
            snakeAttachment = snake[-1].copy()
            appleIndex = x          # apple index will be destroyed (?)
            score += 1

    random = np.random.randint(0, 100)
    if random <= 1 and len(appleCoordination) < 4 or len(appleCoordination) == 0:   # random <= 1 equals a 2% probability. if there are already four apples on the field. len(appleCoordination) == 0 means that if there is no apple on the field one has to be spwaned!
        appleCoordination.append(appleCoordinateGenerator())        # apple will be created

    if end == False:            # check for collision with a wall or the snake itself
        draw()
        textGround, textBox = textObject("Score: " + str(score), font)
        textBox.center = ((350, 40))
        screen.blit(textGround, textBox)
        pygame.display.update()     # changes of the screen will be printed
    else:
        print("You achieved " + str(score) + " points")
        sys.exit()
    clock.tick(10)