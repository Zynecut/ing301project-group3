from classes.room import *

class Floor:
    """Representerer en etasje i ett hus.
        En etasje har et entydig nummer og består av flere rom."""

    def __init__(self, floor_no: int):
        self.floor_no = floor_no
        self.roomlist = []
    def __repr__(self):
        return f"(Floor nr {self.floor_no +1})"
