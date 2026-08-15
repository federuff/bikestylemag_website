#!/usr/bin/env python3
"""Script una tantum: popola il Google Sheet "Bike Style Mag - News Feed" con la nuova
tassonomia a 21 categorie (vedi Google Sheet "Bike-Style-Mag_Elenco-Categorie" in
00_GUIDE BIKE STYLE su Drive e src/content.config.ts):
- colonna "new category" (L, già esistente): categoria macro (es. "e-bike", "culture").
- colonna "bike type" (nuova, aggiunta da questo script se manca): tipologia bici,
  quando individuabile (es. "mountain-bike", "cargo-bike") — lasciata vuota altrimenti,
  esattamente come un articolo del sito può non avere un tag di tipologia bici.

Mapping URL -> (categoria macro, tipologia bici) scelto a mano da Claude in base a
titolo/descrizione di ciascuna riga esistente al 15 agosto 2026.

Non fa parte del flusso ricorrente (a differenza di update_news_tracker.py) — pensato
per essere eseguito una sola volta, poi lo si può rimuovere dal repo.

Usa le stesse Application Default Credentials (Workload Identity Federation) del resto
dell'automazione News Feed — nessuna nuova credenziale richiesta.
"""
import sys

DEFAULT_SHEET_ID = "1WCBjYxtQmwKv6LlGbDUhPR5qDEhP7Z_Yh23QpMLwEeE"
URL_COLUMN = "URL"
MACRO_CATEGORY_COLUMN = "new category"
BIKE_TYPE_COLUMN = "bike type"

# url -> (categoria macro, tipologia bici o None)
CATEGORY_BY_URL = {
    "http://electrek.co/2026/08/13/urban-arrow-enters-the-longtail-cargo-e-bike-market-in-us-with-its-new-breeze/": ("e-bike", "cargo-bike"),
    "https://www.prnewswire.com/news-releases/urban-arrow-expands-into-the-longtail-segment-with-the-breeze-bringing-its-proven-safety-and-design-to-the-leading-cargo-bike-format-302850544.html": ("e-bike", "cargo-bike"),
    "http://electrek.co/2026/08/12/the-strange-story-behind-colorados-no-catch-free-e-bike-company/": ("e-bike", None),
    "https://theradavist.com/voluntary-safety-recall-ritchey-carbon-fiber-bicycle-forks": ("technology", None),
    "https://theradavist.com/double-pinch-flat-art-show": ("events-awards", None),
    "https://e360.yale.edu/features/2026-film-contest-second-place-cerrado": ("travel", None),
    "https://www.afterdawn.com/news/article.cfm/2026/08/13/google-unveils-pixel-11-series-bicycle-pre-order-campaign": ("culture", None),
    "https://economictimes.indiatimes.com/news/politics-and-nation/4200-vs-6957-aap-puts-delhi-govts-bicycle-purchase-under-scrutiny/articleshow/133196334.cms": ("infrastructure", "urban-bike"),
    "https://bringatrailer.com/listing/no-reserve-1966-schwinn-sting-ray-fastback-bicycle/": ("culture", None),
    "https://road.cc/news/cycling-live-blog-13-august-2026": ("infrastructure", "urban-bike"),
    "https://kottke.org/26/08/0049470-why-werent-bicycles-inven": ("culture", None),
    "https://nypost.com/2026/08/12/us-news/gang-of-e-bike-thugs-caught-on-camera-hurling-rocks-at-california-drivers/": ("culture", None),
    "https://spacedaily.com/m-most-people-assume-the-dutch-have-always-cycled-but-in-the-1960s-the-netherlands-was-rebuilding-its-cities-for-cars/": ("culture", "urban-bike"),
    "https://economictimes.indiatimes.com/news/international/us/in-1839-a-scottish-blacksmith-invented-the-first-rear-wheel-driven-vehicle-which-set-the-world-in-motion-and-laid-the-foundation-of-modern-transport/articleshow/133160314.cms": ("culture", None),
    "https://road.cc/ebiketips/feature/swytch-issues-update-e-bike-kit-nyc-micromobility-new-jersey-ebike-laws-week-in-e-bikes": ("e-bike", "urban-bike"),
    "https://www.notebookcheck.net/Low-step-e-bike-launches-with-90-Nm-Bosch-mid-drive-motor-800-Wh-battery-and-high-payload-capacity.1365790.0.html": ("e-bike", "urban-bike"),
    "http://electrek.co/2026/08/07/batch-eft-3-review-a-28-mph-fat-tire-e-bike-built-for-the-streets/": ("reviews", "mountain-bike"),
    "https://discerningcyclist.com/c/bicycles/electric-bikes/": ("e-bike", None),
    "https://theradavist.com/camera-corner-documentary-wende-cragg/": ("culture", "mountain-bike"),
}


def col_letter(index: int) -> str:
    letters = ""
    index += 1
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def main() -> int:
    try:
        import google.auth
        from googleapiclient.discovery import build
    except ImportError:
        print("google-api-python-client/google-auth not installed — skipping.", file=sys.stderr)
        return 1

    try:
        credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
    except Exception as exc:  # noqa: BLE001
        print(f"No Google Cloud credentials available ({exc}).", file=sys.stderr)
        return 1

    service = build("sheets", "v4", credentials=credentials)
    values_api = service.spreadsheets().values()

    header = values_api.get(spreadsheetId=DEFAULT_SHEET_ID, range="1:1").execute().get("values", [])
    header_row = header[0] if header else []
    if URL_COLUMN not in header_row or MACRO_CATEGORY_COLUMN not in header_row:
        print(f"Missing expected columns in header: {header_row}", file=sys.stderr)
        return 1
    url_col_index = header_row.index(URL_COLUMN)
    macro_col_index = header_row.index(MACRO_CATEGORY_COLUMN)
    macro_letter = col_letter(macro_col_index)

    if BIKE_TYPE_COLUMN in header_row:
        bike_type_col_index = header_row.index(BIKE_TYPE_COLUMN)
    else:
        bike_type_col_index = len(header_row)
        bike_type_letter = col_letter(bike_type_col_index)
        values_api.update(
            spreadsheetId=DEFAULT_SHEET_ID,
            range=f"{bike_type_letter}1",
            valueInputOption="RAW",
            body={"values": [[BIKE_TYPE_COLUMN]]},
        ).execute()
        print(f"Added new header {BIKE_TYPE_COLUMN!r} in column {bike_type_letter}.")
    bike_type_letter = col_letter(bike_type_col_index)

    all_rows = values_api.get(spreadsheetId=DEFAULT_SHEET_ID, range="A:Z").execute().get("values", [])

    updates = []
    matched = 0
    for i, row in enumerate(all_rows[1:], start=1):
        if len(row) <= url_col_index:
            continue
        url = row[url_col_index].strip()
        mapping = CATEGORY_BY_URL.get(url)
        if not mapping:
            print(f"Row {i + 1}: no mapping for URL {url!r} — skipped.")
            continue
        macro, bike_type = mapping
        matched += 1
        updates.append({"range": f"{macro_letter}{i + 1}", "values": [[macro]]})
        if bike_type:
            updates.append({"range": f"{bike_type_letter}{i + 1}", "values": [[bike_type]]})

    if not updates:
        print("Nothing to update.")
        return 0

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=DEFAULT_SHEET_ID,
        body={"valueInputOption": "RAW", "data": updates},
    ).execute()
    print(f"Updated {matched} row(s): column {macro_letter} ({MACRO_CATEGORY_COLUMN}) and, where applicable, column {bike_type_letter} ({BIKE_TYPE_COLUMN}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
