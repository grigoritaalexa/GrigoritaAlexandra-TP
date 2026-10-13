import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]
print("partea1")
def build_url(host, path):

    if path.startswith('/'):
        path = path[1:]
    return f"https://{host}/{path}"

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")
print("partea2")
def show_response(url):
    
    try:
        r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('Content-Type', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Eroare de conexiune: {e}")
print("partea3")
def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type", "unknown"),
            "length": len(r.content),
            "server": r.headers.get("Server", "unknown")
        }
    except requests.exceptions.RequestException as e:
        return {"status": None, "error": f"Eroare: {type(e).__name__}"}
print("partea4")
def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []
    
    for url in SITES:
        rezultat = check_site(url)
        rezultat["url"] = url
        rezultate.append(rezultat)
        
    reusite = [r for r in rezultate if r["status"] == 200]
    reusite.sort(key=lambda x: x.get("length", 0), reverse=True)
    
    for r in reusite:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeți")
        
    esuate = len(rezultate) - len(reusite)
    print(f"Reușite: {len(reusite)} Eșuate: {esuate}")

def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
        present = []
        missing = []
        
        for header in SECURITY_HEADERS:
            if header in r.headers:
                present.append(header)
            else:
                missing.append(header)
                
        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        
        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.exceptions.RequestException as e:
        return {"status": None, "error": f"Eroare rețea: {type(e).__name__}"}

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    incercari = 0
    ultimul_status = None
    eroare = None
    
    while incercari < attempts:
        incercari += 1
        try:
            r = requests.get(url, timeout=5)
            ultimul_status = r.status_code
            if ultimul_status < 500:
                break
        except requests.exceptions.RequestException as e:
            ultimul_status = None
            eroare = str(e)
            
    rezultat = {"status": ultimul_status, "attempts": incercari}
    if ultimul_status is None and eroare:
        rezultat["error"] = "Conexiune eșuată"
        
