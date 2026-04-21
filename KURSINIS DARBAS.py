import sqlite3
import math
import os
from datetime import datetime
from abc import ABC, abstractmethod


class TransportoPriemone(ABC):
    def __init__(self, numeris, bazinis_tarifas):
        self.numeris = numeris
        self.tarifas = self.skaiciuoti_tarifa(bazinis_tarifas)
    
    @abstractmethod
    def skaiciuoti_tarifa(self, bazinis):
        """Abstraktus metodas (Polimorfizmas)"""
        pass

class Transportas(TransportoPriemone):
    def skaiciuoti_tarifa(self, bazinis):
        return bazinis
    def __str__(self): return "Standartinis"

class Elektromobilis(TransportoPriemone):
    def skaiciuoti_tarifa(self, bazinis):
        return bazinis * 0.5 # 50% nuolaida
    def __str__(self): return "Elektromobilis"

# SINGLETON
class DBValdiklis:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBValdiklis, cls).__new__(cls)
            cls._instance.db_pavadinimas = "miesto_parkingas.db"
        return cls._instance

    def vykdyti(self, uzklausa, parametrai=()):
        with sqlite3.connect(self.db_pavadinimas) as conn:
            return conn.execute(uzklausa, parametrai)

#  SISTEMA 
class ParkingoSistema:
    def __init__(self, talpa=50):
        self.talpa = talpa
        self.db = DBValdiklis()
        self.bazinis_tarifas = 2.0
        self.db_pavadinimas = self.db.db_pavadinimas 
        self._sukurti_db()

    def _sukurti_db(self):
        self.db.vykdyti("CREATE TABLE IF NOT EXISTS parkavimas (nr TEXT PRIMARY KEY, tipas TEXT, laikas TEXT, tarifas REAL)")
        self.db.vykdyti("CREATE TABLE IF NOT EXISTS istorija (nr TEXT, tipas TEXT, atvyko TEXT, isvyko TEXT, kaina REAL)")

    def keisti_kaina(self):
        try:
            nauja = float(input(f"Dabartinė kaina {self.bazinis_tarifas}€. Įveskite naują: "))
            self.bazinis_tarifas = nauja
            print(f"SĖKMĖ: Nauja kaina: {self.bazinis_tarifas}€/val.")
        except ValueError:
            print("KLAIDA: Įveskite skaičių.")

    def prideti_auto(self):
        uzimta = self.gauti_uzimtas_vietas()
        if uzimta >= self.talpa:
            print(f"\nAikštelė pilna! ({uzimta}/{self.talpa})")
            return

        nr = input("Įveskite numerį: ").upper().strip()
        if not nr: return

        tipas_input = input("1 - Standartinis, 2 - Elektromobilis: ")
        auto = Elektromobilis(nr, self.bazinis_tarifas) if tipas_input == "2" else Transportas(nr, self.bazinis_tarifas)
        laikas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.db.vykdyti("INSERT INTO parkavimas VALUES (?, ?, ?, ?)", 
                           (auto.numeris, str(auto), laikas, auto.tarifas))
            print(f"Sėkmingai pastatytas: {auto.numeris} ({auto}).")
        except sqlite3.IntegrityError:
            print(f"KLAIDA: Automobilis {nr} jau stovi.")

    def pasalinti_auto(self):
        nr = input("Išvažiuojančio numeris: ").upper().strip()
        res = self.db.vykdyti("SELECT tipas, laikas, tarifas FROM parkavimas WHERE nr = ?", (nr,)).fetchone()

        if res:
            tipas, atvyko_str, tarifas = res
            isvyko = datetime.now()
            atvyko = datetime.strptime(atvyko_str, "%Y-%m-%d %H:%M:%S")
            
            valandos = max(1, math.ceil((isvyko - atvyko).total_seconds() / 3600))
            suma = valandos * tarifas

            self.db.vykdyti("INSERT INTO istorija VALUES (?, ?, ?, ?, ?)", 
                           (nr, tipas, atvyko_str, isvyko.strftime("%Y-%m-%d %H:%M:%S"), suma))
            self.db.vykdyti("DELETE FROM parkavimas WHERE nr = ?", (nr,))
            print(f"\n--- SĄSKAITA ---\nNumeris: {nr}\nLaikas: {valandos} val.\nMokėti: {suma:.2f}€")
        else:
            print("Automobilis nerastas.")

    def detali_aiksteles_busena(self):
        irasai = self.db.vykdyti("SELECT nr, tipas, laikas FROM parkavimas").fetchall()
        print(f"\n========== AIKŠTELĖ ({len(irasai)}/{self.talpa}) ==========")
        if not irasai:
            print("Aikštelė tuščia.")
        else:
            print(f"{'Numeris':<10} | {'Tipas':<15} | {'Atvykimo laikas'}")
            print("-" * 50)
            for r in irasai:
                print(f"{r[0]:<10} | {r[1]:<15} | {r[2]}")
        
        pelnas = self.db.vykdyti("SELECT SUM(kaina) FROM istorija").fetchone()[0] or 0.0
        print("-" * 50)
        print(f"Bendras uždarbis: {pelnas:.2f}€")

    def gauti_uzimtas_vietas(self):
        return self.db.vykdyti("SELECT COUNT(*) FROM parkavimas").fetchone()[0]

#  MENIU
def programa():
    p = ParkingoSistema(talpa=20)
    while True:
        print(f"\nPARKINGO VALDYMAS (Kaina: {p.bazinis_tarifas}€/val)")
        print("1. Įvažiavimas")
        print("2. Išvažiavimas (Apmokėjimas)")
        print("3. DETALI AIKŠTELĖS BŪSENA")
        print("4. Keisti valandinę kainą")
        print("5. Išeiti")
        
        c = input("Pasirinkite veiksmą: ")
        if c == "1": p.prideti_auto()
        elif c == "2": p.pasalinti_auto()
        elif c == "3": p.detali_aiksteles_busena()
        elif c == "4": p.keisti_kaina()
        elif c == "5": break

if __name__ == "__main__":
    programa()