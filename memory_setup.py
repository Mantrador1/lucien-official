# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker
import uuid
import datetime

DATABASE_URL = "PASTE_YOUR_REAL_DATABASE_URL_HERE"

Base = declarative_base()

class MemoryLog(Base):
    __tablename__ = "memory_log"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    session_id = Column(String, nullable=False)
    model = Column(String, nullable=False)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

test_entry = MemoryLog(
    prompt="ping",
    response="pong",
    session_id="maverick-session",
    model="gpt-4"
)

session.add(test_entry)
session.commit()
print("âœ… Table created and test memory inserted.")





