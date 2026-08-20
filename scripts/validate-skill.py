#!/usr/bin/env python3
"""Validatore della skill romanideroma. Solo libreria standard.

Controlla quello che si rompe davvero in silenzio:
frontmatter valido, budget di token del file sempre caricato,
coerenza fra i reference dichiarati e quelli sul disco, e — se lo zip
distribuibile e' presente — che il suo contenuto sia identico ai sorgenti.

Uso:  python3 scripts/validate-skill.py [radice]
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

# SKILL.md entra nel contesto a ogni turno: oltre questa soglia la skill
# costa piu' di quanto fa risparmiare.
MAX_PAROLE_SKILL = 1400
MAX_DESCRIPTION = 1024
CAMPI_OBBLIGATORI = ("name", "description")


def leggi_frontmatter(testo: str) -> dict[str, str]:
    """Parser YAML minimo: chiavi di primo livello, valori scalari."""
    if not testo.startswith("---"):
        return {}
    fine = testo.find("\n---", 3)
    if fine == -1:
        return {}
    campi: dict[str, str] = {}
    for riga in testo[3:fine].splitlines():
        if not riga.strip() or riga.startswith("#") or riga.startswith((" ", "\t")):
            continue
        chiave, sep, valore = riga.partition(":")
        if sep:
            campi[chiave.strip()] = valore.strip().strip("\"'")
    return campi


def verifica_zip(radice: Path, skill_dir: Path) -> list[str]:
    """Lo zip distribuibile deve coincidere byte per byte con i sorgenti.

    E' l'unico file del repo che puo' andare fuori sincrono senza che nulla
    si rompa: chi lo carica su claude.ai installerebbe una versione vecchia
    della skill senza accorgersene.
    """
    zip_path = radice / "romanideroma.zip"
    if not zip_path.is_file():
        return []

    attesi = {
        f"{skill_dir.name}/{p.relative_to(skill_dir).as_posix()}": p.read_bytes()
        for p in sorted(skill_dir.rglob("*"))
        if p.is_file()
    }

    try:
        with zipfile.ZipFile(zip_path) as z:
            presenti = {
                info.filename: z.read(info.filename)
                for info in z.infolist()
                if not info.is_dir()
            }
    except zipfile.BadZipFile:
        return [f"{zip_path.name} non e' uno zip valido: rigeneralo"]

    errori = []
    for mancante in sorted(set(attesi) - set(presenti)):
        errori.append(f"{zip_path.name}: manca {mancante} — rigenera lo zip")
    for extra in sorted(set(presenti) - set(attesi)):
        errori.append(f"{zip_path.name}: contiene {extra}, che non e' nei sorgenti")
    for nome in sorted(set(attesi) & set(presenti)):
        if attesi[nome] != presenti[nome]:
            errori.append(f"{zip_path.name}: {nome} e' diverso dal sorgente — rigenera lo zip")
    return errori


def valida(radice: Path) -> list[str]:
    errori: list[str] = []
    skill_dir = radice / "skills" / "romanideroma"
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return [f"manca {skill_md}"]

    testo = skill_md.read_text(encoding="utf-8")
    campi = leggi_frontmatter(testo)

    if not campi:
        errori.append("SKILL.md: frontmatter YAML assente o non chiuso da ---")

    for campo in CAMPI_OBBLIGATORI:
        if not campi.get(campo):
            errori.append(f"SKILL.md: campo '{campo}' mancante o vuoto")

    nome = campi.get("name", "")
    if nome and nome != skill_dir.name:
        errori.append(f"SKILL.md: name '{nome}' diverso dalla cartella '{skill_dir.name}'")
    if nome and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome):
        errori.append(f"SKILL.md: name '{nome}' non e' in minuscolo-con-trattini")

    descrizione = campi.get("description", "")
    if len(descrizione) > MAX_DESCRIPTION:
        errori.append(
            f"SKILL.md: description di {len(descrizione)} caratteri, massimo {MAX_DESCRIPTION}"
        )

    corpo = testo[testo.find("\n---", 3) + 4:] if campi else testo
    parole = len(corpo.split())
    if parole > MAX_PAROLE_SKILL:
        errori.append(
            f"SKILL.md: {parole} parole, massimo {MAX_PAROLE_SKILL} — "
            "sposta il dettaglio in references/"
        )

    riferimenti = set(re.findall(r"references/([\w-]+\.md)", testo))
    cartella_ref = skill_dir / "references"
    presenti = {p.name for p in cartella_ref.glob("*.md")} if cartella_ref.is_dir() else set()

    for mancante in sorted(riferimenti - presenti):
        errori.append(f"SKILL.md rimanda a references/{mancante}, che non esiste")
    for orfano in sorted(presenti - riferimenti):
        errori.append(f"references/{orfano} non e' citato in SKILL.md: non verra' mai caricato")

    for ref in sorted(presenti):
        if not (cartella_ref / ref).read_text(encoding="utf-8").strip():
            errori.append(f"references/{ref} e' vuoto")

    errori.extend(verifica_zip(radice, skill_dir))

    return errori


def main() -> int:
    radice = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errori = valida(radice)
    for errore in errori:
        print(f"ERRORE: {errore}", file=sys.stderr)
    if errori:
        print(f"\n{len(errori)} problemi.", file=sys.stderr)
        return 1
    print("Tutto a posto: la skill e' valida.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
