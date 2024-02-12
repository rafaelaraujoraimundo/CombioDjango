from pydantic import BaseModel

# Create your models here.
class UserSchema(BaseModel):
    email: str
    usuario_datasul: str
    usuario_fluig: str
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        from_attributes = True