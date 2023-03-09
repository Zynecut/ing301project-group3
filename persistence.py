import time
from sqlite3 import Connection
import sqlite3
from classes.smarthouse import *
from classes.devices import Device
from classes.devices import Sensor
from typing import Optional, List, Dict, Tuple
from datetime import date, datetime, timedelta



class SmartHousePersistence:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = Connection(db_file, timeout=10)
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
        self.connection.row_factory = sqlite3.Row
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
        querylist = self.cursor.fetchall()
        for row in querylist:
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
        # querystring = "select avg(value), device  from measurements group by device"
        querystring = "select avg(m.value) as v1,m.device, d.id, d.room, r.id, r.name " \
                      "from measurements as m " \
                      "left join devices as d on m.device=d.id " \
                      "left join rooms as r on d.room=r.id " \
                      "group by m.device " \
                      "order by v1"
        a = self.persistence.query(querystring)
        return a[0]['name']

    def get_sensor_readings_in_timespan(self, sensor: Device, from_ts: datetime, to_ts: datetime) -> List[float]:
        """
        Returns a list of sensor measurements (float values) for the given device in the given timespan.
        """
        querystring = "select time_stamp, device, value from measurements " \
                      "where device == {0} and time_stamp between '{1}' and '{2}'".format(sensor.nr,from_ts.isoformat(), to_ts.isoformat())
        a = self.persistence.query(querystring)
        templist = []
        for row in a:
            templist.append(row['value'])
        return templist

    def describe_temperature_in_rooms(self) -> Dict[str, Tuple[float, float, float]]:
        """
        Returns a dictionary where the key are room names and the values are triples
        containing three floating point numbers:
        - The first component [index=0] being the _minimum_ temperature of the room.
        - The second component [index=1] being the _maximum_ temperature of the room.
        - The third component [index=2] being the _average_ temperature of the room.
        expected = {
            "Living Room / Kitchen": (15.0708, 24.1327, 20.606689623287576),
            "Entrance": (0.1589, 17.1905, 6.9318578742514925),
            "Master Bedroom": (12.0813, 21.3091, 16.473596511627903)
        }    
        This function can be seen as a simplified version of the DataFrame.describe()
        function that exists in Pandas:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html?highlight=describe
        """ # I HATE YOU PANDAS!!!
        querystring = "select avg(m.value), min(m.value),max(m.value),m.device, d.id, d.room, r.id, r.name " \
                      "from measurements as m " \
                      "left join devices as d on m.device=d.id " \
                      "left join rooms as r on d.room=r.id " \
                      "group by m.device"
        x = self.persistence.query(querystring)
        the_dict = dict()
        # must be done manualy due to 2 more rooms in table from query
        the_dict[x[1]['name']] = (x[1]['min(m.value)'],x[1]['max(m.value)'],x[1]['avg(m.value)'])
        the_dict[x[2]['name']] = (x[2]['min(m.value)'], x[2]['max(m.value)'], x[2]['avg(m.value)'])
        the_dict[x[4]['name']] = (x[4]['min(m.value)'], x[4]['max(m.value)'], x[4]['avg(m.value)'])
        return the_dict

    def get_hours_when_humidity_above_average(self, room: str, day: date) -> List[int]:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number respresenting hours [0-23].
        """
        somedatestop = day + timedelta(days=1)
        querystring = "select m.value, m.time_stamp ,m.device, d.id, d.room, r.id, r.name " \
                      "from measurements as m " \
                      "left join devices as d on m.device=d.id " \
                      "left join rooms as r on d.room=r.id " \
                      "WHERE r.name == '{0}' and m.time_stamp " \
                      "BETWEEN '{1}' and '{2}' ORDER BY time_stamp".format(room, day.isoformat(), somedatestop.isoformat())
        list_of_measurements = self.persistence.query(querystring)
        querystring2 = "select avg(m.value) ,m.device, d.id, d.room, r.id, r.name " \
                       "from measurements as m " \
                       "left join devices as d on m.device=d.id " \
                       "left join rooms as r on d.room=r.id " \
                       "WHERE r.name == '{0}' and m.time_stamp BETWEEN '{1}' and '{2}'".format(room, day.isoformat(), somedatestop.isoformat())
        the_average_value_sql = self.persistence.query(querystring2)
        the_average_value = the_average_value_sql[0]['avg(m.value)']
        the_outer = [None]*24
        returnlist = []
        i = 0
        # EPIC HACK FOR LACK OF SQL SKILLS
        for row in the_outer:
            the_outer[i] = []
            i += 1
        for rowblaster in list_of_measurements:
            a = datetime.fromisoformat(rowblaster['time_stamp'])
            b = a.hour
            if rowblaster['value'] > the_average_value:
                the_outer[b].append(rowblaster['value'])
        i = 0
        for y in the_outer:
            if len(y) > 3:
                returnlist.append(i)
            i += 1;
        return returnlist