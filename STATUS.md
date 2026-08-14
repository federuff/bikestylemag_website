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
- **Primo articolo "vero" scritto**: la news sui Paesi Bassi/come Amsterdam è tornata una città per le biciclette (fonte: SpaceDaily). File `src/content/articles/2026-08-14-amsterdam-cycling-history.md`, `draft: true`, in attesa di revisione umana.
- **Regola sui nomi file**: sia i file bozza/pubblicati nel repo sia i Google Doc in `02_Draft_Articoli`/`03_Pubblicati` seguono ora la convenzione `AAAA-MM-GG-slug-descrittivo` (vedi `README.md`, sezione "Contenuti e flusso bozza → pubblicazione").
- **Flusso bozze via Google Docs** (vedi `README.md`, sezione "Contenuti e flusso bozza → pubblicazione", per i dettagli): le bozze si scrivono ora come Google Doc nella cartella Drive `02_Draft_Articoli`, con blocco "Metadati" + corpo formattato; l'umano rilegge/corregge/aggiunge immagini nel Doc; su richiesta l'agente rilegge il Doc e rigenera il file Markdown nel repo. Cartella `03_Pubblicati` creata come archivio degli articoli usciti. Struttura allineata al playbook interno già scritto dalla redazione su Drive ("Guida Operativa Master: Workflow Editoriale AI"). Il Doc di prova per l'articolo Amsterdam è già in `02_Draft_Articoli`.

**⏳ Non ancora fatto — prossimo passo concreto:**
- Revisione umana della bozza Amsterdam (nel repo o nel Doc Drive corrispondente) e decisione se aprire una PR e/o pubblicarla (`draft: false`).

## Come si usa da una nuova conversazione

- Per scrivere un articolo: basta chiedere a Claude di scrivere un pezzo su una news (la skill `editorial-voice` si applica da sola, dato che è nel repo). Flusso previsto: bozza come Google Doc in `02_Draft_Articoli` su Drive → revisione/immagini nel Doc → su richiesta l'agente rilegge il Doc e crea/aggiorna il file Markdown (`draft: true`) nel repo → revisione finale in locale → `draft: false` + merge per pubblicare.
- Per problemi di deploy/dominio: vedi `README.md`, sezione Deploy, per i dettagli su Pages/DNS/HTTPS (già tutto configurato e funzionante a oggi).
