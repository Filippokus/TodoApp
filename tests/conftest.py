from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def db_mock() -> Mock:
    """Создаём mock Session для каждого теста"""
    return Mock(spec=Session)
