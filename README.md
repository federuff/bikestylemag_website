# BikeStyle Mag — sito web

Sito editoriale su design e biciclette, costruito con [Astro](https://astro.build) (output
statico). Repository pubblica dedicata al solo sito, separata da
[`bikestylemag-idea`](https://github.com/federuff/bikestylemag-idea) (privata), dove vive lo
scraper Python che raccoglie le news.

## Sviluppo locale

```bash
npm install
npm run dev       # http://localhost:4321 — mostra anche le bozze (draft: true)
npm run build     # build statica in dist/, esclude le bozze
npm run preview   # serve dist/ localmente per un controllo finale pre-deploy
```

## Contenuti e flusso bozza → pubblicazione

Ogni articolo è un file Markdown in `src/content/articles/`.

**Nome del file**: `AAAA-MM-GG-slug-descrittivo.md`, dove `AAAA-MM-GG` è la data di
realizzazione dell'articolo (di norma coincide con `pubDate`) e `slug-descrittivo` richiama
il titolo. Esempio: `2026-08-14-amsterdam-cycling-history.md`. Il nome non cambia quando
l'articolo passa da bozza a pubblicato (è lo stesso file, cambia solo `draft` nel
frontmatter) — la data nel nome resta quella di realizzazione, non va aggiornata ad ogni
modifica. Vale la stessa convenzione anche per il nome del Google Doc di bozza in
`02_Draft_Articoli` e per l'eventuale copia archiviata in `03_Pubblicati` (vedi sotto).

Frontmatter:

```yaml
---
title: "Titolo dell'articolo"
description: "Riassunto breve, usato anche come meta description SEO"
pubDate: 2026-08-13
category: ebike        # luxury | ebike | design | urban_commuter | general
heroImage: "/images/articles/nome-file.jpg"   # opzionale
sourceUrl: "https://..."                       # opzionale, news di partenza selezionata
sourceName: "Nome della fonte"                 # opzionale
draft: true             # true = bozza, false = pubblicato
---
```

- **`draft: true`** (default se il campo è omesso): l'articolo è visibile solo in locale con
  `npm run dev`, navigando direttamente al suo URL (`/articles/<nome-file-senza-estensione>`).
  Non compare nell'elenco News, in RSS, nella sitemap, né viene generato come pagina statica
  nella build di produzione.
- **`draft: false`**: l'articolo è pubblico — compare in Home, News, RSS e sitemap dopo il
  prossimo deploy.

