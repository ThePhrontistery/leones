from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    proyecto = Column(String, nullable=False, default="demo_metasketch")
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)

class MarkdownDocumentORM(Base):
    __tablename__ = "markdown_documents"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
