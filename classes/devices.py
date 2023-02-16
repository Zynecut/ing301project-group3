class Device:
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        self.nr = nr
        self.typ = typ
        self.produsent = produsent
        self.produktNavn = produktnavn
        self.serieNummer = serienummer
        self.number_of_devices = []

    def add_device(self):
        pass

class Actuator(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str, on_off: bool = False):
        self.setValue = float(0)  # casting float
        self.on_off = on_off  # casting bool
        self.unit = ""

        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # henter variablene til parent class Device

    def __repr__(self):
        return f'Set Value: {self.setValue}, On/Off: {self.on_off}'

class Sensor(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str, unit):
        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # henter variablene til parent class Device
        self.maaltVerdi = float(0)
        self.unit = unit

    def createSensor(self):
        return f"Målt Verdi: {self.maaltVerdi}{self.unit}"


    def GetReading(self):
        pass

    def ReadSensorValue(self):  # selve verdien
        pass

    def GetUnit(self):  # Her skal vi sjekke type unit sensoren måler (celcius, %, whatever)
        pass

# TODO! Her skal du utvikle din egen design av en klassestruktur med enheter og deres funkjsoner!


# a1 = Actuator(1, "Smart Lys", "Fritsch Group", "Tresom Bright 1.0", "f11bb4fc-ba74-49cd")
s1 = Sensor(8, "Temperatursensor", "Moen Inc", "Prodder Ute 1.2", "e237beec-2675-4cb0", 25, chr(176))
print(s1.createSensor())



# Numeric point for degree symbol is 176: chr(176)
# print('8' + chr(176))
