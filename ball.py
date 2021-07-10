import math
import os, system
from global_stuff import *
from entity import *
from typing import Any
import brick
from colorama import Fore, Style

class ball(entity):
    def __init__(self, x, y, x_vel=-1, y_vel=1, stuck=True, fire=False, fast_ball=1, gold=False):
        getattr(super(), "__init__")(x,y)
        self.x_vel: Any =x_vel
        self.y_vel: Any =y_vel
        self.stuck: Any =stuck
        self.fire: Any =fire
        self.gold_ball: Any = gold_ball
        if fire:
            self.icon: Any=getattr(Fore, "RED")+"\u2B24"+getattr(Style, "RESET_ALL")
        elif:
            self.icon: Any=Fore.YELLOW+"\u2B24"+Style.RESET_ALL
        else:
            self.icon: Any="\u2B24"
        self.fast_ball: Any = fast_ball

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
        self.y+=getattr(self, "y_vel")*self.fast_ball
            
    def ballfell(self):
        if math.floor(getattr(self, "x") +self.x_vel)>=rows:
            return True
        return False

    def topwallcollision(self):
        getattr(os, "system")("aplay brickwall.wav &")
        getattr(self, "reflect_x_velocity") ()
        if getattr(self, "x")<1:
            self.x=0
    
    def sidewallcollision(self):
        gettattr(os, "system")("aplay brickwall.wav &")
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
            brick_x=getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].x
            brick_y=getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].y
            if getattr(self, "gold_ball"):
                getattr(os, "system")("aplay Explosion.wav &")
                getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].destroy(board, self)
                if brick_y+6<global_stuff.cols and getattr(board, "_board")[brick_x+1][brick_y+6]:
                    getattr(board, "_board")[brick_x+1][brick_y+6].destroy(board, self)
                if brick_y+6<global_stuff.cols and getattr(board, "_board")[brick_x][brick_y+6]:
                    getattr(board, "_board")[brick_x][brick_y+7].destroy(board, self)
                for k in range(-1,7):
                    if getattr(board, "_board")[brick_x+1][brick_y+k]:
                        getattr(board, "_board")[brick_x+1][brick_y+k].destroy(board, self)
                if getattr(board, "_board")[brick_x-1][brick_y-1]:
                    getattr(board, "_board")[brick_x-1][brick_y-1].destroy(board, self)
                if getattr(board, "_board")[brick_x][brick_y-1]:
                    getattr(board, "_board")[brick_x][brick_y-1].destroy(board, self)
                for k in range(-1,7):
                    if getattr(board, "_board")[brick_x-1][brick_y+k]:
                        getattr(board, "_board")[brick_x-1][brick_y+k].destroy(board, self)
                if not self.fire:
                    getattr(self, "reflect_y_velocity")()
                
                # a=self.generate_powerup(brick_x,brick_y, ball.x_vel, ball.y_vel)
                # if a:
                #     board.add_powerup(a)
            
            elif self.fire:
                getattr(os, "system")("aplay Explosion.wav &")
                getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].destroy(board, self)
            else:
                # if time.time()-board.level_time>10:
                getattr(os, "system")("aplay brickwall.wav &")
                getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)].reducelvl(board, self)
                self.reflect_y_velocity()

        if getattr(board, "check_bricks")(int(curr_x+x_dir), int(curr_y)) and not board.check_bricks(int(curr_x), int(curr_y)):
            brick_x=getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].x
            brick_y=getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].y
            if self.gold_ball:
                getattr(os, "system")("aplay Explosion.wav &")
                getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].destroy(board, self)
                if brick_y+6<global_stuff.cols and getattr(board, "_board")[brick_x+1][brick_y+6]:
                    getattr(board, "_board")[brick_x+1][brick_y+6].destroy(board, self)
                if brick_y+6<global_stuff.cols and getattr(board, "_board")[brick_x][brick_y+6]:
                    getattr(board, "_board")[brick_x][brick_y+6].destroy(board, self)
                for k in range(-1,7):
                    if getattr(board, "_board")[brick_x+1][brick_y+k]:
                        getattr(board, "_board")[brick_x+1][brick_y+k].destroy(board, self)
                if getattr(board, "_board")[brick_x-1][brick_y-1]:
                    getattr(board, "_board")[brick_x-1][brick_y-1].destroy(board, self)
                if getattr(board, "_board")[brick_x][brick_y-1]:
                    getattr(board, "_board")[brick_x][brick_y-1].destroy(board, self)
                for k in range(-1,7):
                    if getattr(board, "_board")[brick_x-1][brick_y+k]:
                        getattr(board, "_board")[brick_x-1][brick_y+k].destroy(board, self)
                # if getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)] != getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)]:
                if not self.fire:
                    getattr(self, "reflect_x_velocity")()
                
                # a=getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].generate_powerup(brick_x,brick_y, ball.x_vel, ball.y_vel)
                # if a:
                    # board.add_powerup(a)
            elif self.fire:
                getattr(os, "system")("aplay Explosion.wav &")
                getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].destroy(board, self)
            else:
                if getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)] != getattr(board, "_board")[int(curr_x)][int(curr_y+y_dir)]:
                    # if time.time()-board.level_time>10:
                    getattr(os, "system")("aplay brickwall.wav &")
                    getattr(board, "_board")[int(curr_x+x_dir)][int(curr_y)].reducelvl(board, self)
                    getattr(self, "reflect_x_velocity")()

    
    def reflect_x_velocity(self):
        self.x_vel=getattr(self, "x_vel")*-1
    
    def reflect_y_velocity(self):
        self.y_vel=getattr(self, "y_vel")*-1
            
        
    def detectpaddlecollision(self, paddle, board):
        x_dir=int(math.copysign(1,getattr(self, "x_vel")))
        y_dir=int(math.copysign(1,getattr(self, "y_vel")))
        curr_x=math.floor(getattr(self, "x"))
        curr_y=math.floor(getattr(self, "y"))
        if x_dir==1 and curr_y>=getattr(paddle, "get_left_coor")() and curr_y<=getattr(paddle, "get_right_coor")() and curr_x==rows-2:
            getattr(self, "reflect_x_velocity")()
            if getattr(time, "time")()-board.level_time>=30 and board.ufo is None:
                getattr(board, "fallbricks")()
            dist_from_centre=getattr(paddle, "get_left_coor")()+getattr(paddle, "get_length")()/2-curr_y
            factor_change=math.floor(dist_from_centre/2.5)
            self.y_vel=-factor_change*0.5
            if getattr(paddle, "isstick")():
                self.stuck=True
            else:
                getattr(os, "system")("aplay bounce.wav &")


    
    def movestuckball(self, dist):
        self.y+=dist
    
    def releaseball(self):
        self.stuck=False 
    
    def setfire(self):
        self.icon=getattr(Fore, "RED")+"\u2B24"+getattr(Style, "RESET_ALL")
        self.fire=True
    
    def stopfire(self):
        self.fire=False
        if getattr(self, "gold_ball"):
            self.icon=getattr(Fore, "YELLOW") + "\u2B24"+Style.RESET_ALL
        else:
            self.icon="\u2B24"


    def isstuck(self):
        return getattr(self, "stuck")

    def setgold(self):
        self.icon=getattr(Fore, "YELLOW")+"\u2B24"+getattr(Style, "RESET_ALL")
        self.gold_ball=True
    
    def stopgold(self):
        self.gold_ball=False
        if getattr(self, "fire"):
            self.icon=getattr(Fore, "RED")+"\u2B24"+getattr(Style, "RESET_ALL")
        else:
            self.icon="\u2B24"


    def increase_ball_velocity(self):
        self.fast_ball=2

    def decrease_ball_velocity(self):
        self.fast_ball=1

    def detectufocollision(self, ufo, board):
        if not ufo:
            return
        x_dir=int(math.copysign(1,getattr(self, "x_vel")))
        y_dir=int(math.copysign(1,getattr(self, "y_vel")))
        curr_x=math.floor(getattr(self, "x"))
        curr_y=math.floor(getattr(self, "y"))
        flag=0
        if getattr(ufo, "check")(int(curr_x), int(curr_y+y_dir)):
                # if time.time()-board.level_time>10:
            getattr(ufo, "reducelvl")()
            getattr(board, "increase_score")(30)
            if getattr(ufo, "health")==70:
                getattr(board, "spawnblocks1")()
                pass
            if getattr(ufo, "health")==40:
                getattr(board, "spawnblocks2")()
            if getattr(ufo, "health")==0:
                board.game_on=2
            getattr(os, "system")("aplay bounce.wav &")
            flag=1
            if self.y-getattr(ufo, "y")>getattr(ufo, "y")+ufo.length-self.y:
                self.y_vel=abs(getattr(self, "y_vel"))
                self.y=getattr(ufo, "y")+ufo.length+1
            else:
                self.y_vel=-(abs(getattr(self, "y_vel")))
                self.y=getattr(ufo, "y")-1
        elif ufo.check(int(curr_x+x_dir), int(curr_y)):
                # if time.time()-board.level_time>10:
            getattr(os, "system")("aplay bounce.wav &")
            if flag==0:
                getattr(ufo, "reducelvl")()
                getattr(board, "increase_score")(30)
                if getattr(ufo, "health")==70:
                    getattr(board, "spawnblocks1")()
                    pass
                if getattr(ufo, "health")==40:
                    getattr(board, "spawnblocks2")()
                if getattr(ufo, "health")==0:
                    board.game_on=2
            getattr(self, "reflect_x_velocity")()