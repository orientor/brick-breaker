from powerup import PowerUp
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
