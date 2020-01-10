from .utils import create_route_table
from sqlsite.database import connect, install_row_factory

import isort
import pytest


@pytest.fixture
def in_memory_db():
    db = connect(":memory:")
    install_row_factory(db)
    create_route_table(db)
    return db
