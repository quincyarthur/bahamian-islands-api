from db.base_model import Base
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, relationship

class Country(Base):
    __tablename__ = "countries"

    name = mapped_column(String, nullable=False)
    iso_2 = mapped_column(String, nullable=False)
    iso_3 = mapped_column(String, nullable=False)
    phone_code = mapped_column(String, nullable=False)
    currency = mapped_column(String, nullable=False)
    currency_name = mapped_column(String, nullable=False)
    currency_symbol = mapped_column(String, nullable=False)
    latitude = mapped_column(String, nullable=True)
    longitude = mapped_column(String, nullable=True)
    currency_name = mapped_column(String, nullable=False)
    emoji_unicode = mapped_column(String, nullable=False)
    states = relationship("State",back_populates="country")
