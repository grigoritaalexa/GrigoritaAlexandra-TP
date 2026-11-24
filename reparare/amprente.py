import argparse
import hashlib
import os

MAGIC = {
    b"\x89PNG": "PNG",
    b"%PDF": "PDF",
    b"PK\x03\x04": "ZIP",
}


def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    # Greseala 1 reparata: return "necunoscut" mutat dupa bucla for (nu in interior)
    return "necunoscut"


def amprenta_fisier(cale):
    # Greseala 2 reparata: deschidere in mod binar "rb" cu with (nu mod text)
    with open(cale, "rb") as f:
        date = f.read()
    return {
        "nume": os.path.basename(cale),
        "tip": tip(date[:8]),
        # Greseala 3 reparata: pastrate primele 16 caractere din SHA-256 (nu doar 8)
        "sha256": hashlib.sha256(date).hexdigest()[:16],
    }


def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()
    for fisa in scaneaza(args.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")


if __name__ == "__main__":
    main()