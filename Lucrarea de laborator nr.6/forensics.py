import re
import zipfile
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


def extrage_strings(cale):
    with open(cale, "rb") as f:
        date = f.read()
    return [m.decode("ascii") for m in re.findall(rb"[ -~]{4,}", date)]


def extrage_exif_gps(cale):
    with Image.open(cale) as img:
        exif = img.getexif()
        if not exif:
            print("Fisierul nu contine metadate EXIF.")
            return {}

        print("--- METADATE EXIF ---")
        for tag_id, val in exif.items():
            nume_tag = TAGS.get(tag_id, tag_id)
            if nume_tag != "GPSInfo":
                print(f"{nume_tag} = {val}")

        gps = exif.get_ifd(34853)
    if not gps:
        print("Nu s-au gasit coordonate GPS.")
        return {}

    info_gps = {GPSTAGS.get(tag_id, tag_id): val for tag_id, val in gps.items()}
    for nume, val in info_gps.items():
        print(f"{nume} = {val}")

    def in_grade(zecimale):
        grade, minute, secunde = zecimale
        return float(grade) + float(minute) / 60 + float(secunde) / 3600

    if "GPSLatitude" in info_gps and "GPSLatitudeRef" in info_gps:
        latitudine = in_grade(info_gps["GPSLatitude"])
        if info_gps["GPSLatitudeRef"] == "S":
            latitudine = -latitudine
        info_gps["Latitudine zecimala"] = latitudine
    if "GPSLongitude" in info_gps and "GPSLongitudeRef" in info_gps:
        longitudine = in_grade(info_gps["GPSLongitude"])
        if info_gps["GPSLongitudeRef"] == "W":
            longitudine = -longitudine
        info_gps["Longitudine zecimala"] = longitudine

    print("--- COORDONATE GPS ---")
    if "Latitudine zecimala" in info_gps and "Longitudine zecimala" in info_gps:
        print(
            f'{info_gps["Latitudine zecimala"]}, '
            f'{info_gps["Longitudine zecimala"]}'
        )
    return info_gps


def extrage_fisier_ascuns(cale_sursa, cale_destinatie="gasit.zip"):
    with open(cale_sursa, "rb") as f:
        date = f.read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        print("Nu s-a gasit nicio semnatura ZIP.")
        return False
    with open(cale_destinatie, "wb") as f_out:
        f_out.write(date[i:])
    print(f"Arhiva extrasa de la octetul {i} in {cale_destinatie}")
    return True


def ascunde_lsb(cale_sursa, mesaj, cale_destinatie="stego.png"):
    if not isinstance(mesaj, bytes):
        raise TypeError("Mesajul trebuie furnizat ca bytes.")
    with Image.open(cale_sursa) as sursa:
        img = sursa.convert("RGB")
    pixels = img.load()
    px = [
        pixels[x, y]
        for y in range(img.height)
        for x in range(img.width)
    ]
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")
    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul este prea lung pentru această imagine!")

    px_nou = []
    idx_bit = 0
    for pixel in px:
        canale_noi = []
        for canal in pixel:
            if idx_bit < len(biti):
                canal = (canal & ~1) | int(biti[idx_bit])
                idx_bit += 1
            canale_noi.append(canal)
        px_nou.append(tuple(canale_noi))

    img_noua = Image.new("RGB", img.size)
    img_noua.putdata(px_nou)
    img_noua.save(cale_destinatie, format="PNG")
    print(f"Mesaj ascuns cu succes in {cale_destinatie}")


def dezvaluie_lsb(cale_stego):
    with Image.open(cale_stego) as img:
        img = img.convert("RGB")
        pixels = img.load()
        px = [
            pixels[x, y]
            for y in range(img.height)
            for x in range(img.width)
        ]

    biti = "".join(str(canal & 1) for pixel in px for canal in pixel)
    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        valoare = int(biti[i : i + 8], 2)
        if valoare == 0:
            break
        octeti.append(valoare)
    mesaj = octeti.decode("utf-8", errors="replace")
    print(f"Mesaj recuperat: {mesaj}")
    return mesaj


def analizeaza_arhiva(cale_arhiva):
    with zipfile.ZipFile(cale_arhiva) as arhiva:
        for nume in arhiva.namelist():
            print(f"Fisier in arhiva: {nume}")
            continut = arhiva.read(nume)
            try:
                print(continut.decode("utf-8"))
            except UnicodeDecodeError:
                print(f"Continut binar ({len(continut)} octeti).")


if __name__ == "__main__":
    director = Path(__file__).resolve().parent
    probe = director / "probe"
    cale_foto = probe / "foto.jpg"
    cale_ascuns = probe / "ascuns.png"
    if not cale_foto.exists() or not cale_ascuns.exists():
        raise FileNotFoundError(
            "Lipsesc probele laboratorului. Ruleaza mai intai "
            "'python probe/pregateste.py'."
        )

    print("Tip real foto.jpg:", tip_real(cale_foto))
    print("Tip real ascuns.png:", tip_real(cale_ascuns))
    print("--- STRINGS DIN ascuns.png ---")
    for sir in extrage_strings(cale_ascuns):
        print(sir)
    extrage_exif_gps(cale_foto)

    cale_zip = director / "gasit.zip"
    if extrage_fisier_ascuns(cale_ascuns, cale_zip):
        analizeaza_arhiva(cale_zip)

    cale_stego = director / "stego.png"
    ascunde_lsb(cale_foto, b"FLAG{ascuns_in_pixeli}", cale_stego)
    dezvaluie_lsb(cale_stego)