import pygame
from random import *
from const import *
from objects import *
from tile import *
from board import *
from dragger import *
from rule import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #화면 크기 설정
        self.clock = pygame.time.Clock()
        self.board = Board(pygame,self.screen)
        self.spawnAllArmy()
        self.turn = Turn()
        self.turn.initArmies(self.board.armies)
        self.turn.findAbleArmy()
        self.dragger = Dragger(self.turn)
        self.dragger.game = self
        self.isEnd = False
        self.turn.board = self.board

    def mainloop(self):
        self.screen.fill((255,255,255))
        for tile in self.board.tiles:
            tile.drawColor(self.screen)
        
        self.dragger.showMoveAble(pygame,self.screen)
        self.board.showArmies()
        self.drawLine(color=(0,0,0),line_width=3)
        if(self.isEnd):
            self.gameEnd(self.turn.turn)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(self.dragger.dragging == False):
                    self.dragger.updateMouse(event.pos)
                    clicked_col = int(self.dragger.mousex // SQSIZE)
                    clicked_row = int(self.dragger.mousey // SPSIZE)
                    self.dragger.updatePos(clicked_col,clicked_row)
                    self.dragger.calcAble(self.board.tiles)
                else:
                    self.dragger.DraggerTwiceGo(event.pos,self.board.armies)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_t):
                    self.turn.changeTrun()
                    self.turn.findAbleArmy()
                    self.dragger.turn = self.turn
                    self.dragger.ableArmy = self.turn.ableArmy

        pygame.display.update() #모든 화면 그리기 업데이트
        self.clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
        return "play"
    def drawLine(self, color, line_width):
        for i in range(1,COLS):
            startPos = (i*SQSIZE,0)
            endPos = (i*SQSIZE, WIDTH)
            pygame.draw.line(self.screen, color, startPos, endPos, line_width)
        for i in range(1,ROWS):
            startPos = (0,i*(HEIGHT/ROWS))
            endPos = (WIDTH, i*(HEIGHT/ROWS))
            pygame.draw.line(self.screen, color, startPos, endPos, line_width)           
    def quit(self):
        sys.exit()
    def spawnAllArmy(self):
        spawn = self.board.spawnArmy
        for i in range(0,16,2):
            spawn("ger",infantry,(i,14))
            spawn("sov",infantry,(i,1))
            spawn("ger",armored,(i,10))
            spawn("sov",armored,(i,5))
        for i in range(0,16):
            spawn("ger",infantry,(i,9))
            spawn("sov",infantry,(i,6))
        for i in range(0,16,4):
            spawn("ger",fighter,(i,11))
            spawn("sov",fighter,(i,4))
        for i in range(0,16,5):
            spawn("ger",bomber,(i,12))
            spawn("sov",bomber,(i,3))
        spawn("ger",base,(10,13))
        spawn("sov",base,(10,2))
    def gameEnd(self,Win):
        font = pygame.font.SysFont("arial", 150,True,False)
        text = font.render("{} Win!".format(Win), True, (255,255,255))
        self.screen.blit(text, (100,300))
        print("{} Win!".format(Win))
