from typing import List, Optional
from datetime import date
from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    published: bool = Field(default=False)
    ts: date = Field(default=None)
