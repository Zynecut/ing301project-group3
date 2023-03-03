from classes.devices import Device
from classes.room import *
from classes.floor import *
from typing import List, Optional
import os
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

    def get_all_rooms(self) -> List[Room]:
        """Gir tilbake en liste med alle rom i huset."""
        rooms = []
        for x in self.floorlist:
            if hasattr(x, 'roomlist'):
                for y in x.roomlist:
                    rooms.append(y)
        return rooms

    def load_devicelist(self):
        """Henter sensor og actuators fra data.txt liste."""
        path = os.getcwd()
        my_file = open((path + "\classes\data.txt"), "r")
        data = my_file.read()
        data_into_list = data.split("\n")
        for x in data_into_list:
            y = x.split(',')
            if y[6] == "Actuator":
                device = Actuator(y[0], y[1], y[2], y[3], y[4])
            else:
                device = Sensor(y[0], y[1], y[2], y[3], y[4])
            room = self.get_room(y[5])
            self.register_device(device, room)

    def register_device(self, device: Device, room: Room):
        """Registrerer en enhet i et gitt rom."""
        room.devicelist.append(device)

    def get_room(self, roomname: str) -> Room:
        for floor in self.floorlist:
            for room in floor.roomlist:
                if room.name == roomname:
                    return room
        return None

    def find_device_by_serial_no(self, serial_no: str) -> Device:
        for floor in self.floorlist:
            for room in floor.roomlist:
                for device in room.devicelist:
                    if device.serieNummer == serial_no:
                        return device
        return None

    def get_all_devices(self) -> List[Device]:
        """Gir tilbake en liste med alle enheter som er registrert i huset."""
        somelist = []
        for floor in self.floorlist:
            for room in floor.roomlist:
                for device in room.devicelist:
                    somelist.append(device)
        return somelist

    def get_total_area(self) -> float:
        """Regner ut det totale arealet av huset."""
        totalarea = 0
        for x in self.floorlist:
            if hasattr(x, 'roomlist'):
                for y in x.roomlist:
                    if hasattr(y, 'area'):
                        totalarea += y.area

        return totalarea
    def get_all_devices_in_room(self, room: Room) -> List[Device]:
        """Gir tilbake en liste med alle enheter som er registrert på rommet."""
        somelist = []
        for device in room.devicelist:
            somelist.append(device)
        return somelist
    def get_no_of_devices(self) -> int:
        """Gir tilbake antall registrerte enheter i huset."""
        x = self.get_all_devices()
        return len(x)

    def get_no_of_sensors(self):
        """Git tilbake antall av registrerte sensorer i huset."""
        x = self.get_all_devices()
        sensor = 0
        for y in x:
            if isinstance(y, Sensor):
                sensor += 1
        return sensor

    def get_no_of_actuators(self):
        """Git tilbake antall av registrerte aktuatorer i huset."""
        x = self.get_all_devices()
        actuator = 0
        for y in x:
            if isinstance(y, Actuator):
                actuator += 1
        return actuator

    def move_device(self, device: Device, from_room: Room, to_room: Room):
        """Flytter en enhet fra et gitt romm til et annet."""
        from_room.devicelist.remove(device)
        to_room.devicelist.append(device)

    def get_room_with_device(self, device2: Device):
        """Gir tilbake rommet der en gitt enhet er resitrert."""
        for floor in self.floorlist:
            for room in floor.roomlist:
                for device in room.devicelist:
                    if device == device2:
                        return room
        return None

    def turn_on_lights_in_room(self, room: Room):
        """Slår på alle enheter av type 'Smart Lys' i et gitt rom."""
        for device in room.devicelist:
            if isinstance(device, Actuator) and device.typ == "Smart Lys":
                device.on_off = True
    def turn_off_lights_in_room(self, room: Room):
        """Slår av alle enheter av type 'Smart Lys' i et gitt rom."""
        for device in room.devicelist:
            if isinstance(device, Actuator) and device.typ == "Smart Lys":
                device.on_off = False

    def get_temperature_in_room(self, room: Room) -> Optional[float]:
        """Prøver å finne ut temperaturen i et gitt rom ved å finne
        enheter av type 'Temperatursensor' der og gi tilake verdien som kommatall."""
        for device in room.devicelist:
            if isinstance(device, Sensor) and device.typ == "Temperatursensor":
                 return device.maaltVerdi


    def set_temperature_in_room(self, room: Room, temperature: float):
        """Prøver å sette temperaturen i et gitt rom ved å sette alle aktuatorer
        som kan påvirke temperatur ('Paneloven', 'Varmepumpe', ...) til ønsket
        temperatur."""
        for device in room.devicelist:
            if isinstance(device, Actuator) and (device.typ == "Paneloven" or device.typ == "Varmepumpe" or device.typ == "Gulvvarmepanel"):
                device.on_off = True
                device.setValue = temperature



    def manualy_alter_sensordevice(self, device: Device, unit: str = "", maaltverdi: float = ""):
        device.maaltVerdi = maaltverdi
        device.unit = unit