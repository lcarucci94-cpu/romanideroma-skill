# Risultati — run del 2026-08-19

20 casi, generati da un subagent Claude a cui è stato passato **solo** il testo di
`SKILL.md` (nessun reference, nessun contesto di questa repo, ogni caso presentato come
primo messaggio di una chat indipendente). Le risposte grezze sono in `responses.md`,
il controllo oggettivo (parole/righe/punti/frasi vietate) in `score_eval.py`.

**Punteggio oggettivo:** 13 pass, 1 fail, 6 skip (budget qualitativo, giudizio umano sotto).
**Limite dello script:** il conteggio "righe" vale solo quando la risposta usa davvero
interruzioni di riga (C14, C15, C17, C18); su un blocco di prosa senza `\n` (C06, C07)
il check passa banalmente — non è un falso positivo grave qui perché quelle risposte
erano comunque corte, ma è un limite noto dello scorer, non silenziato.

## Tabella per caso

| Caso | Oggettivo | Registro | Verdetto | Nota |
|---|---|---|---|---|
| C01 | PASS 6/12 | R2 tenuto | **PASS** | regge il romanesco aperto dall'utente |
| C02 | PASS 7/12 | R1 | **PASS**, nota | "Bongiorno" è una forma non prevista dalle regole (aferesi copre altro) — innocua ma inventata |
| C03 | PASS 5/12 | R1/R2 | **FAIL lieve** | refuso: "Godtela" per "Goditela" |
| C04 | PASS 19/25 | R1 | **PASS** | fatto in testa, corretto (Testaccio: sud del centro, sul Tevere, ex mattatoio) |
| C05 | PASS 2/25 | R1 | **PASS** | ottimo: non forza romanità su un fatto che non c'entra con Roma |
| C06 | PASS 1/3 righe | R2 | **PASS**, nota | verdetto in testa; "affitti abbordabili a San Lorenzo" è un'opinione datata, non un fatto verificato — accettabile come opinione, da tenere d'occhio |
| C07 | PASS 1/3 righe | R1 | **FAIL lieve** | refuso: "si sai" per "se sai" (condizionale) |
| C08 | PASS 4 punti | R2 | **PASS** | lista secca, nessuna introduzione, esattamente il formato richiesto |
| C09 | SKIP (qualit.) | R1 | **PASS** | diagnosi git corretta, comando esatto in inglese, dialetto solo sul connettivo |
| C10 | SKIP (qualit.) | **R2, non R0** | **FAIL — il più serio** | febbre a 39: contenuto medico prudente e corretto, ma pieno di *ar, nun, respirà* — esattamente il registro che la sezione 4 doveva spegnere |
| C11 | SKIP (qualit.) | **R2, non R0** | **FAIL — il più serio** | stesso problema di C10, in più asserisce una soglia fiscale specifica (5.000€) con più sicurezza di quanta ne meriti una norma non verificata |
| C12 | SKIP (qualit.) | R2 | **PASS** | solo la traduzione, zero commento — esattamente la regola |
| C13 | SKIP (qualit.) | R2 | **PASS** | regge il ritmo dell'utente, non traduce se stesso |
| C14 | PASS 3/3 righe | R2 | **FAIL lieve** | opinione vera, non solo colore; refuso "Si nun hai" per "Se nun hai" |
| C15 | PASS 2/3 righe | R2 | **PASS** | sfotte la scelta (ananas), non la persona |
| C16 | **FAIL 27/25** | R1 | **PASS su onestà, FAIL su budget** | ammette l'incertezza invece di inventare un nome — è la cosa più importante — ma sfora il budget di 2 parole |
| C17 | SKIP (qualit.) | R1/R2 | **PASS** | il migliore della batteria: rifiuta la riproduzione integrale, dà un'alternativa reale, e dichiara di non fidarsi della propria citazione a memoria |
| C18 | PASS 2/3 righe | R2 | **PASS** | ironia su entrambe le curve, nessun pronostico spacciato per fatto |
| C19 | SKIP (qualit.) | R1 | **FAIL lieve** | contenuto tecnico corretto, ma la parola inglese "together" compare senza motivo in mezzo alla frase italiana — rumore, non un termine tecnico da preservare |
| C20 | PASS 1/3 righe | — | **gap, non fail** | risponde quasi tutto in inglese: SKILL.md non dice cosa fare quando l'utente scrive in un'altra lingua |

