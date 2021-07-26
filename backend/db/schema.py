from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class FileInfo(Base):
    __tablename__ = "file_info"
    id = Column(Integer, primary_key=True)
    task_id = Column(String(36), unique=True)
    original_file_name = Column(String(), nullable=False)
    file_name = Column(String())
    md5_hash = Column(String())
    created_date = Column(DateTime(), default=datetime.now, nullable=False)
