import pygame
from time import sleep
from zipfile import *
pygame.init()

config = dict((x.strip(), y.strip()) for x, y in (element.split(':') for element in open('config.txt').read().split('\n')))
config['FASTMODE'] = int(config['FASTMODE'])
filename = input("Enter filename: ")
scalar = float(input("Enter scalar value, or one for no scaling"))
filetype = 'manual' 
text = "CIRCLE: 0, 0, 20"
featsurfaces = {}
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

def getMaxSize(textlines):
  maxwidth = 0
  maxheight = 0
  for line in textlines:
    if not line == "":
      if line[0:5] == 'RECT:':
        cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("RECT:", "")
        datavals = cleanline.split(",")
        x = int(datavals[0])
        y = int(datavals[1])
        width = int(datavals[2])
        height = int(datavals[3])
        if (y + height) > maxheight:
          maxheight = y+height
        if (x + width) > maxwidth:
          maxwidth = x+width
      elif line[0:5] == 'GRAD':
        cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("GRAD:", "")
        datavals = cleanline.split(",")
        x = int(datavals[0])
        y = int(datavals[1])
        width = int(datavals[2])
        height = int(datavals[3])
        if (y + height) > maxheight:
          maxheight = y+height
        if (x + width) > maxwidth:
          maxwidth = x+width
      elif line[0:7] == "CIRCLE:":
        cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("CIRCLE:", "")
        datavals = cleanline.split(",")
        x = int(datavals[0])
        y = int(datavals[1])
        radius = int(datavals[2])
        if (y + radius*2) > maxheight:
          maxheight = y+radius*2
        if (x + radius*2) > maxwidth:
          maxwidth = x+radius*2
  return (maxwidth, maxheight)

def compileLines(textlines, destination):
  print('CompileLine run')
  maxwidth = 0
  maxheight = 0
  for line in textlines:
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
          pygame.draw.rect(destination, currentColor, pygame.Rect(x*scalar, y*scalar, width*scalar, height*scalar))
          if not bool(config['FASTMODE']):
            pygame.display.flip()
          if (y + height) > maxheight:
            maxheight = y+height
          if (x + width) > maxwidth:
            maxwidth = x+width
        elif line[0:5] == "GRAD:":
          cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("GRAD:", "")
          datavals = cleanline.split(",")
          x = int(datavals[0])
          y = int(datavals[1])
          width = int(datavals[2])
          height = int(datavals[3])
          if (y + height) > maxheight:
            maxheight = y+height
          if (x + width) > maxwidth:
            maxwidth = x+width
          direction = datavals[4]
          endColor = pygame.Color(255, 255, 255)
          gradColor = pygame.Color(currentColor.r, currentColor.g, currentColor.b)
          endColor.r = int(datavals[5])
          endColor.g = int(datavals[6])
          endColor.b = int(datavals[7])
          try:
            endColor.a = int(datavals[8])
            if direction == 'side':
              
              diffred = currentColor.r - endColor.r
              diffgreen = currentColor.g - endColor.g
              diffblue = currentColor.b - endColor.b
              diffalpha = currentColor.a - endColor.a
              
              rstep = int(diffred / width)
              gstep = int(diffgreen / width)
              bstep = int(diffblue / width)
              astep = int(diffalpha / width)
              for line in range(0, int(width*scalar)):
                pygame.draw.rect(destination, gradColor, pygame.Rect((x+line)*scalar, y*scalar, scalar, height*scalar))
                if not bool(config['FASTMODE']):
                  pygame.display.flip()
                
                if endColor.r > currentColor.r:
                  gradColor.r += abs(rstep)
                else:
                  gradColor.r -= rstep
                
                if endColor.g > currentColor.g:
                  gradColor.g += abs(gstep)
                else:
                  gradColor.g -= gstep
                
                if endColor.b > currentColor.b:
                  gradColor.b += abs(bstep)
                else:
                  gradColor.b -= bstep

                if endColor.a > currentColor.a:
                  gradColor.a += abs(astep)
                else:
                  gradColor.a -= astep
                
                
            elif direction == 'down':
              raise NotImplementedError
            elif direction == 'circle':
              diffred = currentColor.r - endColor.r
              diffgreen = currentColor.g - endColor.g
              diffblue = currentColor.b - endColor.b
              diffalpha = currentColor.a - endColor.a
              
              rstep = int(diffred / width)
              gstep = int(diffgreen / width)
              bstep = int(diffblue / width)
              astep = int(diffalpha / width)
              for line in range(0, int((width*scalar)/2)):
                pygame.draw.circle(destination, gradColor, (int(x*scalar), int(y*scalar)), abs(line-int((width*scalar)/2)), int(scalar))
                if not bool(config['FASTMODE']):
                  pygame.display.flip()
                print(gradColor)
                if endColor.r > currentColor.r:
                  gradColor.r += abs(rstep)
                else:
                  gradColor.r -= rstep
                
                if endColor.g > currentColor.g:
                  gradColor.g += abs(gstep)
                else:
                  gradColor.g -= gstep
                
                if endColor.b > currentColor.b:
                  gradColor.b += abs(bstep)
                else:
                  gradColor.b -= bstep

                if endColor.a > currentColor.a:
                  gradColor.a += abs(astep)
                else:
                  gradColor.a -= astep
          except IndexError:
            raise NotImplementedError
        elif line[0:7] == "CIRCLE:":
          cleanline = line.replace("(", "").replace(")", "").replace(" ", "").replace("CIRCLE:", "")
          datavals = cleanline.split(",")
          x = int(datavals[0])
          y = int(datavals[1])
          radius = int(datavals[2])
          if (y + radius*2) > maxheight:
            maxheight = y+radius*2
          if (x + radius*2) > maxwidth:
            maxwidth = x+radius*2
          pygame.draw.circle(destination, currentColor, (x, y), radius*scalar)
      
