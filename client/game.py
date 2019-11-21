import pygame
from win32api import GetSystemMetrics


pygame.init()
screenWidth = (int)(GetSystemMetrics(1) -  0.08*GetSystemMetrics(1))
screenHeigth = screenWidth
win = pygame.display.set_mode((screenWidth,screenWidth))

pygame.display.set_caption("CHINCZYK")
run = True
x = 50
y = 50
vel = 2
i = 0
z = x
q = y
background = pygame.image.load('resources/table.png')
background = pygame.transform.scale(background,(screenWidth,screenWidth))
redPawn = pygame.image.load('resources/redPawn.png')
redPawn = pygame.transform.scale(redPawn,((int)(0.073*screenWidth),(int)(0.073*screenWidth)))

while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= vel
        
    if keys[pygame.K_RIGHT]:
        x += vel
        
    if keys[pygame.K_UP]:
        y -= vel

    if keys[pygame.K_DOWN]:
        y += vel
    if keys[pygame.K_SPACE]:
        
        if q != y or z != x:
            q = y
            z = x
            print('i = '+ str(i) + ' x = '+ str(x) + ' y = ' + str(y) )
            i+=1
        
        
    win.blit(background,(0,0))
    
    win.blit(redPawn,(x,y))
    pygame.display.update()
    
pygame.quit()