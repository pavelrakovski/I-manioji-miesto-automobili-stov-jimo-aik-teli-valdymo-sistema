import unittest
import importlib.util
import sqlite3
import os

# Prijungiame pagrindinį programos failą
spec = importlib.util.spec_from_file_location("kursinis", "KURSINIS DARBAS.py")
kursinis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kursinis)

class TestParkingoSistema(unittest.TestCase):

    def setUp(self):
        # Paruošiame laikiną bazę testams, kad nesugadintume tikrosios
        self.test_db = "test_laikinas.db"
        self.p = kursinis.ParkingoSistema(talpa=10)
        
        # Pasakome programai naudoti šį laikiną failą
        self.p.db.db_pavadinimas = self.test_db
        self.p._sukurti_db()
        
        # Kiekvieną kartą išvalome lentelę, kad būtų tuščia
        self.p.db.vykdyti("DELETE FROM parkavimas")

    def tearDown(self):
        # Po visko ištriname tą laikiną failą iš kompiuterio
        if os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except:
                pass

    def test_vietu_skaiciavimas(self):
        # Tikriname, ar sistema mato, kai atsiranda mašina
        self.assertEqual(self.p.gauti_uzimtas_vietas(), 0) # Pradžioje 0
        self.p.db.vykdyti("INSERT INTO parkavimas VALUES ('TEST777', 'Standartinis', '2026-04-21 15:00:00', 2.0)")
        self.assertEqual(self.p.gauti_uzimtas_vietas(), 1) # Įdėjus - turi būti 1

    def test_dublikatu_apsauga(self):
        # Tikriname, ar neleis įrašyti tų pačių numerių antrą kartą
        nr = "DUP111"
        self.p.db.vykdyti("INSERT INTO parkavimas VALUES (?, ?, ?, ?)", (nr, "Standartinis", "2026-04-21 12:00:00", 2.0))
        
        # Bandome dar kartą - turi „išmesti“ klaidą
        with self.assertRaises(sqlite3.IntegrityError):
            self.p.db.vykdyti("INSERT INTO parkavimas VALUES (?, ?, ?, ?)", (nr, "Elektromobilis", "2026-04-21 13:00:00", 1.0))

    def test_elektromobilio_tarifas(self):
        # Žiūrime, ar tikrai elektromobiliams pritaiko nuolaidą
        ev = kursinis.Elektromobilis("EV001", 4.0)
        self.assertEqual(ev.tarifas, 2.0) # Turi būti perpus pigiau

    def test_ar_vienas_db_valdiklis(self):
        # Tikriname, ar programa naudoja tą patį susijungimą visur
        db1 = kursinis.DBValdiklis()
        db2 = kursinis.DBValdiklis()
        self.assertIs(db1, db2) # Turi būti tas pats objektas

    def test_kainos_keitimas(self):
        # Tikriname, ar pasikeičia kaina sistemos nustatymuose
        self.p.bazinis_tarifas = 10.0
        self.assertEqual(self.p.bazinis_tarifas, 10.0)

if __name__ == "__main__":
    unittest.main(exit=False)