from typing import NewType


Meta = NewType('Meta', dict[str, any])
# class Meta(dict[str, any]):

#     class Config:
#         from_attributes = True
#         arbitrary_types_allowed = True
