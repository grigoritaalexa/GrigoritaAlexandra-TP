import os

from arsenal.forensics.amprente import amprenta_fisier, scaneaza, tip

PROBE = os.path.join(os.path.dirname(__file__), "probe")


# A4.1: verifica identificarea tipului dupa magic bytes si cazul necunoscut
def test_tip_din_magic():
    assert tip(b"\x89PNG") == "PNG"
    assert tip(b"text") == "necunoscut"


# A4.2: verifica amprenta SHA-256 (16 caractere) pentru imagine.png
def test_amprenta_png():
    r = amprenta_fisier(os.path.join(PROBE, "imagine.png"))
    assert r["sha256"] == "ea3a9848da7e6c1d"


# A4.3: verifica faptul ca scaneaza gaseste toate cele 4 fisiere din probe
def test_scaneaza_toate():
    assert len(scaneaza(PROBE)) == 4