from powerup import PowerUp
from ball import ball
from typing import Any

class ballmultiplier(PowerUp):
    def __init__(self, x, y, x_vel, y_vel):
        icon: Any='❌'
        getattr(super(), "__init__")(x, y, x_vel, y_vel, icon)
    
    def execute(self, board):
        getattr(super(), "execute")()
        new_balls=[]
        for each_ball in getattr(board, "_balls"):
            ball1=ball(getattr(each_ball,"x"), getattr(each_ball, "y"), getattr(each_ball,"x_vel"), min(getattr(each_ball, "y_vel"),1), False, each_ball.fire, each_ball.fast_ball, each_ball.gold_ball)
            ball2=ball(getattr(each_ball,"x"), each_ball.y, each_ball.x_vel, max(-1,-each_ball.y_vel), False, each_ball.fire, each_ball.fast_ball, each_ball.gold_ball)
            new_balls=new_balls+[ball1, ball2]
        board._balls=new_balls

    def deactivate(self, board):
        pass
