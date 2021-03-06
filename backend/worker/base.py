from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .app import app
from backend.config import get_db_conn_str


class BaseDbTask(app.Task):
    abstract = True
    _db_session = None

    def after_return(self, *args, **kwargs):
        if self._db_session is not None:
            self._db_session.remove()

    @property
    def db(self):
        if self._db_session is None:
            engine = create_engine(get_db_conn_str())
            self._db_session = scoped_session(sessionmaker(bind=engine))
        return self._db_session
