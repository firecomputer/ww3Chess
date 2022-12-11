from const import *
from math import *


class Turn():
    def __init__(self):
        self.turn = "ger"
        self.ableArmy = []
        self.movedArmy = []
        self.armies = []
        self.tiles = []
        self.board = 0
    def setTiles(self):
        self.board.tiles = self.tiles
    def initArmies(self, armies):
        self.armies = armies
    def findAbleArmy(self):
        ableArmy = []
        for army in self.armies:
            if(army.type == self.turn):
                ableArmy.append(army)
        self.ableArmy = ableArmy
    def deleteAble(self,army):
        if army in self.armies:
            army.trench = 0
            self.movedArmy.append(army)
            if(army in self.ableArmy):
                self.ableArmy.remove(army)
    def changeTrun(self,ger,sov):
        for army in self.armies:
            if army in self.movedArmy:
                pass
            else:
                army.reinforce_trench()
            army.reinforce_org(ger,sov)
        if(self.turn == "ger"):
            self.turn = "sov"
        elif(self.turn == "sov"):
            self.turn = "ger"
            self.movedArmy = []
    def battle(self,tiles,one,two,attack,defence,armies,defence_tile):
        self.armies = armies
        self.tiles = tiles
        defence_trench = two.trench
        attack_org = one.organization
        defence_org = two.organization
        attack_hp = one.hp
        defence_hp = two.hp
        defence_pos = two.pos
        attack_fighter = 0
        attack_bomber = 0
        defence_fighter = 0
        defence_bomber = 0
        airSuperiority = 0
        for i in range(-3,4):
            for j in range(-3,4):
                if(i == 0 and j == 0): continue
                newPos = (defence_pos[0]+i,defence_pos[1]+j)
                army = 0
                if(tileExist(newPos)):
                    army = tiles[tileCalc(newPos)].army
                if(army != 0):
                    if(army.name == "fighter"):
                        if(army.type == attack):
                            attack_fighter += 1+(army.ace*ace_factor)
                        elif(army.type == defence):
                            defence_fighter += 1+(army.ace*ace_factor)
                    elif(army.name == "bomber"):
                        if(army.type == attack):
                            attack_bomber += 1+(army.ace*ace_factor)
                        elif(army.type == defence):
                            defence_bomber += 1+(army.ace*ace_factor)
        if(attack_fighter > defence_fighter):
            airSuperiority = attack
        elif(attack_fighter < defence_fighter):
            airSuperiority = defence
        else:
            airSuperiority = 0
        attackPower = 0
        defencePower = 0
        if(attack_org > 0):
            attackPower += sqrt(attack_org)*attack_hp*soft_attack_factor*one.attack
        attackPower1 = ace_factor*one.ace*attackPower
        if(defence_org > 0):
            defencePower += sqrt(defence_org)*defence_hp*soft_attack_factor
        defencePower1 = ace_factor*two.ace*defencePower
        defencePower2 = defencePower * defence_trench * trench_defence_factor
        attackPower2 = -attackPower * defence_trench * trench_defence_factor
        attackPower3 = 0
        defencePower3 = 0
        if(airSuperiority == attack):
            attackPower3 = attackPower * attack_bomber * airPower_factor
            defencePower3 = -defencePower * attack_bomber * airPower_factor
        elif(airSuperiority == defence):
            defencePower3 = defencePower * defence_bomber * airPower_factor
            attackPower3 = -attackPower * defence_bomber * airPower_factor
        defencePower4 = -defence_tile.panelty * defencePower
        attackPower4 = defence_tile.panelty * attackPower
        if(one.name != "fighter"):
            attackPower += attackPower1+attackPower3#+attackPower2+attackPower4
            defencePower += defencePower1+defencePower3+defencePower2+defencePower4
        else:
            attackPower += attackPower1+attackPower3#+attackPower2+attackPower4
            defencePower += defencePower1+defencePower3
        print("airSuperiority={}".format(airSuperiority))
        if(attackPower > defencePower):
            two.trench -= trench_damage_factor * two.trench
            two.organization -= attackPower*(ace_loss_factor/(two.ace*ace_loss_decline_factor))
            one.organization -= defencePower*(ace_loss_factor/(one.ace*ace_loss_decline_factor))
            if(one.organization < 0):
                one.hp += one.organization*hp_damage_factor*(ace_hp_factor/(one.ace*ace_hp_decline_factor))
                one.organization = 0
            if(two.organization < 0):
                two.hp += two.organization*hp_damage_factor*(ace_hp_factor/(two.ace*ace_hp_decline_factor))
                two.organization = 0
            if(one.hp < 0):
                if one in self.armies:
                    self.armies.remove(one)
                self.board.tiles[tileCalc(one.pos)].army = 0
                self.setTiles()
            if(two.hp < 0):
                if two in self.armies:
                    self.armies.remove(two)
                self.board.tiles[tileCalc(two.pos)].army = 0
                self.setTiles()
            if(one.ace < max_ace):
                one.ace += 1
            if(two.ace < max_ace):
                two.ace += 0.1
            return True
        elif(attackPower <= defencePower):
            two.organization -= attackPower*(ace_loss_factor/(two.ace*ace_loss_decline_factor))
            one.organization -= defencePower*(ace_loss_factor/(one.ace*ace_loss_decline_factor))
            if(one.organization < 0):
                one.hp += one.organization*hp_damage_factor*(ace_hp_factor/(one.ace*ace_hp_decline_factor))
                one.organization = 0
            if(two.organization < 0):
                two.hp += two.organization*hp_damage_factor*(ace_hp_factor/(two.ace*ace_hp_decline_factor))
                two.organization = 0
            if(one.hp < 0):
                if one in self.armies:
                    self.armies.remove(one)
                self.board.tiles[tileCalc(one.pos)].army = 0
                self.setTiles()
            if(two.hp < 0):
                if two in self.armies:
                    self.armies.remove(two)
                self.board.tiles[tileCalc(two.pos)].army = 0
                self.setTiles()
            if(one.ace < max_ace):
                one.ace += 0.1
            if(two.ace < max_ace):
                two.ace += 1
            return False
    def ableRetreat(self,armies,army):
        for i in range(-1,2):
            for j in range(-1,2):
                if(tileExist((army.pos[0]+i,army.pos[1]+j))):
                    tile = self.tiles[tileCalc((army.pos[0]+i,army.pos[1]+j))]
                    if(tile.army == 0):
                        tile.army = army
                        return ((army.pos[0]+i,army.pos[1]+j))
        return 0
