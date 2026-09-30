from sqlalchemy.orm import Mapped

from app.models.base import Base


class CategoryORM(Base):
    """Модель для таблицы категории в БД"""
    __tablename__ = "categories"
    name: Mapped[str]