def colorCompileText(argtextlines, rle=False):
  savedLines = {}
  trimRGB = '255,255,255'
  fastcomp = False
  lastPercent = '0%'
  for line in range(0, len(argtextlines)):
    if not str((line/len(argtextlines))*100).split('.')[0] + '%' == lastPercent:
            lastPercent = str((line/len(argtextlines))*100).split('.')[0] + '%'
            print(lastPercent)
    if argtextlines[line][0:4] == 'RGB:' or argtextlines[line][0:1] == 'C':
      trimRGB = argtextlines[line]
    elif argtextlines[line][0:5] == 'RECT:' or argtextlines[line][0:2] == 'RT':
      try:
          savedLines[trimRGB] += argtextlines[line] + "\n"
      except KeyError:
          savedLines[trimRGB] = ''
          savedLines[trimRGB] += argtextlines[line] + "\n"
  print('Number of colors: ' + str(len(savedLines)))
  numColors = len(savedLines.items())
  count = 0
  for color in savedLines.items():
    if not str((count/numColors)*100).split('.')[0] + '%' == lastPercent:
            lastPercent = str((count/numColors)*100).split('.')[0] + '%'
            print(lastPercent)
    if rle:
        datavals = color[0].replace(" ", "").replace("C", "").replace("\n", "").split(",")
    else:
        datavals = color[0].replace(" ", "").replace("RGB:", "").replace("\n", "").split(",")


    currentColor.r = int(datavals[0])
    currentColor.g = int(datavals[1])
    currentColor.b = int(datavals[2])
    for rectangle in color[1].split("\n"):
      if rle:
        cleanline = rectangle.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("RT", "")
      else:
        cleanline = rectangle.replace("(", "").replace(")", "").replace(" ", "").replace("x", ",").replace("RECT:", "")
      datavals = cleanline.split(",")
      if not datavals[0] == '':
        x = int(datavals[0])
        y = int(datavals[1])
        width = int(datavals[2])
        height = int(datavals[3])
        pygame.draw.rect(screen, currentColor, pygame.Rect(x*scalar, y*scalar, width*scalar, height*scalar))
    pygame.event.get()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          fastcomp = True
    if not fastcomp:
      if not bool(config['FASTMODE']):
        pygame.display.flip()
    count += 1

def featureCompileText(argtextlines):
  savedLines = {}
  featureName = 'TESTFEATURE'
  for line in range(0, len(argtextlines)):
    if argtextlines[line][0:8] == 'FEATURE:':
      featureName = argtextlines[line]
    else:
      try:
        savedLines[featureName] += argtextlines[line] + "\n"
      except KeyError:
        savedLines[featureName] = ''
        savedLines[featureName] += argtextlines[line]
  print('Number of features: ' + str(len(savedLines)))
  for feature in savedLines.items():
    maxwidth, maxheight = getMaxSize(feature[1].split('\n'))
    featsurfaces[feature] = pygame.Surface((maxwidth, maxheight))
    featsurfaces[feature].blit(screen, (0, 0))
    #screen.fill(


for i in range(0, len(textlines)):
  pygame.event.get()
  
  line = textlines[i]
  if line[0:5] == "SIZE:":
        datavals = line.replace("SIZE:", "").replace(" ", "").split(",")
        width = int(datavals[0]) * scalar
        height = int(datavals[1]) * scalar
        screen = pygame.display.set_mode((int(width), int(height)))
        pygame.draw.rect(screen, (255, 255, 255, 0), pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
  
  if line[0:5] == 'TYPE:':
      datavals = line.replace(" ", "").replace("TYPE:", "")
      filetype = datavals
      if filetype == 'converted':
        print('Alt compile method used')
        colorCompileText(textlines, False)
        pygame.display.flip()
        break
      elif filetype == 'multi':
        print('Multi-feature image detected')
        pass
      elif filetype == 'RLE':
        print('RLE compressed file detected')
        colorCompileText(textlines, True)
        pygame.display.flip()
        break
      else:
        print("Unknown type")
if filetype == 'manual':
  print(compileLines(textlines, screen))
  pygame.display.flip()
print("Done. Quit to save")
done = False

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
pygame.image.save(screen, filename.split('.')[0] + '.png')
exit()
