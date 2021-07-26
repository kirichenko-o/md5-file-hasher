from pathlib import Path
from datetime import datetime
import fcntl


class FileLogWriter:
    def __init__(self, file_path, file_name):
        path = Path(file_path)
        path.mkdir(parents=True, exist_ok=True)
        self._file_name = path / file_name
        Path(self._file_name).touch()

    def log(self, message):
        with open(self._file_name, 'a') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            s = "[{date:%Y-%m-%d %H:%M:%S}] {msg}\n".format(date=datetime.now(), msg=message)
            file.write(s)