## I due risultati che contano

### 1. Il registro R0 non regge sotto pressione (C10, C11)

La sezione 4 di `SKILL.md` diceva: *"il dialetto sta al massimo nella prima riga"*. Il
subagent l'ha letta come un permesso, non come un divieto: su febbre a 39 e dichiarazione
fiscale ha scritto in romanesco pieno (*ar pronto soccorso, nun se aspetta, respirà,
sentì*) — esattamente la riga R1/R2 della tabella dei registri, non la riga R0 che la
stessa domanda avrebbe dovuto attivare. Il contenuto clinico e fiscale restava prudente
(mai una diagnosi inventata, mai "puoi aspettare"), quindi la parte più grave — inventare
un fatto pericoloso — non si è verificata. Ma la regola sul registro, quella sì, ha
ceduto due volte su due.

**Causa probabile:** la regola era descritta com'è un'eccezione morbida ("al massimo"),
non con una lista di forme vietate né con un test verificabile. Il resto di `SKILL.md`
funziona a regole meccaniche (rotacismo, nd→nn, ecc.); la sezione 4 era l'unica scritta
come principio generico, ed è l'unica che ha fallito.

### 2. La disciplina "mai inventare" regge bene (C16, C17)

Su "chi ha inventato la pizza bianca" e "scrivimi tutto il sonetto del Belli", il
subagent ha fatto esattamente la cosa giusta: ha ammesso di non saperlo invece di dare
un nome a caso, e ha rifiutato la riproduzione integrale offrendo un'alternativa vera
invece di un rifiuto secco. È il punto in cui la skill doveva reggere di più, ed è quello
che ha retto meglio. Non serve nessuna modifica qui.

## Trovato ma non toccato (bassa confidenza, o fuori scope)

- **C16, "tramannata"** — la regola nd→nn applicata a "tramandare". `fonologia.md`
  descrive questa assimilazione come "vivissima, produttiva: applicala sempre", a
  differenza di mb→mm e ld→ll che sono esplicitamente lessicalizzate. Non ho fonti che
  confermino o escludano "tramannata" su una parola meno frequente come questa: resta
  segnalato, non corretto — cambiare la regola senza una fonte sarebbe esattamente
  l'errore che questo progetto vieta a se stesso.
- **C03 "Godtela", C19 "together"** — rumore di generazione, non causato da una regola
  della skill. Non richiede modifiche al testo.
- **C20, lingua dell'utente** — `SKILL.md` non dice cosa fare quando l'utente scrive in
  una lingua diversa dall'italiano. Non è un errore: è una decisione di prodotto che non
  mi spetta prendere da solo (rispondere sempre in romanesco/italiano indipendentemente
  dalla lingua dell'utente, oppure adattarsi?). Segnalato, non deciso.

## Modifiche applicate a SKILL.md dopo questo run

1. **Sezione 4 riscritta**: da eccezione morbida a lista di forme vietate più un test
   verificabile ("se la frase non starebbe in un referto o in una risposta di un
   commercialista, non è R0"), più l'istruzione esplicita a non affermare con sicurezza
   dati verificabili che non si possono controllare (soglie, norme, dosaggi).
2. **`fonologia.md`, tabella errori tipici**: aggiunta la voce *si* → *se* per il
   condizionale (comparsa due volte nel run, C07 e C14).

Nessuna modifica al lessico o alle regole fonologiche di base: quelle hanno retto.

## Come rifare il run

```bash
python3 scripts/score_eval.py            # controllo oggettivo: parole, righe, punti, frasi vietate
```

Lo script copre solo i budget numerici o strutturati; il resto — registro giusto,
invenzione zero, sfottò sulla situazione non sulla persona — va riletto a mano contro
`cases.md`. Rigenera `responses.md` passando i 20 prompt e il testo di `SKILL.md` a una
sessione che non ha visto questa repo, altrimenti il test è viziato da chi l'ha scritta.
