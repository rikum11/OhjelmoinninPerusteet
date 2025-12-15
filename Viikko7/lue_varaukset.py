from datetime import datetime
from typing import List, Dict, Any

Varaus = Dict[str, Any]
def muunna_varaustiedot(varaus_lista: list[str]) -> Varaus:
    return {
        "id": int(varaus_lista[0]),
        "nimi": varaus_lista[1],
        "sähköposti": varaus_lista[2],
        "puhelin": varaus_lista[3],
        "paiva": datetime.strptime(varaus_lista[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus_lista[5], "%H:%M").time(),
        "kesto": int(varaus_lista[6]),
        "hinta": float(varaus_lista[7]),
        "vahvistettu": varaus_lista[8].lower() == "true",
        "kohde": varaus_lista[9],
        "luotu": datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S"),
    }

def hae_varaukset(varaustiedosto: str) -> List[Varaus]:
    varaukset: List[Varaus] = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            rivi = rivi.strip()
            if not rivi:
                continue
            varaustiedot_lista = rivi.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot_lista))
    return varaukset

def vahvistetut_varaukset(varaukset: List[Varaus]):
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"- {varaus['nimi']}, {varaus['kohde']}, {varaus['paiva'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: List[Varaus]):
    for varaus in varaukset:
        if varaus["kesto"] >= 3:
            print(f"- {varaus['nimi']}, {varaus['paiva'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['kohde']}")
    print()

def varausten_vahvistusstatus(varaukset: List[Varaus]):
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")
    print()

def varausten_lkm(varaukset: List[Varaus]):
    vahvistetut_varaukset_lkm = 0
    ei_vahvistetut_varaukset_lkm = 0
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            vahvistetut_varaukset_lkm += 1
        else:
            ei_vahvistetut_varaukset_lkm += 1

    print(f"- Vahvistettuja varauksia: {vahvistetut_varaukset_lkm} kpl")
    print(f"- Ei-vahvistettuja varauksia: {ei_vahvistetut_varaukset_lkm} kpl")
    print()

def varausten_kokonaistulot(varaukset: List[Varaus]):
    varausten_tulot = 0.0
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            varausten_tulot += varaus["kesto"] * varaus["hinta"]

    print("Vahvistettujen varausten kokonaistulot:", f"{varausten_tulot:.2f}".replace('.', ','), "€")
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()