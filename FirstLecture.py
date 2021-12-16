import pygame
import sys

elementSize = 25
snake = [[13,13],[13,14]]   # [13,13] is the head of the snake. [13,14] is the first body part of the snake
direction = 0   # 0 = up, 1 = right, 2 = down, 3 = left

green = (0, 255, 0)
lightGreen = (0, 102, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (180, 0, 0)

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode([700,700]) # 700 is the size of the gamefield

def draw():
    screen.fill(black)

    head = True
    for x in snake:
        coordinate = [x[0] * elementSize, x[1] * elementSize] # To identify at which point on the screen the head of the snake is. x[0] represents the x coordinate and equals 13 whereas x[1] represents the y coordinate and equals 14
        if head:
            pygame.draw.rect(screen, red, (coordinate[0], coordinate[1], elementSize, elementSize),0) # rect is a square. (0,0,0) is the color black. coordinate[0] = x coordinate, coordinate[1] = y coordinate. elementSize = width and height of the square. 0 = square is filled out
            head = False
        else:
            pygame.draw.rect(screen, green, (coordinate[0], coordinate[1], elementSize, elementSize), 1) # (47, 79, 79) is a grey color body