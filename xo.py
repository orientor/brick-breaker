from powerup import PowerUp
from ball import ball
from typing import Any

class ballmultiplier(PowerUp):
    def __init__(self, x, y):
        icon: Any='❌'
        getattr(super(), "__init__")(x, y, icon)
    
    def execute(self, board):
        getattr(super(), "execute")()
        new_balls=[]
        for each_ball in getattr(board, "_balls"):
            ball1=ball(getattr(each_ball,"x"), getattr(each_ball, "y"), getattr(each_ball,"x_vel"), min(getattr(each_ball, "y_vel"),1), False)
            ball2=ball(getattr(each_ball,"x"), each_ball.y, each_ball.x_vel, max(-1,-each_ball.y_vel), False)
            new_balls=new_balls+[ball1, ball2]
        board._balls=new_balls

    def deactivate(self, board):
        pass
import math
from global_stuff import *
from entity import *
from typing import Any
import brick
from colorama import Fore, Style

class ball(entity):
    def __init__(self, x, y, x_vel=-1, y_vel=1, stuck=True, fire=False):
        getattr(super(), "__init__")(x,y)
        self.x_vel: Any =x_vel
        self.y_vel: Any =y_vel
        self.stuck: Any =stuck
        self.fire: Any =fire
        if fire:
            self.icon: Any=getattr(Fore, "RED")+"\u2B24"+getattr(Style, "RESET_ALL")
        else:
            self.icon: Any="\u2B24"

    def moveball(self, board):
        
        if getattr(self, "stuck"):
            return  
        
        if getattr(self, "ballfell")():
            getattr(self, "removeballs")(board)
            return
        self.update_ball_position()
        if((self.x)<=0):
            getattr(self, "topwallcollision")()
        if((self.y)<=0 or (self.y)>=cols-1):
            getattr(self, "sidewallcollision")()
    
    def update_ball_position(self):
        self.x+=getattr(self, "x_vel")
        self.y+=getattr(self, "y_vel")
            
    def ballfell(self):
        if math.floor(getattr(self, "x") +self.x_vel)>=rows:
            return True
        return False

    def topwallcollision(self):
        getattr(self, "reflect_x_velocity") ()
        if getattr(self, "x")<1:
            self.x=0
    
    def sidewallcollision(self):
        getattr(self, "reflect_y_velocity")()
        if getattr(self, "y")<1:
            self.y=0
        else:
            self.y=cols-1
    
    def removeballs(self, board):
        getattr(board, "_balls").remove(self)
        if getattr(board, "balls_remaining")()==0:
            getattr(board, "liveslost")()
        
    def detectbrickcollision(self, board):
        x_dir=int(math.copysign(1,getattr(self, "x_vel")))
        y_dir=int(math.copysign(1,getattr(self, "y_vel")))
        curr_x=math.floor(self.x)
        curr_y=math.floor(self.y)
        if getattr(board, "check_bricks")(int(curr_x), int(curr_y+y_dir)):
            if self.fire:
                getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].destroy(board)
            else:
                getattr(self, "reflect_y_velocity")()
                getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].reducelvl(board)
        if getattr(board, "check_bricks")(int(curr_x+x_dir), int(curr_y)) and not board.check_bricks(int(curr_x), int(curr_y)):
            if self.fire:
                getattr(board, "_board" )[int(curr_x+x_dir)][int(curr_y)].destroy(board)
            else:
                if getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)] != board._board[int(curr_x)][int(curr_y+y_dir)]:
                    getattr(self, "reflect_x_velocity")()
                    getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].reducelvl(board)
    
    def reflect_x_velocity(self):
        self.x_vel=getattr(self, "x_vel")*-1
    
    def reflect_y_velocity(self):
        self.y_vel=getattr(self, "y_vel")*-1
            
        
    def detectpaddlecollision(self, paddle):
        x_dir=int(math.copysign(1,getattr(self, "x_vel")))
        y_dir=int(math.copysign(1,getattr(self, "y_vel")))
        curr_x=math.floor(getattr(self, "x"))
        curr_y=math.floor(getattr(self, "y"))
        if x_dir==1 and curr_y>=getattr(paddle, "get_left_coor")() and curr_y<=getattr(paddle, "get_right_coor")() and curr_x==rows-2:
            getattr(self, "reflect_x_velocity")()
            dist_from_centre=getattr(paddle, "get_left_coor")()+getattr(paddle, "get_length")()/2-curr_y
            factor_change=math.floor(dist_from_centre/2.5)
            self.y_vel=-factor_change*0.5
            if getattr(paddle, "isstick")():
                self.stuck=True

    
    def movestuckball(self, dist):
        self.y+=dist
    
    def releaseball(self):
        self.stuck=False 
    
    def setfire(self):
        self.icon=getattr(Fore, "RED")+"\u2B24"+getattr(Style, "RESET_ALL")
        self.fire=True
    
    def stopfire(self):
        self.fire=False
        self.icon="\u2B24"

    def isstuck(self):
        return getattr(self, "stuck")

    def increase_ball_velocity(self):
        self.y_vel=getattr(self, "y_vel")+math.copysign(1,self.y_vel)import sys
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

