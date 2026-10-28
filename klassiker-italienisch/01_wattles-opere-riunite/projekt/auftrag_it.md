# Incarico: traduzione italiana – Wallace D. Wattles, Opere riunite

Cartella di lavoro: /tmp/claude-0/-home-user-bibel/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/wattles/
- Testo di partenza di riferimento (inglese, rivisto e collazionato con i facsimili): `eng/<opera>.md`
- Uscita: `ita/parts/<file indicato nel tuo incarico>.md`
- Strumenti ausiliari: creali SOLO in una nuova sottocartella tua di /tmp/claude-0/-home-user/ec169ed4-2c84-5e4f-ac02-4a773ce9afe5/scratchpad/

Obiettivo: una traduzione integrale, fedele e pronta per la stampa, in un italiano impeccabile, colto e naturale.
Niente riassunti né omissioni: OGNI paragrafo, ogni frase.

## Metodo
1. Traduci sezione per sezione (`## `) e PARAGRAFO PER PARAGRAFO. La sequenza dei paragrafi deve corrispondere esattamente
   all'inglese (stesso numero di paragrafi per capitolo). Salva il file a tappe se è lungo (capitolo per capitolo,
   aggiungendo al file), per non perdere lavoro.
2. Alla fine rileggi tutto il file di seguito e correggi ortografia, grammatica, concordanze, punteggiatura e stile.
3. Verifica: `python3 check_it.py eng/<opera>.md ita/parts/<file>.md <primo_indice> <ultimo_indice>`
   (gli indici di capitolo del tuo incarico, a partire da 0). Risultato atteso: `problems: 0`. Il rapporto tra le parole
   è solo un indizio di omissioni: non allungare MAI il testo per aumentarlo.
4. Rapporto breve: capitoli, numero di parole, decisioni e passi dubbi.

## Regole comuni (OBBLIGATORIE per tutto il libro)
- Ci si rivolge al lettore con il **tu** (come è uso nei libri di crescita personale in Italia); plurale **voi**.
  Eccezioni: dialoghi del romanzo (vedi incarico) e citazioni bibliche (voi/tu come nella Bibbia).
- Pronomi riferiti a Dio e a Gesù in **minuscolo** (egli, lui, suo).
- Citazioni bibliche: nello stile della **Bibbia Riveduta (Luzzi, 1924)**, di pubblico dominio, adattate alla formulazione
  citata da Wattles. Riferimenti nel formato «Giovanni 10:30», «Marco 11:23-24», solo dove l'originale li dà.
- «man»/«men» in senso generico: «l'uomo», «gli uomini» o «l'essere umano» secondo il contesto; niente neutralizzazione
  sistematica.

### Glossario fisso
| inglese | italiano |
|---|---|
| Certain Way / a Certain Way | il Certo Modo / in un Certo Modo (con le maiuscole, come nell'originale) |
| Right Way | il Giusto Modo (per non confonderlo con il Certo Modo) |
| formless substance / Formless Stuff / the Formless | sostanza informe / materia informe / la Sostanza Informe (maiuscole dove le ha l'originale) |
| Thinking Substance / thinking stuff | Sostanza Pensante / materia pensante |
| Original Substance / Intelligent Substance | Sostanza Originaria / Sostanza Intelligente |
| Living Substance / the Living One | Sostanza Vivente / il Vivente |
| increase | accrescimento (the impression of increase = l'impressione di accrescimento) |
| use value / cash value | valore d'uso / valore in denaro |
| creative plane / competitive plane | piano creativo / piano competitivo |
| competitive mind / creative mind | mentalità competitiva / mentalità creativa |
| the Advancing Man / advancing | l'uomo che avanza / che avanza |
| Principle of Health / of Life / of Power | Principio di Salute / Principio di Vita / Principio di Potenza |
| New Thought | Nuovo Pensiero |
| mind / spirit | mente / spirito (spiritual = spirituale) |
| All-Mind / All-Health / All-Power | la Mente Totale / la Salute Totale / l'Onnipotenza |
| the Supreme / Intelligence | il Supremo / Intelligenza |
| supply / Formless Supply | la provvista / la Provvista Informe |
| work-power / vital power / vital energy | potenza di lavoro / potenza vitale / energia vitale |
| will / faith / gratitude / purpose | volontà / fede / gratitudine / proposito |
| Mental Science / Christian Science | Scienza Mentale / Scienza Cristiana |

Credo di *La scienza del diventare ricchi* (da riprendere parola per parola dove Wattles lo ripete):
- Esiste una materia pensante di cui sono fatte tutte le cose e che, nel suo stato originario, permea, penetra e riempie gli interstizi dell'universo.
- Un pensiero, in questa sostanza, produce la cosa la cui immagine è formata dal pensiero.
- L'uomo può formare delle cose nel suo pensiero e, imprimendo il suo pensiero sulla sostanza informe, può far sì che venga creata la cosa a cui pensa.

### Titoli delle opere (in corsivo anche quando sono citati nel testo)
- The Science of Getting Rich → *La scienza del diventare ricchi*
- The Science of Being Well → *La scienza dello stare bene*
- The Science of Being Great → *La scienza dell'essere grandi*
- How to Get What You Want → *Come ottenere ciò che vuoi*
- Making the Man Who Can → *Formare l'uomo che può*
- The New Science of Living and Healing → *La nuova scienza del vivere e del guarire*
- What Is Truth? → *Che cos'è la verità?*
- A New Christ → *Un nuovo Cristo*
- Jesus: The Man and His Work → *Gesù: l'uomo e la sua opera*
- Hell-Fire Harrison → *Harrison l'Infernale* (il soprannome del protagonista è sempre «Harrison l'Infernale»;
  the Hell-Fire Club = il Club del Fuoco Infernale)
- The Nautilus: resta in inglese, in corsivo.
- Quando il testo parla della scienza stessa (non del libro): «la scienza del diventare ricchi», senza corsivo.

### Tipografia (uso editoriale italiano)
- Virgolette basse «…» (senza spazi all'interno); dentro di esse “…”. Mai virgolette dritte " '. Apostrofo tipografico ’.
- Lineetta — per gli incisi: «testo — inciso — testo», con spazi.
- Nel ROMANZO i dialoghi vanno tra virgolette basse: «Buongiorno» disse Harrison. «Come state?»
- Puntini di sospensione con il carattere … ; accenti corretti (è/é, perché, poiché, né, sé; à, ì, ò, ù); È maiuscola accentata.
- Corsivi dell'originale: *corsivo*. Le parole in MAIUSCOLO di enfasi vanno in corsivo minuscolo.

### Formato (identico a eng/)
- `## <titolo del capitolo in italiano>` senza numero, iniziale maiuscola solo alla prima parola e ai nomi propri.
  Prefazione dell'autore: `## Prefazione`. Prefazione del 1905 di *Gesù*: `## Prefazione degli editori (1905)`.
  Capitoli del romanzo: `## Capitolo primo` … `## Capitolo ottavo`.
- Paragrafi separati da una riga vuota; `> ` citazioni in blocco (riga della fonte: `> — Autore`); `| ` versi;
  `### ` sottotitoli; `%% ` righe di sommario sotto i titoli (come in eng/); note a piè di pagina come in eng/ (¹ in esponente
  nel testo e riga `~~ ¹ …` in fondo al capitolo); `^^` e `=>` come in eng/.
- Nessun capitolo «About This Work», nessuna nota del traduttore.
