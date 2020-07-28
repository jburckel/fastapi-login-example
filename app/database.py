from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import model
from app.setting import settings

if settings.DB_TYPE == 'SQLite':
    engine = create_engine(
        settings.DB_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        settings.DB_URL
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

model.AppModelBase.metadata.create_all(bind=engine)


def get_db():
    try:
        yield db
    finally:
        db.close()
