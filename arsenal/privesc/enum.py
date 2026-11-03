import argparse
import json
import os

# A1. Citeste liniile din fisier eliminand spatiile libere si comentariile
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [linie.strip() for linie in f if linie.strip() and not linie.strip().startswith("#")]

# A2. Extrage numele fisierului de dupa ultimul slash folosind rsplit
def nume(cale):
    return cale.rsplit("/", 1)[-1]

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}

# A3. Construieste lista de dictionare cu caile unice si stabileste riscul
def suid_constatari(cale):
    cai = citeste_linii(cale)
    cai_unice = sorted(set(cai))
    out = []
    for c in cai_unice:
        n = nume(c)
        out.append({
            "cale": c,
            "nume": n,
            "risc": "mare" if n in GTFO else "normal"
        })
    return out

# A4. Despacheteaza liniile din sudo si extrage campurile pentru cron
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        if len(campuri) >= 7:
            user = campuri[5]
            comanda = " ".join(campuri[6:])
            out.append({
                "user": user,
                "comanda": comanda
            })
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

# A5. Gestioneaza argumentele, afiseaza rezumatul si salveaza raportul JSON
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    raport = enumereaza(a.capturi)
    
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
        
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
        
    useri_sudo = {s["user"] for s in raport["sudo"]}
    useri_cron = {c["user"] for c in raport["cron"]}
    useri_implicati = useri_sudo | useri_cron
    print("utilizatori implicati:", ", ".join(sorted(useri_implicati)))
    
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")

if __name__ == "__main__":
    main()
