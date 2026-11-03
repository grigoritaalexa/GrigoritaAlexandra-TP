from arsenal.privesc.enum import citeste_linii, nume, GTFO

# B1. Două mulțimi: curat și acum
def cai(fisier):
    # Întoarce mulțimea căilor din fișier folosind funcția citeste_linii din enum
    return set(citeste_linii(fisier))

baza = cai("arsenal/privesc/start/baza_suid.txt")
acum = cai("arsenal/privesc/start/suid.txt")
print("baza:", len(baza), " acum:", len(acum))

# B2. Diferența: ce a apărut
# Ce este în "acum" dar nu și în "bază" reprezintă fișierele SUID noi (operație de diferență de mulțimi)
noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)

# B3. Dicționar de risc și filtrul final
# Construim un dicționar de risc pentru elementele noi folosind dict comprehension
risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}

# Filtrăm doar fișierele periculoase folosind list comprehension cu if
periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
print("periculoase NOI:", periculoase)
