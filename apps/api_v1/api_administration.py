from ninja import Router
from typing import List
from administration.models import User
from .schema import UserSchema
from ninja_jwt.authentication import JWTAuth

from django.shortcuts import get_object_or_404

router = Router()



@router.get("/user", response=List[UserSchema])
def get_UserList(request):
    return User.objects.all()


@router.get("/user/{user_id}", response=UserSchema,auth=JWTAuth())
def get_user(request, user_id: int):
    # Busca o usuário no banco de dados
    user = get_object_or_404(User, id=user_id)
    return user

