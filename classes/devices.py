class Device:
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str):
        self.nr = nr
        self.typ = typ
        self.produsent = produsent
        self.produktNavn = produktnavn
        self.serieNummer = serienummer


class Actuator(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str, on_off: bool = False):
        self.setValue = float(0)  # casting float
        self.on_off = bool(on_off)  # casting bool
        self.unit = ""
        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # henter variablene til parent class Device

    def __repr__(self):
        if self.on_off:
            paster = "ON"
        else:
            paster = "OFF"
        return f"Aktuator({self.serieNummer}) TYPE: {self.typ} STATUS: {paster} PRODUCT DETAILS: {self.produsent} {self.produktNavn}"


class Sensor(Device):
    def __init__(self, nr: int, typ: str, produsent: str, produktnavn: str, serienummer: str, unit: str = ""):
        super().__init__(nr, typ, produsent, produktnavn, serienummer)  # henter variablene til parent class Device
        self.maaltVerdi = float(0)
        self.unit = unit
    def __repr__(self):
        return f"Sensor({self.serieNummer}) TYPE: {self.typ} STATUS: {self.maaltVerdi} {self.unit} PRODUCT DETAILS: {self.produsent} {self.produktNavn}"
        return f'Målt Verdi: {self.maaltVerdi}, unit: {self.unit}'

