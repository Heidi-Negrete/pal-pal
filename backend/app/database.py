from sqlmodel import Session, SQLModel, create_engine
from .models import *
# from .config import settings // uncomment all and remove sqlite engine when moving to postgres


# Run db in debug mode by default
env_mode: bool = True
# if settings.ENVIRONMENT != "local":
#    debug_mode = False

connect_args = {"check_same_thread": False}
# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI),
#                       echo=env_mode, connect_args=connect_args)

engine = create_engine("sqlite://", echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
