import pygame
from random import *
from const import *
from objects import *
from tile import *
from board import *
from dragger import *
from rule import *

import cv2
from google.colab.patches import cv2_imshow
from google.colab import output
import time 
import os, sys

# set SDL to use the dummy NULL video driver, 
#   so it doesn't need a windowing system.
os.environ["SDL_VIDEODRIVER"] = "dummy"


class Game:
    def __init__(self):
        pygame.display.init()
        info = pygame.display.Info()
        screensize = info.current_w,info.current_h
        print(screensize)
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
        self.fast = 0

    def reset(self):
        pygame.display.quit()
        pygame.quit()
        pygame.init()
        info = pygame.display.Info()
        screensize = info.current_w,info.current_h
        print(screensize)
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
        pygame.display.flip()

        #convert image so it can be displayed in OpenCV
        view = pygame.surfarray.array3d(screen)

        #  convert from (width, height, channel) to (height, width, channel)
        view = view.transpose([1, 0, 2])

        #  convert from rgb to bgr
        img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)

        #Display image, clear cell every 0.5 seconds
        cv2_imshow(img_bgr)
        time.sleep(0.5)
        output.clear()
        self.screen.fill((255,255,255))
        for tile in self.board.tiles:
            tile.drawColor(self.screen)
        
        self.dragger.showMoveAble(pygame,self.screen)
        self.board.showArmies()
        self.drawLine(color=(0,0,0),line_width=3)
        self.confirmTile()
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
                    self.dragger.updateMouse(event.pos)
                    clicked_col = int(self.dragger.mousex // SQSIZE)
                    clicked_row = int(self.dragger.mousey // SPSIZE)
                    self.dragger.DraggerTwiceGo((clicked_col,clicked_row),self.board.armies)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_t):
                    self.turn.changeTrun(self.dragger.ger_factor,self.dragger.sov_factor)
                    self.turn.findAbleArmy()
                    self.dragger.turn = self.turn
                    self.dragger.ableArmy = self.turn.ableArmy
                if(event.key == pygame.K_a):
                    if(self.fast > 0):
                        self.fast -= 1
                if(event.key == pygame.K_s):
                    self.fast += 1

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

    def confirmTile(self):
        for tile in self.board.tiles:
            if(tile.army != 0):
                if(tile.army.pos != (tile.startPos[0]//SQSIZE,tile.startPos[1]//SQSIZE)):
                    tile.army = 0
    def gameEnd(self,Win):
        font = pygame.font.SysFont("arial", 150,True,False)
        if(Win == "ger"):
            text = font.render("{} Win!".format("KOR"), True, (0,0,255))
        else:
            text = font.render("{} Win!".format("CHI"), True, (255,0,0))
        self.screen.blit(text, (100,300))
        print("{} Win!".format(Win))
