from sqlalchemy import Column, String, Text

from app.core.db import Base
from .base import CharityDonationBase


class CharityProject(Base, CharityDonationBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f"{super().__repr__()}"
                f"{self.name=}, {self.description=}")
