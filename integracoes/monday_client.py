import json
import time
import io
import csv
from typing import Dict, List, Optional, Tuple, Set
import requests

API_URL = "https://api.monday.com/v2"
REQUEST_TIMEOUT = 30
RETRY_MAX = 3
RETRY_BACKOFF = 1.5
PAGE_SIZE = 100

# =========================
# GraphQL
# =========================
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

# Query atualizada: inclui created_at, updated_at e group { id title } em items e subitems
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
        created_at
        updated_at
        group { id title }
        column_values { id text value }
        subitems {
          id
          name
          created_at
          updated_at
          group { id title }
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
      created_at
      updated_at
      group { id title }
      column_values { id text value }
      subitems {
        id
        name
        created_at
        updated_at
        group { id title }
        column_values { id text value }
        board { id name }
      }
    }
  }
}
"""

# =========================
# HTTP helpers
# =========================
def _headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

def _post_graphql(api_key: str, query: str, variables: Dict) -> Dict:
    attempt = 0
    while True:
        attempt += 1
        try:
            resp = requests.post(
                API_URL,
                headers=_headers(api_key),
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
                raise RuntimeError(f"Rate limit (429): {resp.text}")
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

# =========================
# Fetchers
# =========================
def fetch_board_columns_map(api_key: str, board_id: int) -> Dict[str, str]:
    """
    Retorna {column_id: title} preservando a ordem reportada pelo Monday.
    """
    data = _post_graphql(api_key, QUERY_BOARD_COLUMNS, {"board_id": [str(board_id)]})
    boards = data.get("data", {}).get("boards", [])
    if not boards:
        return {}
    cols = boards[0].get("columns") or []
    return {c["id"]: (c.get("title") or c["id"]) for c in cols}

def fetch_all_items_and_subitems(api_key: str, board_id: int, page_size: int = PAGE_SIZE) -> Tuple[str, List[Dict]]:
    """
    Retorna (nome_do_board, lista_de_itens)
    Cada item possui: id, name, created_at, updated_at, group, column_values, 
    subitems[{id,name,created_at,updated_at,group,column_values,board{id,name}}]
    """
    items: List[Dict] = []
    board_name: Optional[str] = None
    cursor: Optional[str] = None
    try:
        while True:
            data = _post_graphql(api_key, QUERY_ITEMS_PAGE, {"board_id": [str(board_id)], "cursor": cursor, "limit": page_size})
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

    # Fallback para API antiga
    page = 1
    items = []
    board_name = None
    while True:
        data = _post_graphql(api_key, QUERY_ITEMS_OLD, {"board_id": [str(board_id)], "page": page, "limit": page_size})
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
    return (board_name or f"Board {board_id}", items)

# =========================
# Helpers de formatação
# =========================
def safe_text(cv: Dict) -> str:
    """
    Preferir 'text'; se vazio e houver 'value', serializa JSON em string.
    """
    txt = cv.get("text")
    if txt:
        return txt
    val = cv.get("value")
    if val in (None, ""):
        return ""
    try:
        return json.dumps(json.loads(val), ensure_ascii=False)
    except Exception:
        return str(val)

def build_header_from_monday(
    include_subitems: bool,
    main_cols_map: Dict[str, str],
    sub_cols_maps: Dict[int, Dict[str, str]],
) -> List[str]:
    """
    Header final (sem 'level'):
      ["id_item","Title","Group","Updated At", <títulos do item>, "id_subitem","name_subitem", <títulos extras do subitem>]
    """
    base_item_fields = ["id_item", "Title", "Group", "Updated At"]
    base_subitem_fields = ["id_subitem", "name_subitem"]

    main_titles = list(main_cols_map.values())
    extra_subitem_titles: List[str] = []
    if include_subitems and sub_cols_maps:
        seen = set(main_titles)
        for _, m in sub_cols_maps.items():
            for t in m.values():
                if t not in seen:
                    extra_subitem_titles.append(t)
                    seen.add(t)

    return base_item_fields + main_titles + base_subitem_fields + extra_subitem_titles

def rows_with_titles(
    include_subitems: bool,
    items: List[Dict],
    header: List[str],
    main_cols_map: Dict[str, str],
    sub_cols_maps: Dict[int, Dict[str, str]],
) -> List[Dict]:
    """
    Gera linhas com os campos do item (incluindo Group/Updated At) e, se houver,
    os dados dos subitens.
    """
    rows: List[Dict] = []

    main_titles = list(main_cols_map.values())
    extra_subitem_titles: set = set(
        h for h in header if h not in (
            ["id_item","Title","Group","Updated At","id_subitem","name_subitem"] + main_titles
        )
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

    if not include_subitems:
        for it in items:
            r = empty_row()
            r["id_item"] = it.get("id", "")
            r["Title"] = it.get("name", "")
            grp = (it.get("group") or {})
            r["Group"] = grp.get("title", "")
            r["Updated At"] = it.get("updated_at", "")
            fill_values_by_map(r, it.get("column_values") or [], main_cols_map, allowed_titles=set(main_titles))
            rows.append(r)
        return rows

    # Com subitens
    for it in items:
        subitems = it.get("subitems") or []

        if subitems:
            for si in subitems:
                r = empty_row()

                # Parte do ITEM
                r["id_item"] = it.get("id", "")
                r["Title"] = it.get("name", "")
                grp = (it.get("group") or {})
                r["Group"] = grp.get("title", "")
                r["Updated At"] = it.get("updated_at", "")
                fill_values_by_map(r, it.get("column_values") or [], main_cols_map, allowed_titles=set(main_titles))

                # Parte do SUBITEM
                r["id_subitem"] = si.get("id", "")
                r["name_subitem"] = si.get("name", "")

                siboard = (si.get("board") or {}).get("id")
                si_map: Optional[Dict[str, str]] = None
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

                rows.append(r)
        else:
            r = empty_row()
            r["id_item"] = it.get("id", "")
            r["Title"] = it.get("name", "")
            grp = (it.get("group") or {})
            r["Group"] = grp.get("title", "")
            r["Updated At"] = it.get("updated_at", "")
            fill_values_by_map(r, it.get("column_values") or [], main_cols_map, allowed_titles=set(main_titles))
            rows.append(r)

    return rows

def build_csv(api_key: str, board_id: int, include_subitems: bool) -> Tuple[str, bytes]:
    """
    Retorna (nome_arquivo, conteudo_csv_em_bytes) no layout:
    ["id_item","Title","Group","Updated At", <títulos do item>, "id_subitem","name_subitem", <títulos extras do subitem>]
    """
    board_name, items = fetch_all_items_and_subitems(api_key, board_id)

    main_cols_map = fetch_board_columns_map(api_key, board_id)

    sub_boards: Set[int] = set()
    if include_subitems:
        for it in items:
            for si in (it.get("subitems") or []):
                b = (si.get("board") or {}).get("id")
                if b:
                    try:
                        sub_boards.add(int(b))
                    except Exception:
                        pass

    sub_cols_maps: Dict[int, Dict[str, str]] = {}
    if include_subitems and sub_boards:
        for sbid in sub_boards:
            sub_cols_maps[sbid] = fetch_board_columns_map(api_key, sbid)

    header = build_header_from_monday(include_subitems, main_cols_map, sub_cols_maps)
    rows = rows_with_titles(include_subitems, items, header, main_cols_map, sub_cols_maps)

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=header, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for r in rows:
        writer.writerow({h: r.get(h, "") for h in header})

    filename = f"monday_board_{board_id}.csv"
    content = buf.getvalue().encode("utf-8-sig")
    return filename, content
