from api_v1.api_administration import router
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

#Alterar o parser para ORJSON
from ninja.parser import Parser
from django.http import HttpRequest
#Django Nija API
    
api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/v1/administration", router)