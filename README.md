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
Tai padėjo man padaryti nuolaidą elektromobiliams.

```python
def skaiciuoti_tarifa(self, bazinis):
    return bazinis * 0.5  # 50% nuolaida elektromobiliams
```

### Inkapsuliacija
Paslėpiau duomenų bazės sukūrimo funkciją.

```python
def _sukurti_db(self):
    # Vidinis metodas bazės paruošimui
```

### Singleton modelis
Užtikrinau, kad duomenų bazės valdiklis būtų tik vienas.

```python
class DBValdiklis:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBValdiklis, cls).__new__(cls)
        return cls._instance
```

---

## 3. Testavimas

Savo programos stabilumą patikrinau naudodamas `unittest` biblioteką:

```python
def test_kainos_skaiciavimas(self):
    rezultatas = self.sistema.paskaiciuoti_kaina(valandos=2, tarifas=1.0)
    self.assertEqual(rezultatas, 2.0)
```

---

## 4. Išvados
Darbas padėjo suprasti, kaip praktiškai pritaikyti OOP principus. Sistema veikia stabiliai.
