class Tile():
    def __init__(self,pygame,type,startPos,endPos,screen):
        self.type = type
        self.startPos = startPos
        self.endPos = endPos
        self.pygame = pygame
        self.panelty = type[2]
        self.army = 0
        if(type == "sea"):
            self.color = (68, 108, 219)
        else:
            self.color = type[3]
        self.drawColor(screen)
    def drawColor(self,screen):
        self.pygame.draw.rect(screen,self.color,[self.startPos[0],self.startPos[1],self.endPos[0],self.endPos[1]])
    def setArmy(self, army):
        self.army = army

