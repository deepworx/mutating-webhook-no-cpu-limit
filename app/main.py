from fastapi import APIRouter, FastAPI

from app import __version__
from app.endpoints import healthz, mutate

app = FastAPI(
    title='Mutating Webhook no CPU limit',
    description='Kubernetes Dynamic Admission Control which removes CPU limits when creating pods',
    version=__version__,
)

api_router = APIRouter()
api_router.include_router(healthz.router, prefix='/healthz', tags=['healthz'])
api_router.include_router(mutate.router, prefix='/mutate', tags=['mutate'])

app.include_router(api_router)
