from RenderObject import RenderObject
import random
import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))


def circleGradient(x, y, width, height, startColor, endColor, scalar):
    destination = pygame.Surface((int(width*scalar), int(height*scalar)))
    gradColor = pygame.Color(startColor.r, startColor.g, startColor.b)
    diffred = startColor.r - endColor.r
    diffgreen = startColor.g - endColor.g
    diffblue = startColor.b - endColor.b
    diffalpha = startColor.a - endColor.a
    
    rstep = int(diffred / width)
    gstep = int(diffgreen / width)
    bstep = int(diffblue / width)
    astep = int(diffalpha / width)
    for line in range(0, int((width*scalar)/2)):
      pygame.draw.circle(destination, gradColor, (int(x*scalar) + int((width*scalar)/2), int(y*scalar) + int((height*scalar)/2)), abs(line-int((width*scalar)/2)), int(scalar))
      pygame.display.flip()
      #print(gradColor)
      if endColor.r > startColor.r:
        gradColor.r += abs(rstep)
      else:
        gradColor.r -= rstep
      
      if endColor.g > startColor.g:
        gradColor.g += abs(gstep)
      else:
        gradColor.g -= gstep
      
      if endColor.b > startColor.b:
        gradColor.b += abs(bstep)
      else:
        gradColor.b -= bstep
      if endColor.a > startColor.a:
        gradColor.a += abs(astep)
      else:
        gradColor.a -= astep
    return destination



class Light(RenderObject):
    def __init__(self, x, y, width, height, brightness):
        RenderObject.__init__(self, x, y, width, height) 
        self.brightness = brightness
    def lights(self):
        pass
    def action(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))


class LightableRect(RenderObject):
    def __init__(self, x, y, width, height):
        RenderObject.__init__(self, x, y, width, height)
        self.basecolor = (255, 0, 0)
        self.downbound = screen.get_height()
        self.rightbound = screen.get_width()
        self.texscaling = 2
        self.tex = circleGradient(0, 0, int(self.width/self.texscaling), int(self.height/self.texscaling), pygame.Color(255, 0, 0), pygame.Color(0, 0, 0), 1)
        self.tex = pygame.transform.scale(self.tex, (self.width, self.height))
    def reRender(self):
        self.tex = circleGradient(0, 0, int(self.width/self.texscaling), int(self.height/self.texscaling), pygame.Color(255, 0, 0), pygame.Color(0, 0, 0), 1)
        self.tex = pygame.transform.scale(self.tex, (self.width, self.height))
    def action(self):
        screen.blit(self.tex, (self.x, self.y))
        self.handleVelocity(False)
        self.keepInBounds()
    def camera(self, renderList):
        #selfsize = rect(0, 
        for obj in renderList:
            if isinstance(obj, Light):
                pass
                #if obj.lights()
                #print('Light found! location is (' + str(obj.x) + ',' + str(obj.y) + ')')

renderList = []
renderList.append(LightableRect(0, 0, 100, 100))
renderList.append(Light(400, 400, 2, 2, 10))
scaleup = True
done = False
while not done:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for obj in renderList:
                    obj.push(random.randint(-1, 1)/10, random.randint(-1, 1)/10)
            if event.key == pygame.K_f:
                for obj in renderList:
                    obj.vx = 0
                    obj.vy = 0
            if event.key == pygame.K_p:
                for obj in renderList:
                    if isinstance(obj, LightableRect):
                        if obj.texscaling > 1:
                            obj.texscaling -= 1
                        obj.reRender()
            if event.key == pygame.K_o:
                for obj in renderList:
                    if isinstance(obj, LightableRect):
                        obj.texscaling += 1
                        obj.reRender()
    for obj in renderList:
        obj.camera(renderList)
        #obj.lights()
        obj.action()
    pygame.display.flip()
