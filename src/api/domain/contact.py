from sqlmodel import Field, SQLModel, Column, String
from sqlalchemy.dialects import postgresql
from typing import Optional, List
from datetime import datetime


class Contact(SQLModel, table=True):
    __tablename__ = "contact"
    id: Optional[int] = Field(nullable=False, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False)

    region: str = Field(nullable=False)
    tags: Optional[List[str]] = Field(
        default=[], sa_column=Column(postgresql.ARRAY(String()))
    )
    notes: Optional[str] = Field(nullable=True)
    created_at: datetime = Field(default=datetime.now())
