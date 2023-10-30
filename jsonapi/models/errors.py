from typing import Optional
from pydantic import BaseModel, ConfigDict

from .links import Links
from .meta import Meta


class Error(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: Optional[str] = None
    links: Optional[Links] = None
    status: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    source: Optional[dict] = None
    meta: Optional[Meta] = None
    # meta: Optional[dict[str, any]] = None

    # class Config:
    #     from_attributes = True
    #     arbitrary_types_allowed = True

    # need to add validation to ensure at least one of the fields is present
