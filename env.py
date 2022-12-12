import gym
from game import *
from const import *
import numpy as np
import time

class HOIEnv(gym.Env,gym.utils.EzPickle):
    def __init__(self,isplayable):
        #self.observation_space = gym.spaces.box
        #self.action_space = <gym.space>
        self.game = Game()
        self.armies = self.game.board.armies
        self.country = 0
        self.armyLength = 0
        self.dragger = self.game.dragger
        self.rule = self.game.turn
        self.action_space = gym.spaces.Tuple(tuple(np.array([[gym.spaces.Discrete(COLS),gym.spaces.Discrete(ROWS)] for i in range(0,int(len(self.armies)))]).reshape(len(self.armies)*2)))
        self.observation_space = gym.spaces.Tuple((tuple(np.array([(gym.spaces.Discrete(16),gym.spaces.Discrete(16),gym.spaces.Discrete(2),gym.spaces.Discrete(len(self.armies))) for i in range(0,len(self.armies))]).reshape(len(self.armies)*4))))
        self.isplayable = isplayable

    def setDuraction(self,duraction):
        self.duraction = duraction

    def reset(self):
        self.game.reset()
        self.country = 0
        self.armyLength = 0
        self.dragger = self.game.dragger
        self.rule = self.game.turn
        # reset the environment to initial state
        self.armies = self.game.board.armies
        state = []
        for army in self.armies:
            pos = army.pos
            if(army.type == "ger"):
                newType = 0
            else:
                newType = 1
            newId = army.id
            state.append([pos[0],pos[1],newType,newId])
        state = np.array([state]).reshape(len(self.armies)*4)
        state = np.append(np.array(self.country),state)
        state = list(state)
        return [state,state]

    def step(self, action):
        self.game.mainloop()
        self.armies = self.game.board.armies
        state = [[],[]]
        newPos = []
        newIds = []
        newId = [0,0]
        reward = [0,0]
        info = [0,0]
        done = False
        if(self.isplayable == 1 and self.country == 0):
            if(self.game.turn.turn == "ger"):
                self.country = 0
            else:
                self.country = 1
            return
        for i in range(self.isplayable,2):
            newPos = []
            idx = 0
            lastNum = -1
            for army in self.armies:

                if(army.number != lastNum+1):
                    while(army.number > lastNum+1):
                        state[i].append([None,None,None,None])
                        if((army.type == "ger" and self.country == 0) or (army.type == "sov" and self.country == 1)):
                            newPos.append((None,None))
                        lastNum += 1
                pos = army.pos
                if(army.type == "ger"):
                    newType = 0
                else:
                    newType = 1
                newId = army.id
                state[i].append([pos[0],pos[1],newType,newId])
                lastNum += 1
                if((army.type == "ger" and self.country == 0) or (army.type == "sov" and self.country == 1)):
                    newPos.append(pos)
            state[i] = np.array(state[i]).reshape((lastNum+1)*4)
            state[i] = np.append(np.array(self.country),state[i])
            state[i] = list(state[i])
            if(done == True):
                break
            if((self.game.turn.turn == "ger" and self.country == 0) or (self.game.turn.turn == "sov" and self.country == 1)):
                for idx,Pos in enumerate(newPos):
                    if(Pos[0] == None or Pos[1] == None):
                        continue
                    thisTile = self.game.board.tiles[tileCalc(Pos)]
                    thisArmy = thisTile.army
                    tileStartPosition = (thisTile.startPos[0],thisTile.startPos[1])
                    self.dragger.updateMouse(tileStartPosition)
                    self.dragger.updatePos(Pos[0], Pos[1])
                    #print(thisTile in self.rule.ableArmy, Pos[1])
                    self.dragger.calcAble(self.game.board.tiles)
                    thisArmyAction = (action[idx+(i*len(newPos))],action[idx+1+(i*len(newPos))])
                    AbleTiles = self.dragger.sideTiles
                    if(len(AbleTiles) > 0 and self.game.dragger.tiles[tileCalc(thisArmyAction)] != thisTile):
                        actionTilePos = self.game.dragger.tiles[tileCalc(thisArmyAction)]
                        actionTileStartPos = actionTilePos.startPos
                        shortestDistance = 999999
                        shortestTileId = -1
                        for idx, AbleTile in enumerate(AbleTiles):
                            if(np.linalg.norm(np.subtract(AbleTile.startPos,actionTileStartPos)) < shortestDistance):
                                shortestDistance = np.linalg.norm(np.subtract(AbleTile.startPos,actionTileStartPos))
                                shortestTileId = idx
                        for idx, AbleTile in enumerate(AbleTiles):
                            if(AbleTile.army != 0):
                                if(AbleTile.army.name == "base"):
                                    if((AbleTile.army.type == "ger" and self.country == 1) or (AbleTile.army.type == "sov" and self.country == 0)):
                                        shortestDistance = np.linalg.norm(np.subtract(AbleTile.startPos,actionTileStartPos))
                                        shortestTileId = idx
                        shortestTile = AbleTiles[shortestTileId]
                        shortestTilePos = (shortestTile.startPos[0],shortestTile.startPos[1])
                        self.dragger.updateMouse(shortestTilePos)
                        clicked_col = int(self.dragger.mousex // SQSIZE)
                        clicked_row = int(self.dragger.mousey // SPSIZE)
                        self.dragger.updatePos(clicked_col, clicked_row)
                        result = self.dragger.DraggerTwiceGo((clicked_col,clicked_row), self.game.board.armies)
                        enemyBase = 0
                        distance = 0
                        if(self.country == 0):
                            enemyBase = self.dragger.tiles[tileCalc((10,2))].startPos
                            distance = np.linalg.norm(np.subtract(enemyBase, shortestTilePos))
                        else:
                            enemyBase = self.dragger.tiles[tileCalc((10,13))].startPos
                            distance = np.linalg.norm(np.subtract(enemyBase, shortestTilePos))
                        if(result == 1):
                            win = self.country
                            if(self.country == 1):
                                print("WIN == SOV")
                            else:
                                print("WIN == GER")
                            reward[i] += 0.01
                        elif(result == 0):
                            if(self.country == 0):
                                win = 1
                                print("WIN == SOV")
                            else:
                                win = 0
                                print("WIN == GER")
                        elif(result == -2):
                            reward[i] += 2
                            done = True
                        elif(result == -1):
                            print("An error occured: tile does not exists")
                        if(self.isplayable == 0):
                            for j in range(0,self.game.fast):
                                self.game.mainloop()
                        else:
                            for j in range(0,10):
                                self.game.mainloop()
                    else:
                        #reward[i] -= 0.001
                        pass
            if(self.country == 0):
                self.country = 1
            else:
                self.country = 0
            self.rule.changeTrun(self.dragger.ger_factor,self.dragger.sov_factor)
            self.rule.findAbleArmy()
            self.dragger.turn = self.rule
            self.dragger.ableArmy = self.rule.ableArmy
        self.game.mainloop()
            
        # perform one step in the game logic
        return state, reward, done, info