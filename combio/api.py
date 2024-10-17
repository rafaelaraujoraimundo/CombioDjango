from api_v1.api_administration import routerUser
from api_v1.api_fluig import routerFLuig
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from inventario.api_inventario import routerHardware, routerMonitor

  
api = NinjaExtraAPI(version='2.0.0', urls_namespace='Fluig')

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/v1/administration", routerUser)
api.add_router("/v1/fluig", routerFLuig)
api.add_router("/v1/inventario", routerHardware)
api.add_router("/v1/inventario2", routerMonitor)
