import pygame
import lzma

class ByteReader:
    def __init__(self, file):
        self.data = lzma.decompress(file.read(-1))
        self.pointer = 0
    def read(self, numbytes):
        returnbytes = bytearray(numbytes)
        try:
            for index in range(0, numbytes):
                returnbytes[index] = self.data[self.pointer+index]
        except IndexError: #EOF! Return empty bytes
            return bytes(0)
        self.pointer += numbytes
        return returnbytes

filename = input("Please enter filename: ")
file = open(filename, mode='rb')
br = ByteReader(file)

winwidth = int.from_bytes(br.read(2), byteorder='big')
winheight = int.from_bytes(br.read(2), byteorder='big')
hsize = 2
vsize = 2
if winwidth < 256:
  hsize = 1
if winheight < 256:
  vsize = 1
screen = pygame.display.set_mode((winwidth, winheight))
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, winwidth, winheight))
done = False
color = (255, 255, 255)


while not done:
    cmd = br.read(1)
    if len(cmd) == 0:
        file.close()
        done = True
        continue
    if cmd == b'C':
        r = int.from_bytes(br.read(1), byteorder='big')
        g = int.from_bytes(br.read(1), byteorder='big')
        b = int.from_bytes(br.read(1), byteorder='big')
        color = (r, g, b)
        #pygame.display.flip()
    elif cmd == b'R':
        x = int.from_bytes(br.read(hsize), byteorder='big')
        y = int.from_bytes(br.read(vsize), byteorder='big')
        width = int.from_bytes(br.read(hsize), byteorder='big')
        height = int.from_bytes(br.read(vsize), byteorder='big')
        pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))
    #pygame.event.
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, filename.split('.')[0] + '.png')
            pygame.quit()
            exit()
    pygame.display.flip()
