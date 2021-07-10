from entity import *
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
