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

**⏳ Non ancora fatto — prossimo passo concreto:**
- **Nessun articolo "vero" ancora scritto.** Il primo candidato è già stato selezionato e marcato nel Google Sheet dello scraper: la news sui Paesi Bassi/come Amsterdam è tornata una città per le biciclette (URL: `https://spacedaily.com/m-most-people-assume-the-dutch-have-always-cycled-but-in-the-1960s-the-netherlands-was-rebuilding-its-cities-for-cars/`). Manca solo scrivere l'articolo applicando la skill `editorial-voice` e aprire la PR di bozza.

## Come si usa da una nuova conversazione

- Per scrivere un articolo: basta chiedere a Claude di scrivere un pezzo su una news (la skill `editorial-voice` si applica da sola, dato che è nel repo). Il flusso previsto è: bozza (`draft: true`) → PR aperta per revisione → `draft: false` + merge per pubblicare.
- Per problemi di deploy/dominio: vedi `README.md`, sezione Deploy, per i dettagli su Pages/DNS/HTTPS (già tutto configurato e funzionante a oggi).
