import argparse

from forensics import ascunde_lsb, dezvaluie_lsb


def main():
    parser = argparse.ArgumentParser(
        description="Ascunde sau dezvaluie mesaje LSB in imagini."
    )
    subparsers = parser.add_subparsers(dest="actiune", required=True)

    ascunde = subparsers.add_parser("ascunde", help="Ascunde un mesaj intr-o imagine.")
    ascunde.add_argument("sursa", help="Imaginea sursa")
    ascunde.add_argument("mesaj", help="Mesajul text de ascuns")
    ascunde.add_argument(
        "--iesire", default="stego.png", help="Imaginea PNG rezultata"
    )

    dezvaluie = subparsers.add_parser(
        "dezvaluie", help="Recupereaza mesajul LSB dintr-o imagine."
    )
    dezvaluie.add_argument("imagine", help="Imaginea stego PNG")

    args = parser.parse_args()
    if args.actiune == "ascunde":
        ascunde_lsb(args.sursa, args.mesaj.encode("utf-8"), args.iesire)
    else:
        dezvaluie_lsb(args.imagine)


if __name__ == "__main__":
    main()
