from sqlalchemy import (
    create_engine,
    MetaData,
    Column,
    Integer,
    String,
    Boolean,
    PrimaryKeyConstraint,
    UniqueConstraint,
    ForeignKey,
)
from config import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Создание соединения с базой данных
engine = create_engine(
    f"postgresql://{config.db_user}:{config.db_password.get_secret_value()}@{config.db_host}/{config.db_name}"
)
metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    is_active = Column(Boolean(), default=False)
    tasks = relationship("Task", back_populates="user")
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_pk"),
        UniqueConstraint("user_id"),
    )


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    category = Column(String)
    link = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    items = relationship("Item", back_populates="task")
    __table_args__ = (
        PrimaryKeyConstraint("id", name="task_pk"),
        UniqueConstraint("link"),
    )


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    price = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))


# Создание таблицы, если она не существует
Base.metadata.create_all(bind=engine)
# Закрытие соединения
engine.dispose()
