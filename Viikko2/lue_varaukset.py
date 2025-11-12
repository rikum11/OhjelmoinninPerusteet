"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    # Tulostetaan varaus konsoliin
    #print(varaus)

    # Kokeile näitä
    #print(varaus.split('|'))
    varausId = varaus.split('|')
    print(varausId)
    #print(type(varausId))

    print(f"Varausnumero: {varausId[0]}")
    print(f"Varaaja: {varausId[1]}")
    paivamaara = varausId[2].split('-')
    print(f"Päivämäärä: {paivamaara[2]}.{paivamaara[1]}.{paivamaara[0]}")
    print(f"Aloitusaika: {varausId[3].replace(':', '.')}")
    print(f"Tuntimäärä: {varausId[4]}")
    print(f"Tuntihinta: {varausId[5]} €")
    kokonaishinta = float(varausId[4]) * float(varausId[5])
    print(f"Kokonaishinta: {kokonaishinta} €")
    print(f"Maksettu: {'Kyllä' if varausId[6] == 'True' else 'Ei'}")
    print(f"Kohde: {varausId[7]}")
    print(f"Puhelin: {varausId[8]}")
    print(f"Sähköposti: {varausId[9]}")

    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    main()