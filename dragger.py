from const import *
from rule import *
import asyncio

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
        self.sov_factor=0
        self.ger_factor=0
        self.loop = asyncio.get_event_loop()
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

        if(type(self.selectedArmy) == int):
            print("that tile has no army")
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
                        if(t!= 0 and j!= 0):
                            isdefended = self.checkDragDefenced(t,j,(self.initialCol+((i-1)*t),self.initialRow+((i-1)*j)),sideTile,tiles)
                            if(isdefended):
                                break
                        if(sideTile.army == 0):
                            sideTiles.append(sideTile)
                            #print(pos)
                        elif(sideTile.army.type != self.selectedArmy.type):
                            if(sideTile.army.name == "fighter" or sideTile.army.name == "bomber"):
                                if(self.selectedArmy.name == "fighter" or self.selectedArmy.name == "bomber"):
                                    sideTiles.append(sideTile)
                                    break
                            elif(self.selectedArmy.name != "fighter" and self.selectedArmy.name != "bomber"):
                                sideTiles.append(sideTile)
                                break
                            else:
                                pass
        self.sideTiles = sideTiles
    def showMoveAble(self,pygame,screen):
        self.color = (0, 0, 255)
        for Tile in self.sideTiles:
            s = pygame.Surface((SPSIZE,SQSIZE))  # the size of your rect
            s.set_alpha(90)                # alpha level
            s.fill(self.color)           # this fills the entire surface
            screen.blit(s, Tile.startPos)    # (0,0) are the top-left coordinates

    def checkDragDefenced(self,x,y,pos,tile,tiles):
        leftPos = (pos[0]+x,pos[1])
        rightPos = (pos[0],pos[1]+y)
        if(tileExist(leftPos)==False or tileExist(rightPos)==False):
            return False
        leftTile = tiles[tileCalc(leftPos)]
        upTile = tiles[tileCalc(rightPos)]
        if(leftTile.army != 0 and upTile.army != 0):
            print("army is blocking...")
            if(leftTile.army.type != self.selectedArmy.type and upTile.army.type != self.selectedArmy.type):
                print("we could not go drag cause enemy defence it")
                return True
        return False
    def DraggerTwiceGo(self,pos,armies):
        self.tiles = self.game.board.tiles
        self.armies = armies
        self.afterCol = int(self.mousex // SQSIZE)
        self.afterRow = int(self.mousey // SPSIZE)
        attackWin = -1
        if(self.posIsAble()):
            self.dragging = False
            self.defence_tile = self.tiles[tileCalc((self.afterCol,self.afterRow))]
            if(self.defence_tile.army != 0):
                self.defence_army = self.defence_tile.army
                if(self.defence_army.name == 'base'):
                    self.game.isEnd = True
                    return -2
                attack_wining = self.turn.battle(self.tiles,self.selectedArmy,self.defence_army,self.turn.turn,self.defence_army.type,self.armies,self.defence_tile)
                if(attack_wining):
                    retreatTile = self.turn.ableRetreat(self.armies,self.defence_army)
                    if(retreatTile != 0):
                        self.tiles[tileCalc(retreatTile)].army = self.defence_army
                        self.defence_army.changePos(self.defence_army.pos,retreatTile,0)
                        self.selectedArmy.changePos((self.initialCol,self.initialRow),(self.afterCol,self.afterRow),0)
                        self.game.board.tiles[tileCalc((self.initialCol,self.initialRow))].army = 0
                        self.game.board.tiles[tileCalc((self.afterCol,self.afterRow))].army = self.selectedArmy
                    self.sideTiles = []
                    self.turn.deleteAble(self.selectedArmy)
                    if(self.selectedArmy.type == "ger"):
                        if(self.sov_factor > morale*GER_moral_factor):
                            self.ger_factor += morale*GER_moral_factor
                            self.sov_factor -= morale*GER_moral_factor
                        else:
                            self.ger_factor += addi_morale
                    else:
                        if(self.ger_factor > morale*SOV_moral_factor):
                            self.ger_factor -= morale*SOV_moral_factor
                            self.sov_factor += morale*SOV_moral_factor
                        else:
                            self.sov_factor += addi_morale
                else:
                    self.turn.deleteAble(self.selectedArmy)
                    self.sideTiles = []
                if(attack_wining):
                    return 1
                else:
                    return 0
            else:
                self.selectedArmy.changePos((self.initialCol,self.initialRow),(self.afterCol,self.afterRow),0)
                self.game.board.tiles[tileCalc((self.initialCol,self.initialRow))].army = 0
                self.game.board.tiles[tileCalc((self.afterCol,self.afterRow))].army = self.selectedArmy
                self.sideTiles = []
                self.turn.deleteAble(self.selectedArmy)
                return -1
        else:
            self.dragging = False
            self.sideTiles = []
            return -1
    def posIsAble(self):
        if self.tiles[tileCalc((self.afterCol,self.afterRow))] in self.sideTiles:
            return True
        else:
            return False