Flusso previsto:
1. Un umano seleziona una news dal Google Sheet dello scraper (repo
   [`bikestylemag-idea`](https://github.com/federuff/bikestylemag-idea)).
2. Un agente scrive la bozza dell'articolo come Google Doc nella cartella Drive
   `02_Draft_Articoli`, con un blocco "Metadati" in testa (slug, description, category,
   sourceUrl, sourceName, pubDate, draft, heroImage, **image prompt**) seguito dal corpo
   con formattazione vera (titoli, grassetti — non simboli Markdown grezzi). Il campo
   "slug" nei Metadati è solo la parte descrittiva (es. `amsterdam-cycling-history`, senza
   data): la data va anteposta automaticamente quando si genera il nome del file, secondo
   la convenzione sopra. Il campo "image prompt" è generato automaticamente dall'agente
   seguendo la skill `.claude/skills/article-images/` (stile fisso Nano Banana) — pronto
   da incollare così com'è su Gemini/AI Studio per ottenere l'immagine di copertina.
3. Un umano rilegge e corregge il testo direttamente nel Doc, genera l'immagine copiando
   l'"image prompt" su Gemini/AI Studio (Nano Banana), e trascina il risultato nel Doc o
   lo consegna direttamente.
4. A questo punto ci sono due comandi possibili:
   - **"aggiorna"**: l'agente rilegge il Doc e ricostruisce solo il file Markdown con
     frontmatter in `src/content/articles/` (`draft: true`), committa/pusha, senza aprire
     PR — utile se la revisione finale si vuole fare nel repo (`npm run dev`) invece che
     nel Doc.
   - **"pubblica"**: presuppone che testo e immagine siano già stati rivisti dall'umano nel
     Doc. L'agente procede **in autonomia, end-to-end, senza chiedere ulteriore conferma**:
     rilegge il Doc, salva l'immagine in `public/images/articles/` (vedi sezione
     "Immagini" sotto), ricostruisce il Markdown con `draft: false`, committa/pusha, apre
     la PR verso `main`, la mergia, **e sposta il Doc di bozza da `02_Draft_Articoli` a
     `03_Pubblicati`** (stesso file, non una copia — `02_Draft_Articoli` deve contenere solo
     bozze ancora in corso). Nessuno di questi passaggi va riconfermato ogni volta — sono
     già autorizzati quando arriva il comando "pubblica" dopo la revisione dell'umano nel
     Doc.
5. Il push su `main` fa partire il deploy automatico.

Un umano può ovviamente anche scrivere e pubblicare un articolo direttamente, senza passare
dallo scraper o dal Google Doc: basta creare il file con `draft: false` fin da subito.

Tutta la logica di esclusione delle bozze è centralizzata in `src/lib/articles.ts`
(`getPublishedArticles()`) — ogni pagina o feed che elenca articoli deve usare questa funzione,
non `getCollection('articles')` direttamente, altrimenti rischia di mostrare le bozze in
produzione.

## Deploy

Il sito è pubblicato su GitHub Pages con dominio custom `bikestylemag.com`, via il workflow
[`.github/workflows/deploy-astro.yml`](.github/workflows/deploy-astro.yml): ogni push su `main`
builda ed effettua il deploy automaticamente.

**Configurazione una tantum da fare manualmente su GitHub (non automatizzabile da qui):**
1. Repo → Settings → Pages → Source: impostare su **"GitHub Actions"** (richiede repo pubblica,
   già soddisfatto).
2. DNS del dominio `bikestylemag.com`: puntarlo a GitHub Pages (record A verso gli IP di GitHub
   Pages, o CNAME se si usa un sottodominio) — GitHub mostra le istruzioni esatte in
   Settings → Pages dopo il primo deploy, insieme allo stato di verifica del dominio.

## Immagini

- **Logo**: `public/images/logo.png`, usato nell'header. Per sostituirlo basta rimpiazzare il
  file (sfondo trasparente consigliato).
- **Immagine di apertura Home**: `public/images/hero-placeholder.jpg` (formato 16:9), richiamata
  in `src/pages/index.astro`. Sostituisci il file con la tua immagine mantenendo lo stesso nome,
  oppure aggiorna il percorso nel componente.
- **Immagine di anteprima articolo**: campo `heroImage` nel frontmatter dell'articolo — viene
  usata sia come copertina nella pagina articolo sia come miniatura nelle card di Home/News.
  Metti il file in `public/images/articles/` e referenzialo come `/images/articles/nome-file.jpg`.
- **Immagini nel testo**: nel corpo Markdown dell'articolo si possono inserire immagini con la
  sintassi standard `![testo alternativo](/images/articles/nome-file.jpg)` — vengono già
  formattate automaticamente (larghezza piena, angoli arrotondati).
- **Generazione con AI (Google Nano Banana)**: lo stile visivo fisso della testata (per
  copertine e immagini nel corpo) è documentato nella skill `.claude/skills/article-images/`
  e nel Google Doc "Bike-Style-Mag_Guida-Immagini" in `00_GUIDE BIKE STYLE` su Drive — da
  seguire per qualsiasi immagine generata per il magazine, per mantenere coerenza tra gli
  articoli.

## Struttura

- `src/content/articles/` — articoli (Markdown)
- `src/content.config.ts` — schema degli articoli (Zod)
- `src/lib/articles.ts` — filtro bozze/pubblicati, helper categorie
- `src/layouts/`, `src/components/` — layout e componenti UI
- `src/pages/` — routing: Home, News, `articles/[slug]`, About, RSS, 404
- `src/styles/global.css` — font, colori, spaziatura (design tokens)
