from __future__ import annotations

from pydantic import BaseModel

from typing import Generic, List, Optional, TypeVar
from typing import TypeVar

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, model_validator

from .errors import Error
from .meta import Meta
from .resource import Resource
from .pagination import Pagination

DataT = TypeVar("DataT")


class JsonApi(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    version: str = "1.1"
    ext: Optional[List[AnyHttpUrl]] = None
    profile: Optional[List[AnyHttpUrl]] = None
    meta: Optional[Meta] = None


class TopLevelLinks(Pagination):
    model_config = ConfigDict(from_attributes=True)

    self: AnyHttpUrl
    related: Optional[AnyHttpUrl] = None
    describedby: Optional[AnyHttpUrl] = None


class GenericORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class JsonApiResponse(GenericORMModel, Generic[DataT]):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, exclude_unset=True
    )

    data: Optional[DataT] = None
    errors: Optional[List[Error]] = None
    meta: Optional[Meta] = None
    jsonapi: Optional[JsonApi] = None
    links: Optional[TopLevelLinks] = None
    included: Optional[List[Resource]] = None  # needs to be a set

    @model_validator(mode="after")
    def check_valid_fields(self) -> JsonApiResponse:
        if all(field is None for field in [self.data, self.errors, self.meta]):
            raise ValueError(
                "A JSON:API document MUST contain at least one of the following top-level members: data, errors, meta"
            )
        if all(field is not None for field in [self.data, self.errors]):
            raise ValueError(
                "The members 'data' and 'errors' MUST NOT coexist in the same document."
            )
        if self.included is not None and self.data is None:
            raise ValueError(
                "If a document does not contain a top-level 'data' key, the 'included' member MUST NOT be present either."
            )
        return self


class DTOBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, populate_by_name=True
    )
