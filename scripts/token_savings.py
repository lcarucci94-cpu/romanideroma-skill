#!/usr/bin/env python3
"""Misura il risparmio della skill confrontando due run sugli stessi prompt.

Confronta `eval/responses.md` (skill attiva) con `eval/baseline.md` (stessi prompt,
nessuna skill) e produce il delta per caso e per categoria.

Il conteggio dei token e' una **stima**: in questo ambiente non c'e' un tokenizer
(ne' tiktoken ne' anthropic), quindi si usa il rapporto ~4 caratteri per token, che
per l'italiano e' un'approssimazione ragionevole ma resta un'approssimazione. Le
parole invece sono contate esatte: dove serve un numero difendibile, usa quelle.

Uso:  python3 scripts/token_savings.py [--md]
      --md  stampa la tabella in markdown, da incollare in eval/results.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CARATTERI_PER_TOKEN = 4

# Ogni caso appartiene a una categoria di budget della §1 di SKILL.md.
CATEGORIE = {
    "saluto": ["C01", "C02", "C03", "C22"],
    "domanda secca": ["C04", "C05", "C16", "C21"],
    "consiglio": ["C06", "C07", "C13", "C14", "C15", "C18", "C20"],
    "lista": ["C08"],
    "tecnica": ["C09", "C19", "C24"],
    "materia seria (R0)": ["C10", "C11", "C23"],
    "traduzione": ["C12"],
    "limite/rifiuto": ["C17"],
}


# Marcatori romaneschi: se il baseline ne contiene almeno DUE distinti, la skill e'
# scattata anche li' e il confronto misurerebbe zero. Vedi l'avviso in baseline.md.
MARCATORI = (
    r"\ber\b", r"\bar\b", r"\bnun\b", r"\bgnente\b", r"\bde\b", r"\bli\b",
    r"'sto\b", r"'sta\b", r"'na\b", r"\bsemo\b", r"\bfamo\b", r"\bmagnà",
    r"\bannà", r"\bmo'", r"\bdaje\b", r"\bje\b", r"\bcor\b", r"\bder\b",
)
SOGLIA_MARCATORI = 2


def marcatori_trovati(testo: str) -> list[str]:
    bassa = testo.lower()
    return [m for m in MARCATORI if re.search(m, bassa)]


def e_contaminato(testo: str) -> bool:
    return len(marcatori_trovati(testo)) >= SOGLIA_MARCATORI


def leggi_blocchi(percorso: Path) -> dict[str, str]:
    """Estrae {id_caso: testo} dai blocchi '## Cxx' di un file di run.

    Spezza su un'intestazione di *qualunque* livello: altrimenti separatori e titoli
    di sezione fra un caso e l'altro entrano nella risposta precedente e ne gonfiano
    il conteggio, falsando la misura del risparmio.
    """
    testo = percorso.read_text(encoding="utf-8")
    blocchi = {}
    for blocco in re.split(r"(?m)^#{1,6}\s+", testo)[1:]:
        intestazione, _, corpo = blocco.partition("\n")
        id_caso = intestazione.strip()
        if re.fullmatch(r"C\d+", id_caso):
            blocchi[id_caso] = corpo.strip().rstrip("-").strip()
    return blocchi


def stima_token(testo: str) -> int:
    return round(len(testo) / CARATTERI_PER_TOKEN)


def conta_parole(testo: str) -> int:
    return len(re.findall(r"\S+", testo))


def categoria_di(id_caso: str) -> str:
    for nome, casi in CATEGORIE.items():
        if id_caso in casi:
            return nome
    return "non classificato"


def confronta(skill: dict[str, str], baseline: dict[str, str]) -> list[dict]:
    righe = []
    for id_caso in sorted(set(skill) & set(baseline), key=lambda x: (len(x), x)):
        s, b = skill[id_caso], baseline[id_caso]
        righe.append(
            {
                "id": id_caso,
                "categoria": categoria_di(id_caso),
                "parole_skill": conta_parole(s),
                "parole_base": conta_parole(b),
                "token_skill": stima_token(s),
                "token_base": stima_token(b),
                "contaminato": e_contaminato(b),
            }
        )
    return righe


def per_categoria(righe: list[dict]) -> dict[str, dict]:
    """Aggrega solo i casi con baseline pulito: i contaminati falserebbero il delta."""
    aggregato: dict[str, dict] = {}
    for r in (r for r in righe if not r["contaminato"]):
        voce = aggregato.setdefault(
            r["categoria"], {"n": 0, "token_skill": 0, "token_base": 0}
        )
        voce["n"] += 1
        voce["token_skill"] += r["token_skill"]
        voce["token_base"] += r["token_base"]
    for voce in aggregato.values():
        voce["media_skill"] = round(voce["token_skill"] / voce["n"])
        voce["media_base"] = round(voce["token_base"] / voce["n"])
        voce["risparmio"] = voce["media_base"] - voce["media_skill"]
        voce["percentuale"] = (
            round(100 * voce["risparmio"] / voce["media_base"]) if voce["media_base"] else 0
        )
    return aggregato


def totali(righe: list[dict]) -> tuple[int, int, int]:
    puliti = [r for r in righe if not r["contaminato"]]
    tot_s = sum(r["token_skill"] for r in puliti)
    tot_b = sum(r["token_base"] for r in puliti)
    perc = round(100 * (tot_b - tot_s) / tot_b) if tot_b else 0
    return tot_s, tot_b, perc


def stampa_markdown(righe: list[dict], aggregato: dict[str, dict]) -> None:
    puliti = [r for r in righe if not r["contaminato"]]
    print("| Categoria | Casi | Token stimati con skill | Senza skill | Risparmio |")
    print("|---|---|---|---|---|")
    for nome, v in sorted(aggregato.items(), key=lambda kv: -kv[1]["risparmio"]):
        print(
            f"| {nome} | {v['n']} | ~{v['media_skill']} | ~{v['media_base']} | "
            f"**-{v['risparmio']}** ({v['percentuale']}%) |"
        )
    tot_s, tot_b, perc = totali(righe)
    print(
        f"| **totale (baseline pulito)** | {len(puliti)} | ~{tot_s} | ~{tot_b} | "
        f"**-{tot_b - tot_s}** ({perc}%) |"
    )
    esclusi = [r["id"] for r in righe if r["contaminato"]]
    if esclusi:
        print(f"\nEsclusi per baseline contaminato ({len(esclusi)}): {', '.join(esclusi)}.")


def stampa_testo(righe: list[dict], aggregato: dict[str, dict]) -> None:
    print(f"{'caso':6} {'categoria':20} {'parole':>14} {'token stimati':>16}  baseline")
    print(f"{'':6} {'':20} {'skill/base':>14} {'skill/base':>16}")
    for r in righe:
        stato = "CONTAMINATO" if r["contaminato"] else "pulito"
        print(
            f"{r['id']:6} {r['categoria']:20} "
            f"{r['parole_skill']:>6}/{r['parole_base']:<7} "
            f"{r['token_skill']:>7}/{r['token_base']:<8}  {stato}"
        )
    print()
    for nome, v in sorted(aggregato.items(), key=lambda kv: -kv[1]["risparmio"]):
        print(
            f"{nome:20} n={v['n']:<3} media ~{v['media_skill']:>4} vs ~{v['media_base']:<4}"
            f"  risparmio ~{v['risparmio']} token ({v['percentuale']}%)"
        )
    puliti = [r for r in righe if not r["contaminato"]]
    esclusi = [r["id"] for r in righe if r["contaminato"]]
    tot_s, tot_b, perc = totali(righe)
    print(
        f"\nTOTALE su {len(puliti)} casi con baseline pulito: ~{tot_s} vs ~{tot_b} token, "
        f"risparmio ~{tot_b - tot_s} ({perc}%)."
    )
    if esclusi:
        print(f"Esclusi ({len(esclusi)}) perche' il baseline e' gia' in romanesco: {', '.join(esclusi)}.")
    print(f"Stima a {CARATTERI_PER_TOKEN} caratteri/token: le parole sono esatte, i token no.")


def main() -> int:
    radice = Path(__file__).resolve().parent.parent
    percorso_skill = radice / "eval" / "responses.md"
    percorso_base = radice / "eval" / "baseline.md"

    if not percorso_base.is_file():
        print(
            f"manca {percorso_base}: serve un run con gli stessi prompt e la skill spenta",
            file=sys.stderr,
        )
        return 1

    skill = leggi_blocchi(percorso_skill)
    baseline = leggi_blocchi(percorso_base)
    solo_uno = set(skill) ^ set(baseline)
    if solo_uno:
        print(f"ATTENZIONE: casi presenti in un solo run, esclusi: {sorted(solo_uno)}", file=sys.stderr)

    righe = confronta(skill, baseline)
    if not righe:
        print("nessun caso in comune fra i due run", file=sys.stderr)
        return 1

    aggregato = per_categoria(righe)
    if "--md" in sys.argv:
        stampa_markdown(righe, aggregato)
    else:
        stampa_testo(righe, aggregato)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
