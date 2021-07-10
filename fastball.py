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
