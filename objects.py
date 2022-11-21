from enum import Enum
from const import *
import numpy as np

class Army:
    def __init__(self,name,ger_link,sov_link,organization,hp,pos,type,speed):
        self.name = name
        self.ger_link = ger_link
        self.sov_link = sov_link
        self.organization = organization
        self.initial_org = organization
        self.hp = hp
        self.pos = pos
        self.type = type
        self.speed = speed
        self.tiles = []
        self.tile = 0
        self.trench = 0
    def _showArmy(self,screen):
        screen.blit(self.icon,self.rect)
    def _iconInit(self,pygame,tiles):
        if(self.type == "ger"):
            self.icon = pygame.image.load(self.ger_link)
        elif(self.type == "sov"):
            self.icon = pygame.image.load(self.sov_link)
        self.icon = pygame.transform.scale(self.icon,(SQSIZE,HEIGHT/ROWS))
        self.rect = self.icon.get_rect()
        posNum = tileCalc(self.pos)
        self.rect = self.rect.move(tiles[posNum].startPos)
        self.tiles = tiles
        self.tile = tiles[posNum]
        return tiles[posNum]
    def reinforce_trench(self):
        if(self.trench < 1):
            self.trench += 0.2
    def reinforce_org(self):
        if(self.organization < self.initial_org):
            self.organization += self.hp
    def changePos(self,formerPos, pos):
        self.pos = pos
        self.rect = self.rect.move(np.subtract(self.tiles[tileCalc(self.pos)].startPos,self.tiles[tileCalc(formerPos)].startPos))
        self.tile = self.tiles[tileCalc(self.pos)]
        self.trench = 0
    def showOrg(self,screen,pygame):
        Orgbar = (self.tile.endPos[0]-self.tile.startPos[0])*(self.initial_org-self.organization)/self.initial_org
        pygame.draw.line(screen,(0,143,105),(self.tile.startPos[0],self.tile.endPos[1]-3),(self.tile.endPos[0]-Orgbar,self.tile.endPos[1]-3),4)
    def showHP(self,screen,pygame):
        HPbar = (self.tile.endPos[0]-self.tile.startPos[0])*(1-self.hp)
        pygame.draw.line(screen,(128, 0, 0),(self.tile.startPos[0],self.tile.endPos[1]-6),(self.tile.endPos[0],self.tile.endPos[1]-6),3)
    def showTrench(self,screen,pygame):
        Trenchbar = (self.tile.endPos[1]-self.tile.startPos[1])*(1-self.trench)
        pygame.draw.line(screen,(255,205,184),(self.tile.startPos[0]+3,self.tile.startPos[1]+Trenchbar),(self.tile.startPos[0]+3,self.tile.endPos[1]),4)
    def deleteThis(self):
        del(self.rect)
        del(self.icon)
        del(self)

class Ground(Enum):
    flat = (1,0,0,(41, 255, 44))
    hill = (1.5,0,-0.25,(10, 176, 7))
    mountain = (2,0.3,-0.5,(84, 66, 41))
    forest = (1.5,0,-0.15,(0, 125, 48))
    jungle = (1.5,0.2,-0.3,(0, 156, 99))
    marsh = (2,0.35,-0.4,(222, 173, 113))
    desert = (1,0.15,0,(255, 238, 0))
    city = (1.2,0,-0.3,(162, 171, 163))
    sea = "sea"

class base(Army):
    def __init__(self,pos,type):
        self.link_ger = "src/ger_base.png"
        self.link_sov = "src/sov_base.png"
        super().__init__("base",self.link_ger,self.link_sov,1,1,pos,type,0)

class infantry(Army):
    def __init__(self,pos,type):
        self.link_ger = "src/infantry_ger.png"
        self.link_sov = "src/infantry_sov.png"
        super().__init__("infantry",self.link_ger,self.link_sov,5,1,pos,type,1)

class armored(Army):
    def __init__(self,pos,type):
        self.link_ger = "src/armored_ger.png" 
        self.link_sov = "src/armored_sov.png"
        super().__init__("armored",self.link_ger,self.link_sov,8,1,pos,type,2)

class fighter(Army):
    def __init__(self,pos,type):
        self.link_ger = "src/ger_fighter.png"
        self.link_sov = "src/sov_fighter.png"
        super().__init__("fighter",self.link_ger,self.link_sov,1,1,pos,type,7)

class bomber(Army):
    def __init__(self,pos,type):
        self.link_ger = "src/ger_bomber.png" 
        self.link_sov = "src/sov_bomber.png"
        super().__init__("bomber",self.link_ger,self.link_sov,1,1,pos,type,5)

class destroyer(Army):
    def __init__(self):
        self.link_ger = "src/destroyer_ger.png"
        self.link_sov = "src/destroyer_sov.png"


class battleship:
    def __init__(self):
        self.link_ger = "src/battleship_ger.png" 
        self.link_sov = "src/battleship_sov.png"


class cruiser:
    def __init__(self):
        self.link_ger = "src/cruiser_ger.png"
        self.link_sov = "src/cruiser_sov.png"

class submarine:
    def __init__(self):
        self.link_ger = "src/submarine_ger.png" 
        self.link_sov = "src/submarine_sov.png"
