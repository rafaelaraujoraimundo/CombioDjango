from pydantic import BaseModel
from ninja import ModelSchema
from administration.models import ServidorFluig

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


class ServidorFluigSchema(ModelSchema):
    class Config:
        model = ServidorFluig
        model_fields = ['servidor', 'nome_servidor', 'client_key', 'consumer_secret', 'access_token', 'access_secret']


 