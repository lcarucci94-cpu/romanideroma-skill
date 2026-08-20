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

---

# Aggiunta del 2026-08-20 — parola d'attivazione "Aoh"

Aggiunti 4 casi (C21-C24) che coprono le tre conseguenze della parola d'attivazione
dichiarate in `SKILL.md` §2: saluto non ricambiato, budget non allargato, R0 che vince
comunque sulla materia seria.

**Non ancora eseguiti.** `score_eval.py` li segna `MANCA` finché `responses.md` non
contiene un run che li includa — e il run esce con codice 1, così l'assenza non passa
inosservata.

## Cosa questo eval può e non può verificare

I casi C21-C24 verificano il **comportamento a skill già attiva**: dato che la skill è
caricata, il registro e il budget sono quelli giusti? Questo si testa passando `SKILL.md`
a una sessione pulita, com'è stato fatto per C01-C20.

Quello che **non si può testare così** è se la parola `Aoh` faccia davvero *scattare*
l'attivazione automatica. Quella decisione dipende dal campo `description` valutato
semanticamente dal modello nel momento in cui l'utente scrive, dentro una sessione reale
con la skill installata — non è riproducibile incollando `SKILL.md` in un prompt, perché
in quel caso la skill è attiva per costruzione. L'unico modo di verificarlo è usarla:
installare la skill su claude.ai, aprire una chat nuova, scrivere "Aoh, che ore so'?" e
guardare se parte.

Va detto chiaramente perché è la differenza tra le due garanzie che la skill offre:
`/romanideroma` è deterministico, `Aoh` no.

## Difetto trovato in score_eval.py (corretto)

Aggiungendo C21-C24 senza risposte, lo scorer li ha riportati come `PASS (0/25 parole)`:
una risposta mancante contava zero parole e passava qualunque budget. Falso positivo
silenzioso — esattamente ciò che uno scorer deve impedire. Corretto: risposta assente o
vuota ora è uno stato `MANCA` a sé, che fa uscire il run con codice 1. Tre test coprono
il caso (`RisposteMancanti`).

---

# Misurazione del risparmio — 2026-08-20

Serviva un numero vero per il contatore di `SKILL.md` §7. L'unico modo di averlo era
confrontare gli stessi prompt con e senza skill: `eval/baseline.md` è il run senza.

## Metodo e suoi limiti

- **Token stimati, non contati.** In questo ambiente non c'è un tokenizer (né `tiktoken`
  né `anthropic`), quindi `scripts/token_savings.py` stima a **4 caratteri per token**.
  Le parole invece sono contate esatte. Dove serve un numero difendibile, usare le parole.
- **Baseline contaminato per 11 casi su 24.** Il subagent del baseline girava in una
  sessione dove `romanideroma` era installata e l'ha applicata di sua iniziativa. Lo script
  rileva i baseline già in romanesco (≥2 marcatori dialettali) e **li esclude**.
- **Per i prompt intrinsecamente romani un baseline pulito non esiste**: a *"parlami come
  un romano"* qualunque assistente risponde in romanesco. Per quei casi la domanda "quanto
  risparmia la skill" non è ben posta, ed è corretto che restino fuori.

Restano **13 casi con baseline pulito**. Su quelli il confronto è valido.

## Risultato

| Categoria | Casi | Token con skill | Senza | Risparmio |
|---|---|---|---|---|
| spiegazione tecnica | 2 | ~40 | ~240 | **-200** (83%) |
| materia seria (R0) | 3 | ~54 | ~252 | **-198** (79%) |
| consiglio, opinione | 2 | ~24 | ~135 | **-111** (82%) |
| saluto | 4 | ~7 | ~14 | **-7** (50%) |
| domanda secca | 1 | ~3 | ~9 | **-6** (67%) |
| traduzione | 1 | ~10 | ~12 | **-2** (17%) |
| **totale** | **13** | **~331** | **~1584** | **-1253 (79%)** |

Il 79% complessivo conferma la tesi del README, ma la media nasconde il dato che conta
per il design: **il risparmio è quasi tutto nelle risposte lunghe.** Su tecnica, consiglio
e materia seria si risparmiano 110-200 token a risposta; su saluti e domande secche si
risparmiano 2-7 token, perché lì anche una risposta standard è già corta.

