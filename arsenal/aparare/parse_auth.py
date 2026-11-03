import re
from collections import Counter

# A1. Scheletul și funcția care întoarce o fișă
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")

def esec(linie):
    """
    Analizează o linie din jurnal. 
    Întoarce (user, ip) dacă rândul este un eșec de autentificare, altfel None.
    """
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))

# A2. Lista de eșecuri, robustă la rânduri stricate
def citeste_esecuri(cale):
    """
    Citește fișierul de jurnal și returnează o listă de dicționare cu eșecurile găsite.
    Este robust la fișiere inexistente sau linii stricate.
    """
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri

    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})

    return esecuri

# A3. Numărarea pe IP: o funcție cu return
def pe_ip(esecuri):
    """
    Primește lista de eșecuri și întoarce un obiect Counter cu numărul de eșecuri per IP.
    """
    return Counter(e["ip"] for e in esecuri)

# A4. Rezumatul
def main():
    import sys
    if len(sys.argv) > 1:
        cale = sys.argv[1]
    else:
        cale = "arsenal/aparare/start/auth.log"

    esecuri = citeste_esecuri(cale)
    print(f"Esecuri de autentificare: {len(esecuri)}")
    counts = pe_ip(esecuri)
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")

if __name__ == "__main__":
    main()
