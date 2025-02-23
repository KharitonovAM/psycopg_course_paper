from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LOG_FILE = Path(BASE_DIR, 'logging', 'log_file.txt')
DATA_FILENAME = Path(BASE_DIR, 'data', 'datafile.json')
