from const import *

class Tile():
    def __init__(self,pygame,type,startPos,endPos,screen,icon):
        self.type = type
        self.startPos = startPos
        self.endPos = endPos
        self.pygame = pygame
        self.icon = icon
        self.icon = pygame.transform.scale(self.icon,(SQSIZE,SPSIZE))
        self.rect = self.icon.get_rect()
        self.rect = self.rect.move(self.startPos)
        self.panelty = type[2]
        self.army = 0
        self.drawColor(screen)
    def drawColor(self,screen):
        screen.blit(self.icon,self.rect)
    def setArmy(self, army):
        self.army = army

