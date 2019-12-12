import pygame
import lzma
from ByteReader import ByteReader

filename = input("Please enter filename: ")
filetype = filename.split('.')[1]
file = open(filename, mode='rb')
br = ByteReader(file)

winwidth = int.from_bytes(br.read(2), byteorder='big')
winheight = int.from_bytes(br.read(2), byteorder='big')
hsize = 2
vsize = 2
if winwidth < 240:
  hsize = 1
if winheight < 240:
  vsize = 1
screen = pygame.display.set_mode((winwidth, winheight))
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, winwidth, winheight))
done = False
color = (255, 255, 255)
COLORBYTE = (245).to_bytes(1, byteorder='big')

while not done:
    cmd = br.peek(1)
    if len(cmd) == 0:
        file.close()
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
            width = int.from_bytes(br.read(hsize), byteorder='big')
            height = int.from_bytes(br.read(vsize), byteorder='big')
            pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))
        elif filetype == 'glp':
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 1, 1))
    #pygame.event.get()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, filename.split('.')[0] + '.png')
            pygame.quit()
            exit()
    pygame.display.flip()
