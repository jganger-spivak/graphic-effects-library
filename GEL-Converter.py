import pygame
from zipfile import *
from time import sleep


def compressLines(genText):
    lastPercent = '0%'
    textlines = genText.split("\n")
    savedLines = {}
    trimtext = "SIZE: " + str(width) + ", " + str(height) + "\nTYPE: converted"
    trimRGB = '255,255,255'
    for line in range(0, len(textlines)):
        if not str((line/len(textlines))*100).split('.')[0] + '%' == lastPercent:
            lastPercent = str((line/len(textlines))*100).split('.')[0] + '%'
            print(lastPercent)
        if textlines[line][0:4] == 'RGB:':
            trimRGB = textlines[line]
        elif textlines[line][0:5] == 'RECT:':
            try:
                savedLines[trimRGB] += textlines[line] + "\n"
            except KeyError:
                savedLines[trimRGB] = ''
                savedLines[trimRGB] += textlines[line] + "\n"

    savedLines['RGB: 255, 255, 255'] = '' #Should remove all white
    print(str(len(savedLines.items())) + ' colors')
    allColors = len(savedLines.items())
    count = 0
    for color in savedLines.items():
        if not str((count/allColors)*100).split('.')[0] + '%' == lastPercent:
            lastPercent = str((count/allColors)*100).split('.')[0] + '%'
            print(lastPercent)
        trimtext += color[0] + "\n"
        trimtext += color[1]
        count += 1
    trimtext = trimtext.replace("RGB: 255, 255, 255", "") #Removes spurious RGB call
    return trimtext


converttype = 'lines'
pygame.init()
filename = input("Enter filename: ")
lastPercent = '0%'
if filename.split('.')[1] == 'txt':
    if input('Text file selected. Would you like to compress? Press ENTER to cancel').upper() == 'Y':
        fh = open(filename.split('.')[0] + '.txt', 'r')
        text = fh.read()
        print('File read')
        width = int(text.split('\n')[0].replace('SIZE:', '').split(',')[0])
        height = int(text.split('\n')[0].replace('SIZE:', '').split(',')[1])
        fh.close()
        fh = open('_' + filename.split('.')[0] + '.txt', 'w')
        fh.write(compressLines(text))
        fh.close()
        exit()
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
        if not str((column/width)*100).split('.')[0] + '%' == lastPercent:
            lastPercent = str((column/width)*100).split('.')[0] + '%'
            print(lastPercent)
        pygame.display.flip()
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
                #pygame.display.flip()

lastPercent = '0%'
fh = open(filename.split('.')[0] + '.txt', 'w')
fh.write(generatedText)
fh.close()
input('Image scanning and initial save done. Press enter to optimize and save')

fh = open(filename.split('.')[0] + '.txt', 'w')
fh.write(compressLines(generatedText))
fh.close()
#exit()
