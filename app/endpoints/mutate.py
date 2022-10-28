import base64

import jsonpatch
import structlog
from fastapi import APIRouter

from app.schemas import AdmissionResponse, AdmissionReview, MutateResponse


log = structlog.get_logger(__name__)
router = APIRouter()


@router.post(
    '',
    response_model=AdmissionResponse,
    summary='Mutate Endpoint'
)
def mutate_endpoint(request: AdmissionReview) -> None:

    spec = request.request.object
    modified_spec = spec.copy(deep=True)

    namespace = spec.metadata.namespace or request.request.namespace or '<unknown>'
    pod = spec.metadata.name or spec.metadata.generateName or '<unknown>'

    for container in modified_spec.spec.containers:
        if container.resources.limits:
            log.info('removing_cpu_limit', namespace=namespace, pod=pod, container=container.name)
            del container.resources.limits['cpu']

    patch = jsonpatch.JsonPatch.from_diff(spec.dict(), modified_spec.dict())

    response = AdmissionResponse(
        response=MutateResponse(
            uid=request.request.uid,
            patch=base64.b64encode(str(patch.to_string()).encode()).decode(),
        )
    )

    return response
