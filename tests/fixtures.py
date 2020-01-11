from .utils import create_route_table
from sqlsite.database import connect

import isort
import pytest


@pytest.fixture
def in_memory_db():
    db = connect(":memory:")
    create_route_table(db)
    return db
