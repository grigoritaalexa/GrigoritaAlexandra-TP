from httptools import PATHS, report


def get_seconds(pagina):
    return pagina["seconds"]


def main():
    rezultate = []
    for path in PATHS:
        info = report(path)
        info["path"] = path
        rezultate.append(info)

    reusite = []
    esuate = 0
    for info in rezultate:
        if info["status"] == 200:
            reusite.append(info)
        else:
            esuate = esuate + 1

    reusite.sort(key=get_seconds, reverse=True)

    for info in reusite:
        print(info["path"], "->", info["status"], ",", info["seconds"], "secunde")

    print("Reusite:", len(reusite), "| Esuate:", esuate)


if __name__ == "__main__":
    main()