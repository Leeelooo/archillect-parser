from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

DB_URI = 'sqlite:///./archillect_parser.db'
Base = declarative_base()


class ArchillectItem(Base):
    __tablename__ = 'archillect_items'

    item_id = Column(Integer, primary_key=True, sqlite_on_conflict_unique='UPDATE')
    sources = Column(String)

    def __init__(self, item_id, sources_array):
        self.item_id = item_id
        self.sources = json.dumps(sources_array)


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
