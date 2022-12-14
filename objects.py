from enum import Enum
from const import *
import numpy as np

class Army:
    def __init__(self,name,ger_link,sov_link,organization,hp,pos,type,speed,attack,id,number):
        self.id = id
        self.number = number
        self.name = name
        self.ger_link = ger_link
        self.sov_link = sov_link
        self.organization = organization
        self.initial_org = organization
        self.hp = hp
        self.pos = pos
        self.attack = attack
        self.type = type
        self.speed = speed
        self.tiles = []
        self.tile = 0
        self.trench = 0
        self.ace = 1
        self.board = 0
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
            self.trench += 0.2*self.organization/self.initial_org
    def reinforce_org(self,ger_factor,sov_factor):
        if(self.organization < self.initial_org):
            if(self.type == "ger"):
                self.organization += self.hp*GER_org_up_factor+ger_factor
            elif(self.type == "sov"):
                self.organization += self.hp*SOV_org_up_factor+sov_factor
    def changePos(self,formerPos, pos,progress):
        if(progress < 10):
            self.pos = pos
            distance = (np.subtract(self.tiles[tileCalc(self.pos)].startPos,self.tiles[tileCalc(formerPos)].startPos))
            distance = (distance/10)
            distance_batch = distance
            self.rect.move_ip(distance_batch)
            self.tile = self.tiles[tileCalc(self.pos)]
            self.trench = 0
            if(progress == 0):
                self.board.movingArmies.append([self.changePos,formerPos, pos, progress+1])
            if(progress >= 9):
                self.rect.update((self.tiles[tileCalc(self.pos)].startPos),(SQSIZE,SPSIZE))
        
    def showOrg(self,screen,pygame):
        Orgbar = (self.tile.endPos[0]-self.tile.startPos[0])*(self.initial_org-self.organization)/self.initial_org
        pygame.draw.line(screen,(0,143,105),(self.tile.startPos[0],self.tile.endPos[1]-3),(self.tile.endPos[0]-Orgbar,self.tile.endPos[1]-3),4)
    def showHP(self,screen,pygame):
        HPbar = (self.tile.endPos[0]-self.tile.startPos[0])*(1-self.hp)
        pygame.draw.line(screen,(128, 0, 0),(self.tile.startPos[0],self.tile.endPos[1]-6),(self.tile.endPos[0]-HPbar,self.tile.endPos[1]-6),3)
    def showTrench(self,screen,pygame):
        Trenchbar = (self.tile.endPos[1]-self.tile.startPos[1])*(1-self.trench)
        pygame.draw.line(screen,(255,205,184),(self.tile.startPos[0]+3,self.tile.startPos[1]+Trenchbar),(self.tile.startPos[0]+3,self.tile.endPos[1]),4)
    def deleteThis(self):
        del(self.rect)
        del(self.icon)
        del(self)

class Ground():
    def __init__(self):
        self.flat = (1,0,0,"src/flat.jpg")
        self.hill = (1.5,0,-0.25,"src/hill.jpg")
        self.mountain = (2,0.3,-0.5,"src/mountain.jpg")
        self.forest = (1.5,0,-0.15,"src/forest.jpg")
        self.jungle = (1.5,0.2,-0.3,"src/jungle.jpg")
        self.marsh = (2,0.35,-0.4,"src/marsh.jpg")
        self.desert = (1,0.15,0,"src/sand.jpg")
        self.city = (1.2,0,-0.3,"src/city.jpg")
        self.sea = "src/sea.jpg"
    def returnIcon(self,land,pygame):
        if(land != "src/sea.jpg"):
            return pygame.image.load(land[3])
        else:
            return pygame.image.load(land)

class base(Army):
    def __init__(self,pos,type,number):
        self.link_ger = "src/ger_base.png"
        self.link_sov = "src/sov_base.png"
        super().__init__("base",self.link_ger,self.link_sov,1,1,pos,type,0,1,0,number)

class infantry(Army):
    def __init__(self,pos,type,number):
        self.link_ger = "src/infantry_ger.png"
        self.link_sov = "src/infantry_sov.png"
        super().__init__("infantry",self.link_ger,self.link_sov,5,1,pos,type,1,1.3,1,number)

class armored(Army):
    def __init__(self,pos,type,number):
        self.link_ger = "src/armored_ger.png" 
        self.link_sov = "src/armored_sov.png"
        super().__init__("armored",self.link_ger,self.link_sov,10,1,pos,type,2,2,2,number)

class fighter(Army):
    def __init__(self,pos,type,number):
        self.link_ger = "src/ger_fighter.png"
        self.link_sov = "src/sov_fighter.png"
        super().__init__("fighter",self.link_ger,self.link_sov,15,1,pos,type,7,1,3,number)

class bomber(Army):
    def __init__(self,pos,type,number):
        self.link_ger = "src/ger_bomber.png" 
        self.link_sov = "src/sov_bomber.png"
        super().__init__("bomber",self.link_ger,self.link_sov,10,1,pos,type,5,1,4,number)

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
