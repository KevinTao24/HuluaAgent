from fastapi.routing import APIRouter

from hulua.apis import agents  # , auth, metadata, models, monitoring

api_router = APIRouter()
# api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(agents.router, prefix="/agent", tags=["agent"])
# api_router.include_router(models.router, prefix="/models", tags=["models"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
