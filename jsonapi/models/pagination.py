from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, ConfigDict


class Pagination(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)

    first: Optional[AnyHttpUrl] = None
    prev: Optional[AnyHttpUrl] = None
    next: Optional[AnyHttpUrl] = None
    last: Optional[AnyHttpUrl] = None

    # class Config:
    #     from_attributes = True
    #     arbitrary_types_allowed = True
