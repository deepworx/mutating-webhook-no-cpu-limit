from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, Field


class ResourcesSpec(BaseModel):
    limits: dict = Field(None)
    requests: dict = Field(None)

    class Config:
        extra = Extra.allow


class ContainerSpec(BaseModel):
    name: str
    resources: ResourcesSpec

    class Config:
        extra = Extra.allow


class PodSpec(BaseModel):
    containers: List[ContainerSpec]

    class Config:
        extra = Extra.allow


class Metadata(BaseModel):
    name: Optional[str]
    generateName: Optional[str]
    namespace: str

    class Config:
        extra = Extra.allow


class AdmissionObject(BaseModel):
    kind: str = Field('Pod', const=True)
    apiVersion: str = Field('v1', const=True)
    spec: PodSpec
    metadata: Metadata

    class Config:
        extra = Extra.allow


class AdmissionRequest(BaseModel):
    uid: UUID
    operation: str = Field('CREATE', const=True)
    object: AdmissionObject

    class Config:
        extra = Extra.allow


class AdmissionReview(BaseModel):
    kind: str = Field('AdmissionReview', const=True)
    apiVersion: str = Field('admission.k8s.io/v1', const=True)
    request: AdmissionRequest

    class Config:
        extra = Extra.allow


class MutateResponse(BaseModel):
    uid: UUID
    allowed: bool = True
    patch: str = Field(None)
    patchType: str = Field('JSONPatch', const=True)


class AdmissionResponse(BaseModel):
    kind: str = Field('AdmissionReview', const=True)
    apiVersion: str = Field('admission.k8s.io/v1', const=True)
    response: MutateResponse
