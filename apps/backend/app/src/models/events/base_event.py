from pydantic import BaseModel


class BaseEvent(BaseModel):
    class Config:
        arbitrary_types_allowed: bool = True
        allow_population_by_field_name: bool = True
        use_enum_values: bool = True
