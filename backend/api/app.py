import uuid
from pathlib import Path
from functools import wraps

import aiofiles
from fastapi import FastAPI, HTTPException, status, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.schema import FileInfo
from backend.worker.tasks import calculate_md5_hash_task
from backend.config import conf
from .dependencies import get_db

# Size of chunks for writing file
CHUNK_SIZE = 1024

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=conf.get('ALLOWED_HOSTS', ['*']).split(',')
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=conf.get('ALLOWED_ORIGINS').split(','),
    allow_methods=conf.get('ALLOWED_METHODS').split(','),
    allow_headers=conf.get('ALLOWED_HEADERS').split(',')
)


def get_uniq_value():
    return uuid.uuid4().hex


def process_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
           return await func(*args, **kwargs)
        except Exception as ex:
            if ex.__class__ != HTTPException:
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
            else:
                raise

    return wrapper;


@app.post("/upload", status_code=status.HTTP_201_CREATED)
@process_exceptions
async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    Save file and run task for computation mdf hash
    Information about file and task will be saved to the database

    :param file: UploadFile
    :param db: AsyncSession, database session
    :return: json object with id of new FileInfo record
    """
    # File names can be the same so create a new name
    try:
        suffix = Path(file.filename).suffix
        uniq_file_name = get_uniq_value()
        file_path = Path(conf.get('INPUT_FILES_PATH')) / Path(uniq_file_name).with_suffix(suffix)

        async with aiofiles.open(file_path, 'wb') as buffer:
            while content := await file.read(CHUNK_SIZE):
                await buffer.write(content)
    except Exception as ex:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save file: {str(ex)}")

    file_info = FileInfo(original_file_name=file.filename, file_name=str(file_path))
    db.add(file_info)
    await db.commit()

    res = calculate_md5_hash_task.delay(file_info.id)

    file_info.task_id = res.id
    await db.commit()

    return {"id": file_info.id}


@app.get("/get_task_info/{id}", status_code=status.HTTP_200_OK)
@process_exceptions
async def get_task_info(id: int, db: AsyncSession = Depends(get_db)):
    """
    Return information about task for computation mdf hash
    (result, task state and so on)

    :param id: int, identifier of FileInfo record
    :param db: AsyncSession, database session
    :return: json object with information about file and task
    """
    file_info = await db.get(FileInfo, id)
    if file_info is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="FileInfo record not found")

    task_state = calculate_md5_hash_task.AsyncResult(file_info.task_id).state

    return {
        "id": file_info.id,
        "task_state": task_state,
        "original_file_name": file_info.original_file_name,
        "md5_hash": file_info.md5_hash,
        "created_date": file_info.created_date
    }
