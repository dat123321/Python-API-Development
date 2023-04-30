from app.database import Base
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = "taikhoan"
    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Produce(Base):
    __tablename__ = "Produce"
    id = Column(Integer, primary_key=True, nullable=False)
    name_produce = Column(String, nullable=False)
    quantity_produce = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("taikhoan.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
