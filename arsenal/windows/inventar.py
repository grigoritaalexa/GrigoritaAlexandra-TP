from dataclasses import dataclass, asdict
import json
import argparse

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}

# A1. Clasa Proces cu decoratorul @dataclass pentru generarea automată a constructorului
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    # A2. Metoda e_suspect folosește self pentru a verifica calea proprie
    def e_suspect(self):
        return any(cautat in self.cale for cautat in CAI_SUSPECTE)

# A3. Clasa Eveniment modelează jurnalele de securitate Windows
@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"

# A4. Funcție pentru citirea JSON și despachetarea dicționarului în obiecte Proces
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]

# B1. Clasa-container Inventar cu constructor alternativ din_json folosind @classmethod
@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    # Suprascrierea metodei magice __len__ pentru funcția len()
    def __len__(self):
        return len(self.procese)

    # B2. Metoda suspecte returnează procesele care activează e_suspect()
    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    # B2. Metoda pe_user grupează procesele per utilizator folosind setdefault
    def pe_user(self):
        grupate = {}
        for p in self.procese:
            grupate.setdefault(p.user, []).append(p.nume)
        return grupate

# B3. Funcția principală main gestionează argumentele din linia de comandă și afișarea raportului
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in inv.suspecte()],
            "evenimente_alarma": [asdict(e) for e in alarma]
        }
        print(json.dumps(raport, indent=2))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")
        for p in inv.suspecte():
            print(f"  [{p.pid}] {p.nume}  ({p.user})  {p.cale}")
        
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()