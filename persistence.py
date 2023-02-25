from sqlite3 import Connection
import sqlite3
from classes.devices import Device
from classes.devices import Sensor
from classes.smarthouse import Room
from typing import Optional, List, Dict, Tuple
from datetime import date, datetime


class SmartHousePersistence:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = Connection(db_file)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.rollback()
        self.connection.close()

    def save(self):
        self.connection.commit()

    def reconnect(self):
        self.connection.close()
        self.connection = Connection(self.db_file)
        self.cursor = self.connection.cursor()

    def check_tables(self) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_schema WHERE type = 'table';")
        result = set()
        for row in self.cursor.fetchall():
            result.add(row[0])
        return 'rooms' in result and 'devices' in result and 'measurements' in result

    def injector(self, injectionstring):
        """insert injection load....into DB """
        self.cursor.execute(injectionstring)

    def query(self, querystring) -> list:
        """insert query and receive awsome list containing key,value from query"""
        self.cursor.execute(querystring)
        result = []
        for row in self.cursor.fetchall():
            inner_dict = {}
            keys = row.keys()
            i = 0
            for x in row:
                inner_dict[keys[i]] = x
                i += 1
            result.append(inner_dict)
        return result


class SmartHouseAnalytics:

    def __init__(self, persistence: SmartHousePersistence):
        self.persistence = persistence

    def get_most_recent_sensor_reading(self, sensor: Device) -> Optional[float]:
        """
        Retrieves the most recent (i.e. current) value reading for the given
        sensor device.
        Function may return None if the given device is an actuator or
        if there are no sensor values for the given device recorded in the database.
        """
        if isinstance(sensor, Sensor):
            return sensor.maaltVerdi
        else:
            return None

    def get_coldest_room(self) -> Room:
        """
        Finds the room, which has the lowest temperature on average.
        """
        return NotImplemented()

    def get_sensor_readings_in_timespan(self, sensor: Device, from_ts: datetime, to_ts: datetime) -> List[float]:
        """
        Returns a list of sensor measurements (float values) for the given device in the given timespan.
        """
        return NotImplemented()

    def describe_temperature_in_rooms(self) -> Dict[str, Tuple[float, float, float]]:
        """
        Returns a dictionary where the key are room names and the values are triples
        containing three floating point numbers:
        - The first component [index=0] being the _minimum_ temperature of the room.
        - The second component [index=1] being the _maximum_ temperature of the room.
        - The third component [index=2] being the _average_ temperature of the room.

        This function can be seen as a simplified version of the DataFrame.describe()
        function that exists in Pandas:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html?highlight=describe
        """
        return NotImplemented()

    def get_hours_when_humidity_above_average(self, room: Room, day: date) -> List[int]:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number respresenting hours [0-23].
        """
        return NotImplemented()