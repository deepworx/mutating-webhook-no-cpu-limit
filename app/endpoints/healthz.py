from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()


@router.get(
    '',
    status_code=204,
    response_class=Response,
    summary="Healthcheck",
    description="The endpoint will always return the status code 204."
)
def healthz() -> None:
    pass
