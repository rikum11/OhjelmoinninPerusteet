"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus):
    print(f"Varausnumero: {varaus[0]}")

def hae_varaaja(varaus):
    print(f"Varaaja: {varaus[1]}")

def hae_paiva(varaus):
    pvm = datetime.strptime(varaus[2], "%Y-%m-%d")
    print(f"Päivämäärä: {pvm.strftime('%d.%m.%Y')}")

def hae_aloitusaika(varaus):
    aika = datetime.strptime(varaus[3], "%H:%M")
    print(f"Aloitusaika: {aika.strftime('%H.%M')}")

def hae_tuntimaara(varaus):
    print(f"Tuntimäärä: {int(varaus[4])}")

def hae_tuntihinta(varaus):
    hinta = float(varaus[5])
    print(f"Tuntihinta: {hinta:.2f}".replace('.', ',') + " €")

def laske_kokonaishinta(varaus):
    hinta = float(varaus[5])
    tunnit = int(varaus[4])
    kokonaishinta = hinta * tunnit
    print(f"Kokonaishinta: {kokonaishinta:.2f}".replace('.', ',') + " €")

def hae_maksettu(varaus):
    maksettu = "Kyllä" if varaus[6] == "True" else "Ei"
    print(f"Maksettu: {maksettu}")

def hae_kohde(varaus):
    print(f"Kohde: {varaus[7]}")

def hae_puhelin(varaus):
    print(f"Puhelin: {varaus[8]}")

def hae_sahkoposti(varaus):
    print(f"Sähköposti: {varaus[9]}")

def main():
    varaukset = "varaukset.txt"

    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip().split('|')

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)

if __name__ == "__main__":
    main()