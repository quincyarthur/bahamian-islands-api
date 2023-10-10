from db.base_model import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship


class State(Base):
    __tablename__ = "states"

    name = mapped_column(String, nullable=False)
    code = mapped_column(String, nullable=True)
    latitude = mapped_column(String, nullable=True)
    longitude = mapped_column(String, nullable=True)
    country_id = mapped_column(ForeignKey("countries.id"))
    country = relationship("Country",back_populates="states")
    cities = relationship("City",back_populates="state")