import pygame

elementSize = 25
snake = [[13,13],[13,14]]   # [13,13] is the head of the snake. [13,14] is the first body part of the snake

green = (0, 255, 0)     # RGB value
lightGreen = (0, 102, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (180, 0, 0)

pygame.init()
screen = pygame.display.set_mode([700,700]) # 700 is the size of the gamefield


"""
This method draws the the snake and the apples (white boxes) on the playground and fills the background in black color.
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
