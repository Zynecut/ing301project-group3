class Device:
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        self.nr = nr
        self.typ = typ
        self.produsent = produsent
        self.produktNavn = produktnavn
        self.serieNummer = serienummer

class Actuator(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        self.setValue = float(0)    # casting float
        self.on_off = bool(False)   # casting bool
        self.unit = ""

        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # sender variablene til parent class Device

class Sensor(Device):
    def __init__(self):
        pass


# TODO! Her skal du utvikle din egen design av en klassestruktur med enheter og deres funkjsoner!