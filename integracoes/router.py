from ninja import Router, Schema
from typing import Optional
from django.http import Http404
from .models import MondayToken
from django.http import Http404, HttpResponse
from .models import MondayToken
from .monday_client import build_csv

router = Router()

class ItemsRequest(Schema):
    token: str
    includeSubitem: bool = False
    board_id: Optional[int] = None

class LinkOut(Schema):
    level: str
    id: int
    name: str
    board_id: int
    url: str
    parent_item_id: Optional[int] = None

class ItemsResponse(Schema):
    board_id: int
    board_name: str
    count: int
    includeSubitem: bool
    links: list[LinkOut]




@router.get("/items")
def get_items_csv(request, token: str, includeSubitem: bool = False, board_id: Optional[int] = None):
    """
    Retorna um CSV com itens e (opcionalmente) subitens
    """
    try:
        tk = MondayToken.objects.get(pk=token)
    except MondayToken.DoesNotExist:
        raise Http404("Token não encontrado.")

    bid = int(board_id or tk.monday_board)
    filename, content = build_csv(api_key=tk.monday_key, board_id=bid, include_subitems=includeSubitem)

    response = HttpResponse(content, content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response