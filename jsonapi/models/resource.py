from typing import Generic, Optional, TypeVar

# from pydantic.generics import GenericModel
from pydantic import BaseModel, ConfigDict

from .links import Links
from .meta import Meta
from .relationships import Relationships, ResourceIdentifierObject

TypeT = TypeVar('TypeT')
IdT = TypeVar('IdT')
AttributesT = TypeVar('AttributesT')


# class Resource(GenericModel, Generic[IdT, AttributesT]):
class ResourceNoId(BaseModel, Generic[AttributesT]):
    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)

    type: str
    attributes: Optional[AttributesT] = None
    relationships: Optional[Relationships] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None

    # class Config:
    #     from_attributes = True
    #     arbitrary_types_allowed = True

    def to_resource_identifier_object(self):
        return None

class Resource(BaseModel, Generic[IdT, AttributesT]):
    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)

    type: str
    id: Optional[IdT] = None
    attributes: Optional[AttributesT] = None
    relationships: Optional[Relationships] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None

    def to_resource_identifier_object(self):
        return ResourceIdentifierObject(type=self.type, id=str(self.id))

    # class Config:
    #     from_attributes = True
    #     arbitrary_types_allowed = True


# class ResourceCreate(GenericModel, Generic[IdT, AttributesT]):
class ResourceCreate(BaseModel, Generic[IdT, AttributesT]):
    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)

    type: str
    id: Optional[IdT] = None
    attributes: Optional[AttributesT] = None
    relationships: Optional[Relationships] = None
    links: Optional[Links] = None
    meta: Optional[Meta] = None

    # class Config:
    #     from_attributes = True
    #     arbitrary_types_allowed = True
