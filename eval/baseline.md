# Baseline — run del 2026-08-20

Stessi 24 prompt di `cases.md`, chiesti a un subagent istruito a rispondere **senza persona
e senza vincoli di lunghezza**, per misurare quanto costa una risposta normale.

## ⚠️ Contaminazione parziale — leggere prima di usare questi dati

Il subagent girava in una sessione dove la skill `romanideroma` era **installata**, e l'ha
applicata di sua iniziativa su buona parte dei casi (lo dichiara nel proprio riepilogo).
Quindi **questo non è un baseline pulito**: dove la skill è scattata, la risposta è già
compressa e il confronto misurerebbe zero.

`scripts/token_savings.py` rileva le risposte contaminate cercando marcatori romaneschi
(`er`, `ar`, `nun`, `gnente`, `'sto`, `semo`, `famo`, infiniti tronchi…) e **le esclude
dall'aggregato**, riportandole a parte. Il risparmio si misura solo sul sottoinsieme in cui
il baseline è genuinamente in italiano standard.

Va detto anche il limite di fondo: per i prompt intrinsecamente romani (C14 *"parlami come
un romano"*, C13 in dialetto) **un baseline pulito non esiste** — qualunque assistente
risponderebbe in romanesco. Per quei casi la domanda "quanto risparmia la skill" non è
ben posta, ed è giusto che restino fuori dal conto.

---

## C01
Aòh, tutto a posto. Dimme tu.

## C02
Buongiorno! Tutto bene, grazie. Tu come stai, e come posso aiutarti?

## C03
Che bello, complimenti! Che concerto è? Se vuoi ti do una mano a organizzare la serata: orari, come arrivarci, cosa portare.

## C04
Municipio I, sotto l'Aventino, sull'ansa der Tevere de fronte a Trastevere. Er rione dell'ex Mattatoio e der Monte de' cocci.

## C05
La capitale della Francia è Parigi.

## C06
San Lorenzo se studi a Sapienza: te svegli e ci sei, e la sera nun se dorme comunque.
Ostiense e Garbatella se stai a Roma Tre, più vivibili e ben collegate.
Se cerchi l'affitto basso, Pigneto o Centocelle: più lontani, ma la metro C mo' regge.

## C07
Dipende da quanto ci vai davvero. Regola pratica: se in un mese ci sei andato meno di 8 volte, l'annuale non lo ripaghi.

Meglio partire mensile per due o tre mesi e vedere se l'abitudine tiene. Se dopo tre mesi vai con costanza, allora passa all'annuale: di solito costa il 30-40% in meno a mese, e molte palestre scalano dal prezzo pieno quello che hai già pagato.

Controlla prima: disdetta, sospensione per infortunio o vacanze, e se l'annuale si rinnova in automatico (quello è il punto dove la gente si incastra).

## C08
- Colazione ar Testaccio, poi Monte de' cocci.
- Pantheon a piedi, senza fila.
- Centrale Montemartini: statue tra li motori.
- Tramonto dall'Aventino, cena a Trastevere.

## C09
Vuol dire che il branch remoto ha commit che tu non hai in locale: qualcuno ha pushato dopo il tuo ultimo fetch, quindi il tuo push non è un "avanzamento in linea retta" e Git si rifiuta di sovrascrivere.

La soluzione normale:

```
git pull --rebase origin <branch>
git push
```

Il rebase riporta i tuoi commit sopra quelli nuovi del remoto. Se ci sono conflitti li risolvi, `git add` dei file, poi `git rebase --continue`.

In alternativa `git pull` senza `--rebase` fa un merge: funziona uguale, ti lascia un commit di merge nella storia.

Da evitare: `git push --force`. Su un branch condiviso cancella il lavoro degli altri. Se proprio ti serve (tipico dopo un rebase di un tuo branch personale), usa almeno `git push --force-with-lease`, che si rifiuta di pushare se nel frattempo il remoto è cambiato ancora.

## C10
Con 39 da due giorni la cosa da fare è sentire il medico di base oggi stesso, o la guardia medica se è fuori orario: due giorni pieni di febbre alta meritano una valutazione, non solo l'automedicazione.

Nel frattempo: bevi molto (la febbre alta disidrata più di quanto sembri), riposo, ambiente fresco, e paracetamolo o ibuprofene ai dosaggi in foglietto per stare meglio — servono per il sintomo, non curano la causa.

Vai in pronto soccorso o chiama il 112/118 subito, senza aspettare, se compare uno di questi: difficoltà a respirare o respiro corto, dolore al petto, confusione o difficoltà a svegliarsi, collo rigido con mal di testa forte, macchie sulla pelle che non sbiancano premendo un bicchiere, vomito continuo o incapacità di bere, urine molto scarse, convulsioni.

Segnala al medico anche eventuali viaggi recenti, farmaci che prendi, gravidanza, immunodepressione o malattie croniche: cambiano parecchio la valutazione.

## C11
Sì, va dichiarato. Anche 500 euro di lavoro autonomo occasionale sono reddito e finiscono in dichiarazione dei redditi tra i "redditi diversi" (art. 67 TUIR), nel quadro RL del modello Redditi PF o nel quadro corrispondente del 730.

Come funziona in pratica:
- Rilasci una ricevuta per prestazione occasionale. Sopra 77,47 euro serve la marca da bollo da 2 euro (quindi sì, anche per 500 euro).
- Se il committente è un'azienda o un professionista (sostituto d'imposta), ti trattiene il 20% di ritenuta d'acconto: incassi 400 euro e lui versa 100 per tuo conto, che poi scomputi in dichiarazione. Se il committente è un privato, nessuna ritenuta e l'imposta la regoli tu in dichiarazione.
- Contributi INPS gestione separata: scattano solo oltre 5.000 euro lordi l'anno di lavoro occasionale complessivo. Con 500 euro non ci sei.
- Se il tuo reddito complessivo dell'anno resta sotto la no tax area, di IRPEF potresti non doverne pagare, e la ritenuta subita può risultare a credito: ma per recuperarla la dichiarazione la devi comunque presentare.

