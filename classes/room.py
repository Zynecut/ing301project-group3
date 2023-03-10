from classes.devices import *

class Room:
    """Representerer et rom i en etasje i ett hus.
        Et rom har et areal og det kan gis et kort navn.
        På et romm kan også registreres smarte enheter."""
    def __init__(self, area: float, name: str = None, room_id: int = -1):
        self.area = area
        self.name = name
        self.ID = room_id
        self.devicelist = []

    def __repr__(self):
        return f"{self.name} ({self.area} m^2)"
