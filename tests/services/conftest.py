"""fixtures for the service layer"""

from unittest.mock import Mock

import pytest

from app.repositories.category import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.category import CategoryService
from app.services.task import TaskService


@pytest.fixture
def task_repository_mock() -> Mock:
    """Создаем мок TaskRepository для каждого теста"""

    return Mock(spec=TaskRepository)


@pytest.fixture
def task_service(db_mock: Mock, task_repository_mock: Mock) -> TaskService:
    """Создаем TaskService на основе моковых service, repository"""
    task_service = TaskService(db_mock)
    task_service.repository = task_repository_mock
    return task_service


@pytest.fixture
def category_repository_mock() -> Mock:
    """Создаем мок CategoryRepository для каждого теста"""

    return Mock(spec=CategoryRepository)


@pytest.fixture
def category_service(db_mock: Mock, category_repository_mock: Mock) -> CategoryService:
    """Создаем CategoryService на основе моковых service, repository"""
    category_service = CategoryService(db_mock)
    category_service.repository = category_repository_mock
    return category_service
