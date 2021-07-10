import sys
import time
import datetime
import numpy as np
import brick
from os import system
from paddle import *
from ball import *
import math
import random
import global_stuff
from colorama import Fore, Style, Style

from typing import Any

from bullets import *
from ufo import *
from ufo_ascii import *
from bombs import *
from laser import *
import os


class board():
    def __init__(self, rows, columns, score=0, strttime=0, lives_left=10):
        self._rows: Any=rows
        self._columns: Any=columns
        self._board: Any = np.empty(shape=(rows+1, columns+1), dtype=np.object)
        self._paddle: Any = paddle(rows-1,columns/2)
        posn=getattr(random, "randint")(int(self._paddle.y), int(self._paddle.y+self._paddle.length))
        dist_from_centre=getattr(self, "_paddle").get_left_coor()+(self._paddle.get_length())/2-posn
        factor_change=getattr(math, "floor")(dist_from_centre/2.5)
        y_vel=-factor_change*0.5
        self._balls: Any = [ball(rows-2, posn, -1, y_vel)]
        self._powerups: Any =[]
        self.score: Any=score
        self.remaining_lives: Any=lives_left
        if strttime==0:
            self.start_time: Any=time.time()
        else:
            self.start_time: Any=strttime
        self.game_on: Any=1
        self.level_time: Any=time.time()
        self._bullets: Any=[]
        self.max_score: Any=0
        self.ufo: Any=None
        self.bombs: Any=[]
        self.frame_no: Any=0

    def getdim(self):
        return (getattr(self, "_rows"), getattr(self, "_columns"))
    
    def get_brick(self, x, y, typ):
        if typ==0:
            return getattr(brick,"brick1")(x,y)
        elif typ==1:
            return  getattr(brick,"brick2")(x,y)
        elif typ==2:
            return getattr(brick,"brick3")(x,y)
        elif typ==3:
            return getattr(brick,"brick4")(x,y)
        elif typ==4:
            return getattr(brick,"brickfixed")(x,y)
        elif typ==5:
            return getattr(brick,"explodingbrick")(x,y)
        else:
            return None
    
    def createlevel2(self):
        for x in range(6, 22, 2):
            y=1
            while y<116:
                if getattr(self, "_board")[x][y]:
                    y+=1
                    continue
                ob=getattr(self,"get_random_brick")(x,y)
                for k in range(6):
                    for h in range(2):
                        self._board[x+h][y+k]=ob
                if ob:
                    y+=5
                else:
                    y+=1
    
    def createlevel3(self):
        arr=[[16, 6, 1], [16, 18, 2], [16, 24, 3], [16, 30, 4], [16, 42, 3], [16, 48, 4], [16, 54, 1], [16, 60, 4], [16, 66, 1], [16, 72, 2], [16, 78, 3], [16, 84, 4], [16, 90, 0], [16, 96, 1], [16, 102, 2], [16, 108, 3], [16, 114, 4]]
        arr2=[[2, 18, 3], [2, 24, 2], [2, 30, 4], [2, 42, 4], [2, 48, 1], [2, 54, 0], [2, 60, 1], [2, 66, 2], [2, 72, 4], [2, 78, 1], [2, 84, 0], [2, 90, 4], [2, 96, 3], [2, 102, 4], [2, 108, 2], [2, 114, 1]]
        arr3=[[2,30,5],[2,36,5],[2,42,5],[4,36,5],[2,42,5],[2,48,5]]
        arr4=[[4, 6, 3], [4, 18, 4], [4, 24, 2], [4, 30, 3], [4, 42, 2], [4, 48, 0], [4, 54, 4], [4, 60, 4], [4, 66, 2], [4, 72, 1], [4, 78, 2], [4, 84, 4], [4, 90, 2], [4, 96, 4], [4, 102, 3], [4, 108, 4], [4, 114, 1], [6, 6, 4], [6, 24, 0], [6, 30, 1], [6, 42, 1], [6, 48, 4], [6, 54, 3], [6, 60, 0], [6, 66, 1], [6, 72, 2], [6, 78, 2], [6, 84, 4], [6, 90, 4], [6, 96, 0], [6, 102, 1], [6, 108, 0], [6, 114, 2], [8, 6, 0], [8, 18, 3], [8, 24, 0], [8, 30, 0], [8, 42, 0], [8, 48, 4], [8, 54, 1], [8, 60, 1], [8, 66, 4], [8, 72, 2], [8, 78, 1], [8, 84, 4], [8, 90, 1], [8, 96, 2], [8, 102, 0], [8, 108, 4], [8, 114, 4], [10, 6, 1], [10, 18, 2], [10, 24, 4], [10, 30, 4], [10, 42, 4], [10, 48, 2], [10, 54, 0], [10, 60, 3], [10, 66, 0], [10, 72, 2], [10, 78, 2], [10, 84, 3], [10, 90, 0], [10, 96, 0], [10, 102, 3], [10, 108, 0], [10, 114, 3], [12, 6, 2], [12, 18, 3], [12, 24, 3], [12, 30, 2], [12, 42, 0], [12, 48, 0], [12, 54, 0], [12, 60, 2], [12, 66, 4], [12, 72, 4], [12, 78, 1], [12, 84, 1], [12, 90, 0], [12, 96, 2], [12, 102, 1], [12, 108, 2], [12, 114, 1], [14, 6, 2], [14, 18, 1], [14, 24, 3], [14, 30, 1], [14, 42, 3], [14, 48, 3], [14, 54, 2], [14, 60, 3], [14, 66, 2], [14, 72, 4], [14, 78, 3], [14, 84, 4], [14, 90, 0], [14, 96, 3], [14, 102, 1], [14, 108, 3], [14, 114, 3]]
        arr5=[[2, 6, 5], [4, 12, 5], [6, 18, 5], [8, 24, 5], [10, 30, 5], [12, 36, 5], [14, 36, 5]]
        arr = arr+arr2+arr3+arr4+arr5
        for typ in arr:
            ob=getattr(self,"get_brick")(typ[0],typ[1],typ[2])
            for a in range(6):
                    self._board[typ[0]][typ[1]+a]=ob
    
    def createlevel1(self):
        arr=[[4, 18, 2], [4, 24, 0], [4, 30, 2], [4, 36, 1], [4, 42, 2], [4, 48, 1], [6, 18, 1], [6, 24, 1], [6, 30, 1], [6, 36, 2], [6, 42, 2], [6, 48, 2], [8, 18, 2], [8, 24, 2], [8, 30, 1], [8, 36, 4], [8, 42, 2], [8, 48, 3], [10, 18, 3], [10, 24, 4], [10, 30, 3], [10, 36, 1], [10, 42, 2], [10, 48, 3], [12, 18, 1], [12, 24, 3], [12, 30, 1], [12, 36, 0], [12, 42, 1], [12, 48, 0], [14, 18, 4], [14, 24, 0], [14, 30, 2], [14, 36, 3], [14, 42, 0], [14, 48, 1]]
        arr2=[[4, 60, 0], [4, 66, 2], [4, 72, 0], [4, 78, 2], [4, 84, 0], [4, 90, 2], [6, 60, 0], [6, 66, 0], [6, 72, 0], [6, 78, 0], [6, 84, 0], [6, 90, 0], [8, 60, 4], [8, 66, 2], [8, 72, 0], [8, 78, 1], [8, 84, 4], [8, 90, 2], [10, 60, 0], [10, 66, 1], [10, 72, 2], [10, 78, 3], [10, 84, 4], [10, 90, 0], [12, 60, 0], [12, 66, 1], [12, 72, 0], [12, 78, 1], [12, 84, 0], [12, 90, 1], [14, 60, 4], [14, 66, 0], [14, 72, 2], [14, 78, 3], [14, 84, 0], [14, 90, 1]]
        arr3=[[4, 102, 2], [4, 108, 1], [4, 114, 0], [4, 120, 4], [6, 102, 2], [6, 108, 0], [6, 114, 0], [6, 120, 0], [8, 102, 0], [8, 108, 2], [8, 114, 1], [8, 120, 0], [10, 102, 0], [10, 108, 1], [10, 114, 0], [10, 120, 0], [12, 102, 2], [12, 108, 4], [12, 114, 0], [12, 120, 1], [14, 102, 4], [14, 108, 2], [14, 114, 0], [14, 120, 1]]
        arr4=[[4,18,5],[4,24,5],[5,24,5],[6,30,5],[7,36,5],[8,36,5]]
        arr5=[[10,36,5],[11,36,5],[12,30,5],[13,24,5],[14,24,5],[15,18,5]]
        arr = arr + arr2 + arr3 + arr4 + arr5
        for typ in arr:
            ob=getattr(self,"get_brick")(typ[0],typ[1],typ[2])
            for a in range(6):
                    self._board[typ[0]][typ[1]+a]=ob

    def liveslost(self):
        self.remaining_lives-=1
        getattr(self,"finish_powerups")()
        if getattr(self, "remaining_lives") == 0:
            system('clear')
            self.gameon=-1

        else:
            a=random.randint(getattr(self, "_paddle").y, self._paddle.y+self._paddle.length)
            self._balls=[ball(global_stuff.rows-2, a)]

    def finish_powerups(self):
        for powu in getattr(self, "_powerups"):
            if powu.remaining_time>0:
                getattr(self, "_powerups").remove(powu)
                getattr(powu,"deactivate")(self)
        self._powerups=[]

    def printboard(self):
        print_str=""
        print_str+="LIVES: "+str(getattr(self, "remaining_lives"))+"\t"+"TIME: "+str(datetime.timedelta(seconds=int(time.time()-self.start_time)))+"\t"+"SCORE: "+str(self.score)
        for powu in getattr(self, "_powerups"):
            if powu.remaining_time>0:
                print_str+=powu.icon
        curlen=len(print_str)
        for y in range(getattr(global_stuff, "cols")+1-curlen):
            print_str+=" "
        print_str+="\n"
        for y in range(getattr(global_stuff, "cols")+1):
            print_str+="\u23AF"
        print_str+="\n"
        for x in range(global_stuff.rows+1):
            print_str+="\u23B9"
            y=0
            while y<len(getattr(self, "_board")[x]):
                if (x==getattr(self, "_paddle").x and y==self._paddle.y):
                    for k in range(getattr(self, "_paddle").length):
                        print_str+="\u2588"
                    # print("\u2588", end="")
                    y+=self._paddle.length
                    continue
                if(isinstance(self._board[x][y], brick.brick)) and self._board[x][y].lvl>0:
                    # print(self._board[x][y].lvl, end="")
                    ob=self._board[x][y]
                    if getattr(ob, "lvl")==1:
                        print_str+=Fore.GREEN+"\u2588"+ getattr(Style, "RESET_ALL")
                        y+=1
                        continue
                        # print(Fore.GREEN+"\u2588"+ getattr(Style, "RESET_ALL"),end="")
                    if getattr(ob, "lvl")==2:
                        print_str+=Fore.YELLOW+"\u2588" +getattr(Style, "RESET_ALL")
                        y+=1
                        continue
                        # print(Fore.YELLOW+"\u2588" +getattr(Style, "RESET_ALL"),end="")
                    if getattr(ob, "lvl")==3:
                        y+=1
                        print_str+=Fore.RED+"\u2588"+ getattr(Style, "RESET_ALL")
                        continue
                        # print(Fore.RED+"\u2588"+ getattr(Style, "RESET_ALL"),end="")
                    if getattr(ob, "lvl")==4:
                        y+=1
                        print_str+=getattr(Fore, "LIGHTMAGENTA_EX")+"\u2588" +getattr(Style, "RESET_ALL")
                        continue
                        # print(getattr(Fore, "LIGHTMAGENTA_EX")+"\u2588" +getattr(Style, "RESET_ALL"),end="")
                    if getattr(ob, "lvl")==10:
                        y+=1
                        print_str+=Fore.WHITE+"\u2588" +getattr(Style, "RESET_ALL")
                        continue
                    if getattr(ob, "lvl")==20:
                        y+=1
                        print_str+=Fore.CYAN+"\u2588" +getattr(Style, "RESET_ALL")
                        continue
                
                # elif (x==math.floor(self._ball.x) and y==math.floor(self._ball.y)):
                #     # print("\u2B24", end="")
                #     print_str+="\u2B24"
                else:
                    flag1=0
                    for ball in getattr(self, "_balls"):
                        if math.floor(getattr(ball, "x"))==x and math.floor(ball.y)==y:
                            print_str+=ball.icon
                            flag1=1
                            break
                    if flag1:
                        y+=1
                        continue
                    flag=0
                    for pow_up in getattr(self, "_powerups"):
                        if getattr(pow_up, "x")==x and pow_up.y==y:
                            # print("\u2795",end="")
                            print_str+=getattr(pow_up, "icon")
                            flag=1
                            break
                    if flag:
                        y+=2
                        continue
                    print_str+=" "
                    y+=1
                
                
                        # print(" ", end="")
            # print()
            print_str+="\u23B8\n"
        system('clear')
        print(print_str)
        # np.set_printoptions(threshold=sys.maxsize)
        # print(self._board)
        

    def moveboardpaddle(self, key):
        self._paddle.movepaddle(key, self._balls)
    
    def droppows(self):
        for pow_up in self._powerups:
            getattr(pow_up,"droppowerup")()
            if pow_up.x==self._paddle.x-1 and pow_up.y>=self._paddle.y and pow_up.y<=self._paddle.y+self._paddle.length:
                getattr(pow_up,"execute")(self)
    
    def reducepows(self):
        for index, pow_up in enumerate(self._powerups):
            getattr(pow_up,"reducetime")()
            if pow_up.remaining_time==0:
                self._powerups.remove(pow_up)
                getattr(pow_up,"deactivate")(self)
        
    def moveballs(self):
        for index, ball in enumerate(self._balls):
            getattr(ball,"moveball")(self)
    
    def detectcollisionballs(self):
        for ball in self._balls:
            getattr(ball,"detectbrickcollision")(self)
            getattr(ball,"detectpaddlecollision")(self._paddle)
    
    def releaseballs(self):
        for ball in self._balls:
            getattr(ball,"releaseball")()

    def check_bricks(self, x, y):
        if isinstance(self._board[x][y], brick.brick) and getattr(self, "_board")[x][y].lvl>0:
            return True
        else:
            return False
    
    def balls_remaining(self):
        return len(getattr(self,"_balls"))
    
    def add_powerup(self, powu):
        getattr(self, "_powerups").append(powu)
    
    def increase_score(self, val):
        self.score+=val
        if getattr(self, "score")>=862.5:
            self.gameon=0

    def fallbricks(self):
        new_board=np.empty(shape=(getattr(global_stuff, "rows")+1, global_stuff.cols+1), dtype=np.object)
        for row in range(len(getattr(self, "_board"))):
            for column in range(len(getattr(self, "_board")[row])):
                if isinstance(getattr(self, "_board")[row][column], brick.brick) and getattr(self, "_board")[row][column].lvl>0:
                    new_board[row+1][column]=getattr(self, "_board")[row][column]
        last_row=-1
        for row in range(len(getattr(self, "_board"))):
            column=0
            while column<(len(getattr(self, "_board")[row])):
                if isinstance(new_board[row][column],brick.brick):
                    last_row=row
                    new_board[row][column].x+=1
                    column+=6
                else:
                    column+=1
        pass
        self._board=new_board
        if last_row==getattr(self, "_paddle").x:
            self.game_on=-1
        pass
    
    def changehardnessbrick(self):
        for x in range(len(getattr(self, "_board"))):
            for y in range(len(getattr(self, "_board")[x])):
                if isinstance(self._board[x][y], brick.colorchangingbrick):
                # if True:
                    # print(self._board[x][y].lvl)
                    # input()
                    getattr(self, "_board")[x][y].changecolor()
                    # getattr(self, "_board")[row][column]
                    y+=4
    
    
    def shoot_bullets(self):
        if self.frame_no%4==0 and self._paddle.shoot:
            getattr(self, "_bullets").append(bullet(self._paddle.x, self._paddle.y))
            getattr(self, "_bullets").append(bullet(self._paddle.x-1, self._paddle.y+self._paddle.length-1))
    
    def detectbulletcollision(self):
        for bullet in getattr(self, "_bullets"):
            getattr(bullet, "checkcollision")(self)
    
    def createbombs(self):
        if getattr(self, "ufo") is None:
            return
        if (self.frame_no)%10==0:
            getattr(self, "bombs").append(bomb(self.ufo.x, self.ufo.y))
    
    def dropbombs(self):
        for bom in getattr(self, "bombs"):
            getattr(bom, "dropbomb")()
            if bom.x==getattr(self, "_paddle").x and (bom.y>=self._paddle.y and bom.y<=self._paddle.y+self._paddle.length):
                getattr(self, "liveslost")()
            if getattr(bom, "x")>self._paddle.x:
                getattr(self, "bombs").remove(bom)
        
    def increment_frame(self):
        self.frame_no=getattr(self, "frame_no") +1
    
    def spawnblocks1(self):
        row=getattr(self, "ufo").x+getattr(self, "ufo").width+2
        col=0
        while col<getattr(global_stuff, "cols"):
            br=getattr(brick, "brick1")(row, col)
            for a in range(0,6):
                    self._board[row][col+a]=br
            col+=6
        pass

    def spawnblocks2(self):
        row=self.ufo.x+getattr(self, "ufo").width+4
        col=0
        while col<getattr(global_stuff, "cols"):
            br=getattr(brick, "brick2")(row, col)
            for a in range(0,6):
                    self._board[row][col+a]=br
            col+=6
        pass