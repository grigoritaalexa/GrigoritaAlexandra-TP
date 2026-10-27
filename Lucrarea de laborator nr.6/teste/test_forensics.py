import io
import zipfile

from PIL import Image

from forensics import (
    ascunde_lsb,
    dezvaluie_lsb,
    extrage_fisier_ascuns,
    extrage_strings,
    tip_real,
)


def test_tip_real_pe_semnatura(tmp_path):
    cale = tmp_path / "imagine.jpg"
    cale.write_bytes(b"\x89PNG\r\n\x1a\ncontinut")
    assert tip_real(cale) == "png"


def test_extrage_strings_binar(tmp_path):
    cale = tmp_path / "date.bin"
    cale.write_bytes(b"\x00cale/proba.txt\x00FLAG{ok}\x01")
    assert extrage_strings(cale) == ["cale/proba.txt", "FLAG{ok}"]


def test_extrage_arhiva_lipita(tmp_path):
    cale_sursa = tmp_path / "sursa.png"
    cale_zip = tmp_path / "gasit.zip"
    continut = io.BytesIO()
    with zipfile.ZipFile(continut, "w") as arhiva:
        arhiva.writestr("mesaj.txt", "ascuns")
    cale_sursa.write_bytes(b"imagine" + continut.getvalue())

    assert extrage_fisier_ascuns(cale_sursa, cale_zip)
    with zipfile.ZipFile(cale_zip) as arhiva:
        assert arhiva.read("mesaj.txt") == b"ascuns"


def test_ascunde_si_dezvaluie_lsb_png(tmp_path):
    cale_sursa = tmp_path / "sursa.png"
    cale_stego = tmp_path / "stego.png"
    Image.new("RGB", (32, 32), (120, 80, 40)).save(cale_sursa)

    ascunde_lsb(cale_sursa, b"FLAG{test_lsb}", cale_stego)

    assert tip_real(cale_stego) == "png"
    assert dezvaluie_lsb(cale_stego) == "FLAG{test_lsb}"
