from api_v1.api_administration import router

from ninja import NinjaAPI

#Django Nija API
api = NinjaAPI()

api.add_router("/api/v1/administration", router)