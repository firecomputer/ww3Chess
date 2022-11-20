from const import *
from math import *

class Turn():
    def __init__(self):
        self.turn = "ger"
        self.ableArmy = []
        self.movedArmy = []
        self.armies = []
        self.tiles = []
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
            self.ableArmy.remove(army)
    def changeTrun(self):
        for army in self.armies:
            if army in self.movedArmy:
                army.trench = 0
            else:
                army.reinforce_trench()
            army.reinforce_org()
        if(self.turn == "ger"):
            self.turn = "sov"
        elif(self.turn == "sov"):
            self.turn = "ger"
    def battle(self,tiles,one,two,attack,defence,armies,defence_tile):
        self.armies = armies
        self.tiles = tiles
        defence_trench = one.trench
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
                army = tiles[tileCalc(newPos)].army
                if(army != 0):
                    if(army.name == "fighter"):
                        if(army.type == attack):
                            attack_fighter += 1
                        elif(army.type == defence):
                            defence_fighter += 1
                    elif(army.name == "bomber"):
                        if(army.type == attack):
                            attack_bomber += 1
                        elif(army.type == defence):
                            defence_bomber += 1
        if(attack_fighter > defence_fighter):
            airSuperiority = attack
        elif(attack_fighter < defence_fighter):
            airSuperiority = defence
        else:
            airSuperiority = 0
        attackPower = 0
        defencePower = 0
        print(defence_org)
        print(defence_hp)
        attackPower += sqrt(attack_org)*attack_hp*0.5
        defencePower += sqrt(defence_org)*defence_hp*0.5
        defencePower += defencePower * defence_trench * 0.4
        if(airSuperiority == attack):
            attackPower += attackPower * attack_bomber * 0.2
        elif(airSuperiority == defence):
            defencePower += defencePower * defence_bomber * 0.2
        attackPower -= defence_tile.panelty * attackPower
        print(airSuperiority)
        hp_damage_factor = 0.15
        if(attackPower > defencePower):
            two.trench = 0
            two.organization -= attackPower
            one.organization -= defencePower
            if(one.organization < 0):
                one.hp += one.organization*hp_damage_factor
                one.organization = 0
            if(two.organization < 0):
                two.hp += two.organization*hp_damage_factor
                two.organization = 0
            if(one.hp < 0):
                self.armies.remove(one)
                self.tiles[tileCalc(one.pos)].army = 0
            if(two.hp < 0):
                self.armies.remove(two)
                self.tiles[tileCalc(two.pos)].army = 0
            return True
        elif(attackPower <= defencePower):
            two.trench = 0
            two.organization -= attackPower
            one.organization -= defencePower
            if(one.organization < 0):
                one.hp += one.organization*hp_damage_factor
                one.organization = 0
            if(two.organization < 0):
                two.hp += two.organization*hp_damage_factor
                two.organization = 0
            if(one.hp < 0):
                self.armies.remove(one)
                self.tiles[tileCalc(one.pos)].army = 0
            if(two.hp < 0):
                self.armies.remove(two)
                self.tiles[tileCalc(two.pos)].army = 0
            return False
    def ableRetreat(self,armies,army):
        for i in range(-1,2):
            for j in range(-1,2):
                if(tileExist((army.pos[0]+i,army.pos[1]+j))):
                    tile = self.tiles[tileCalc((army.pos[0]+i,army.pos[1]+j))]
                    if(tile.army == 0):
                        tile.army = army
                        return ((army.pos[0]+i,army.pos[1]+j))
        armies.remove(army)
        army.deleteThis()
        return 0