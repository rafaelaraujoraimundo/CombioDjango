from ninja import Schema
from typing import Optional

class GenerateTokenIn(Schema):
    key: str
    board: int

class ItemsQuery(Schema):
    token: Optional[str] = None
    key: Optional[str] = None
    board: Optional[int] = None
    includeSubitems: bool = False

    def validate_consistency(self):
        if not self.token and not (self.key and self.board):
            raise ValueError("Informe token OU key+board.")
