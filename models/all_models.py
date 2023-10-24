from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    PrimaryKeyConstraint,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


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
    user = relationship("User", back_populates="tasks")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    price = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task")
