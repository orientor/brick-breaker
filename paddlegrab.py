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
