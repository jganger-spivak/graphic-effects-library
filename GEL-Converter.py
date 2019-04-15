import pygame
from zipfile import *
from time import sleep

converttype = 'lines'
pygame.init()
filename = input("Enter filename: ")
width = int(input("Enter Image Width: "))
height = int(input("Enter Image Height: "))
screen = pygame.display.set_mode((width, height))
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
    generatedText += "SIZE: " + str(width) + ", " + str(height) + "\n"
    for column in range(0, len(pixels)):
        for row in range(0, len(pixels[column])):
            events = pygame.event.get()
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



textlines = generatedText.split("\n")
savedLines = {}
trimtext = "SIZE: " + str(width) + ", " + str(height) + "\nTYPE: converted"
trimRGB = '255,255,255'
for line in range(0, len(textlines)):
    if textlines[line][0:4] == 'RGB:':
        trimRGB = textlines[line]
    elif textlines[line][0:5] == 'RECT:':
        try:
            savedLines[trimRGB] += textlines[line] + "\n"
        except KeyError:
            savedLines[trimRGB] = ''
            savedLines[trimRGB] += textlines[line] + "\n"

savedLines['RGB: 255, 255, 255'] = '' #Should remove all white
for color in savedLines.items():
    trimtext += color[0] + "\n"
    trimtext += color[1]
trimtext = trimtext.replace("RGB: 255, 255, 255", "") #Removes spurious RGB call
fh = open(filename.split('.')[0] + '.txt', 'w')
fh.write(trimtext)
fh.close()
#exit()