class board():
    def __init__(self, rows, columns):
        self._rows: Any=rows
        self._columns: Any=columns
        self._board: Any = np.empty(shape=(rows+1, columns+1), dtype=np.object)
        self._paddle: Any = paddle(rows-1,columns/2)
        self._balls: Any = [ball(rows-2, random.randint(int(self._paddle.y), int(self._paddle.y+self._paddle.length)))]
        self._powerups: Any =[]
        self.score: Any=0
        self.remaining_lives: Any=10
        self.start_time: Any=time.time()
        self.gameon: Any=1
    
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
        # arr=[[0,0,5], [2,6,5], [4, 12, 5], [6,18,5],]
        arr=[[16, 6, 1], [16, 18, 2], [16, 24, 3], [16, 30, 4], [16, 42, 3], [16, 48, 4], [16, 54, 1], [16, 60, 4], [16, 66, 1], [16, 72, 2], [16, 78, 3], [16, 84, 4], [16, 90, 0], [16, 96, 1], [16, 102, 2], [16, 108, 3], [16, 114, 4]]
        arr2=[2, 18, 3], [2, 24, 2], [2, 30, 4], [2, 42, 4], [2, 48, 1], [2, 54, 0], [2, 60, 1], [2, 66, 2], [2, 72, 4], [2, 78, 1], [2, 84, 0], [2, 90, 4], [2, 96, 3], [2, 102, 4], [2, 108, 2], [2, 114, 1]]
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
        for x in range(getattr(global_stuff, "rows")+1):
            print_str+="\u23B9"
            y=0
            while y<len(getattr(self, "_board")[x]):
                if (x==getattr(self, "_paddle").x and y==self._paddle.y):
                    for k in range(getattr(self, "_paddle.length")):
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
                        if getattr(pow_up. "x")==x and pow_up.y==y:
                            # print("\u2795",end="")
                            print_str+=getattr(pow_up, "icon
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
            self.gameon=0from entity import *
from powerup import *
from expandpaddle import *
from shrinkpaddle import *
from ballmultiplier import *
from fastball import *
from paddlegrab import *
from thruball import *
import global_stuff
import random
from typing import Any

class brick(entity):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x,y)
        self.lvl=-1
    
    def reducelvl(self, board):
        self.lvl-=1
        if getattr(self, "lvl")==0:
            for y in range(6):
                board._board[getattr(self, "x")][getattr(self, "y")+y]=None
            getattr(self, "increasescore")(board)
            getattr(board, "add_powerup")(self.generate_powerup(getattr(self, "x"),getattr(self, "y")))
    
    def destroy(self, board):
        self.lvl=0
        for y in range(6):
            board._board[getattr(self, "x")][getattr(self, "y")+y]=None
        getattr(self, "increasescore")(board)
        getattr(board,"add_powerup")(self.generate_powerup(getattr(self, "x"),getattr(self, "y")))
    
    def increasescore(self, board): #overloaded
        pass
        
    
    def generate_powerup(self, x,y):
        num=random.randint(0,5)
        switcher = { 
            0: expandpaddle, 
            1: shrinkpaddle, 
            2: ballmultiplier,
            3: fastball,
            4: paddlegrab,
            5: thruball 
        }
        return switcher[num](x,y)
        
            
    
class brick1(brick):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x, y)
        self.lvl=1

    def increasescore(self, board):
        getattr(board, "increase_score")(5)
    
class brick2(brick):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x, y)
        self.lvl=2

    def increasescore(self, board):
        getattr(board, "increase_score")(10)


