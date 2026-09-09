import os
import pytest
from page_analyzer import app


os.environ['DATABASE_URL'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/page_analyzer'
)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client