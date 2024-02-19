from api_v1.api_administration import router
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

  
api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/v1/administration", router)