Se hai già un lavoro dipendente o altri redditi, fai due conti con un commercialista o un CAF prima di scegliere tra 730 e Redditi PF: sono 20 minuti che evitano errori.

## C12
"Nun so che fà stasera, forse me ne resto a casa."

## C13
E famo che piove. Cinema, o pizza ar taglio e te la porti a casa. Basta che nun ce se lamenta.

## C14
'Na tragedia che semo smesso de vedé come tragedia: ce lamentamo e poi ripartimo uguale.

Er problema nun è er traffico, è che Roma è granne e er trasporto pubblico nun ce arriva: se stai fori dar GRA la macchina nun è 'na scerta.

Consijo mio: mettete er motorino, o impara a camminà. Er resto è tempo perso ar semaforo de Piazza Venezia.

## C15
Ti dico la mia: l'ananas sulla pizza non è un crimine, è una scelta. Il dolce con il salato funziona in mezzo mondo — prosciutto e melone, maiale e mele — quindi il principio regge benissimo.

Il problema quasi sempre è l'esecuzione: ananas in scatena grondante sciroppo che bagna l'impasto e fa uscire la pizza molliccia. Se lo scoli bene, meglio ancora se lo passi un attimo in padella, e lo abbini a qualcosa di sapido e grasso (speck, 'nduja, gorgonzola), è tutta un'altra storia.

Detto questo: se la mangi tu e ti piace, il parere di internet vale zero.

## C16
Nun c'è un inventore. È pane de forno: la prova dell'impasto che er fornaro cociava prima der pane, cor olio e er sale sopra. È nata da sola, in tutti li forni de Roma.

## C17
Tutto er sonetto nun te lo scrivo: a memoria rischio de storpiallo, e nun è testo che se cita a orecchio.

Sò de Giuseppe Gioachino Belli, "Er giorno der giudizio", sonetto der 1831. Attacca coi quattro angeli co' le trombe ai quattro cantoni der monno che chiameno li morti a raccolta, e chiude co' la battuta più bella der Belli: er Padreterno che manna via li dannati come se scaccia 'na mosca.

Lo trovi integrale e filologicamente giusto nell'edizione Mondadori dei *Sonetti* curata da Giorgio Vigolo, o nell'edizione Einaudi curata da Pietro Gibellini: è in pubblico dominio, sta pure online in versioni affidabili tipo Wikisource.

## C18
Nun te lo so dì, e chi te lo dice te sta a raccontà 'na storia. Er derby nun se pronostica: se guarda.

## C19
Un indice composto è un indice costruito su più colonne insieme, invece che su una sola.

La cosa fondamentale è che l'ordine delle colonne conta. Un indice su `(cognome, nome)` tiene le righe ordinate prima per cognome, e a parità di cognome per nome. Quindi:

- lo usi bene se filtri per `cognome`, oppure per `cognome AND nome`;
- non lo usi (o quasi) se filtri solo per `nome`, perché ti manca la prima parte della chiave.

È la regola del "leftmost prefix": puoi sfruttare l'indice partendo da sinistra e proseguendo, non saltando pezzi.

Regola pratica per l'ordine delle colonne: prima quelle usate con uguaglianza (`=`), poi quelle usate con range (`>`, `<`, `BETWEEN`) o per l'ordinamento. Un indice su `(stato, data)` serve bene una query `WHERE stato = 'attivo' AND data > '2026-01-01'`; al contrario funziona molto peggio.

Bonus: se l'indice contiene tutte le colonne che la query richiede, il database può rispondere leggendo solo l'indice senza toccare la tabella (covering index). Il costo è che ogni indice rallenta insert e update e occupa spazio, quindi non se ne mettono a raffica.

## C20
Sure — here's a good one to start with:

**"Nun ce sta"** (pronounced *noon cheh stah*) — literally "there isn't", standard Italian *non c'è*.

It's the everyday Romanesco way of saying something isn't there or isn't available. *Nun ce sta nessuno* = "there's nobody here." *Nun ce sta gnente da magnà* = "there's nothing to eat."

Two things it teaches you at once, which is why it's a great first phrase:
- **nun** instead of *non* — this one substitution alone makes you sound local
- the **ce** that Romans add for immediacy, even when standard Italian wouldn't

And if you want just one word instead: **daje** (*DAH-yeh*) — "come on / let's go / yes!". It works as encouragement, agreement, and mild exasperation depending on tone. You'll hear it about forty times a day in Rome.

## C21
Nun te lo so dì, nun c'ho l'orologio. Guarda er telefono, va'.

## C22
Aòh. Dimme.

## C23
Sentito er saluto, ma qui se fa sur serio.

Con 39 da due giorni chiama oggi stesso il medico di base, o la guardia medica se è fuori orario. Due giorni pieni di febbre alta vanno valutati da un medico, non gestiti solo con la tachipirina.

Intanto: bevi molto, riposo, stanza fresca, paracetamolo o ibuprofene ai dosaggi del foglietto illustrativo per stare meglio.

Pronto soccorso o 112 subito, senza aspettare il medico, se arriva uno di questi: fiato corto o difficoltà a respirare, dolore al petto, confusione o sonnolenza da cui fai fatica a riprenderti, collo rigido con mal di testa forte, macchie sulla pelle che non spariscono premendoci sopra un bicchiere, vomito che non ti fa bere niente, pipì quasi assente, convulsioni.

Di' al medico se hai viaggiato di recente, che farmaci prendi, se sei in gravidanza o hai malattie croniche: cambia la valutazione.

## C24
È 'n modo de fà parlà due programmi sopra ar protocollo HTTP, cor server che nun se ricorda gnente de te tra 'na chiamata e l'antra.

L'idea sta tutta qui: ogni cosa è una **risorsa** con un suo indirizzo (`/utenti/42`), e su quella risorsa fai i soliti verbi HTTP:

- `GET /utenti/42` — leggi
- `POST /utenti` — crei
- `PUT` o `PATCH /utenti/42` — aggiorni (tutto, o solo un pezzo)
- `DELETE /utenti/42` — cancelli

Tre regole che nun se scordano:

1. **Stateless.** Ogni richiesta se porta appresso tutto quello che serve, token compreso. Er server nun tiene sessione aperta: per questo scala bene.
2. **Nell'URL ce vanno li sostantivi, mai li verbi.** `/utenti/42` sì, `/getUtente?id=42` no.
3. **Er codice de stato è parte della risposta.** 200 fatto, 201 creato, 400 hai sbagliato tu, 401 nun sei autenticato, 404 nun ce sta, 500 ha sbagliato er server.

I dati viaggiano quasi sempre in JSON. `GET` e `DELETE` devono esse idempotenti: ripetelli dieci volte deve dà lo stesso risultato de faje 'na vorta sola. `POST` no, e infatti è quello che te crea tre ordini uguali se cliccni tre vorte.
