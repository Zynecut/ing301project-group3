from classes.devices import Device
from classes.room import *
from classes.floor import *
from typing import List, Optional

"""Blir vel noe av dette også"""


class SmartHouse:
    """Den sentrale klasse i et smart hus system.
        Den forvalter etasjer, rom og enheter.
        Også styres alle enheter sentralt herifra."""

    def __init__(self):
        self.floorlist = []

    def create_floor(self, floor_no: int) -> Floor:
        """Legger til en etasje og gi den tilbake som objekt.
            Denne metoden ble kalt i initialiseringsfasen når
            strukturen av huset bygges opp-."""
        somefloor = Floor(floor_no)
        self.floorlist.append(somefloor)
        return Floor(somefloor)

    def create_room(self, floor_no: int, area: float, name: str = None) -> Room:
        """Legger til et rom i en etasje og gi den tilbake som objekt.
            Denne metoden ble kalt i initialiseringsfasen når
            strukturen av huset bygges opp-."""
        someroom = Room(area, name)
        self.floorlist[floor_no].roomlist.append(someroom)
        return someroom

    def get_no_of_rooms(self) -> int:
        """Gir tilbake antall rom i huset som heltall"""
        rooms = 0
        for x in self.floorlist:
            if hasattr(x, 'roomlist'):
                for y in x.roomlist:
                    rooms += 1
        return rooms

    def get_all_devices(self) -> List[Device]:
        """Gir tilbake en liste med alle enheter som er registrert i huset."""
        return NotImplemented

    def get_all_rooms(self) -> List[Room]:
        """Gir tilbake en liste med alle rom i huset."""
        rooms = []
        for x in self.floorlist:
            if hasattr(x, 'roomlist'):
                for y in x.roomlist:
                    rooms.append(y)
        return rooms

    def get_total_area(self) -> float:
        """Regner ut det totale arealet av huset."""
        toatlarea = 0
        for x in self.floorlist:
            if hasattr(x, 'roomlist'):
                for y in x.roomlist:
                    if hasattr(y, 'area'):
                        toatlarea += y.area

        return toatlarea

    def register_device(self, device: Device, room: Room):
        """Registrerer en enhet i et gitt rom."""
        return NotImplemented

    def get_no_of_devices(self):
        """Gir tilbake antall registrerte enheter i huset."""
        return NotImplemented

    def get_no_of_sensors(self):
        """Git tilbake antall av registrerte sensorer i huset."""
        return NotImplemented

    def get_no_of_actuators(self):
        """Git tilbake antall av registrerte aktuatorer i huset."""
        return NotImplemented

    def move_device(self, device: Device, from_room: Room, to_room: Room):
        """Flytter en enhet fra et gitt romm til et annet."""
        return NotImplemented

    def find_device_by_serial_no(self, serial_no: str) -> Optional[Device]:
        """Prøver å finne en enhet blant de registrerte enhetene ved å
        søke opp dens serienummer."""
        return NotImplemented

    def get_room_with_device(self, device: Device):
        """Gir tilbake rommet der en gitt enhet er resitrert."""
        return NotImplemented

    def get_all_devices_in_room(self, room: Room) -> List[Device]:
        """Gir tilbake en liste med alle enheter som er registrert på rommet."""
        return NotImplemented

    def turn_on_lights_in_room(self, room: Room):
        """Slår på alle enheter av type 'Smart Lys' i et gitt rom."""
        return NotImplemented

    def turn_off_lights_in_room(self, room: Room):
        """Slår av alle enheter av type 'Smart Lys' i et gitt rom."""
        return NotImplemented

    def get_temperature_in_room(self, room: Room) -> Optional[float]:
        """Prøver å finne ut temperaturen i et gitt rom ved å finne
        enheter av type 'Temperatursensor' der og gi tilake verdien som kommatall."""
        return NotImplemented

    def set_temperature_in_room(self, room: Room, temperature: float):
        """Prøver å sette temperaturen i et gitt rom ved å sette alle aktuatorer
        som kan påvirke temperatur ('Paneloven', 'Varmepumpe', ...) til ønsket
        temperatur."""
        return NotImplemented
