# Copyright (c) 2025 Riku Martinmäki
# License: MIT
from datetime import datetime, date
from typing import List, Dict
import csv
import sys
import os

def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa rivit sopivassa rakenteessa."""
    data = []
    try:
        with open(tiedoston_nimi, mode='r', encoding='utf-8') as tiedosto:
            lukija = csv.DictReader(tiedosto, delimiter=';')
            for rivi in lukija:
                try:
                    kulutus = float(rivi['Kulutus (netotettu) kWh'].replace(',', '.'))
                    tuotanto = float(rivi['Tuotanto (netotettu) kWh'].replace(',', '.'))
                    lampotila = float(rivi['Vuorokauden keskilämpötila'].replace(',', '.'))
                    
                    data.append({
                        "aika": datetime.fromisoformat(rivi['Aika']),
                        "kulutus": kulutus,
                        "tuotanto": tuotanto,
                        "lampotila": lampotila
                    })
                except ValueError:
                    pass
    except FileNotFoundError:
        print(f"Virhe: Tiedostoa '{tiedoston_nimi}' ei löydy.")
        sys.exit(1)
    return data
def nayta_paavalikko() -> str:
    """Tulostaa päävalikon ja palauttaa käyttäjän valinnan merkkijonona."""
    print(" ")
    print("VALITSE RAPORTTITYYPPI")
    print(" ")
    print("1) Päiväkohtainen yhteenveto aikaväliltä")
    print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
    print("3) Vuoden 2025 kokonaisyhteenveto")
    print("4) Lopeta ohjelma")
    print(" ")
    return input("Anna valintasi (1-4): ")

def nayta_toimintovalikko() -> str:
    """Tulostaa toimintovalikon raportin jälkeen ja palauttaa käyttäjän valinnan."""
    print(" ")
    print("MITÄ HALUAT TEHDÄ SEURAAVAKSI?")
    print(" ")
    print("1) Kirjoita raportti tiedostoon raportti.txt")
    print("2) Luo uusi raportti")
    print("3) Lopeta ohjelma")
    print(" ")
    return input("Anna valintasi (1-3): ")

def luo_paivaraportti(data: List[Dict]) -> List[str]:
    """Muodostaa päiväkohtaisen raportin valitulle aikavälille."""
    while True:
        try:
            alku_str = input("Anna alkupäivä (pp.kk.vvvv): ")
            loppu_str = input("Anna loppupäivä (pp.kk.vvvv): ")
            alku_pvm = datetime.strptime(alku_str, "%d.%m.%Y").date()
            loppu_pvm = datetime.strptime(loppu_str, "%d.%m.%Y").date()
            if alku_pvm > loppu_pvm:
                print("Alkupäivä ei voi olla myöhemmin kuin loppupäivä. Yritä uudelleen.")
                continue
            break
        except ValueError:
            print("Virheellinen päivämäärämuoto. Käytä muotoa pp.kk.vvvv. Yritä uudelleen.")
    
    kulutus_summa, tuotanto_summa, lampotila_summa, tuntien_maara = 0.0, 0.0, 0.0, 0
    for mittaus in data:
        if alku_pvm <= mittaus['aika'].date() <= loppu_pvm:
            kulutus_summa += mittaus['kulutus']
            tuotanto_summa += mittaus['tuotanto']
            lampotila_summa += mittaus['lampotila']
            tuntien_maara += 1
    if tuntien_maara == 0:
        return ["Ei dataa valitulla aikavälillä."]
    keskilampotila = lampotila_summa / tuntien_maara
    raportti_rivit = []
    raportti_rivit.append(f"Raportti aikaväliltä {alku_pvm.strftime('%d.%m.%Y')}-{loppu_pvm.strftime('%d.%m.%Y')}\n")
    raportti_rivit.append(f"{'Kokonaiskulutus:':<20} {format_float_fi(kulutus_summa)} kWh")
    raportti_rivit.append(f"{'Kokononaistuotanto:':<20} {format_float_fi(tuotanto_summa)} kWh")
    raportti_rivit.append(f"{'Keskilämpötila:':<20} {format_float_fi(keskilampotila)} °C")
    return raportti_rivit

def luo_kuukausiraportti(data: List[Dict]) -> List[str]:
    """Muodostaa kuukausikohtaisen yhteenvedon valitulle kuukaudelle."""
    while True:
        try:
            kuukausi = int(input("Anna kuukauden numero (1-12): "))
            if not (1 <= kuukausi <= 12):
                print("Kuukauden numeron tulee olla 1 ja 12 välillä. Yritä uudelleen.")
                continue
            break
        except ValueError:
            print("Virheellinen syöte. Anna numero. Yritä uudelleen.")
    kulutus_summa, tuotanto_summa, lampotila_summa, tuntien_maara = 0.0, 0.0, 0.0, 0
    for mittaus in data:
        if mittaus['aika'].month == kuukausi:
            kulutus_summa += mittaus['kulutus']
            tuotanto_summa += mittaus['tuotanto']
            lampotila_summa += mittaus['lampotila']
            tuntien_maara += 1   
    if tuntien_maara == 0:
        return ["Ei dataa valitulle kuukaudelle."]
    keskilampotila = lampotila_summa / tuntien_maara
    raportti_rivit = []
    raportti_rivit.append(f"Kuukausiraportti kuukaudelle {kuukausi}\n")
    raportti_rivit.append(f"{'Kokonaiskulutus:':<20} {format_float_fi(kulutus_summa)} kWh")
    raportti_rivit.append(f"{'Kokononaistuotanto:':<20} {format_float_fi(tuotanto_summa)} kWh")
    raportti_rivit.append(f"{'Keskilämpötila:':<20} {format_float_fi(keskilampotila)} °C")
    return raportti_rivit

def luo_vuosiraportti(data: List[Dict]) -> List[str]:
    """Muodostaa koko vuoden yhteenvedon."""
    kulutus_summa, tuotanto_summa, lampotila_summa, tuntien_maara = 0.0, 0.0, 0.0, 0
    for mittaus in data:
        kulutus_summa += mittaus['kulutus']
        tuotanto_summa += mittaus['tuotanto']
        lampotila_summa += mittaus['lampotila']
        tuntien_maara += 1      
    if tuntien_maara == 0:
        return ["Ei dataa vuodelle 2025."]   
    keskilampotila = lampotila_summa / tuntien_maara
    raportti_rivit = []
    raportti_rivit.append("Vuoden 2025 kokonaisyhteenveto\n")
    raportti_rivit.append(f"{'Kokonaiskulutus:':<20} {format_float_fi(kulutus_summa)} kWh")
    raportti_rivit.append(f"{'Kokononaistuotanto:':<20} {format_float_fi(tuotanto_summa)} kWh")
    raportti_rivit.append(f"{'Keskilämpötila:':<20} {format_float_fi(keskilampotila)} °C")
    return raportti_rivit

def format_float_fi(arvo: float) -> str:
    """Muotoilee desimaaliluvun suomalaiseen muotoon."""
    return f"{arvo:.2f}".replace('.', ',')

def tulosta_raportti_konsoliin(rivit: List[str]) -> None:
    """Tulostaa raportin rivit konsoliin."""
    print(" ")
    for rivi in rivit:
        print(rivi)
    print(" ")

def kirjoita_raportti_tiedostoon(rivit: List[str]) -> None:
    """Kirjoittaa raportin rivit tiedostoon raportti.txt."""
    try:
        with open("raportti.txt", "w", encoding="utf-8") as tiedosto:
            for rivi in rivit:
                tiedosto.write(rivi + "\n")
        print("Raportti kirjoitettu tiedostoon raportti.txt")
    except IOError as e:
        print(f"Virhe tiedoston kirjoittamisessa: {e}")

def main() -> None:
    """Ohjelman pääfunktio: lukee datan, näyttää valikot ja ohjaa raporttien luomista."""
    data = lue_data("2025.csv")
    raportti_valmis: List[str] = []

    while True:
        valinta = nayta_paavalikko()

        if valinta == '1':
            raportti_valmis = luo_paivaraportti(data)
        elif valinta == '2':
            raportti_valmis = luo_kuukausiraportti(data)
        elif valinta == '3':
            raportti_valmis = luo_vuosiraportti(data)
        elif valinta == '4':
            print("Lopetetaan ohjelma.")
            break
        else:
            print("Virheellinen valinta. Yritä uudelleen (1-4).")
            continue
        tulosta_raportti_konsoliin(raportti_valmis)
        while True:
            toiminto = nayta_toimintovalikko()
            if toiminto == '1':
                kirjoita_raportti_tiedostoon(raportti_valmis)
                break
            elif toiminto == '2':
                break
            elif toiminto == '3':
                print("Lopetetaan ohjelma.")
                sys.exit(0)
            else:
                print("Virheellinen valinta. Yritä uudelleen (1-3).")
                continue

if __name__ == "__main__":
    if not os.path.exists("2025.csv"):
        print("Luodaan mallitiedosto '2025.csv' testausta varten...")
        with open("2025.csv", "w", encoding="utf-8") as f:
            f.write("Aika;Kulutus (netotettu) kWh;Tuotanto (netotettu) kWh;Vuorokauden keskilämpötila\n")
            f.write("2025-01-01T00:00:00.000+02:00;1,569;0,000;-4,5\n")
            f.write("2025-01-01T01:00:00.000+02:00;1,879;0,000;-4,5\n")
            f.write("2025-01-02T00:00:00.000+02:00;1,870;0,000;-7,3\n")
            f.write("2025-01-02T01:00:00.000+02:00;2,000;0,000;-7,3\n")
            f.write("2025-02-01T00:00:00.000+02:00;1,000;0,500;2,0\n")
        print("Tiedosto luotu. Suorita ohjelma uudelleen.")
    else:
        main()