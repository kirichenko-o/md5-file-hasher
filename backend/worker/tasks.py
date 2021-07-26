import hashlib
import os

from .app import app
from .base import BaseDbTask
from .logger import FileLogWriter
from backend.db.schema import FileInfo
from backend.config import conf

# Size of chunks for reading file
CHUNK_SIZE = 4096


def calculate_md5_hash(file):
    h = hashlib.md5()
    with open(file, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            h.update(chunk)
    return h.hexdigest()


@app.task(base=BaseDbTask, bind=True)
def calculate_md5_hash_task(self, id):
    """
    Task for computation mdf hesh

    :param self: BaseDbTask
    :param id: int, identifier of FileInfo record
    :return:
    """
    logger = None
    try:
        logger = FileLogWriter(conf.get("WORKER_LOG_PATH"), conf.get("WORKER_LOG_FILE"))

        file_info = self.db.query(FileInfo).get(id)
        if file_info is None:
            raise Exception("FileInfo record not found")

        result = calculate_md5_hash(file_info.file_name)

        os.remove(file_info.file_name)

        file_info.md5_hash = result
        file_info.file_name = None  # Clear the field because the file has been deleted already
        self.db.commit()

        logger.log(f"Task {id}: SUCCESS Result: {result}")

        return {"hesh": result}
    except Exception as ex:
        if logger is not None:
            logger.log(f"Task {id}: ERROR {ex}")
        raise
