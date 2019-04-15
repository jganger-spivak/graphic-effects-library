import pygame
from RenderObject import RenderObject
pygame.init()

filename = input("Enter filename:")
scalar = float(input("Enter scalar value, or one for no scaling"))

fh = open(filename, 'r')
text = fh.read()
fh.close()
textlines = text.split("\n")
particleList = []
currentColor = pygame.Color(255, 255, 255)
class Particle(RenderObject):
    def __init__(self, tex):
        RenderObject.__init__(self, tex[0].x, tex[0].y, tex[0].width, tex[0].height)
        self.color = tex[1]
        self.origx = self.x
        self.origy = self.y
        self.rightbound = screen.get_width()
        self.downbound = screen.get_height()
    def render(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
        self.handleVelocity(False)
        self.keepInBounds()
def particleLine(line):
    if not line == "":
      if line[0:5] == "SIZE:":
        datavals = line.replace("SIZE:", "").replace(" ", "").split(",")
        width = int(datavals[0]) * scalar
        height = int(datavals[1]) * scalar
        global screen
        screen = pygame.display.set_mode((int(width), int(height)))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, screen.get_width(), screen.get_height()))
      elif line[0:4] == "RGB:":
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
        particleList.append([pygame.Rect(x*scalar, y*scalar, width*scalar, height*scalar), pygame.Color(currentColor.r, currentColor.g, currentColor.b, currentColor.a)])


for i in range(0, len(textlines)):
  pygame.event.get()
  line = textlines[i]
  particleLine(line)

renderList = []
for rect in particleList:
    renderList.append(Particle(rect))
done = False
framecount = 0
while not done:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen.fill((255, 255, 255))
                pygame.display.flip()
            if event.key == pygame.K_SPACE:
                for obj in renderList:
                    obj.push(obj.vx*1.2, obj.vy*1.2)
            if event.key == pygame.K_m:
                mxy = pygame.mouse.get_pos()
                mx = mxy[0]
                my = mxy[1]
                for obj in renderList:
                    obj.push((mx - obj.x) / 1000, (my - obj.y) / 1000)
            if event.key == pygame.K_u:
                for obj in renderList:
                    obj.push((obj.origx - obj.x) / 1000, (obj.origy - obj.y) / 1000)
            if event.key == pygame.K_f:
                for obj in renderList:
                    obj.vx = 0
                    obj.vy = 0
            if event.key == pygame.K_RETURN:
                for obj in renderList:
                    obj.vx = 0
                    obj.vy = 0
                    obj.x = obj.origx
                    obj.y = obj.origy
    for obj in renderList:
        obj.render()
    pygame.display.flip()
    framecount += 1
    #pygame.image.save(screen, "/" + filename.split('.')[0] + "frames/" + str(framecount) + ".png")
exit()
