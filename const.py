WIDTH = 700
HEIGHT = 700

ROWS = 16
COLS = 16
SQSIZE = WIDTH / COLS
SPSIZE = HEIGHT / ROWS

SEA_LAND = 0

def tileCalc(pos):
    totalPos = ((pos[1])*COLS)+pos[0]
    return totalPos

def tileExist(pos):
    if((pos[0] < 0 or pos[0] > ROWS-1) or (pos[1] < 0 or pos[1] > ROWS-1)):
        return False
    else:
        return True
        