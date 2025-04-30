from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.infrastructure.database.models.base import Base
from backend.utils.enums import TaskStatuses


class Task(Base):
    __tablename__ = "tasks"
    
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default=TaskStatuses.PENDING)
    priority: Mapped[int]
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")