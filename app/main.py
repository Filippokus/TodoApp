from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.models.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Все нужные модели должны быть импортированы перед запуском
    from app.models.task import TaskORM
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router)

# class CategoryORM(Base):
#     """Модель для таблицы категории в БД"""
#     __tablename__ = "categories"
#
#     name: Mapped[str]
#
#
#
# class Category(BaseModel):
#     id: str
#     name: str
#
#
# class CategoryCreate(BaseModel):
#     name: str
#
#
# class CategoryUpdate(BaseModel):
#     name: str | None = None


# def category_to_model(category: CategoryORM) -> Category:
#     """Конвертация объекта ORM в Pydantic"""
#     return Category(id=category.id, name=category.name)


# @app.get("/categories", response_model=list[Category])
# def read_categories(db: Session = Depends(get_db)) -> list[Category]:
#     categories = db.scalars(select(CategoryORM)).all()
#     return [category_to_model(category) for category in categories]


# @app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
# def create_categories(payload: CategoryCreate, db: Session = Depends(get_db)) -> Category:
#     category = CategoryORM(name=payload.name)
#
#     db.add(category)
#     db.commit()
#     return category_to_model(category)


# @app.patch("/categories/{category_id}", response_model=Category)
# def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)) -> Category:
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
#     category.name = payload.name if payload.name is not None else category.name
#     db.commit()
#     return category_to_model(category)


# @app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
#
#     db.delete(category)
#     db.commit()
