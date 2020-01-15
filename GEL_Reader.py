import pygame
import lzma
from ByteReader import ByteReader

filename = input("Please enter filename: ")
scale = float(input("Please enter scale, or 1 for no scaling: "))
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
surf = pygame.Surface((winwidth, winheight))
screen = pygame.display.set_mode((int(winwidth*scale), int(winheight*scale)))
pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(0, 0, winwidth, winheight))
done = False
color = (255, 255, 255)
COLORBYTE = (245).to_bytes(1, byteorder='big')
lastPercent = '0%'

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
        screen.blit(pygame.transform.scale(surf, (int(winwidth*scale), int(winheight*scale))), (0,0))
        pygame.display.flip()
    elif cmd < COLORBYTE:
        x = int.from_bytes(br.read(hsize), byteorder='big')
        y = int.from_bytes(br.read(vsize), byteorder='big')
        if filetype == 'gel':
            #width = int.from_bytes(br.read(hsize), byteorder='big')
            height = int.from_bytes(br.read(vsize), byteorder='big')
            pygame.draw.rect(surf, color, pygame.Rect(x, y, 1, height))
        elif filetype == 'glp':
            pygame.draw.rect(surf, color, pygame.Rect(x, y, 1, 1))
    if not str((br.pointer/len(br.data))*100).split('.')[0] + '%' == lastPercent:
            lastPercent = str((br.pointer/len(br.data))*100).split('.')[0] + '%'
            print(lastPercent)
    pygame.event.get()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, filename.split('.')[0] + '.png')
            pygame.quit()
            exit()
    screen.blit(pygame.transform.scale(surf, (int(winwidth*scale), int(winheight*scale))), (0,0))
    pygame.display.flip()
