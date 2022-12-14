WIDTH = 700
HEIGHT = 700

ROWS = 16
COLS = 16
SQSIZE = WIDTH / COLS
SPSIZE = HEIGHT / ROWS

SEA_LAND = 17

hp_damage_factor = 0.3
trench_defence_factor = 0.7
airPower_factor = 0.4
trench_damage_factor = 0.6
GER_org_up_factor = 0.5
SOV_org_up_factor = 0.8
ace_factor = 0.1
ace_loss_factor = 0.5
ace_loss_decline_factor = 0.2
ace_hp_factor = 0.1
ace_hp_decline_factor = 0.01
max_ace = 15
soft_attack_factor = 0.5
morale = 0.05
addi_morale=0
GER_moral_factor = 1
SOV_moral_factor = 1.1
GER_Attack = 1
SOV_Attack = 1.5

def tileCalc(pos):
    totalPos = ((pos[1])*COLS)+pos[0]
    return totalPos

def tileExist(pos):
    if((pos[0] < 0 or pos[0] > ROWS-1) or (pos[1] < 0 or pos[1] > ROWS-1)):
        return False
    else:
        return True
        
