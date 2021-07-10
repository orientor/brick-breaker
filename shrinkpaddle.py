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
