import argparse
import hashlib
import os

# A1: semnaturile magic bytes pentru detectia tipului de fisier
MAGIC = {
    b"\x89PNG": "PNG",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP",
}


# A1: intoarce tipul dupa magic bytes, iar "necunoscut" ramane dupa bucla
def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"


# A2: citeste fisierul binar cu with si intoarce fisa cu tip si sha256 (16 caractere)
def amprenta_fisier(cale):
    with open(cale, "rb") as f:
        date = f.read()
    return {
        "nume": os.path.basename(cale),
        "tip": tip(date[:8]),
        "sha256": hashlib.sha256(date).hexdigest()[:16],
    }


# A3: parcurge sortat fisierele din folder si construieste lista de fise
def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez


# A3: parseaza argumentul folder din linia de comanda si afiseaza tabelul
def main():
    parser = argparse.ArgumentParser(description="Scaneaza fisiere dupa magic bytes si SHA-256.")
    parser.add_argument("folder", help="Folderul de scanat")
    args = parser.parse_args()

    for fisa in scaneaza(args.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")


if __name__ == "__main__":
    main()