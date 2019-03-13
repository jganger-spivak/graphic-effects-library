import pygame
from zipfile import *
from time import sleep

converttype = 'lines'
pygame.init()
filename = input("Enter filename: ")
screen = pygame.display.set_mode((int(input("Enter Image Width: ")), int(input("Enter Image Height: "))))
image = pygame.image.load(filename).convert()
screen.blit(image, (0, 0))
pygame.display.flip()
pixels = pygame.PixelArray(screen)
generatedText = ""

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

if converttype == 'all': #This will probably make a MASSIVE file! 
    for column in range(0, len(pixels)):
        for row in range(0, len(pixels[column])):
            generatedText += "RGB: " + str(getRGBfromI(pixels[column][row])).replace("(", "").replace(")", "") + "\n"
            generatedText += "RECT: (" + str(column) + ", " + str(row) + ", 1x1)" + "\n"
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(column, row, 1, 1))
            pygame.display.flip()
elif converttype == 'lines': #This will be smaller, but still at least image width in number of lines
    currentColor = (255, 255, 255)
    currentHeight = 1
    currentX = 0
    currentY = 0
    for column in range(0, len(pixels)):
        for row in range(0, len(pixels[column])):
            newColor = getRGBfromI(pixels[column][row])
            if newColor == currentColor:
                currentHeight += 1
            else:
                #Place down last line
                generatedText += "RGB: " + str(currentColor).replace("(", "").replace(")", "") + "\n"
                generatedText += "RECT: (" + str(currentX) + ", " + str(currentY) + ", 1x" + str(currentHeight) + ")\n"
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(currentX, currentY, 1, currentHeight))
                #Start new line
                currentHeight = 1
                currentX = column
                currentY = row
                currentColor = newColor
                pygame.display.flip()
                #sleep(.05)

fh = open(filename.split('.')[0] + '.txt', 'w')
fh.write(generatedText)
fh.close()
exit()
