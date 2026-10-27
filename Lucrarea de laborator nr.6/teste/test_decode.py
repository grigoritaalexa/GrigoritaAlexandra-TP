from arsenal.forensics.decode import desfa
import hashlib

import pytest

from arsenal.forensics.decode import (
    decodare_multipla,
    desfa,
    ghici_strat,
    sparge_challenge,
    sparge_hash,
    sparge_hashuri,
    sparge_xor,
)


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


@pytest.mark.parametrize(
    ("text", "strat"),
    [
        ("%2Fetc", "url"),
        ("48656c6c6f", "hex"),
        ("U2FsdXQ=", "base64"),
        ("un cod necunoscut!", "necunoscut"),
    ],
)
def test_ghici_strat(text, strat):
    assert ghici_strat(text) == strat


def test_decodare_multipla_din_straturi():
    strat, rezultat = decodare_multipla("%55%32%46%73%64%58%51%3D")
    assert strat == "base64"
    assert rezultat == b"Salut"


def test_decodare_multipla_hex_peste_base64():
    import base64

    intrare = base64.b64encode(b"48656c6c6f").decode("ascii")
    strat, rezultat = decodare_multipla(intrare)
    assert strat == "hex"
    assert rezultat == b"Hello"


def test_sparge_xor(tmp_path):
    text = (" " + "".join(chr(c) for c in range(32, 127))).encode("ascii")
    cheie = 0x5A
    cale = tmp_path / "xor.bin"
    cale.write_bytes(bytes(octet ^ cheie for octet in text))
    assert (cheie, text.decode("ascii")) in sparge_xor(cale)


def test_sparge_toate_hashurile(tmp_path):
    parole = ["parola2026", "secretlab", "forensics"]
    algoritmi = ["md5", "sha1", "sha256"]
    cale_hashuri = tmp_path / "hashuri.txt"
    cale_wordlist = tmp_path / "wordlist.txt"
    cale_hashuri.write_text(
        "\n".join(
            hashlib.new(algoritm, parola.encode()).hexdigest()
            for algoritm, parola in zip(algoritmi, parole)
        ),
        encoding="ascii",
    )
    cale_wordlist.write_text("\n".join(parole), encoding="ascii")

    rezultate = sparge_hashuri(cale_hashuri, cale_wordlist)
    assert [rezultat[2] for rezultat in rezultate] == parole
    assert sparge_hash(cale_hashuri, cale_wordlist) == parole[0]


def test_sparge_hash_rejecteaza_hash_invalid(tmp_path):
    cale_hashuri = tmp_path / "hashuri.txt"
    cale_wordlist = tmp_path / "wordlist.txt"
    cale_hashuri.write_text("nu este un hash\n", encoding="ascii")
    cale_wordlist.write_text("parola\n", encoding="ascii")
    with pytest.raises(ValueError, match="Hash neacceptat"):
        sparge_hash(cale_hashuri, cale_wordlist)


def test_sparge_challenge_base64_xor_si_sha256(tmp_path):
    import base64

    mesaj = b"FLAG{challenge_test}"
    cheie = 0x37
    criptat = bytes(octet ^ cheie for octet in mesaj)
    cale_challenge = tmp_path / "challenge.bin"
    cale_hint = tmp_path / "challenge_hint.txt"
    cale_challenge.write_bytes(base64.b64encode(criptat) + b"\n")
    cale_hint.write_text(
        f"SHA256: {hashlib.sha256(mesaj).hexdigest()}\n",
        encoding="ascii",
    )

    assert sparge_challenge(cale_challenge, cale_hint) == (cheie, mesaj)