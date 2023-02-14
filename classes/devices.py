class Device:
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        self.nr = nr
        self.typ = typ
        self.produsent = produsent
        self.produktNavn = produktnavn
        self.serieNummer = serienummer


class Actuator(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        self.setValue = float(0)  # casting float
        self.on_off = bool(False)  # casting bool
        self.unit = ""

        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # henter variablene til parent class Device


class Sensor(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # henter variablene til parent class Device
        self.maaltVerdi = maaltVerdi

    def __repr__(self):
        return f'Recorded Value: {self.GetReading()}, Annotation: {self.GetUnit()}'

    def GetReading(self):
        pass

    def ReadSensorValue(self):  # selve verdien
        pass

    def GetUnit(self):  # Her skal vi sjekke type unit sensoren måler (celcius, %, whatever)
        pass

# TODO! Her skal du utvikle din egen design av en klassestruktur med enheter og deres funkjsoner!


# lag en def som create sensor