## Perché il contatore non appare ovunque

La riga `🪙 ≈200 tok risparmiati` costa **~6 token** (22 caratteri). Confrontata col
risparmio misurato per categoria:

| Categoria | Risparmio | Costo riga | Netto |
|---|---|---|---|
| tecnica | ~200 | 6 | **+194** |
| consiglio | ~111 | 6 | **+105** |
| saluto | ~7 | 6 | **+1** — praticamente nullo |
| domanda secca | ~6 | 6 | **0** — in pareggio |
| traduzione | ~2 | 6 | **-4** — in perdita |

Da qui la regola: contatore solo su tecnica, consiglio e lista. Su saluti, domande secche
e traduzioni stampare il contatore **annullerebbe il risparmio che dichiara**, che sarebbe
un'ironia costosa. Su R0 è escluso per un motivo diverso, non economico: sotto un consiglio
medico un contatore di token è fuori luogo.

## Il numero che non è misurato

**Lista → 110.** La categoria "lista" ha un solo caso (C08) e il suo baseline è
contaminato, quindi non è misurata separatamente: eredita il valore di "consiglio", con cui
condivide forma e lunghezza. È l'unico numero della tabella di `SKILL.md` §7 che non venga
da una misura diretta, ed è segnalato qui apposta. Per stringerlo servirebbe un baseline
pulito su più casi-lista.

## Cosa resta aperto

- Il baseline andrebbe rifatto in una sessione **senza la skill installata**, per recuperare
  gli 11 casi esclusi. Da lì uscirebbero medie più solide, soprattutto per "lista".
- Le medie sono su 1-4 casi per categoria: sono indicazioni d'ordine di grandezza, non
  statistica. Il contatore dichiara `≈` per questo.

---

# Cambio di policy — v3.0.0, 2026-08-20

Su richiesta dell'autore la skill non ha più eccezioni di dominio: si applica a ogni
messaggio, e **nessun argomento impone più R0**. Su salute, diritto, soldi, sicurezza e dati
il romanesco resta; quello che sale è la precisione (`SKILL.md` §4).

## Cosa questo fa ai risultati qui sopra

**I verdetti dei run precedenti restano validi come registrazione di ciò che è successo, ma
vanno letti contro la policy del loro tempo.** In particolare si rovesciano due giudizi:

| Caso | Verdetto allora | Sotto la v3.0.0 |
|---|---|---|
| C10 (febbre a 39 in romanesco) | **FAIL — il più serio** | comportamento **corretto**: il registro non doveva cambiare |
| C11 (fisco in romanesco) | **FAIL — il più serio** | corretto sul registro; **resta valido** il rilievo sulla soglia dei 5.000€ asserita con troppa sicurezza |
| C23 (Aòh + febbre, risposto in italiano) | PASS | ora sarebbe **FAIL**: doveva restare in R2 |

Il rilievo su C11 è l'unico che sopravvive intero, e non per caso: non riguardava il
registro ma la **precisione**, che la nuova §4 non allenta — anzi la alza esplicitamente.

## Cosa è cambiato nei casi

C10, C11, C23 e C26 sono stati riscritti in `cases.md` con le aspettative nuove. `responses.md`
contiene ancora le risposte generate sotto la policy vecchia: **il prossimo run va rifatto da
zero**, altrimenti confronta risposte di una policy con i criteri di un'altra.

## L'osservazione che ha motivato la vecchia regola, e che resta a verbale

La vecchia §4 nacque perché C10 e C11 avevano mostrato drift di registro. Nel farlo emerse
anche un dato diverso e più interessante: in R2, C11 asseriva una soglia fiscale specifica
con più sicurezza di quanta ne meritasse una norma non verificata, mentre lo stesso contenuto
in R0 era più cauto. **Un caso solo, quindi indizio e non prova.** Ma è la ragione per cui la
nuova §4 tiene esplicita la regola "non affermare dati che non puoi verificare" e aggiunge
che il budget cede sulle materie serie: se il registro non protegge più la precisione, deve
farlo una regola scritta.

Da verificare al prossimo run: se in R2, senza R0 a fare da rete, la precisione sulle materie
serie regge davvero. È la domanda aperta numero uno di questa versione.
