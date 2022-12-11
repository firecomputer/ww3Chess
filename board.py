from const import *
from random import *
from objects import *
from tile import *

class Board(object):
    def __init__(self,pygame,screen):
        self.tiles = []
        self.armies = []
        self.movingArmies = []
        self.screen = screen
        self.pygame = pygame
        self.add_tile()
        self.armyID = 0
    def add_tile(self):
        for i in range(0,ROWS):
            for j in range(0, COLS):
                ground = Ground()
                if(j+1 < SEA_LAND):
                    type = choice([ground.flat, ground.hill, ground.mountain, ground.forest, ground.jungle, ground.marsh, ground.desert, ground.city])
                else:
                    type = ground.sea
                icon = ground.returnIcon(type,self.pygame)
                startPos = (j*SQSIZE,i*SPSIZE)
                endPos = ((j+1)*SQSIZE,(i+1)*SPSIZE)
                newtile = Tile(self.pygame,type,startPos,endPos,self.screen,icon)
                self.tiles.append(newtile)
    def spawnArmy(self,type,target,pos):
        army = target(pos,type,self.armyID)
        self.armyID += 1
        tile = army._iconInit(self.pygame,self.tiles)
        army.board = self
        tile.setArmy(army)
        self.armies.append(army)
    def showArmies(self):
        for army in self.armies:
            army._showArmy(self.screen)
            army.showOrg(self.screen,self.pygame)
            army.showHP(self.screen,self.pygame)
            army.showTrench(self.screen,self.pygame)
        for idx, value in enumerate(self.movingArmies):
            if(value[3] < 100):
                value[0](value[1],value[2],value[3])
                self.movingArmies[idx] = [value[0],value[1],value[2],value[3]+1]
            else:
                self.movingArmies.remove(value)
