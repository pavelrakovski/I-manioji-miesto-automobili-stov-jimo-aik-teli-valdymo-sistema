# Išmanioji parkingo sistema (Kursinis darbas)

Tai mano kursinis projektas, skirtas automobilių aikštelės valdymui. Programa leidžia registruoti mašinas, skaičiuoti laiką ir kainą, o visi duomenys saugomi SQLite duomenų bazėje.

## 1. Kaip viskas veikia
Programa veikia per konsolę (terminalą). Paleidus `KURSINIS DARBAS.py`, atsidaro meniu, kuriame galima valdyti visą aikštelės procesą realiu laiku: registruoti įvažiavimus, išvažiavimus ir stebėti statistiką.

---

## 2. Programos analizė (OOP dalis)

Savo kode panaudojau pagrindinius objektinio programavimo principus:

### Abstrakcija
Sukūriau bendrą šabloną transportui, kad visos mašinos turėtų tuos pačius pagrindinius duomenis ir funkcijas.
```python
class TransportoPriemone(ABC):
    @abstractmethod
    def skaiciuoti_tarifa(self, bazinis_tarifas):
        pass
```

### Paveldėjimas
Sukūriau atskiras klases paprastoms mašinoms ir elektromobiliams. Jos paveldi viską iš pagrindinės klasės.
```python
class Elektromobilis(TransportoPriemone):
    # Paveldi numerį ir kitus laukus iš TransportoPriemone
```

### Polimorfizmas
Tai padėjo man padaryti nuolaidą elektromobiliams. Nors metodas vadinasi taip pat, jo viduje logika skiriasi.
```python
def skaiciuoti_tarifa(self, bazinis):
    return bazinis * 0.5  # 50% nuolaida elektromobiliams
```

### Inkapsuliacija
Paslėpiau duomenų bazės sukūrimo funkciją, kad ji nebūtų pasiekiama tiesiogiai iš kitų klasių.
```python
def _sukurti_db(self):
    # Vidinis metodas bazės paruošimui
```

### Singleton modelis
Užtikrinau, kad duomenų bazės valdiklis būtų tik vienas visoje programoje.
```python
class DBValdiklis:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBValdiklis, cls).__new__(cls)
        return cls._instance
```

### Ryšiai tarp objektų
- **Kompozicija (Composition):** `ParkingoSistema` savyje sukuria `DBValdiklis` objektą. Be šio objekto sistema negalėtų funkcionuoti.
- **Agregacija (Aggregation):** Aikštelės objektas talpina automobilių objektus, tačiau automobiliai gali egzistuoti ir nepriklausomai nuo pačios aikštelės.

---

## 3. SOLID principų taikymas

Projekte laikausi **SOLID** principų, kurie užtikrina kodo lankstumą:

1. **S (Single Responsibility):** Kiekviena klasė atsakinga tik už vieną dalyką (pvz., `DBValdiklis` tik už duomenis, `ParkingoSistema` tik už logiką).
2. **O (Open/Closed):** Sistema yra atvira naujiems transporto tipams (pvz., galima lengvai pridėti `Motociklas`), nekeičiant esamo kodo.
3. **L (Liskov Substitution):** Bet kurią transporto priemonę galime pakeisti jos „vaiku“ (pvz., `Elektromobilis`), ir programa veiks teisingai.
4. **I (Interface Segregation):** Klasės naudoja tik tuos metodus, kurių joms tikrai reikia.
5. **D (Dependency Inversion):** Aukšto lygio logika priklauso nuo abstrakcijų (`TransportoPriemone`), o ne nuo konkrečių klasių.

---

## 4. Testavimas

Programos veikimą patikrinau naudodamas `unittest` biblioteką:

### 1. Kainos skaičiavimo testas
Tikrinama, ar sistema teisingai suskaičiuoja kainą paprastam automobiliui.
```python
def test_kainos_skaiciavimas(self):
    rezultatas = self.sistema.paskaiciuoti_kaina(valandos=2, tarifas=1.0)
    self.assertEqual(rezultatas, 2.0)
```

### 2. Elektromobilio nuolaidos testas
Tikrinama, ar elektromobiliui teisingai pritaikoma 50% nuolaida.
```python
def test_elektromobilio_nuolaida(self):
    rezultatas = self.elektro_auto.skaiciuoti_tarifa(1.0)
    self.assertEqual(rezultatas, 0.5)
```

### 3. Singleton modelio patikra
Užtikrinama, kad programoje visada naudojama ta pati duomenų bazės jungtis.

---

## 5. Išvados
Darbas padėjo geriau suprasti OOP ir SOLID principų svarbą. Sistema veikia stabiliai, o paruošti testai padeda užtikrinti kodo kokybę.