class brick3(brick):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x, y)
        self.lvl=3

    def increasescore(self, board):
        # board.score+=15
        board.increase_score(15)


class brick4(brick):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x, y)
        self.lvl=4

    def increasescore(self, board):
        # board.score+=20
        board.increase_score(20)


class brickfixed(brick):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x, y)
        self.lvl=10

    def reducelvl(self, board):
        return None

    def increasescore(self, board):
        pass

class explodingbrick(brick):
    def __init__(self, x, y):
        getattr(super(), "__init__")(x, y)
        self.lvl=20

    def reducelvl(self, board):
        return self.destroy(board)

    def destroy(self, board):
        if not board._board[getattr(self, "x")][getattr(self, "y")]:
            return
        self.lvl=0
        self.increasescore(board)
        board._board[getattr(self, "x")][getattr(self, "y")]=None
        if getattr(self, "y")+6<global_stuff.cols and board._board[getattr(self, "x")+1][getattr(self, "y")+6]:
            board._board[getattr(self, "x")+1][getattr(self, "y")+6].destroy(board)
        if getattr(self, "y")+6<global_stuff.cols and board._board[getattr(self, "x")][getattr(self, "y")+6]:
            board._board[getattr(self, "x")][getattr(self, "y")+6].destroy(board)
        for k in range(-1,7):
            if board._board[getattr(self, "x")+1][getattr(self, "y")+k]:
                board._board[getattr(self, "x")+1][getattr(self, "y")+k].destroy(board)
        if board._board[getattr(self, "x")-1][getattr(self, "y")-1]:
            board._board[getattr(self, "x")-1][getattr(self, "y")-1].destroy(board)
        if board._board[getattr(self, "x")][getattr(self, "y")-1]:
            board._board[getattr(self, "x")][getattr(self, "y")-1].destroy(board)
        for k in range(-1,7):
            if board._board[getattr(self, "x")-1][getattr(self, "y")+k]:
                board._board[getattr(self, "x")-1][getattr(self, "y")+k].destroy(board)
        board.add_powerup(self.generate_powerup(getattr(self, "x"),getattr(self, "y")))
    
    def increasescore(self, board):
        board.increase_score(2.5)
from typing import Any
class entity:
    def __init__(self, x, y):
        self.x: Any=x
        self.y: Any=yfrom powerup import PowerUp
from typing import Any

class expandpaddle(PowerUp):
    def __init__(self, x, y):
        icon: Any="\u2795"
        getattr(super(), "__init__")(x, y, icon)
    
    def execute(self, board):
        getattr(super(), "execute")()
        getattr(board, "_paddle").increasesize()
    
    def deactivate(self, board):
        getattr(super(), "deactivate")()
        getattr(board, "_paddle").decreasesize()
from powerup import *
import math
from typing import Any
class fastball(PowerUp):
    def __init__(self, x, y):
        icon: Any="⚡"
        getattr(super(),"__init__")(x, y, icon)
    
    def execute(self, board):
        getattr(super(),"execute")()
        for ball in getattr(board,"_balls"):
            getattr(ball, "increase_ball_velocity")()
    
    def deactivate(self, paddle):
        pass
from board import *
from input import *
import numpy as np
from os import *
from typing import Any
from global_stuff import *
import datetime, time, sys
getch=Get()

class Game:
    def __init__(self):
        self.game_on: Any=True
        self.current_board: Any=board(rows, cols)
    
    def rungame(self):
        getattr(self,"current_board").createlevel1()
        while(self.game_on==1):
            c: Any=input_to(getch)
            if c=='q':
                sys.exit(0)
            if c=='a' or c=='d':
                getattr(self,"current_board").moveboardpaddle(c)
            if c=='p':
                for ball in getattr(self,"current_board")._balls:
                    print(ball.x_vel, ball.y_vel)
                input()
            if c==' ':
                getattr(self,"current_board").releaseballs()
            if c:
                time.sleep(0.05)    
            getattr(getattr(self, "current_board"),"moveballs")()
            getattr(self,"current_board").detectcollisionballs()
            getattr(self,"current_board").droppows()
            getattr(self,"current_board").reducepows()
            getattr(self,"current_board").printboard()
            time.sleep(0.02)
        system('clear')
        if self.game_on==-1:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\tGAME OVER!!!")
            print("\t\t\tSCORE: ",getattr(self,"current_board").score)
            print("\t\t\tTIME PLAYED: ",str(datetime.timedelta(seconds=int(time.time()-getattr(self,"current_board").start_time))))
            print("PRESS ENTER TO PLAY AGAIN")
        else:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t\t\tYOU WONNN!!!")
            print("\t\t\tSCORE: ",getattr(self,"current_board").score)
            print("\t\t\tTIME PLAYED: ",str(datetime.timedelta(seconds=int(time.time()-getattr(self,"current_board").start_time))))
            print("PRESS ENTER TO PLAY AGAIN")
