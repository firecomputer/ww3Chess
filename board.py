from const import *
from random import *
from objects import *
from tile import *

class Board(object):
    def __init__(self,pygame,screen):
        self.tiles = []
        self.armies = []
        self.screen = screen
        self.pygame = pygame
        self.add_tile()
    def add_tile(self):
        for i in range(0,ROWS):
            for j in range(0, COLS):
                if(j+1 >= SEA_LAND):
                    type = choice([Ground.flat, Ground.hill, Ground.mountain, Ground.forest, Ground.jungle, Ground.marsh, Ground.desert, Ground.city]).value
                else:
                    type = Ground.sea.value
                startPos = (j*SQSIZE,i*(HEIGHT/ROWS))
                endPos = ((j+1)*SQSIZE,(i+1)*(HEIGHT/ROWS))
                newtile = Tile(self.pygame,type,startPos,endPos,self.screen)
                self.tiles.append(newtile)
    def spawnArmy(self,type,target,pos):
        army = target(pos,type)
        tile = army._iconInit(self.pygame,self.tiles)
        tile.setArmy(army)
        self.armies.append(army)
    def showArmies(self):
        for army in self.armies:
            army._showArmy(self.screen)
            army.showOrg(self.screen,self.pygame)
            army.showHP(self.screen,self.pygame)
