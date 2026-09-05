from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime
    (timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime
    (timezone=True), onupdate=func.now()) 


