import pygame

converttype = 'all'
pygame.init()
filename = input("Enter filename: ")
screen = pygame.display.set_mode((int(input("Enter Image Width: ")), int(input("Enter Image Height: "))))
image = pygame.image.load(filename).convert()
screen.blit(image, (0, 0))
pixels = pygame.PixelArray(screen)

if converttype == 'all':
    pass
