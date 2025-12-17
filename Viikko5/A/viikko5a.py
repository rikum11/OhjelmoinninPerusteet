# Copyright (c) 2025 Riku Martinmäki
# License: MIT

import csv
from datetime import datetime, date
from typing import List, Dict

def tiedosto(tiedoston_nimi: str) -> List[List[str]]:
    """Lukee CSV-tiedoston"""
    with open(tiedoston_nimi, encoding="utf-8") as tiedosto:
        lukija = csv.reader(tiedosto, delimiter=";")
        next(lukija)
        return list(lukija)
def paivalasku(rivit: List[List[str]]) -> Dict[date, Dict[str, List[int]]]:
    """Laskee päiväkohtaisen kulutuksen"""
    tulos: Dict[date, Dict[str, List[int]]] = {}

    for rivi in rivit:
        aika = datetime.fromisoformat(rivi[0])
        paiva = aika.date()

        if paiva not in tulos:
            tulos[paiva] = {
                "kulutus": [0, 0, 0],
                "tuotanto": [0, 0, 0]
            }

        for i in range(3):
            tulos[paiva]["kulutus"][i] += int(rivi[1 + i])
            tulos[paiva]["tuotanto"][i] += int(rivi[4 + i])

    return tulos
def kwhmuunnos(arvo_wh: int) -> str:
    """Muunnos Wh -> kWh"""
    arvo_kwh = arvo_wh / 1000
    return f"{arvo_kwh:.2f}".replace(".", ",")

def raportti(data: Dict[date, Dict[str, List[int]]]) -> None:
    """Tulostaa raportin viikolta"""
    viikonpaivat = [
        "maanantai", "tiistai", "keskiviikko",
        "torstai", "perjantai", "lauantai", "sunnuntai"
    ]

    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    print("Päivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]")
    print("             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    print("-" * 75)

    for paiva in sorted(data.keys()):
        nimi = viikonpaivat[paiva.weekday()]
        pvm_str = f"{paiva.day}.{paiva.month}.{paiva.year}"

        k = data[paiva]["kulutus"]
        t = data[paiva]["tuotanto"]

        print(
            f"{nimi:<13}"
            f"{pvm_str:<12}  "
            f"{kwhmuunnos(k[0]):>6}   {kwhmuunnos(k[1]):>6}   {kwhmuunnos(k[2]):>6}      "
            f"{kwhmuunnos(t[0]):>5}   {kwhmuunnos(t[1]):>5}   {kwhmuunnos(t[2]):>5}"
        )
def main() -> None:
    """pääfunktio."""
    rivit = tiedosto("viikko42.csv")
    paivadata = paivalasku(rivit)
    raportti(paivadata)
if __name__ == "__main__":
    main()