import numpy as np
rows=38
cols=150
why_dis = True"""Defining input class."""
import sys
import termios
import tty
import signal

class Get:
    """Class to get input."""

    def __call__(self):
        """Defining __call__."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        newSettings = termios.tcgetattr(sys.stdin)
        newSettings[tty.LFLAG] &= ~termios.ICANON
        newSettings[tty.LFLAG] &= ~termios.ECHO
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, newSettings)
        return ch


class AlarmException(Exception):
    """Handling alarm exception."""
    pass


def alarmHandler(signum, frame):
    """Handling timeouts."""
    raise AlarmException


def input_to(getch, timeout=0.05):
    """Taking input from user."""
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return Nonefrom Game import Game
from typing import Any
while True:
    current_game: Any=Game()
    current_game.rungame()
    input()
from powerup import *
from ball import *
from typing import Any
class paddlegrab(PowerUp):
    def __init__(self, x, y):
        icon: Any="\u270A"
        getattr(super(),"__init__")(x, y, icon)
    
    def execute(self, board):
        getattr(super(),"execute")()
        board._paddle.stick=True

    def deactivate(self, board):
        getattr(super(),"deactivate")()
        board._paddle.stick=False
        pass
import global_stuff 
from entity import *
from typing import Any
class paddle(entity):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.length: Any=20
        self.actual_length: Any=20
        self.stick: Any=False
    
    def movepaddle(self, key, balls):
        if key=='d':
            max_d=min(3, global_stuff.cols-getattr(self, "length")-self.y+1)
            self.y+=max_d
            for ball in balls:
                if getattr(ball, "isstuck")():
                    getattr(ball, "movestuckball")(max_d)
        elif key=='a':
            max_d=self.y-max(0, self.y-3)
            self.y-=max_d
            for ball in balls:
                if getattr(ball, "isstuck")():
                    gettattr(ball, "movestuckball")(-max_d)
    
    def increasesize(self):
        self.actual_length+=6
        self.length=max(getattr(self, "actual_length"),2)
    
    def decreasesize(self):
        self.actual_length-=6
        self.length=max(getattr(self, "actual_length"),2)
    
    def get_left_coor(self):
        return getattr(self,"y")
    
    def get_right_coor(self):
        return getattr(self,"y") + self.length
    
    def get_length(self):
        return getattr(self, "length")
    
    def isstick(self):
        return getattr(self, "stick")
from typing import Any
class PowerUp:
    def __init__(self, x, y, icon):
        self.remaining_time: Any=-1
        self.x: Any=x
        self.y: Any=y
        self.v_x: Any=1
        self.icon: Any=icon
    
    def execute(self):
        self.remaining_time: Any=120
        self.x: Any=-1
        self.y: Any=-1
        pass
    
    def deactivate(self):
        pass
    
    def droppowerup(self):
        self.x= self.x + self.v_x

    def reducetime(self):
        self.remaining_time= getattr(self, "remaining_time")-1
from powerup import *

class shrinkpaddle(PowerUp):
    def __init__(self, x, y):
        icon="\u2796"
        getattr(super(),"__init__")(x, y, icon)
    
    def execute(self, board):
        super().execute()
        getattr(board,"_paddle").decreasesize()

    def deactivate(self, board):
        super().deactivate()
        getattr(board,"_paddle").increasesize()
ofrom powerup import *
from ball import *

class thruball(PowerUp):
    def __init__(self, x, y):
        icon="🔥"
        super().__init__(x, y, icon)
    
    def execute(self, board):
        getattr(super(),"execute")()
        for ball in getattr(board, "_balls"):
            getattr(ball, "setfire")()

    def deactivate(self, board):
        for ball in getattr(board,"_balls"):
            getattr(ball,"stopfire")()
