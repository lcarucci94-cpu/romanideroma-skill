# RomaniDeRoma

Una skill per Claude che risponde **da romano de Roma**: dialetto vero, non macchietta,
e risposte che costano **meno** token di una risposta standard, non di più.

Se la versione romanesca è più lunga di quella italiana, la skill ha fallito.

## Perché esiste

Le skill di persona di solito allungano l'output: aggiungono colore, spiegano il colore,
poi traducono il colore. Questa fa il contrario. Due meccanismi:

1. **Un budget dichiarato per tipo di richiesta.** Un saluto vale 12 parole, una domanda
   secca 25, una lista 5 punti da 8 parole. Il budget si decide prima di scrivere.
2. **Progressive disclosure.** In contesto entra solo `SKILL.md` (~1.000 parole): le regole
   minime per parlare romano bastano da sole. I sette approfondimenti — fonologia completa,
   morfologia, lessico, modi di dire, cultura, registri, fonti — si caricano **solo quando
   servono**, cioè quasi mai.

Il risparmio non viene dal dialetto. Viene dal budget e dal divieto di premesse, cortesie
e traduzioni non richieste.

## Struttura

```
skills/romanideroma/
├── SKILL.md                    # sempre in contesto: budget, registri, 8 regole
└── references/                 # caricati su richiesta
    ├── fonologia.md            # la pipeline italiano → romanesco, in ordine
    ├── morfologia.md           # pronomi, possessivi, coniugazioni, avecce
    ├── lessico.md              # ~120 voci con registro e occasione d'uso
    ├── modi-di-dire.md         # proverbi col significato e quando escono
    ├── cultura.md              # cucina, rioni, calendario, letteratura, carattere
    ├── registri.md             # R0-R3: quanto dialetto, con chi, fino a dove
    └── fonti.md                # da dove vengono le regole, cosa si può citare
examples/conversazioni.md       # esempi con il costo in parole, giusti e sbagliati
scripts/validate-skill.py       # frontmatter, budget, reference orfani o mancanti
tests/                          # test del validatore
```

## I quattro registri

| | Quando | Come suona |
|---|---|---|
| **R0** italiano con cadenza | salute, soldi, legale, codice, dati | italiano pulito, ritmo romano |
| **R1** romanesco leggero — *default* | quasi tutto | `er`, `'sto`, `nun`, `mo'`, infiniti tronchi |
| **R2** romanesco pieno | l'utente lo chiede, o si parla di Roma | tutte le regole + lessico + un detto |
| **R3** romanaccio | mai di default | solo su richiesta esplicita, mai contro qualcuno |

Il registro può scendere a metà risposta, mai salire. Su materie serie il dialetto si spegne:
**la persona non tocca la precisione**.

## Come suona

> **"Che ore so'?"** → "Le tre e mezza, daje che fai tardi."
>
> **"Perché a Roma se magnano li gnocchi de giovedì?"** → "Perché venerdì era magro: pesce e
> basta. Er giovedì te caricavi prima. Sabato poi trippa."
>
> **"Mi spieghi cos'è un indice in un database?"** → "È 'na scorciatoia. Senza, er database
> se legge tutta la tabella riga per riga; con l'indice va dritto ar punto. Costa spazio in
> scrittura, te ripaga in lettura."

## Installazione

**Claude Code** — copia la cartella della skill fra quelle del progetto o dell'utente:

```bash
git clone https://github.com/lcarucci94-cpu/romanideroma-skill.git
mkdir -p ~/.claude/skills
cp -r romanideroma-skill/skills/romanideroma ~/.claude/skills/
```

Per un singolo progetto, copiala in `.claude/skills/` dentro il repo.
Si attiva da sola sui trigger nel `description`, oppure chiamandola: *"parlame da romano"*.

**Claude.ai / API** — incolla `SKILL.md` come istruzioni di sistema o come Project
instruction; i `references/` restano il materiale da fornire solo su necessità.

## Verifica

```bash
python3 -m unittest discover tests
python3 scripts/validate-skill.py
```

Il validatore fallisce se `SKILL.md` supera il budget di 1.400 parole, se il frontmatter è
rotto, se un reference citato non esiste o se un reference esiste ma nessuno lo cita —
un file che nessuno carica è peso morto.

## Limiti, dichiarati

- **Niente testi altrui**: mai canzoni, poesie, copioni o pagine di libri, per intero o in
  porzioni ampie. Sì a citazioni brevissime di autori in pubblico dominio (Belli, Pascarella,
  Trilussa) **con la fonte**.
- **Lo sfottò guarda la situazione, mai la persona.** Zero battute su origine, religione,
  aspetto, genere, orientamento, disabilità.
- **Il romanesco non è ignoranza**: la risposta è prima competente, poi romana.
- I tratti di carattere in `cultura.md` sono chiavi di lettura per **la voce**, non giudizi
  su chi vive a Roma.

## Fonti

Grammatica e fonologia da fonti accademiche — Treccani (Paolo D'Achille, *Italiano e dialetto
a Roma*), Accademia della Crusca, Wikipedia, Tito Morino (1899) su Wikisource. Lessico e
proverbi da raccolte divulgative. Elenco completo con link in
[`references/fonti.md`](skills/romanideroma/references/fonti.md).

Dove una forma è controversa (*antro* / *artro*), la skill sceglie la variante più diffusa
nel parlato di oggi, non la più antica.

## Licenza

MIT. Vedi [LICENSE](LICENSE).
