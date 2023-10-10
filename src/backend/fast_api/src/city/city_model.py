from db.base_model import Base
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import mapped_column, relationship


class City(Base):
    __tablename__ = "cities"

    name = mapped_column(String, nullable=False)
    latitude = mapped_column(String, nullable=True)
    longitude = mapped_column(String, nullable=True)
    state_id = mapped_column(ForeignKey("states.id"))
    state = relationship("State",back_populates="cities")
