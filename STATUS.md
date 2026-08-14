# Stato del progetto — repo sito (`bikestylemag_website`)

> Documento di handoff, pensato per dare contesto rapido a una nuova conversazione che lavora
> su questo repo, senza dover riassumere a voce cosa è già stato fatto. Aggiornalo quando
> qualcosa di rilevante cambia; non è documentazione tecnica (per quella vedi `README.md`).

## Cosa fa questo repo

Sito editoriale BikeStyle Mag, Astro, output statico. Repo pubblica (necessario per GitHub
Pages su questo piano) — separata da [`bikestylemag-idea`](https://github.com/federuff/bikestylemag-idea)
(privata), dove vive lo scraper che raccoglie le news di partenza.

## Stato attuale (14 agosto 2026)

**✅ Completato e verificato:**
- Sito live su **`https://bikestylemag.com`**, dominio custom con DNS verificato, HTTPS attivo.
- GitHub Pages configurato via GitHub Actions (`.github/workflows/deploy-astro.yml`), deploy automatico ad ogni push su `main`.
- Sito in lingua inglese, con logo, palette colori "Urban Elegance", layout responsive (verificato su mobile/desktop).
- Pagine: Home, News, pagina articolo, About, RSS, 404.
- Flusso di pubblicazione articoli: file Markdown in `src/content/articles/`, campo `draft: true/false` per bozza/pubblicato (vedi `README.md` per i dettagli tecnici).
- **Skill editoriale** (`.claude/skills/editorial-voice/SKILL.md`): distilla la guida di tono/stile della redazione (Google Doc) in istruzioni operative. Si carica automaticamente quando si scrive/rivede un articolo in questo repo — non serve rispiegare il tono ad ogni nuova chat.
- 4 articoli placeholder pubblicati (uno per categoria) per non lanciare il sito vuoto.
- **Primo articolo "vero" pubblicato**: la news sui Paesi Bassi/come Amsterdam è tornata una città per le biciclette (fonte: SpaceDaily). File `src/content/articles/2026-08-14-amsterdam-cycling-history.md`, con copertina generata via Nano Banana, `draft: false`, mergiato su `main` con PR [#3](https://github.com/federuff/bikestylemag_website/pull/3) — live sul sito dopo il deploy automatico.
- **Regola sui nomi file**: sia i file bozza/pubblicati nel repo sia i Google Doc in `02_Draft_Articoli`/`03_Pubblicati` seguono ora la convenzione `AAAA-MM-GG-slug-descrittivo` (vedi `README.md`, sezione "Contenuti e flusso bozza → pubblicazione").
- **Flusso bozze via Google Docs** (vedi `README.md`, sezione "Contenuti e flusso bozza → pubblicazione", per i dettagli): le bozze si scrivono ora come Google Doc nella cartella Drive `02_Draft_Articoli`, con blocco "Metadati" + corpo formattato; l'umano rilegge/corregge/aggiunge immagini nel Doc; su richiesta l'agente rilegge il Doc e rigenera il file Markdown nel repo. Cartella `03_Pubblicati` creata come archivio degli articoli usciti. Struttura allineata al playbook interno già scritto dalla redazione su Drive ("Guida Operativa Master: Workflow Editoriale AI"). Il Doc di prova per l'articolo Amsterdam è già in `02_Draft_Articoli`.
- **Guida immagini AI** (Google Nano Banana / Gemini 2.5 Flash Image): stile visivo fisso della testata (illustrazione fumetto europeo + acquerello, palette pastello, 16:9) documentato nella skill `.claude/skills/article-images/SKILL.md` e nel Google Doc "Bike-Style-Mag_Guida-Immagini" in `00_GUIDE BIKE STYLE` su Drive.
- **Decisione presa sull'automazione immagini**: niente integrazione API per ora. L'agente genera automaticamente, per ogni bozza, il prompt pronto (campo "image prompt" nei Metadati del Doc, vedi `README.md`); l'umano lo esegue manualmente su Gemini/AI Studio (Nano Banana) e consegna il file immagine risultante. Nessuna chiave API/credenziale coinvolta in questo flusso.

- **Pubblicazione autonoma autorizzata dall'utente (14 agosto 2026)**: quando l'umano ha già rivisto testo e immagine nel Doc di bozza e dice "pubblica", l'agente procede da solo fino in fondo — Markdown con `draft: false`, commit/push, apertura PR verso `main` e merge — senza chiedere ulteriore conferma per la PR/merge. Il comando "aggiorna" resta invece per sincronizzare solo il file nel repo (`draft: true`, niente PR), se si preferisce rivedere in locale. Vedi `README.md`, sezione "Contenuti e flusso bozza → pubblicazione", punto 4.

**⏳ Non ancora fatto — prossimo passo concreto:**
- Nessun articolo in coda al momento — prossimo passo è selezionare la prossima news dal Google Sheet dello scraper.
- Se in futuro si vorrà una vera automazione via API Gemini per le immagini (nessuna azione richiesta finché non viene chiesto esplicitamente): servirà una chiave API con billing abilitato, una decisione su dove custodirla e sul trigger (script manuale, GitHub Action, o nello scraper `bikestylemag-idea`).

## Come si usa da una nuova conversazione

- Per scrivere un articolo: basta chiedere a Claude di scrivere un pezzo su una news (la skill `editorial-voice` si applica da sola, dato che è nel repo). Flusso previsto: bozza come Google Doc in `02_Draft_Articoli` su Drive (con "image prompt" pronto nei Metadati) → revisione testo + generazione/inserimento immagine nel Doc da parte dell'umano → comando "pubblica" → l'agente procede in autonomia (Markdown, immagine, commit, PR, merge su `main`) senza altre conferme.
- Per problemi di deploy/dominio: vedi `README.md`, sezione Deploy, per i dettagli su Pages/DNS/HTTPS (già tutto configurato e funzionante a oggi).
