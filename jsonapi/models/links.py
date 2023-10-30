from typing import Any, Dict, List, NewType, Optional, TypeVar, TypedDict, Union
from pydantic import BaseModel, AnyHttpUrl, FileUrl, ConfigDict

from .meta import Meta


class Link(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    href: AnyHttpUrl
    rel: Optional[str] = None  # link relation type
    # link to a description of the link relation type
    describedby: Optional[str] = None
    title: Optional[str] = None  # link title
    type: Optional[str] = None  # link media type
    hreflang: Optional[Union[str, List[str]]] = None  # link language
    meta: Optional[Meta] = None


# class Links(Dict[str, Union[HttpUrl, Link]]):
#     pass


# Links = NewType('Links', dict[str, Union[HttpUrl, Link]])

Links = dict[str, Union[AnyHttpUrl, FileUrl, str, Link]]
# Links = dict[str, Any]
