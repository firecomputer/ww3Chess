from const import *
from rule import *

class Dragger:
    def __init__(self,turn):
        self.selectedArmy = 0
        self.mousex = 0
        self.mousey = 0
        self.initialRow = 0
        self.initialCol = 0
        self.afterCol = 0
        self.afterRow = 0
        self.sideTiles = []
        self.dragging = False
        self.turn = turn
        self.ableArmy = self.turn.ableArmy
        self.armies = []
        self.game = 0
    def updateMouse(self,pos):
        self.mousex = pos[0]
        self.mousey = pos[1]
    def updatePos(self,col,row):
        self.initialCol = col
        self.initialRow = row
    def calcAble(self, tiles):
        self.tiles = tiles
        nowTile = tiles[tileCalc((self.initialCol,self.initialRow))]
        self.selectedArmy = nowTile.army
        if self.selectedArmy not in self.ableArmy:
            return
        if(self.selectedArmy == 0):
            return
        self.dragging = True
        speed = self.selectedArmy.speed
        sideTiles = []
        for t in range(-1,2):
            for j in range(-1,2):
                if(t == 0 and j == 0): continue
                if((self.selectedArmy.name =="infantry") and (t!=0 and j!= 0)): continue
                for i in range(1,speed+1):
                    pos = (self.initialCol+(i*t),self.initialRow+(i*j))
                    if(tileExist(pos)):
                        sideTile = tiles[tileCalc(pos)]
                        if(sideTile.army == 0):
                            sideTiles.append(sideTile)
                            #print(pos)
                        elif(sideTile.army.type != self.selectedArmy.type):
                            if(sideTile.army.name == "fighter" or sideTile.army.name == "bomber"):
                                pass
                            elif(self.selectedArmy.name != "fighter" and self.selectedArmy.name != "bomber"):
                                sideTiles.append(sideTile)
                                break
                            else:
                                pass
        self.sideTiles = sideTiles
    def showMoveAble(self,pygame,screen):
        self.color = (50, 50, 255)
        for Tile in self.sideTiles:
            color = ((self.color[0]+Tile.color[0])//2,(self.color[1]+Tile.color[1])//2,(self.color[2]+Tile.color[2])//2)
            pygame.draw.rect(screen,color,[Tile.startPos[0],Tile.startPos[1],SQSIZE,SPSIZE])

    def DraggerTwiceGo(self,pos,armies):
        self.updateMouse(pos)
        self.armies = armies
        self.afterCol = int(self.mousex // SQSIZE)
        self.afterRow = int(self.mousey // SPSIZE)
        if(self.posIsAble()):
            self.dragging = False
            self.defence_tile = self.tiles[tileCalc((self.afterCol,self.afterRow))]
            if(self.defence_tile.army != 0):
                self.defence_army = self.defence_tile.army
                if(self.defence_army.name == 'base'):
                    self.game.isEnd = True
                    return
                attack_wining = self.turn.battle(self.tiles,self.selectedArmy,self.defence_army,self.turn.turn,self.defence_army.type,self.armies,self.defence_tile)
                if(attack_wining):
                    retreatTile = self.turn.ableRetreat(self.armies,self.defence_army)
                    if(retreatTile != 0):
                        self.tiles[tileCalc(retreatTile)].army = self.defence_army
                        self.defence_army.changePos(self.defence_army.pos,retreatTile)
                        self.selectedArmy.changePos((self.initialCol,self.initialRow),(self.afterCol,self.afterRow))
                        self.tiles[tileCalc((self.initialCol,self.initialRow))].army = 0
                        self.tiles[tileCalc((self.afterCol,self.afterRow))].army = self.selectedArmy
                    self.sideTiles = []
                    self.turn.deleteAble(self.selectedArmy)
                else:
                    self.turn.deleteAble(self.selectedArmy)
                    self.sideTiles = []
            else:
                self.selectedArmy.changePos((self.initialCol,self.initialRow),(self.afterCol,self.afterRow))
                self.tiles[tileCalc((self.initialCol,self.initialRow))].army = 0
                self.tiles[tileCalc((self.afterCol,self.afterRow))].army = self.selectedArmy
                self.sideTiles = []
                self.turn.deleteAble(self.selectedArmy)
        else:
            self.dragging = False
            self.sideTiles = []
    def posIsAble(self):
        if self.tiles[tileCalc((self.afterCol,self.afterRow))] in self.sideTiles:
            return True
        else:
            return False
