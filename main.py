from classes.smarthouse import SmartHouse
from persistence import SmartHousePersistence
from classes.devices import *

#
# endret en entry, panelovn serial nr fra 'd16d84de-79f1-4f9a' til 'd16d84de-79f1-4f9b' ettersom det var 2 entries
#


def add_rooms_floors(result, persistence):
    rooms = persistence.query("SELECT * FROM rooms")
    for x in rooms:
        if(result.get_floor(x['floor']) == None):
            result.create_floor(x['floor'])
        if result.get_room_by_name(x['name']) == None:
            result.create_room(x['floor'], x['area'], x['name'], x['id'])


def add_actuators_and_sensors(result, persistence):
    # adds actuators and sensors to the various rooms
    devices = persistence.query("SELECT * FROM devices")
    for x in devices:
        if(result.find_device_by_serial_no(x['serial_no']) == None):
            if("måler" in x['type']):
                somedevice = Sensor(x['id'], x['type'], x['producer'], x['product_name'], x['serial_no'])
            elif ("sensor" in x['type']):
                somedevice = Sensor(x['id'], x['type'], x['producer'], x['product_name'], x['serial_no'])
            else:
                somedevice = Actuator(x['id'], x['type'], x['producer'], x['product_name'], x['serial_no'])
            someroom = result.get_room_by_id(x['room'])
            result.register_device(somedevice, someroom)

def add_load_sensors_actuator_values(result, persistence):
    # load latest sensor values to sensors
    measurements = persistence.query("select time_stamp, device ,value from measurements m1 "
                               "WHERE time_stamp = (SELECT MAX(time_stamp) "
                               "FROM measurements m2 "
                               "WHERE m1.device  = m2.device)"
                               "ORDER BY device, time_stamp;")
    for x in measurements:
        somedevice = result.find_device_by_id(x['device'])
        if somedevice != None:
            result.manualy_alter_sensordevice(somedevice, maaltverdi=x['value'])

    actuatorvalues = persistence.query("SELECT * FROM actuators")
    for x in actuatorvalues:
        somedevice = result.find_device_by_serial_no(x['serial_no'])
        if somedevice != None:
            somedevice.on_off = x['on_off']
            somedevice.setValue = x['setvalue']
            somedevice.unit = x['unit']



def load_demo_house(persistence: SmartHousePersistence) -> SmartHouse:
    result = SmartHouse()
    add_rooms_floors(result, persistence)
    add_actuators_and_sensors(result, persistence)
    add_load_sensors_actuator_values(result, persistence)

    return result
def add2db(p, device: Actuator):
    injectstring = "INSERT INTO actuators (setvalue, on_off, unit, serial_no)" \
                   "VALUES ('{0}', '{1}', '{2}', '{3}');".format(device.setValue,device.on_off,device.unit,device.serieNummer)
    p.injector(injectstring)
    pass
def build_demo_house() -> SmartHouse:
    house = SmartHouse()
    house.create_floor(0) #første etasje = 0
    house.create_room(0, 39.75, "Livingroom_kitchen")
    house.create_room(0, 6.3, "Bathroom1")
    house.create_room(0, 13.5, "Entrance")
    house.create_room(0, 8, "GuestRoom1")
    house.create_room(0, 19, "Garage_outside")
    house.create_floor(1)
    house.create_room(1, 11.75, "Office")
    house.create_room(1, 9.25, "Bathroom2")
    house.create_room(1, 8, "GuestRoom2")
    house.create_room(1, 10, "GuestRoom3")
    house.create_room(1, 4, "DressingRoom")
    house.create_room(1, 17, "MasterBedroom")
    house.create_room(1, 10, "Hallway")
    # Sensors
    house.load_devicelist()
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("4cb686fe-6448-4cf6"), '%', 68)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("e237beec-2675-4cb0"), '°C', 1.3)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("c8bb5601-e850-4a80"), 'kWh', 0)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("d16d84de-79f1-4f9a"), '°C', 18.1)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("3b06cf0f-8494-458b"), 'kWh', 1.5)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("c76688cc-3692-4aa3"), 'g/m^2', 0.08)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("8ceb53b2-e88f-4e8c"), '%', 52)
    house.manualy_alter_sensordevice(house.find_device_by_serial_no("481e94bd-ff50-40ea"), '°C', 16.1)

    return house


def do_device_list(smart_house: SmartHouse):
    print("Listing Devices...")
    idx = 0
    for d in smart_house.get_all_devices():
        print(f"{idx}: {d}")
        idx += 1


def do_room_list(smart_house: SmartHouse):
    print("Listing Rooms...")
    idx = 0
    for r in smart_house.get_all_rooms():
        print(f"{idx}: {r}")
        idx += 1

def do_find(smart_house: SmartHouse):
    print("Please enter serial no: ")
    serial_no = input()
    device = smart_house.find_device_by_serial_no(serial_no)
    if device:
        devices = smart_house.get_all_devices()
        rooms = smart_house.get_all_rooms()
        room = smart_house.get_room_with_device(device)
        device_idx = devices.index(device)
        room_idx = rooms.index(room)
        print(f"Device No {device_idx}:")
        print(device)
        print(f"is located in room No {room_idx}:")
        print(room)
    else:
        print(f"Could not locate device with serial no {serial_no}")


def do_move(smart_house):
    devices = smart_house.get_all_devices()
    rooms = smart_house.get_all_rooms()
    print("Please choose device:")
    device_id = input()
    device = None
    if device_id.isdigit():
        device = devices[int(device_id)]
    else:
        device = smart_house.find_device_by_serial_no(device_id)
    if device:
        print("Please choose target room")
        room_id = input()
        if room_id.isdigit() and rooms[int(room_id)]:
            to_room = rooms[int(room_id)]
            from_room = smart_house.get_room_with_device(device)
            smart_house.move_device(device, from_room, to_room)
        else:
            print(f"Room with no {room_id} does not exist!")
    else:
        print(f"Device wit id '{device_id}' does not exist")


def main(smart_house: SmartHouse):
    print("************ Smart House Control *****************")
    print(f"No of Rooms:       {smart_house.get_no_of_rooms()}")
    print(f"Total Area:        {smart_house.get_total_area()}")
    print(f"Connected Devices: {smart_house.get_no_of_devices()} ({smart_house.get_no_of_sensors()} Sensors | {smart_house.get_no_of_actuators()} Actuators)")
    print("**************************************************")
    print()
    print("Management Interface v.0.1")
    while (True):
        print()
        print("Please select one of the following options:")
        print("- List all devices in the house (l)")
        print("- List all rooms in the house (r) ")
        print("- Find a device via its serial number (f)")
        print("- Move a device from one room to another (m)")
        print("- Quit (q)")
        char = input()
        if char == "l":
            do_device_list(smart_house)
        elif char == "r":
            do_room_list(smart_house)
        elif char == "f":
            do_find(smart_house)
        elif char == "m":
            do_move(smart_house)
        elif char == "q":
            break
        else:
            print(f"Error! Could not interpret input '{char}'!")


if __name__ == '__main__':
    house = load_demo_house();
    #house = build_demo_house()
    #main(house)
