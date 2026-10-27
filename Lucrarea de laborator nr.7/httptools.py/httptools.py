import requests

# Adresa de bază a serverului și lista de căi pentru testare
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]


# Partea 1: parametri în URL
def search(params):
    """Partea 1a: trimite o cerere GET cu parametri în URL și returnează parametrii primiți de server."""
    url = BASE + "/get"
    raspuns = requests.get(url, params=params)
    date = raspuns.json()
    return date["args"]


def search_url(params):
    """Partea 1b: returnează adresa completă construită de requests (URL + parametri encodați)."""
    url = BASE + "/get"
    raspuns = requests.get(url, params=params)
    return raspuns.url


# Partea 2: anteturi (headers)
def fetch_with_agent(agent):
    """Partea 2a: trimite o cerere GET cu antetul User-Agent personalizat și returnează ce a văzut serverul."""
    url = BASE + "/headers"
    anteturi = {"User-Agent": agent}
    raspuns = requests.get(url, headers=anteturi)
    date = raspuns.json()
    return date["headers"]["User-Agent"]


def default_agent():
    """Partea 2b: returnează User-Agent-ul implicit trimis de requests când nu setezi nimic."""
    url = BASE + "/headers"
    raspuns = requests.get(url)
    date = raspuns.json()
    return date["headers"]["User-Agent"]


# Partea 3: trimiterea datelor (POST)
def post_json(data):
    """Partea 3a: trimite datele ca corp JSON la /POST și returnează cheia 'json' din răspuns."""
    url = BASE + "/post"
    raspuns = requests.post(url, json=data)
    date = raspuns.json()
    return date["json"]


def post_form(data):
    """Partea 3b: trimite datele ca formular (data=) la /POST și returnează cheia 'form' din răspuns."""
    url = BASE + "/post"
    raspuns = requests.post(url, data=data)
    date = raspuns.json()
    return date["form"]


# Partea 4: coduri de stare
def describe_status(code):
    """Partea 4a: clasifică codul HTTP în 'succes' (2xx), 'eroare client' (4xx) sau 'eroare server' (5xx)."""
    url = BASE + "/status/" + str(code)
    raspuns = requests.get(url)
    if raspuns.status_code >= 500:
        return "eroare server"
    if raspuns.status_code >= 400:
        return "eroare client"
    return "succes"


def is_ok(code):
    """Partea 4b: verifică dacă cererea a reușit folosind raise_for_status() într-un bloc try/except."""
    url = BASE + "/status/" + str(code)
    raspuns = requests.get(url)
    try:
        raspuns.raise_for_status()
        return True
    except requests.HTTPError:
        return False


# Partea 5: redirecționări
def count_redirects(n):
    """Partea 5a: returnează numărul redirecționărilor urmate automat (lungimea lui response.history)."""
    url = BASE + "/redirect/" + str(n)
    raspuns = requests.get(url)
    return len(raspuns.history)


def final_url(n):
    """Partea 5b: returnează adresa URL finală după redirecționări."""
    url = BASE + "/redirect/" + str(n)
    raspuns = requests.get(url)
    return raspuns.url


def first_hop(n):
    """Partea 5c: face o cerere fără urmărirea redirecționărilor (allow_redirects=False) și returnează antetul Location."""
    url = BASE + "/redirect/" + str(n)
    raspuns = requests.get(url, allow_redirects=False)
    return raspuns.headers["Location"]


# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Partea 6a: setează un cookie și îl citește folosind aceeași sesiune (requests.Session())."""
    sesiune = requests.Session()
    url = BASE + "/cookies/set"
    sesiune.get(url, params={name: value})
    raspuns = sesiune.get(BASE + "/cookies")
    date = raspuns.json()
    return date["cookies"]


def no_session_demo(name, value):
    """Partea 6b: execută cererile fără sesiune; cererile separate nu păstrează cookie-urile."""
    url = BASE + "/cookies/set"
    requests.get(url, params={name: value})
    raspuns = requests.get(BASE + "/cookies")
    date = raspuns.json()
    return date["cookies"]


# Partea 7: raportul final
def report(path):
    """Partea 7a: generează un raport complet despre o pagină (status, timp, redirecționări, timeout 3s)."""
    url = BASE + path
    try:
        # Se încearcă cererea cu un timeout de maxim 3 secunde
        raspuns = requests.get(url, timeout=3)
    except requests.RequestException:
        # Se tratează erorile de rețea sau de timeout fără ca programul să se oprească
        return {"status": None, "error": "cererea a esuat"}

    # Se construiește dicționarul cu rezultatele
    rezultat = {}
    rezultat["status"] = raspuns.status_code
    rezultat["final_url"] = raspuns.url
    rezultat["redirects"] = len(raspuns.history)
    rezultat["seconds"] = round(raspuns.elapsed.total_seconds(), 2)
    rezultat["content_type"] = raspuns.headers.get("Content-Type")
    return rezultat