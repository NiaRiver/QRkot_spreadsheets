from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from .base import CharityDonationBase


class Donation(Base, CharityDonationBase):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{super().__repr__()} {self.comment=}"
