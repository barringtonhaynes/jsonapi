from __future__ import annotations
# from pydantic.generics import GenericModel
from pydantic import BaseModel
# from pydantic.utils import to_lower_camel
from pydantic.alias_generators import to_camel
from typing import Generic, List, Optional, TypeVar
from typing import TypeVar

from pydantic import AnyHttpUrl, BaseModel, validator

from .errors import Error
from .meta import Meta
from .pagination import Pagination
from .relationships import Relationship, Relationships

DataT = TypeVar('DataT')
IncludedT = TypeVar('IncludedT')


class JsonApi(BaseModel):
    version: str = '1.1'
    ext: Optional[List[AnyHttpUrl]] = None
    profile: Optional[List[AnyHttpUrl]] = None
    meta: Optional[Meta] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TopLevelLinks(Pagination):
    self: AnyHttpUrl
    related: Optional[AnyHttpUrl] = None
    describedby: Optional[AnyHttpUrl] = None

    class Config:
        from_attributes = True
        # arbitrary_types_allowed = True


# class GenericORMModel(GenericModel):
class GenericORMModel(BaseModel):
    class Config:
        from_attributes = True
        # arbitrary_types_allowed = True


class JsonApiResponse(GenericORMModel, Generic[DataT, IncludedT]):
    data: Optional[DataT] = None
    errors: Optional[List[Error]] = None
    meta: Optional[Meta] = None
    jsonapi: Optional[JsonApi] = None
    links: Optional[TopLevelLinks] = None
    included: Optional[List[IncludedT]] = None  # needs to be a set

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        exclude_unset = True

    # @validator('data', 'errors', 'meta', pre=True)
    # @classmethod
    # def check_required_members(cls, v, values):
    #     # Check if the object has at least one of the required top-level members
    #     if v is None and values['errors'] is None and values['meta'] is None:
    #         raise ValueError(
    #             "A JSON:API document MUST contain at least one of the following top-level members: data, errors, meta")
    #     return v

    @validator('data', 'errors')
    @classmethod
    def check_data_errors(cls, v, values):
        # Check if both data and errors are present
        if values.get('data', None) is not None and values.get('errors', None) is not None:
            raise ValueError(
                "The members 'data' and 'errors' MUST NOT coexist in the same document.")
        return v

    @validator('included')
    @classmethod
    def check_included(cls, v, values):
        # Check if included is present but data is not
        if values.get('data') is None and v is not None:
            raise ValueError(
                "If a document does not contain a top-level 'data' key, the 'included' member MUST NOT be present either.")
        return v


class DTOBaseModel(BaseModel):
    class Config:
        populate_by_name = True
        alias_generator = to_camel
        # alias_generator = to_lower_camel
        from_attributes = True
        arbitrary_types_allowed = True
