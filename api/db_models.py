import enum

from sqlalchemy import *
from api.database import Base


class Status(enum.Enum):
    new = "NEW"
    installing = "INSTALLING"
    running = "RUNNING"


class Apps(Base):
    __tablename__ = "apps"

    id = Column(Integer,
                index=True,
                autoincrement=True)
    UUID = Column(String,
                  primary_key=True,
                  unique=True,
                  nullable=False)
    kind = Column(String,
                  nullable=False)
    name = Column(String,
                  nullable=False)
    version = Column(String,
                     nullable=False)
    description = Column(String,
                         nullable=False)
    state = Column(Enum(Status),
                   default=Status.new)
    json = Column(JSON)