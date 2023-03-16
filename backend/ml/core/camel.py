from pydantic import BaseModel

from stringcase import camelcase


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelcase
