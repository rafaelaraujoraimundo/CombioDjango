from api_v1.api_administration import routerUser
from api_v1.api_fluig import routerFLuig
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from inventario.api_inventario import (routerCelular, routerComputador, routerEstoque,
    routerHardware, routerMonitor, routerStatus, routerTipoItem, routerCentroCusto, routerEstabelecimento)
from comunicacao.api_comunicacao import  routerParametro
from integracoes.router import router as integracoes_router

  
api = NinjaExtraAPI(version='2.0.0', urls_namespace='Fluig')

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/v1/administration", routerUser)
api.add_router("/v1/fluig", routerFLuig)
api.add_router("/v1/inventario", routerHardware)
api.add_router("/v1/inventario", routerMonitor)
api.add_router("/v1/inventario", routerCelular)
api.add_router("/v1/inventario", routerTipoItem)
api.add_router("/v1/inventario", routerEstoque)
api.add_router("/v1/inventario", routerComputador)
api.add_router("/v1/inventario", routerStatus)
api.add_router("/v1/inventario", routerCentroCusto)
api.add_router("/v1/inventario", routerEstabelecimento)
api.add_router("/v1/comunicacao",routerParametro )
api.add_router("/v1/integracoes", integracoes_router)

