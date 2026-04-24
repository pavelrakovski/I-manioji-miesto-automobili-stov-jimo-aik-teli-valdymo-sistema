# Išmanioji parkingo sistema (Kursinis darbas)

Tai mano kursinis projektas, skirtas automobilių aikštelės valdymui. Programa leidžia registruoti mašinas, skaičiuoti laiką ir kainą, o visi duomenys saugomi SQLite duomenų bazėje.

## 1. Kaip viskas veikia
Programa veikia per konsolę (terminalą). Paleidus `KURSINIS DARBAS.py`, atsidaro meniu, kuriame galima:
- Įvesti įvažiuojantį automobilį (reikia nurodyti numerį ir tipą).
- Užregistruoti išvažiavimą (sistema pati paskaičiuoja kainą).
- Pažiūrėti, kiek laisvų vietų liko.
- Pakeisti valandinį kainos tarifą.

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

**Kompozicija (Composition):**
`ParkingoSistema` klasė savyje sukuria `DBValdiklis` objektą. Be šio objekto sistema negalėtų funkcionuoti.
```python
class ParkingoSistema:
    def __init__(self):
        self.db = DBValdiklis() # Kompozicija
```

**Agregacija (Aggregation):**
Aikštelės objektas talpina automobilių objektus, tačiau automobiliai gali egzistuoti ir nepriklausomai nuo pačios aikštelės.
```python
class Aikstele:
    def __init__(self):
        self.automobiliai = [] # Agregacija
```

---

## 3. Testavimas

Programos veikimą patikrinau naudodamas `unittest` biblioteką. Štai atlikti testai:

### 1. Kainos skaičiavimo testas
Tikrinama, ar sistema teisingai suskaičiuoja kainą paprastam automobiliui už tam tikrą valandų kiekį.
```python
def test_kainos_skaiciavimas(self):
    rezultatas = self.sistema.paskaiciuoti_kaina(valandos=2, tarifas=1.0)
    self.assertEqual(rezultatas, 2.0)
```

### 2. Elektromobilio nuolaidos testas
Tikrinama, ar polimorfizmo principas veikia ir elektromobiliui teisingai pritaikoma nuolaida.
```python
def test_elektromobilio_nuolaida(self):
    rezultatas = self.elektro_auto.skaiciuoti_tarifa(1.0)
    self.assertEqual(rezultatas, 0.5)
```

### 3. Laisvų vietų testas
Testuojama, ar įvažiavus automobiliui laisvų vietų skaičius aikštelėje sumažėja vienetu.
```python
def test_laisvos_vietos(self):
    pradinis = self.sistema.laisvos_vietos
    self.sistema.registruoti_ivaziavima("AAA111")
    self.assertEqual(self.sistema.laisvos_vietos, pradinis - 1)
```

### 4. Singleton modelio patikra
Užtikrinama, kad sukūrus kelis valdiklio objektus, jie visi rodytų į tą pačią atminties vietą.
```python
def test_singleton_db(self):
    db1 = DBValdiklis()
    db2 = DBValdiklis()
    self.assertIs(db1, db2)
```

---

## 4. Išvados
Darbas padėjo geriau suprasti OOP principų svarbą. Sistema veikia stabiliai, o paruošti testai padeda užtikrinti kodo kokybę ir loginį teisingumą.
