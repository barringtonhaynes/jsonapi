
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from .links import Links
from .meta import Meta


class ResourceIdentifierObject(BaseModel):
    type: Any
    id: Any

    class Config:
        arbitrary_types_allowed = True


RelationshipData = Union[
    List[ResourceIdentifierObject],
    ResourceIdentifierObject
]


class Relationship(BaseModel):
    links: Optional[Links] = None
    data: Optional[RelationshipData] = None
    meta: Optional[Meta] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


Relationships = dict[str, Relationship]

# class Relationships(Dict[str, Relationship]):
#     # pass

#     class Config:
#         from_attributes = True
