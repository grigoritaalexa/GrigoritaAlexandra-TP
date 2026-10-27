import argparse
import base64
import binascii
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote


def ghici_strat(s):
    # Verifică dacă are caractere codate URL (%xx)
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    # Verifică dacă este doar din caractere hexadecimale și are lungime pară
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    # Verifică alfabetul specific Base64
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"


def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        try:
            rezultat = base64.b64decode(s, validate=True)
            return strat, rezultat
        except (binascii.Error, ValueError):
            return "necunoscut", s.encode("utf-8")
    elif strat == "hex":
        try:
            rezultat = bytes.fromhex(s)
            return strat, rezultat
        except ValueError:
            return "necunoscut", s.encode("utf-8")
    elif strat == "url":
        return strat, unquote(s).encode("utf-8")
    return "necunoscut", s.encode("utf-8")


def citibil(b):
    # Returnează True dacă toți octeții is caractere ASCII (32..126)
    return all(32 <= c < 127 for c in b)


def decodare_multipla(val):
    strat_final = "necunoscut"
    rezultat = val.encode("utf-8")
    for _ in range(8):
        strat, b = desfa(val)
        if strat == "necunoscut":
            return strat_final, rezultat
        strat_final = strat
        rezultat = b
        try:
            val_decodat = b.decode("utf-8")
        except UnicodeDecodeError:
            return strat_final, rezultat
        if citibil(b) and ghici_strat(val_decodat) == "necunoscut":
            return strat_final, rezultat
        val = val_decodat
    return strat_final, rezultat


def sparge_xor(cale_fisier):
    with open(cale_fisier, "rb") as f:
        date = f.read()
    rezultate = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            rezultate.append((k, clar.decode("utf-8", errors="ignore")))
    return rezultate


def sparge_hashuri(cale_hashuri, cale_wordlist):
    algoritmi = {32: "md5", 40: "sha1", 64: "sha256"}
    tinte = []
    with open(cale_hashuri, encoding="ascii") as f:
        for linie in f:
            tinta = linie.strip().lower()
            if not tinta:
                continue
            algoritm = algoritmi.get(len(tinta))
            if algoritm is None or re.fullmatch(r"[0-9a-f]+", tinta) is None:
                raise ValueError(f"Hash neacceptat: {tinta}")
            tinte.append((tinta, algoritm))

    gasite = {}
    with open(cale_wordlist, encoding="latin1", errors="ignore") as f:
        for cuv in f:
            cuv = cuv.strip()
            pentru_cuvant = cuv.encode()
            for tinta, algoritm in tinte:
                if tinta in gasite:
                    continue
                digest = hashlib.new(algoritm, pentru_cuvant).hexdigest()
                if digest == tinta:
                    gasite[tinta] = cuv

    return [
        (tinta, algoritm, gasite[tinta])
        for tinta, algoritm in tinte
        if tinta in gasite
    ]


def sparge_hash(cale_hashuri, cale_wordlist):
    with open(cale_hashuri, encoding="ascii") as f:
        tinta = next((linie.strip().lower() for linie in f if linie.strip()), None)
    if tinta is None:
        return None
    rezultate = sparge_hashuri(cale_hashuri, cale_wordlist)
    return next(
        (parola for hash_curent, _, parola in rezultate if hash_curent == tinta),
        None,
    )


def sparge_challenge(cale_challenge, cale_hint):
    with open(cale_challenge, "rb") as f:
        codificat = f.read().strip()
    try:
        text_base64 = codificat.decode("ascii")
        criptat = base64.b64decode(text_base64, validate=True)
    except (UnicodeDecodeError, binascii.Error, ValueError) as exc:
        raise ValueError("Challenge-ul nu contine Base64 valid.") from exc

    with open(cale_hint, encoding="utf-8") as f:
        hint = f.read()
    potrivire = re.search(
        r"(?im)^\s*sha256\s*:\s*([0-9a-f]{64})\s*$",
        hint,
    )
    if potrivire is None:
        raise ValueError("Fisierul hint trebuie sa contina o linie SHA256: <hash>.")
    hash_asteptat = potrivire.group(1).lower()

    for cheie in range(256):
        clar = bytes(octet ^ cheie for octet in criptat)
        if (
            citibil(clar)
            and hashlib.sha256(clar).hexdigest() == hash_asteptat
        ):
            return cheie, clar
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Decoder universal pentru siruri si probele laboratorului A.",
        epilog=(
            'Exemple: decode.py "U2FsdXQ="; '
            "decode.py probe/mesaj.txt --fisier; "
            "decode.py probe/xor.bin --xor; "
            "decode.py probe/hashuri.txt --wordlist probe/wordlist.txt"
        ),
    )
    parser.add_argument(
        "intrare", help="Sirul codat sau calea catre fisierul de intrare"
    )
    mod = parser.add_mutually_exclusive_group()
    mod.add_argument("--fisier", action="store_true", help="Decodeaza un fisier")
    mod.add_argument(
        "--xor", action="store_true", help="Incearca toate cheile XOR de un octet"
    )
    mod.add_argument(
        "--wordlist", metavar="CALE", help="Cauta hash-ul/hash-urile in wordlist"
    )
    mod.add_argument(
        "--challenge",
        action="store_true",
        help="Decodifica Base64, sparge XOR si verifica SHA-256 din hint",
    )
    args = parser.parse_args()

    if args.xor:
        rezultate = sparge_xor(args.intrare)
        if not rezultate:
            print("Nu a fost gasit niciun rezultat cu text ASCII imprimabil.")
        for cheie, text in rezultate:
            print(f"Cheie XOR: {cheie} (0x{cheie:02x})")
            print(f"Text: {text}")
    elif args.wordlist:
        rezultate = sparge_hashuri(args.intrare, args.wordlist)
        if not rezultate:
            print("Nu a fost gasita nicio parola in wordlist.")
        for tinta, algoritm, parola in rezultate:
            print(f"{algoritm} {tinta}: {parola}")
    elif args.challenge:
        cale_intrare = Path(args.intrare)
        cale_hint = cale_intrare.with_name("challenge_hint.txt")
        rezultat = sparge_challenge(cale_intrare, cale_hint)
        if rezultat is None:
            print("Nu s-a gasit o cheie XOR care sa confirme hash-ul SHA-256.")
        else:
            cheie, clar = rezultat
            print(f"Cheie XOR: {cheie} (0x{cheie:02x})")
            print(f"SHA-256 verificat: {hashlib.sha256(clar).hexdigest()}")
            print(f"Mesaj: {clar.decode('ascii')}")
    else:
        if args.fisier:
            with open(args.intrare, "rb") as f:
                continut = f.read()
        else:
            continut = args.intrare.encode("utf-8")
        try:
            val_str = continut.decode("utf-8")
            strat, rezultat_b = decodare_multipla(val_str)
            try:
                rezultat_str = rezultat_b.decode("utf-8")
            except UnicodeDecodeError:
                rezultat_str = rezultat_b.hex()
        except UnicodeDecodeError:
            strat = "binar"
            rezultat_str = continut.hex()

        fisa = {"strat": strat, "rezultat": rezultat_str}

        cale_fisa = Path(__file__).resolve().with_name("fisa.json")
        with cale_fisa.open("w", encoding="utf-8") as f:
            json.dump(fisa, f, indent=4, ensure_ascii=False)

        print(f"Strat detectat: {strat}")
        print(f"Rezultat: {rezultat_str}")
        print(f"Fisa a fost salvata in {cale_fisa}")