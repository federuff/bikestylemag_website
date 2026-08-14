---
name: article-images
description: Guida per generare le immagini (copertina/hero e immagini nel corpo) degli articoli di BikeStyle Mag con Google Nano Banana (Gemini 2.5 Flash Image), applicando lo stile visivo fisso della testata. Da usare ogni volta che viene chiesto di creare, generare o preparare un'immagine per un articolo del magazine (repo bikestylemag_website).
---

# Immagini AI di BikeStyle Mag — Google Nano Banana

Fonte canonica (modificabile dalla redazione): Google Doc "Bike-Style-Mag_Guida-Immagini" nella
cartella Drive `00_GUIDE BIKE STYLE`. Questo file ne è la traduzione operativa — se la guida
cambia, va riallineato a mano.

"Nano Banana" è il nome informale con cui in redazione ci si riferisce a Gemini 2.5 Flash
Image, il modello usato per generare le immagini del magazine. Tutte le immagini editoriali
(copertina articolo, immagini nel corpo) devono seguire lo stesso stile fisso, per dare
coerenza visiva al sito indipendentemente da chi genera l'immagine o quale articolo
rappresenta.

**Automazione scelta (agosto 2026)**: nessuna chiamata API diretta per ora. Ogni volta che
si scrive la bozza di un articolo come Google Doc in `02_Draft_Articoli`, includi nel
blocco "Metadati" un campo "image prompt" già pronto (soggetto specifico + blocco di stile
sotto), costruito seguendo questa guida — così l'umano deve solo copiarlo su Gemini/AI
Studio, senza doverlo scrivere da zero.

## Stile fisso (canonico)

**Stile artistico:** Illustrazione digitale che fonde lo stile del fumetto europeo (linea
chiara, contorni definiti ma non pesanti) con la delicatezza dell'acquerello.

**Caratteristiche tecniche:**
- **Palette colori:** Toni pastello morbidi, con prevalenza di colori caldi per gli edifici
  (mattoni ocrati, rossi sbiaditi) e toni freddi per i canali e il cielo (azzurri, grigi
  luminosi).
- **Tratto:** Linee di contorno sottili e precise (tipo inchiostro nero leggero), che
  definiscono le forme senza appesantire il disegno.
- **Texture:** Effetto acquerello leggero, con colori che sembrano "sconfinare" appena dai
  bordi, dando un senso di freschezza e non rigidità.
- **Atmosfera:** Luce naturale diurna, soffusa e chiara. Deve risultare semplice, elegante e
  leggibile.
- **Formato:** 16:9 (orizzontale).

Questo blocco di stile è fisso e va sempre incluso nel prompt, indipendentemente
dall'articolo. Non va reinterpretato o "migliorato" articolo per articolo — la coerenza
visiva tra le immagini è il punto.

**Regola vincolante**: nel prompt finale, la parte di stile va riportata **parola per
parola** identica al blocco "Stile fisso (canonico)" qui sopra — stessa lingua (italiano),
stessa formulazione. Non va tradotta in inglese, non va riassunta, non va riformulata
"meglio per il modello". Se la guida cambia, si aggiorna qui e da quel momento si usano le
nuove parole — ma sempre citate alla lettera, mai parafrasate.

## Come costruire il prompt per un articolo

1. Parti dal titolo e dal tema centrale dell'articolo (non serve leggerlo tutto: il soggetto
   dell'immagine è quasi sempre già nel titolo o nell'attacco).
2. Scrivi 1-2 frasi che descrivono la scena specifica: chi/cosa si vede, dove, che azione —
   niente loghi, marchi, testo nell'immagine o volti di persone reali riconoscibili.
3. Incolla subito dopo, parola per parola, l'intero blocco "Stile fisso (canonico)" qui
   sopra (titoli **Stile Artistico**, **Caratteristiche tecniche** con i suoi punti Palette
   colori/Tratto/Texture/Atmosfera/Formato inclusi).

### Esempio (articolo "Amsterdam wasn't born on a bike")

```
A wide cobblestone street in 1970s Amsterdam, canal houses on one side, a handful of
cyclists riding past parked cars and a canal with reflections of the sky, warm afternoon
light.

Stile Artistico: Illustrazione digitale che fonde lo stile del fumetto europeo (linea
chiara, contorni definiti ma non pesanti) con la delicatezza dell'acquerello.

Caratteristiche tecniche:
- Palette colori: Toni pastello morbidi, con prevalenza di colori caldi per gli edifici
  (mattoni ocrati, rossi sbiaditi) e toni freddi per i canali e il cielo (azzurri, grigi
  luminosi).
- Tratto: Linee di contorno sottili e precise (tipo inchiostro nero leggero), che
  definiscono le forme senza appesantire il disegno.
- Texture: Effetto acquerello leggero, con colori che sembrano "sconfinare" appena dai
  bordi, dando un senso di freschezza e non rigidità.
- Atmosfera: Luce naturale diurna, soffusa e chiara. Deve risultare semplice, elegante e
  leggibile.
- Formato: 16:9 (Orizzontale).
```

## Output e nomi file

- Formato **16:9**, esportato come `.jpg`.
- Percorso nel repo: `public/images/articles/`.
- Nome file: stessa convenzione data-slug degli articoli (vedi `README.md`) —
  `AAAA-MM-GG-slug-descrittivo-cover.jpg` per la copertina, `-detail.jpg`/`-02.jpg` per
  eventuali immagini secondarie nel corpo del pezzo.
- Il percorso va poi impostato nel campo `heroImage` del frontmatter dell'articolo (o
  richiamato via `![alt](/images/articles/nome-file.jpg)` nel corpo per le immagini
  interne).

## Nota operativa sull'automazione

Al momento questo repo/agente non ha un accesso diretto e automatizzato a Nano Banana per
generare l'immagine: il prompt va costruito seguendo questa guida e poi eseguito
manualmente (Google AI Studio / Gemini, modello Gemini 2.5 Flash Image), scaricando e
consegnando poi il file immagine risultante per essere salvato nel repo. Vedi `STATUS.md`
per lo stato di un'eventuale automazione end-to-end (generazione automatica legata alla
creazione della bozza).
