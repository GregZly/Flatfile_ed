import os 
import csv


import pytest

from pathlib import Path

from flatfileed import create_app

#Path to folder
local_path = Path.cwd() / "tests"

#Name of used file
CSV_NAME = "test_test.csv"

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'CSV_PATH': local_path / CSV_NAME,
        'CSV_NAME': CSV_NAME,
        'BACKUP_DIR' : local_path / "backup",
        'CSV_DIALECT' : {'CSV_DELIMITER' : ',',
                         'CSV_QUOTING' : csv.QUOTE_ALL,
                         'CSV_DOUBLEQUOTE' : True,
                         'CSV_COLUMNS' : 3}
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
