import pygame
from time import sleep
from zipfile import *
pygame.init()

filename = input("Enter filename: ")
scalar = int(input("Enter scalar value, or one for no scaling"))
screen = pygame.display.set_mode((int(input("Enter Width: "))*scalar, int(input("Enter Height: "))*scalar))
text = "CIRCLE: 0, 0, 20"
if filename.split('.')[1] == "txt":
  fh = open(filename, 'r')
  text = fh.read()
  fh.close()
  textlines = text.split("\n")
elif filename.split('.')[1] == "zip":
  archive = ZipFile(filename, 'r')
  fh = archive.open(filename.replace(".zip", ".txt"), 'r')
  text = fh.read()
  archive.close()
  textlines = text.decode("utf-8").split("\r\n")

currentColor = pygame.Color(255, 255, 255)
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
for i in range(0, len(textlines)):
  line = textlines[i]
  if not line == "":
      if line[0:4] == "RGB:":
        datavals = line.replace(" ", "").replace("RGB:", "").split(",")
        currentColor.r = int(datavals[0])
        currentColor.g = int(datavals[1])
        currentColor.b = int(datavals[2])
      elif line[0:5] == "RGBA:":
        datavals = line.replace(" ", "").replace("RGBA:", "").split(",")
        currentColor.r = int(datavals[0])
        currentColor.g = int(datavals[1])
        currentColor.b = int(datavals[2])
        currentColor.a = int(datavals[3])
      elif line[0:5] == "RECT:":
        cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("RECT:", "")
        datavals = cleanline.split(",")
        x = int(datavals[0])
        y = int(datavals[1])
        width = int(datavals[2])
        height = int(datavals[3])
        pygame.draw.rect(screen, currentColor, pygame.Rect(x*scalar, y*scalar, width*scalar, height*scalar))
      elif line[0:7] == "CIRCLE:":
        cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("CIRCLE:", "")
        datavals = cleanline.split(",")
        x = int(datavals[0])
        y = int(datavals[1])
        radius = int(datavals[2])
        pygame.draw.circle(screen, currentColor, (x, y), radius)
      
  pygame.display.flip()
  sleep(.05)

done = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
pygame.image.save(screen, filename.split('.')[0] + '.png')
exit()
