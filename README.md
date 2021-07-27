# MD5 File Hasher (Test task)

This app allows computing MD5 hash of files in the background using Celery workers.

## Built With

* [FastAPI](https://fastapi.tiangolo.com/): a high performance web framework for building APIs with Python.
* [Celery](https://celeryproject.org/): an asynchronous task queue or job queue which is based on distributed message passing.
* [RabbitMQ](https://www.rabbitmq.com/): a message broker used to route messages between API and the workers from Celery.
* [Redis](https://redis.io/): a database to store results and process status from the tasks.
* [PostgreSQL](https://www.postgresql.org/): an object-relational database to store computed MD5 hash.
* [SqlAlchemy](https://www.sqlalchemy.org/): an object-relational mapper for Python.
* [Alembic](https://alembic.sqlalchemy.org/): a database migrations tool for SQLAlchemy.

## Available Endpoints

### POST /upload

Run task for computation MD5 hash and return identifier of computation request.
Information about file and task will be saved to the database.

**Input**

```
file
```

**Output**
```
{
  "id": 123
}
```

### GET /get_task_info/\<id\>

Return information about file and task by the identifier of a computation request.
If the task is successfully completed the response will also contain the computed hash.

**Input**

```
id
```

**Output**
```
{
    "id": 123,
    "task_state": "SUCCESS",
    "original_file_name": "sample_file.jpg",
    "md5_hash": "e3921603773aa61a1a31e97db61c1453",
    "created_date": "2021-07-23T19:18:05.849634"
}
```

## Install

1. Make sure you have cloned this repository:

```
$ git clone https://github.com/kirichenko-o/md5-file-hasher
```

2. Install [Docker](https://www.docker.com/get-started). To run the docker images prepare your environment variables in the ~/.env file. Then run the command (it should be executed from the project root directory):

```
$ docker-compose up -d --build
```

3. To run multiple workers run the command with the necessary number of workers **\<count\>**:

```
$ docker-compose up -d --build --scale worker=<count>
```

4. Open http://localhost:8080

![img.png](./docs/img.png?raw=true)
