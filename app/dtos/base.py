from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDto(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

class UpdateResult(BaseDto):
    resource_id: str
    message: str | None = None

    def __init__(self, resource_id: any, message: str | None = None):
        super().__init__(resource_id=resource_id if isinstance(resource_id, str) else str(resource_id), message=message)