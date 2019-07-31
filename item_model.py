from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URI = 'sqlite:///./archillect_parser.db'
Base = declarative_base()


class ArchillectItem(Base):
    # TODO: is table creating at all? there is an exception at the endpoint
    __tablename__ = 'archillect_items'

    item_id = Column(Integer, primary_key=True)
    sources = Column(String)


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
