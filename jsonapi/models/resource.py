from typing import Generic, Optional, TypeVar

# from pydantic.generics import GenericModel
from pydantic import BaseModel

from .links import Links
from .meta import Meta
from .relationships import Relationships

TypeT = TypeVar('TypeT')
IdT = TypeVar('IdT')
AttributesT = TypeVar('AttributesT')


# class Resource(GenericModel, Generic[IdT, AttributesT]):
class ResourceNoId(BaseModel, Generic[AttributesT]):
    type: str
    attributes: Optional[AttributesT] = None
    relationships: Optional[Relationships] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class Resource(BaseModel, Generic[IdT, AttributesT]):
    type: str
    id: Optional[IdT] = None
    attributes: Optional[AttributesT] = None
    relationships: Optional[Relationships] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# class ResourceCreate(GenericModel, Generic[IdT, AttributesT]):
class ResourceCreate(BaseModel, Generic[IdT, AttributesT]):
    type: str
    id: Optional[IdT] = None
    attributes: Optional[AttributesT] = None
    relationships: Optional[Relationships] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
