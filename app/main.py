import structlog
from fastapi import APIRouter, FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from app import __version__
from app.endpoints import healthz, mutate

log = structlog.get_logger(__name__)

app = FastAPI(
    title='Mutating Webhook no CPU limit',
    description='Kubernetes Dynamic Admission Control which removes CPU limits when creating pods',
    version=__version__,
)

api_router = APIRouter()
api_router.include_router(healthz.router, prefix='/healthz', tags=['healthz'])
api_router.include_router(mutate.router, prefix='/mutate', tags=['mutate'])

app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    log.error('invalid_data_received', details=exc.errors())
    return await request_validation_exception_handler(request, exc)
