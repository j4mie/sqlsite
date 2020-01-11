from .utils import create_sqlar_file
from sqlsite.sqlar import get_data, get_row


def test_get_data(db):
    create_sqlar_file(db, "hello.txt", b"hello")
    row = get_row(db, "hello.txt")
    data = get_data(db, row)
    assert data == b"hello"
