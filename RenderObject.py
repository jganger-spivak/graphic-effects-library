class RenderObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.rightbound = 1280
        self.downbound = 720
    def render(self):
        pass
    def handleVelocity(self, drag = True):
        self.x += self.vx
        self.y += self.vy
        if drag:
            if self.vx > 0:
                self.vx -= 1
            elif self.vx < 0:
                self.vx += 1
            if self.vy > 0:
                self.vy -= 1
            elif self.vy < 0:
                self.vy += 1
    def keepInBounds(self):
        if self.x < 0:
            self.x = 0
            self.vx *= -1
        if self.y < 0:
            self.y = 0
            self.vy *= -1
        if (self.x + self.width) > self.rightbound:
            self.x = self.rightbound - self.width
            self.vx *= -1
        if (self.y + self.height) > self.downbound:
            self.y = self.downbound - self.height
            self.vy *= -1
    def collide(self, renderList):
        for obj in renderList:
            if not obj == self:
                if (self.x < obj.x + obj.width and self.x + self.width > obj.x and self.y < obj.y + obj.height and self.y + self.height > obj.y):
                    return obj
        return False
    def push(self, vx, vy):
        self.vx += vx
        self.vy += vy
    def bounce(self, xb, yb):
        if xb:
            self.vx *= -1
        if yb:
            self.vy *= -1
