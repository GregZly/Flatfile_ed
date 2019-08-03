from pathlib import Path

#Name of used file
CSV_NAME = "test.csv"

#Path to folder
local_path = Path.cwd()

#Path to used locally CSV FILE
CSV_PATH = local_path / CSV_NAME

#test
SECRET_KEY = 'DEVEVE'

#Backup directory
BACKUP_DIR = local_path / "backup"