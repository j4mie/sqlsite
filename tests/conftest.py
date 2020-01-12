from .utils import create_route_table
from sqlsite.database import install_row_factory

import apsw
import pytest


@pytest.fixture
def db():
    db = apsw.Connection(":memory:")
    install_row_factory(db)
    create_route_table(db)
    return db
