
from monday_sdk import MondayClient
import csv

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2MDE2ODE2NywiYWFpIjoxMSwidWlkIjozMzUzOTk2MSwiaWFkIjoiMjAyMy0wNi0wMlQxMToyMjoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NTQ2NDc1MiwicmduIjoidXNlMSJ9.Kl_rX1Nq6wkwC_bOfXM-MbkJy9Qh1jIVzmOyRyt_wDU"
BOARD_ID = 3857941534 


client = MondayClient(token=API_KEY)
items = client.boards.fetch_all_items_by_board_id(board_id=BOARD_ID)

# Abrir um arquivo CSV para escrita
with open("monday_items.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # Cabeçalho
    writer.writerow(["ID", "Nome", "Atualizado em", "Grupo", "Colunas"])

    for it in items:
        # Alguns atributos vêm como objetos, então usamos getattr com fallback
        item_id = getattr(it, "id", "")
        name = getattr(it, "name", "")
        updated = getattr(it, "updated_at", "")
        group_title = getattr(it.group, "title", "") if hasattr(it, "group") else ""

        # column_values é uma lista de objetos -> vamos salvar como texto/JSON
        col_values = getattr(it, "column_values", [])
        cols_text = "; ".join([f"{c.id}={c.text}" for c in col_values])

        writer.writerow([item_id, name, updated, group_title, cols_text])

print("CSV salvo como monday_items.csv")