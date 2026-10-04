from collections.abc import Sequence
from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category import CategoryNotFoundError, CategoryService


def test_list_categories_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    categories: Sequence[CategoryORM] = [
        CategoryORM(id="category-1", name="FastAPI"),
        CategoryORM(id="category-2", name="Django"),
        CategoryORM(id="category-3", name="SQL"),
    ]
    category_repository_mock.get_all.return_value = categories

    result = category_service.list_categories()

    assert result == [
        CategoryRead(id="category-1", name="FastAPI"),
        CategoryRead(id="category-2", name="Django"),
        CategoryRead(id="category-3", name="SQL"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    created_category = CategoryORM(id="category-1", name="Новая категория")
    category_repository_mock.create.return_value = created_category

    result = category_service.create_category(CategoryCreate(name="Новая категория"))

    category_repository_mock.create.assert_called_once_with(name="Новая категория")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новая категория",
    }


def test_update_category_updates_passed_field(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category = CategoryORM(id="category-1", name="Старая категория")
    category_repository_mock.get_by_id.return_value = category
    expected_name = "Новая категория"

    result = category_service.update_category(
        "category-1", CategoryUpdate(name="Новая категория")
    )

    category_repository_mock.get_by_id.assert_called_once_with("category-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }


def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        category_service.update_category(
            "missing-category", CategoryUpdate(name="Неважно")
        )

    db_mock.commit.assert_not_called()


def test_update_category_does_not_change_name_when_name_is_none(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category = CategoryORM(id="category-1", name="Старая категория")
    category_repository_mock.get_by_id.return_value = category
    expected_name = "Старая категория"
    result = category_service.update_category("category-1", CategoryUpdate(name=None))
    category_repository_mock.get_by_id.assert_called_once_with("category-1")
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }
    db_mock.commit.assert_called_once_with()


def test_delete_category_deletes_category_and_commits(
    category_service: CategoryService, db_mock: Mock, category_repository_mock: Mock
) -> None:
    category = CategoryORM(id="category-1", name="Категория для удаления")
    category_repository_mock.get_by_id.return_value = category
    category_service.delete_category(category.id)

    category_repository_mock.get_by_id.assert_called_once_with(category.id)

    category_repository_mock.delete.assert_called_once_with(category)
    db_mock.commit.assert_called_once_with()


def test_delete_category_raises_when_task_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFoundError):
        category_service.delete_category("missing-category")

    db_mock.commit.assert_not_called()
