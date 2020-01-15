import pygame
import time
import random


def pointlight(surf, plpos, intensity, radius):
    start = time.time()
    pxarray = pygame.PixelArray(surf)
    for column in range(0, len(pxarray)):
        for row in range(0, len(pxarray[column])):
            pxpos = pygame.Vector2(column, row)
            distance = int(pos.distance_to(pxpos))
            if distance < radius:
                distance *= intensity
                distance = abs(distance - 255)#Invert colors
                basecolor = pxarray[column][row]
                if not pxarray[column][row] == mapsurf.map_rgb((0, 0, 0)):
                    if not pxarray[column][row] == mapsurf.map_rgb((0, 255, 0)):
                        basecolor = basecolor << 8
                    basecolor = abs(0xFFFFFF - basecolor)
                if distance <= 255:
                    pxarray[column][row] = pygame.Color(distance, distance, distance) + pygame.Color(basecolor)
    return time.time() - start

if __name__ == "__main__":
    pygame.init()
    scalar = 5
    screen = pygame.display.set_mode((80*scalar, 80*scalar))
    mapsurf = pygame.Surface((80, 80))
    basesurf = pygame.Surface((80, 80))
    pygame.draw.rect(basesurf, (0, 0, 0), (0, 0, 80, 80))
    
    basesurf.blit(pygame.transform.scale(pygame.image.load('lonk_gel.png').convert(), (basesurf.get_width(), basesurf.get_height())), (0, 0))
    pos = pygame.Vector2(4, 4)
    brightmult = 13
    maxdist = 20
    done = False
    while not done:
        for event in pygame.event.get():
            mapsurf.blit(basesurf, (0, 0))
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if brightmult > 1:
                        brightmult -= 1
                if event.key == pygame.K_o:
                    if brightmult < 32:
                        brightmult += 1
                if event.key == pygame.K_k:
                    if maxdist > 1:
                        maxdist -= 1
                if event.key == pygame.K_l:
                    if maxdist < 20:
                        maxdist += 1
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
                mx = int(mpos[0]/scalar)
                my = int(mpos[1]/scalar)
                pos = pygame.Vector2(mx, my)
                pointlight(mapsurf, pos, brightmult, maxdist)
            screen.blit(pygame.transform.scale(mapsurf, (80*scalar, 80*scalar)), (0, 0))
            pygame.display.flip()
    exit()
