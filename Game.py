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
