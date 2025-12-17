# Copyright (c) 2025 Riku Martinmäki
# License: MIT

import csv
from datetime import datetime, date
from typing import List, Dict

def tiedosto(tiedoston_nimi: str) -> List[List[str]]:
    """Lukee CSV-tiedoston."""
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
    return f"{arvo_wh / 1000:.2f}".replace(".", ",")

def raportti(viikko: int, data: Dict[date, Dict[str, List[int]]]) -> List[str]:
    """Tekee raportin viikolta"""
    viikonpaivat = [
        "maanantai", "tiistai", "keskiviikko",
        "torstai", "perjantai", "lauantai", "sunnuntai"
    ]
    rivit: List[str] = []

    rivit.append(f"Viikon {viikko} sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
    rivit.append("")
    rivit.append("Päivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]")
    rivit.append("             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    rivit.append("-" * 75)

    for paiva in sorted(data.keys()):
        nimi = viikonpaivat[paiva.weekday()]
        pvm_str = paiva.strftime("%d.%m.%Y")

        k = data[paiva]["kulutus"]
        t = data[paiva]["tuotanto"]

        rivit.append(
            f"{nimi:<13}"
            f"{pvm_str:<12}  "
            f"{kwhmuunnos(k[0]):>6}   {kwhmuunnos(k[1]):>6}   {kwhmuunnos(k[2]):>6}      "
            f"{kwhmuunnos(t[0]):>5}   {kwhmuunnos(t[1]):>5}   {kwhmuunnos(t[2]):>5}"
        )
    rivit.append("")
    return rivit

def tee_tiedosto(tiedoston_nimi: str, rivit: List[str]) -> None:
    """Tekee raportista tiedoston"""
    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        f.write("\n".join(rivit))
        print("Tiedosto luotu.")
def main() -> None:
    """Paafunktio."""
    kaikki_rivit: List[str] = []
    for viikko in [41, 42, 43]:
        rivit = tiedosto(f"viikko{viikko}.csv")
        paivadata = paivalasku(rivit)
        kaikki_rivit.extend(raportti(viikko, paivadata))

    tee_tiedosto("yhteenveto.txt", kaikki_rivit)

if __name__ == "__main__":
    main()
