import pygame
from RenderObject import RenderObject
from ByteReader import ByteReader
pygame.init()

filename = input("Enter filename:")
scalar = int(input("Enter scalar value, or one for no scaling"))

fh = open(filename, 'rb')
br = ByteReader(fh)
fh.close()
particleList = []
mouseFollow = False

filetype = filename.split('.')[1]
COLORBYTE = (245).to_bytes(1, byteorder='big')
winwidth = int.from_bytes(br.read(2), byteorder='big')
winheight = int.from_bytes(br.read(2), byteorder='big')
screen = pygame.display.set_mode((winwidth*scalar, winheight*scalar))
hsize = 2
vsize = 2
if winwidth < 240:
  hsize = 1
if winheight < 240:
  vsize = 1

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
        if mouseFollow:
            mxy = pygame.mouse.get_pos()
            mx = mxy[0]
            my = mxy[1]
            self.push((mx - self.x) / 1000, (my - self.y) / 1000)
def particleBytes(br, scalar):
    color = (255, 255, 255)
    done = False
    while not done:
        cmd = br.peek(1)
        if len(cmd) == 0:
            fh.close()
            done = True
            continue
        if cmd == COLORBYTE:
            br.read(1)
            r = int.from_bytes(br.read(1), byteorder='big')
            g = int.from_bytes(br.read(1), byteorder='big')
            b = int.from_bytes(br.read(1), byteorder='big')
            color = (r, g, b)
            #pygame.display.flip()
        elif cmd < COLORBYTE:
            x = int.from_bytes(br.read(hsize), byteorder='big')
            y = int.from_bytes(br.read(vsize), byteorder='big')
            if filetype == 'gel':
                #width = int.from_bytes(br.read(hsize), byteorder='big')
                height = int.from_bytes(br.read(vsize), byteorder='big')
                particleList.append([pygame.Rect(x*scalar, y*scalar, scalar, height*scalar), pygame.Color(r, g, b)])
            elif filetype == 'glp':
                particleList.append([pygame.Rect(x*scalar, y*scalar, scalar, scalar), pygame.Color(r, g, b)])
   

particleBytes(br, scalar)

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
