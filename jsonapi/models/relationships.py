from typing_extensions import Annotated
from typing import Any, List, Optional, Union

from pydantic import BaseModel, BeforeValidator, ConfigDict, StrictStr

from .links import Links
from .meta import Meta


class ResourceIdentifierObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: StrictStr
    id: Annotated[StrictStr, BeforeValidator(lambda v: str(v))]


RelationshipData = Union[List[ResourceIdentifierObject], ResourceIdentifierObject]


class Relationship(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    links: Optional[Links] = None
    data: Optional[RelationshipData] = None
    meta: Optional[Meta] = None


Relationships = dict[str, Relationship]

# class Relationships(Dict[str, Relationship]):
#     # pass

#     class Config:
#         from_attributes = True
