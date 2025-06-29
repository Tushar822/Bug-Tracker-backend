from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

engine = create_engine(settings.APP_DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session