from collections.abc import Sequence
from unittest.mock import Mock

import pytest

from app.models.task import TaskORM
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task import TaskNotFoundError, TaskService


def test_list_task_returns_pydantic_models(
    task_service: TaskService,
    task_repository_mock: Mock,
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    tasks: Sequence[TaskORM] = [
        TaskORM(id="task-1", title="Изучить pytest", completed=False),
        TaskORM(id="task-2", title="Написать первый тест", completed=True),
    ]
    task_repository_mock.get_all.return_value = tasks

    result = task_service.list_tasks()

    assert result == [
        TaskRead(id="task-1", title="Изучить pytest", completed=False),
        TaskRead(id="task-2", title="Написать первый тест", completed=True),
    ]


def test_create_task_commits_created_task(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
) -> None:
    created_task = TaskORM(id="task-1", title="Новая задача", completed=False)
    task_repository_mock.create.return_value = created_task

    result = task_service.create_task(TaskCreate(title="Новая задача"))

    task_repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": "Новая задача",
        "completed": False,
    }


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(
            TaskUpdate(title="Обновить заголовок"),  # payload
            "Обновить заголовок",  # expected_title
            False,  # expected_completed
        ),
        pytest.param(
            TaskUpdate(completed=True),  # payload
            "Старая задача",  # expected_title
            True,  # expected_completed
        ),
        pytest.param(
            TaskUpdate(title="Готово", completed=True),  # payload
            "Готово",  # expected_title
            True,  # expected_completed
        ),
    ],
)
def test_update_task_updates_only_passed_fields(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
    payload: TaskUpdate,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(id="task-1", title="Старая задача", completed=False)
    task_repository_mock.get_by_id.return_value = task

    result = task_service.update_task("task-1", payload)

    task_repository_mock.get_by_id.assert_called_once_with("task-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "task-1",
        "title": expected_title,
        "completed": expected_completed,
    }


def test_update_task_raises_when_task_not_found(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
) -> None:
    task_repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):  # Должна произойти указанная ошибка
        task_service.update_task("missing-task", TaskUpdate(title="Неважно"))

    db_mock.commit.assert_not_called()


def test_delete_task_deletes_task_and_commits(
    task_service: TaskService, db_mock: Mock, task_repository_mock: Mock
) -> None:
    # Создаем задачу, которую должен вернуть
    # моковый репозиторий после выполнения get_by_id
    task = TaskORM(id="task-1", title="Задача для удаления", completed=True)
    task_repository_mock.get_by_id.return_value = task  # Задаем задачу
    task_service.delete_task(task.id)
    task_repository_mock.get_by_id.assert_called_once_with(task.id)
    # тут обращается к repository_mock.get_by_id, выполняет
    # self.repository.delete(task)
    # self.db.commit()
    # Поэтому проверяем что mock_repository.delete
    # был вызван один раз и db.mock.commit()
    task_repository_mock.delete.assert_called_once_with(task)
    db_mock.commit.assert_called_once_with()


def test_delete_task_raises_when_task_not_found(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
) -> None:
    task_repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFoundError):
        task_service.delete_task("missing-task")

    db_mock.commit.assert_not_called()
