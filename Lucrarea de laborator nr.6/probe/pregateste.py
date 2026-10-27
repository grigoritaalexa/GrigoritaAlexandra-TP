import base64
import hashlib
import io
import zipfile
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote

from PIL import Image


PROBE = Path(__file__).resolve().parent


def creeaza_mesaj():
    mesaj = b"FLAG{straturi_decodate}"
    hexazecimal = mesaj.hex()
    base64_text = base64.b64encode(hexazecimal.encode("ascii")).decode("ascii")
    return quote(base64_text, safe="")


def creeaza_foto(cale):
    imagine = Image.new("RGB", (160, 120), (116, 164, 196))
    exif = Image.Exif()
    exif[34853] = {
        1: "N",
        2: (Fraction(47), Fraction(0), Fraction(0)),
        3: "E",
        4: (Fraction(28), Fraction(50), Fraction(0)),
    }
    imagine.save(cale, format="JPEG", quality=95, exif=exif)


def creeaza_imagine_cu_zip(cale_foto, cale_destinatie):
    with Image.open(cale_foto) as imagine:
        buffer_imagine = io.BytesIO()
        imagine.save(buffer_imagine, format="PNG")

    buffer_zip = io.BytesIO()
    with zipfile.ZipFile(buffer_zip, "w", zipfile.ZIP_DEFLATED) as arhiva:
        arhiva.writestr(
            "mesaj_ascuns.txt",
            "Arhiva ascunsa extrasa cu succes din imagine.",
        )
    cale_destinatie.write_bytes(buffer_imagine.getvalue() + buffer_zip.getvalue())


def main():
    PROBE.mkdir(parents=True, exist_ok=True)
    (PROBE / "mesaj.txt").write_text(creeaza_mesaj(), encoding="ascii")

    mesaj_xor = (
        "Mesaj XOR pentru laborator; alfabet imprimabil: "
        + "".join(chr(c) for c in range(32, 127))
    ).encode("ascii")
    cheie = 0x5A
    (PROBE / "xor.bin").write_bytes(bytes(octet ^ cheie for octet in mesaj_xor))

    cuvinte = ["parola2026", "secretlab", "forensics", "steganografie"]
    (PROBE / "wordlist.txt").write_text(
        "\n".join(cuvinte) + "\n", encoding="ascii"
    )
    hashuri = [
        hashlib.sha256(b"secretlab").hexdigest(),
        hashlib.md5(b"parola2026").hexdigest(),
        hashlib.sha1(b"forensics").hexdigest(),
    ]
    (PROBE / "hashuri.txt").write_text("\n".join(hashuri) + "\n", encoding="ascii")

    challenge_mesaj = b"FLAG{challenge_decodat_si_verificat}"
    challenge_cheie = 0x37
    challenge_criptat = bytes(
        octet ^ challenge_cheie for octet in challenge_mesaj
    )
    (PROBE / "challenge.bin").write_bytes(
        base64.b64encode(challenge_criptat) + b"\n"
    )
    challenge_hash = hashlib.sha256(challenge_mesaj).hexdigest()
    (PROBE / "challenge_hint.txt").write_text(
        "Challenge local: decodeaza Base64, apoi incearca toate cheile XOR de un octet.\n"
        "Verifica mesajul recuperat cu hash-ul SHA-256 de mai jos.\n"
        f"SHA256: {challenge_hash}\n",
        encoding="ascii",
    )

    cale_foto = PROBE / "foto.jpg"
    creeaza_foto(cale_foto)
    creeaza_imagine_cu_zip(cale_foto, PROBE / "ascuns.png")

    print(f"Probe create in {PROBE}")
    print(f"Mesajul codat: {PROBE / 'mesaj.txt'}")
    print(f"Fisierele XOR/hash: {PROBE / 'xor.bin'}, {PROBE / 'hashuri.txt'}")
    print(f"Challenge: {PROBE / 'challenge.bin'}, {PROBE / 'challenge_hint.txt'}")
    print(f"Imaginile de test: {PROBE / 'foto.jpg'}, {PROBE / 'ascuns.png'}")


if __name__ == "__main__":
    main()
