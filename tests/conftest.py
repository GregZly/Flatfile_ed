import os 
#import tempfile

import pytest

from flatfileed import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'CSV_PATH': "C:\\Users\\grzes\\Desktop\\python_dev\\pet_projects\\flatfile_ed\\tests\\test_test.csv",
        'CSV_NAME': "test_test.csv"
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
