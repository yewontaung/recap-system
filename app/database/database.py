from contextlib import contextmanager

from sqlmodel import Session, create_engine

from app.configs.settings import SETTINGS


engine = create_engine(SETTINGS.db_url, echo=True)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session