#!/usr/bin/env python3
"""Punteggio oggettivo di un run di eval/. Solo libreria standard.

Controlla quello che si misura senza ambiguita': conteggio parole, righe, punti di
una lista, e la presenza delle frasi che SKILL.md vieta sempre (sezione 1). Il resto
— il registro e' giusto? il modo di dire calza? lo sfottio' guarda la situazione? —
resta giudizio umano: va scritto in eval/results.md, non qui.

Uso:  python3 scripts/score_eval.py [cases.md] [responses.md]
Default: eval/cases.md ed eval/responses.md nella radice del repo.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

FRASI_VIETATE = (
    "certo, ecco",
    "bella domanda",
    "spero d'esserte stato utile",
    "famme sapé",
    "famme sape",
)


@dataclass
class Caso:
    id: str
    budget: str


@dataclass
class Esito:
    id: str
    ok: bool
    dettaglio: str


def leggi_casi(testo: str) -> dict[str, Caso]:
    casi: dict[str, Caso] = {}
    for blocco in re.split(r"(?m)^## ", testo)[1:]:
        intestazione, _, corpo = blocco.partition("\n")
        id_caso = intestazione.split("—")[0].strip().split()[0]
        m = re.search(r"^budget:\s*(.+)$", corpo, re.MULTILINE)
        if m:
            casi[id_caso] = Caso(id=id_caso, budget=m.group(1).strip())
    return casi


def leggi_risposte(testo: str) -> dict[str, str]:
    risposte: dict[str, str] = {}
    for blocco in re.split(r"(?m)^## ", testo)[1:]:
        intestazione, _, corpo = blocco.partition("\n")
        risposte[intestazione.strip()] = corpo.strip()
    return risposte


def conta_parole(testo: str) -> int:
    return len(re.findall(r"\S+", testo))


def conta_righe(testo: str) -> int:
    return len([r for r in testo.splitlines() if r.strip()])


def righe_punto(testo: str) -> list[str]:
    return [r.lstrip("-*• ").strip() for r in testo.splitlines() if r.strip()]


def valuta_budget(budget: str, risposta: str) -> Esito | None:
    """None quando il budget e' qualitativo ('quella che serve') e non si misura."""
    m = re.search(r"max\s*(\d+)\s*punti", budget)
    m2 = re.search(r"(\d+)\s*parole a punto", budget)
    if m and m2:
        max_punti, max_parole = int(m.group(1)), int(m2.group(1))
        punti = righe_punto(risposta)
        if len(punti) > max_punti:
            return Esito("", False, f"{len(punti)} punti, massimo {max_punti}")
        sforati = [p for p in punti if conta_parole(p) > max_parole]
        if sforati:
            return Esito("", False, f"{len(sforati)} punti oltre {max_parole} parole")
        return Esito("", True, f"{len(punti)} punti, tutti entro {max_parole} parole")

    m = re.search(r"(\d+)\s*parole", budget)
    if m and "punto" not in budget:
        limite = int(m.group(1))
        parole = conta_parole(risposta)
        return Esito("", parole <= limite, f"{parole}/{limite} parole")

    m = re.search(r"(\d+)\s*righe", budget)
    if m:
        limite = int(m.group(1))
        righe = conta_righe(risposta)
        return Esito("", righe <= limite, f"{righe}/{limite} righe")

    return None


def cerca_frasi_vietate(risposta: str) -> list[str]:
    bassa = risposta.lower()
    return [f for f in FRASI_VIETATE if f in bassa]


def esegui(cases_path: Path, responses_path: Path) -> int:
    casi = leggi_casi(cases_path.read_text(encoding="utf-8"))
    risposte = leggi_risposte(responses_path.read_text(encoding="utf-8"))

    mancanti = set(casi) - set(risposte)
    if mancanti:
        print(f"ATTENZIONE: nessuna risposta per {sorted(mancanti)}", file=sys.stderr)

    pass_n = fail_n = skip_n = 0
    for id_caso in sorted(casi, key=lambda x: (len(x), x)):
        caso, risposta = casi[id_caso], risposte.get(id_caso, "")
        esito = valuta_budget(caso.budget, risposta)
        vietate = cerca_frasi_vietate(risposta)

        if esito is None:
            skip_n += 1
            stato = "SKIP (budget qualitativo)"
        elif esito.ok:
            pass_n += 1
            stato = f"PASS  ({esito.dettaglio})"
        else:
            fail_n += 1
            stato = f"FAIL  ({esito.dettaglio})"

        riga = f"{id_caso}: {stato}"
        if vietate:
            riga += f"  |  frase vietata trovata: {vietate}"
        print(riga)

    print(f"\n{pass_n} pass, {fail_n} fail, {skip_n} skip (budget non numerico, giudizio umano).")
    return 1 if fail_n else 0


def main() -> int:
    radice = Path(__file__).resolve().parent.parent
    cases_path = Path(sys.argv[1]) if len(sys.argv) > 1 else radice / "eval" / "cases.md"
    responses_path = Path(sys.argv[2]) if len(sys.argv) > 2 else radice / "eval" / "responses.md"
    return esegui(cases_path, responses_path)


if __name__ == "__main__":
    raise SystemExit(main())
