from sqlalchemy import String, Integer, ForeignKey , DateTime, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship 
from datetime import datetime
from typing import Annotated, List, Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID 


from app.db.database import Base

timestamp = Annotated[datetime, mapped_column(default=datetime.utcnow)]


class User(Base):
    __tablename__= "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100),  index=True)
    email: Mapped[str]= mapped_column(String(120), unique=True, index=True)
    password: Mapped[str]= mapped_column(String(255), nullable=True)
    imageUrl: Mapped[str]= mapped_column(String(255), nullable=True)
    created_At: timestamp

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__= "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str]= mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    parent_id : Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    child_id : Mapped[Optional[uuid.UUID]]= mapped_column(UUID(as_uuid=True), nullable=True)
    time_limit : Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))

    owner : Mapped['User'] = relationship('User', back_populates='tasks')