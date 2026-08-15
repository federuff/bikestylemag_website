#!/usr/bin/env python3
"""Segna nel Google Sheet "Bike Style Mag - News Feed" le notizie appena diventate
articoli pubblicati, scrivendo "Pubblicato — <url>" nella colonna "Selezionata per
articolo" della riga con lo stesso sourceUrl.

Uso: python3 scripts/update_news_tracker.py <path/to/article1.md> [<path/to/article2.md> ...]

Passo opzionale e "dormiente": usa le Application Default Credentials di Google
(google.auth.default()) — in CI arrivano da Workload Identity Federation (step
`google-github-actions/auth` nel workflow, nessuna chiave JSON scaricabile: questa
organizzazione Google Cloud blocca la creazione di chiavi service account), in locale
da `gcloud auth application-default login`. Se le credenziali non sono disponibili, lo
script esce senza errori e senza fare nulla — vedi STATUS.md per come attivarlo.
Idempotente: non sovrascrive una riga già marcata come pubblicata.
"""
import os
import re
import sys
from typing import Optional

DEFAULT_SHEET_ID = "1WCBjYxtQmwKv6LlGbDUhPR5qDEhP7Z_Yh23QpMLwEeE"
SITE_URL = "https://bikestylemag.com"
URL_COLUMN = "URL"
MARK_COLUMN = "Selezionata per articolo"
PUBLISHED_PREFIX = "Pubblicato"


def parse_frontmatter(path: str) -> Optional[dict]:
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return None

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    frontmatter = match.group(1)

    def field(name: str) -> Optional[str]:
        m = re.search(rf'^{name}:\s*"?([^"\n]+?)"?\s*$', frontmatter, re.MULTILINE)
        return m.group(1).strip() if m else None

    if field("draft") != "false":
        return None
    source_url = field("sourceUrl")
    if not source_url:
        return None

    slug = os.path.basename(path).rsplit(".", 1)[0]
    return {"sourceUrl": source_url, "articleUrl": f"{SITE_URL}/articles/{slug}"}


def col_letter(index: int) -> str:
    letters = ""
    index += 1
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def main() -> int:
    paths = sys.argv[1:]
    if not paths:
        print("No article files given — nothing to do.")
        return 0

    articles = [a for a in (parse_frontmatter(p) for p in paths) if a]
    if not articles:
        print("No newly published articles with a sourceUrl in this push — nothing to do.")
        return 0

    try:
        import google.auth
        from googleapiclient.discovery import build
    except ImportError:
        print("google-api-python-client/google-auth not installed — skipping.", file=sys.stderr)
        return 0

    try:
        credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
    except Exception as exc:  # noqa: BLE001 - qualsiasi errore di credenziali è "non attivo ancora"
        print(
            f"No Google Cloud credentials available ({exc}) — News Feed update skipped "
            "(optional step, see STATUS.md to activate it)."
        )
        return 0

    sheet_id = os.environ.get("NEWS_TRACKER_SHEET_ID", DEFAULT_SHEET_ID)
    service = build("sheets", "v4", credentials=credentials)
    values_api = service.spreadsheets().values()

    header = values_api.get(spreadsheetId=sheet_id, range="1:1").execute().get("values", [])
    header_row = header[0] if header else []
    if URL_COLUMN not in header_row or MARK_COLUMN not in header_row:
        print(
            f"Could not find columns {URL_COLUMN!r}/{MARK_COLUMN!r} in the sheet header "
            "— skipping (has the sheet structure changed?).",
            file=sys.stderr,
        )
        return 0
    url_col_index = header_row.index(URL_COLUMN)
    mark_col_index = header_row.index(MARK_COLUMN)

    all_rows = values_api.get(spreadsheetId=sheet_id, range="A:Z").execute().get("values", [])

    for article in articles:
        matched_row_index = None
        for i, row in enumerate(all_rows[1:], start=1):
            if len(row) > url_col_index and row[url_col_index].strip() == article["sourceUrl"].strip():
                matched_row_index = i
                break

        if matched_row_index is None:
            print(f"No News Feed row found for sourceUrl={article['sourceUrl']!r} — skipping.")
            continue

        row = all_rows[matched_row_index]
        current_mark = row[mark_col_index] if len(row) > mark_col_index else ""
        if current_mark.strip().startswith(PUBLISHED_PREFIX):
            print(f"Row for {article['sourceUrl']!r} already marked as published — skipping.")
            continue

        cell_range = f"{col_letter(mark_col_index)}{matched_row_index + 1}"
        new_value = f"{PUBLISHED_PREFIX} — {article['articleUrl']}"
        values_api.update(
            spreadsheetId=sheet_id,
            range=cell_range,
            valueInputOption="RAW",
            body={"values": [[new_value]]},
        ).execute()
        print(f"Marked {article['sourceUrl']!r} as published -> {article['articleUrl']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
