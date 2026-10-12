from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class AuditableModel(SQLModel):

    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)
