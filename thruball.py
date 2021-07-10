from powerup import *
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
