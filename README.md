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
eval/                            # 27 casi + run reali + baseline + scoring, vedi sotto
romanideroma.zip                # pacchetto pronto da caricare su claude.ai
scripts/validate-skill.py       # frontmatter, budget, reference orfani o mancanti
scripts/score_eval.py           # punteggio oggettivo di un run di eval/
scripts/token_savings.py        # misura il risparmio confrontando i due run
tests/                          # test del validatore
```

## Verifica empirica

`eval/cases.md` fissa 27 prompt con registro e budget attesi. `eval/results.md` è il
punteggio dei run: un subagent che vedeva **solo** `SKILL.md` — non questo repo, non chi
l'ha scritta — ha risposto ai casi, e le risposte sono state valutate contro i criteri
dichiarati.

Il run del 2026-08-19 ha trovato un problema reale — il registro R0 non reggeva su salute
e fisco — corretto in `SKILL.md` §4; il run del 2026-08-20 ha verificato che la correzione
tiene anche con la parola d'attivazione davanti (C23). **La v3.0.0 ha poi rovesciato quella
policy per scelta dell'autore**: R0 non è più imposto da un argomento, e su materie serie
sale la precisione invece di spegnersi il dialetto. I verdetti di quei run restano a
registro, ma vanno letti contro la policy del loro tempo — vedi `eval/results.md`.

I 3 casi sul contatore (C25-C27) sono dichiarati ma non ancora eseguiti: lo scorer li segna
`MANCA` ed esce con codice 1, così l'assenza non passa inosservata.

```bash
python3 scripts/score_eval.py     # controllo oggettivo: parole, righe, punti, frasi vietate
python3 scripts/token_savings.py  # risparmio misurato, skill contro baseline
```

Lo script copre solo i budget numerici; registro corretto, invenzione zero e sfottò sulla
situazione restano giudizio umano — vedi la tabella per caso in `eval/results.md`.

### Quanto risparmia davvero

Misurato confrontando gli stessi prompt con e senza skill (13 casi con baseline pulito,
run del 2026-08-20): **-79% di token complessivi**. Ma la media nasconde il dato che conta:

| Categoria | Con skill | Senza | Risparmio |
|---|---|---|---|
| spiegazione tecnica | ~40 | ~240 | **-200** (83%) |
| materia seria (R0) | ~54 | ~252 | **-198** (79%) |
| consiglio, opinione | ~24 | ~135 | **-111** (82%) |
| saluto | ~7 | ~14 | **-7** (50%) |
| domanda secca | ~3 | ~9 | **-6** (67%) |

**Il risparmio è quasi tutto nelle risposte lunghe.** Su un saluto anche una risposta
standard è già corta, e non c'è molto da comprimere.

Due avvertenze sul metodo, entrambe documentate in `eval/results.md`: i token sono
**stimati** a 4 caratteri/token (in ambiente non c'era un tokenizer — le parole invece sono
esatte), e 11 casi su 24 sono esclusi perché il baseline era contaminato (il subagent
aveva la skill installata e l'ha applicata anche lì).

## I quattro registri

| | Quando | Come suona |
|---|---|---|
| **R0** italiano con cadenza | **solo se l'utente lo chiede** | italiano pulito, ritmo romano |
| **R1** romanesco leggero — *default* | quasi tutto | `er`, `'sto`, `nun`, `mo'`, infiniti tronchi |
| **R2** romanesco pieno | l'utente lo chiede, o si parla di Roma | tutte le regole + lessico + un detto |
| **R3** romanaccio | mai di default | solo su richiesta esplicita, mai contro qualcuno |

Il registro lo decidono solo la richiesta dell'utente, il suo livello di lingua e la parola
d'attivazione: **nessun argomento lo sceglie al posto suo.** Su materie serie — salute, soldi,
diritto — il romanesco resta, ma sale la precisione al massimo: cifre, dosaggi, unità, nomi
propri e riferimenti di legge restano sempre in lingua originale, e il budget cede a quello
che serve per non far danni.

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

### Claude Code (CLI)

Copia la cartella della skill fra quelle del progetto o dell'utente:

```bash
git clone https://github.com/lcarucci94-cpu/romanideroma-skill.git
mkdir -p ~/.claude/skills
cp -r romanideroma-skill/skills/romanideroma ~/.claude/skills/
```

Per un singolo progetto, copiala in `.claude/skills/` dentro il repo invece che in `~/.claude/skills/`.

### Claude.ai (browser, desktop, mobile)

Le skill personalizzate si caricano da **Impostazioni**, non da un file incollato nelle
istruzioni. Serve un piano con code execution abilitata (Free, Pro, Max, Team o Enterprise —
su Team/Enterprise deve abilitarlo l'amministratore dell'organizzazione).

1. **Settings → Capabilities** → attiva *"Code execution and file creation"*. Senza questa
   voce attiva, la sezione Skills resta vuota o in grigio.
2. **Settings → Customize → Skills** → tasto **"+"** → **"Create skill"**.
3. Procurati lo zip. **Pronto all'uso:** [`romanideroma.zip`](romanideroma.zip) nella radice
   di questa repo — scaricalo e passa al punto 4. **Oppure rigeneralo** (necessario se hai
   modificato la skill), con la cartella come radice dello zip:
   ```bash
   cd romanideroma-skill/skills
   zip -r ../romanideroma.zip romanideroma
   ```
   Lo zip deve contenere `romanideroma/SKILL.md` e `romanideroma/references/*.md` — il nome
   della cartella dentro lo zip deve coincidere col campo `name` di `SKILL.md`. Quello in
   repo è tenuto allineato ai sorgenti da `validate-skill.py`: se modifichi la skill senza
   rigenerarlo (o viceversa), la validazione fallisce invece di distribuire in silenzio una
   versione vecchia.
4. Carica `romanideroma.zip` nella finestra di upload. Comparirà nell'elenco delle skill.
5. **Verifica che sia attiva** (toggle acceso) in Customize → Skills — caricata non significa
   accesa.

Le skill caricate così sono **private del tuo account**: non le vede automaticamente il resto
del team, anche su piani Team/Enterprise.

### Claude via API / Claude Code SDK

Non c'è un meccanismo di upload: incolla il contenuto di `SKILL.md` nel system prompt o nelle
istruzioni del Project. I `references/` restano materiale da passare solo quando serve —
manualmente, o via tool call se l'integrazione lo prevede.

## Come invocarla puntualmente

### Con la parola d'attivazione: "Aoh"

Comincia il messaggio con **`Aoh`** — in qualunque grafia (`Aoh`, `Aòh`, `Aó`, `Aò`, `Ao`),
con o senza `!` o `,`:

> **"Aoh, che ore so'?"** · **"Aòh, mi consigli un piatto?"** · **"Ao"**

È il modo previsto per chiamare la skill senza scrivere una frase intera. Cosa comporta:
risponde in **R2** (romanesco pieno), **non ricambia il saluto** (l'*Aòh* è già il saluto,
rispondergli con un altro *aòh* brucia budget per dire zero), e **non allarga il budget** —
la richiesta è quello che viene *dopo* l'*Aoh*, e prende il budget che le spetta. Se quello
che segue è materia seria (salute, soldi, legale), **il registro non cambia**: resta R2 e
sale la precisione. La parola d'attivazione sceglie la voce, non sospende il giudizio.

⚠️ **Non è un trigger deterministico.** L'attivazione automatica passa dal campo
`description`, che Claude valuta semanticamente: è scritto per rendere `Aoh` il più
riconoscibile possibile, ma resta una decisione del modello, non una regola di matching.
Se in una sessione non scatta, usa `/romanideroma` — quella è l'unica via garantita.

### Automatica (per argomento)

Anche senza parola d'attivazione, Claude legge la `description` e decide da solo se il
messaggio riguarda la skill. Funziona bene con un innesco chiaro (*"parlami da romano"*,
*"in romanesco"*) o un argomento tipicamente romano (cibo, quartieri, derby). Su richieste
ambigue può non scattare: in quel caso vale la via esplicita.

### Esplicita

Due modi, entrambi più affidabili dell'attivazione automatica:

- **In linguaggio naturale, nominandola**: *"Usa la skill RomaniDeRoma e rispondimi"*,
  *"Con la skill romanideroma, dimmi come si dice..."*.
- **Con lo slash command**: `/romanideroma` seguito dalla richiesta — chiama la skill per
  nome, bypassando la valutazione automatica.

Se nessuna delle due funziona, controlla in **Customize → Skills** che il toggle sia acceso:
una skill caricata ma spenta non risponde né in automatico né su comando esplicito.

Per tenerla **sempre spenta di default** e usarla solo su comando esplicito, aggiungi
`disable-model-invocation: true` al frontmatter di `SKILL.md` prima di caricarla — questa
repo non lo imposta, perché l'attivazione automatica sui trigger di `description` è il
comportamento previsto.

> I passaggi sopra vengono dalla documentazione ufficiale — [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
> e [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
> (Anthropic Help Center). L'interfaccia cambia nel tempo: se un menu non corrisponde più,
> cerca "Skills" nelle impostazioni dell'account.

## Verifica

```bash
python3 -m unittest discover tests
python3 scripts/validate-skill.py
```

Il validatore fallisce se `SKILL.md` supera il budget di 1.400 parole, se il frontmatter è
rotto, se un reference citato non esiste o se un reference esiste ma nessuno lo cita —
un file che nessuno carica è peso morto.

## Il contatore di token

Ogni risposta lunga si chiude con una riga:

> 🪙 ≈200 tok risparmiati

**Cosa non è**: una misura di quella risposta. Claude non può contare i token di una
risposta che non ha scritto — il confronto con "quanto sarebbe costata senza skill" è un
controfattuale, non un dato. Un numero calcolato lì per lì sarebbe inventato, e questo
progetto non inventa numeri.

**Cosa è**: la media misurata per la categoria di richiesta, dal confronto in
`eval/results.md`. Il `≈` è parte del formato, non una svista.

**Non appare** su saluti, domande secche, traduzioni e sulle materie serie. I primi tre
risparmiano 2-7 token e la riga ne costa 6: stamparla lì annullerebbe il risparmio che
dichiara. Su salute, soldi e diritto
— salute, soldi, legale — è escluso per decenza, non per aritmetica: sotto un consiglio
medico un contatore di token è fuori luogo, in qualunque registro sia scritto.

Per toglierlo del tutto, cancella la §7 di `SKILL.md` e rigenera lo zip.

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
