from api_v1.api_administration import router
from api_v1.api_fluig import router as routerFLuig
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

  
api = NinjaExtraAPI(version='2.0.0', urls_namespace='Fluig')

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/v1/administration", router)
api.add_router("/v1/fluig", routerFLuig)
