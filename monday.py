
# =========================
# VARIÁVEIS FIXAS (AJUSTE AQUI)
# =========================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consulta itens (e opcionalmente subitens) de um board no monday.com
e salva em CSV usando os TÍTULOS de coluna do monday como cabeçalho.

Formato final do CSV (sem 'level'):
  ["id_item","name_item", <títulos do item>, "id_subitem","name_subitem", <títulos extras do subitem>]

- Quando INCLUDE_SUBITEMS=False:
    * 1 linha por item (sem subitens).
- Quando INCLUDE_SUBITEMS=True:
    * Para item com N subitens: gera N linhas (uma por subitem).
    * Em cada linha: repete os dados do item nas colunas do item e,
      mais à frente, os campos do subitem que NÃO existem no board principal.
    * Se um item não tiver subitens, gera 1 linha com os dados do item (para manter o registro).
"""

import os
import json
import time
import csv
from typing import Dict, List, Optional, Tuple, Set
import requests

# =========================
# VARIÁVEIS FIXAS (AJUSTE AQUI)
# =========================
# Defina MONDAY_API_KEY no ambiente do SO (ex.: export MONDAY_API_KEY='seu_token')
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2MDE2ODE2NywiYWFpIjoxMSwidWlkIjozMzUzOTk2MSwiaWFkIjoiMjAyMy0wNi0wMlQxMToyMjoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NTQ2NDc1MiwicmduIjoidXNlMSJ9.Kl_rX1Nq6wkwC_bOfXM-MbkJy9Qh1jIVzmOyRyt_wDU"  # ⚠️ não versionar esse valor
BOARD_ID = 3857941534
PAGE_SIZE = 100
API_URL = "https://api.monday.com/v2"
REQUEST_TIMEOUT = 30
RETRY_MAX = 3
RETRY_BACKOFF = 1.5

OUTPUT_CSV = "monday_board_items.csv"
INCLUDE_SUBITEMS = True   # True = inclui subitens (gera N linhas para N subitens); False = ignora
# =========================

HEADERS_HTTP = {
    "Authorization": MONDAY_API_KEY or "",
    "Content-Type": "application/json",
}

# ---------- GraphQL helpers ----------
def _post_graphql(query: str, variables: Dict) -> Dict:
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = requests.post(
                API_URL,
                headers=HEADERS_HTTP,
                json={"query": query, "variables": variables},
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as e:
            if attempt >= RETRY_MAX:
                raise RuntimeError(f"Falha de rede ao chamar monday.com: {e}") from e
            time.sleep((RETRY_BACKOFF ** (attempt - 1)))
            continue

        if resp.status_code == 429:
            if attempt >= RETRY_MAX:
                raise RuntimeError(f"Rate limit atingido (HTTP 429): {resp.text}")
            retry_after = float(resp.headers.get("Retry-After", "2"))
            time.sleep(max(2.0, retry_after))
            continue

        if resp.status_code >= 500:
            if attempt >= RETRY_MAX:
                raise RuntimeError(f"Erro 5xx do monday.com: {resp.status_code} - {resp.text}")
            time.sleep((RETRY_BACKOFF ** (attempt - 1)))
            continue

        data = resp.json()
        if "errors" in data:
            raise RuntimeError(f"Erro GraphQL: {json.dumps(data['errors'], ensure_ascii=False)}")
        return data

# ---------- Queries ----------
QUERY_BOARD_COLUMNS = """
query GetBoardColumns($board_id: [ID!]) {
  boards (ids: $board_id) {
    id
    name
    columns {
      id
      title
    }
  }
}
"""

QUERY_ITEMS_PAGE = """
query GetBoardItems($board_id: [ID!], $cursor: String, $limit: Int!) {
  boards (ids: $board_id) {
    id
    name
    items_page (limit: $limit, cursor: $cursor) {
      cursor
      items {
        id
        name
        column_values { id text value }
        subitems {
          id
          name
          column_values { id text value }
          board { id name }
        }
      }
    }
  }
}
"""

QUERY_ITEMS_OLD = """
query GetBoardItemsOld($board_id: [ID!], $page: Int!, $limit: Int!) {
  boards (ids: $board_id) {
    id
    name
    items (limit: $limit, page: $page) {
      id
      name
      column_values { id text value }
      subitems {
        id
        name
        column_values { id text value }
        board { id name }
      }
    }
  }
}
"""

# ---------- Fetchers ----------
def fetch_board_columns_map(board_id: int) -> Dict[str, str]:
    """{column_id: title} para um board."""
    data = _post_graphql(QUERY_BOARD_COLUMNS, {"board_id": [str(board_id)]})
    boards = data.get("data", {}).get("boards", [])
    if not boards:
        return {}
    cols = boards[0].get("columns") or []
    # mantém a ordem original do monday
    return {c["id"]: (c.get("title") or c["id"]) for c in cols}

def fetch_all_items_and_subitems(board_id: int, page_size: int = 100) -> Tuple[str, List[Dict]]:
    """Retorna (nome_do_board, lista_de_itens)."""
    items: List[Dict] = []
    board_name: Optional[str] = None
    cursor: Optional[str] = None
    try:
        while True:
            data = _post_graphql(QUERY_ITEMS_PAGE, {"board_id": [str(board_id)], "cursor": cursor, "limit": page_size})
            boards = data.get("data", {}).get("boards", [])
            if not boards:
                return ("", [])
            board = boards[0]
            if board_name is None:
                board_name = board.get("name") or f"Board {board_id}"

            block = board.get("items_page") or {}
            new_cursor = block.get("cursor")
            page_items = block.get("items") or []
            items.extend(page_items)

            if not new_cursor:
                return (board_name, items)
            cursor = new_cursor
    except RuntimeError as e:
        msg = str(e).lower()
        if not any(k in msg for k in ["unknown argument", "cannot query field", "items_page"]):
            raise

    # fallback
    page = 1
    items = []
    board_name = None
    while True:
        data = _post_graphql(QUERY_ITEMS_OLD, {"board_id": [str(board_id)], "page": page, "limit": page_size})
        boards = data.get("data", {}).get("boards", [])
        if not boards:
            return ("", [])
        board = boards[0]
        if board_name is None:
            board_name = board.get("name") or f"Board {board_id}"

        page_items = board.get("items") or []
        items.extend(page_items)
        if len(page_items) < page_size:
            break
        page += 1
    return (board_name, items)

# ---------- Helpers ----------
def safe_text(cv: Dict) -> str:
    """Preferir text; se vazio e houver value, serializa JSON para string."""
    txt = cv.get("text")
    if txt:
        return txt
    val = cv.get("value")
    if val is None or val == "":
        return ""
    try:
        return json.dumps(json.loads(val), ensure_ascii=False)
    except Exception:
        return str(val)

def union_titles_in_order(primary_titles: List[str], extra_titles: List[str]) -> List[str]:
    """União preservando ordem: pega todos de primary e adiciona de extra que faltarem."""
    seen = set(primary_titles)
    result = list(primary_titles)
    for t in extra_titles:
        if t not in seen:
            result.append(t)
            seen.add(t)
    return result

# ---------- CSV ----------
def build_header_from_monday(
    main_cols_map: Dict[str, str],
    sub_cols_maps: Dict[int, Dict[str, str]],
) -> List[str]:
    """
    Header final (sem 'level'):
      ["id_item","name_item", <títulos do item>, "id_subitem","name_subitem", <títulos extras do subitem>]
    - <títulos do item>: na ordem do board principal
    - <títulos extras do subitem>: união (ordem dos boards de subitem) somente dos títulos que não existem no principal
    """
    base_item_fields = ["id_item", "name_item"]
    base_subitem_fields = ["id_subitem", "name_subitem"]

    # títulos do board principal (itens)
    main_titles = list(main_cols_map.values())

    # títulos extras de subitem (sem duplicar os do item)
    extra_subitem_titles: List[str] = []
    if INCLUDE_SUBITEMS and sub_cols_maps:
        seen = set(main_titles)
        for _, m in sub_cols_maps.items():
            for t in m.values():
                if t not in seen:
                    extra_subitem_titles.append(t)
                    seen.add(t)

    return base_item_fields + main_titles + base_subitem_fields + extra_subitem_titles

def rows_with_titles(
    items: List[Dict],
    header: List[str],
    main_cols_map: Dict[str, str],
    sub_cols_maps: Dict[int, Dict[str, str]],
) -> List[Dict]:
    """
    INCLUDE_SUBITEMS=False:
      - 1 linha por item (sem subitens).

    INCLUDE_SUBITEMS=True:
      - Para item com N subitens: gera N linhas.
      - Cada linha repete os campos do item (id_item, name_item e títulos do item) e
        preenche id_subitem, name_subitem e somente os títulos EXTRAS do subitem.
    """
    rows: List[Dict] = []

    main_id_to_title = main_cols_map
    main_titles = list(main_cols_map.values())

    # Títulos extras de subitem (presentes no header; exclui base e títulos do item)
    extra_subitem_titles: set = set(
        h for h in header if h not in (["id_item", "name_item", "id_subitem", "name_subitem"] + main_titles)
    )

    def empty_row() -> Dict[str, str]:
        return {h: "" for h in header}

    def fill_values_by_map(
        row: Dict[str, str],
        column_values: List[Dict],
        id_to_title: Dict[str, str],
        allowed_titles: Optional[set] = None
    ):
        for cv in (column_values or []):
            cid = cv.get("id")
            if not cid:
                continue
            title = id_to_title.get(cid)
            if not title:
                continue
            if allowed_titles is not None and title not in allowed_titles:
                continue
            if title in row:
                row[title] = safe_text(cv)

    if not INCLUDE_SUBITEMS:
        # ----- 1 linha por item -----
        for it in items:
            r = empty_row()
            r["id_item"] = it.get("id", "")
            r["name_item"] = it.get("name", "")
            # Campos do item (títulos do board principal)
            fill_values_by_map(r, it.get("column_values") or [], main_id_to_title, allowed_titles=set(main_titles))
            rows.append(r)
        return rows

    # ----- Com subitens: 1 linha por subitem (repetindo os campos do item) -----
    for it in items:
        subitems = it.get("subitems") or []

        if subitems:
            for si in subitems:
                r = empty_row()

                # 1) Campos do ITEM (repetidos)
                r["id_item"] = it.get("id", "")
                r["name_item"] = it.get("name", "")
                fill_values_by_map(r, it.get("column_values") or [], main_id_to_title, allowed_titles=set(main_titles))

                # 2) Campos do SUBITEM: id/name + SOMENTE títulos extras
                r["id_subitem"] = si.get("id", "")
                r["name_subitem"] = si.get("name", "")

                # Mapa do board do subitem (se existir)
                siboard = (si.get("board") or {}).get("id")
                si_map = None
                if siboard:
                    try:
                        si_map = sub_cols_maps.get(int(siboard))
                    except Exception:
                        si_map = None

                if si_map and extra_subitem_titles:
                    fill_values_by_map(
                        r,
                        si.get("column_values") or [],
                        si_map,
                        allowed_titles=extra_subitem_titles
                    )
                # Se não houver mapa, não tentamos preencher (evita sobrescrever colunas do item).

                rows.append(r)
        else:
            # Item sem subitens -> mantém 1 linha do item
            r = empty_row()
            r["id_item"] = it.get("id", "")
            r["name_item"] = it.get("name", "")
            fill_values_by_map(r, it.get("column_values") or [], main_id_to_title, allowed_titles=set(main_titles))
            rows.append(r)

    return rows

def write_csv(filepath: str, header: List[str], rows: List[Dict]) -> None:
    # BOM UTF-8 para abrir no Excel PT-BR sem quebrar acentos
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({h: r.get(h, "") for h in header})

# ---------- Main ----------
def main():
    if not MONDAY_API_KEY or MONDAY_API_KEY.strip() == "":
        raise SystemExit("Defina a variável de ambiente MONDAY_API_KEY com seu token da API do monday.com.")

    board_name, items = fetch_all_items_and_subitems(BOARD_ID, PAGE_SIZE)
    print(f"Board: {board_name} | Itens raiz: {len(items)}")

    # títulos do board principal
    main_cols_map = fetch_board_columns_map(BOARD_ID)

    # descobrir boards de subitem e coletar seus mapas de títulos
    sub_boards: Set[int] = set()
    if INCLUDE_SUBITEMS:
        for it in items:
            for si in (it.get("subitems") or []):
                b = (si.get("board") or {}).get("id")
                if b:
                    try:
                        sub_boards.add(int(b))
                    except Exception:
                        pass

    sub_cols_maps: Dict[int, Dict[str, str]] = {}
    if INCLUDE_SUBITEMS and sub_boards:
        for sbid in sub_boards:
            sub_cols_maps[sbid] = fetch_board_columns_map(sbid)

    # monta header (itens + extras de subitens)
    header = build_header_from_monday(main_cols_map, sub_cols_maps)

    # monta linhas
    rows = rows_with_titles(items, header, main_cols_map, sub_cols_maps)

    # escreve CSV
    write_csv(OUTPUT_CSV, header, rows)
    print(f"CSV gerado: {OUTPUT_CSV} (INCLUDE_SUBITEMS={INCLUDE_SUBITEMS})")

if __name__ == "__main__":
    main()
