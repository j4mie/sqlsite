from .utils import create_route_table
from sqlsite.database import connect

import pytest


@pytest.fixture
def db():
    db = connect(":memory:")
    create_route_table(db)
    return db
