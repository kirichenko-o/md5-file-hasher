import os
from pathlib import Path
from dotenv import load_dotenv

# Possible it's not a good solution to use .env that way,
# but this is a quick way to make settings easier to use.
# In "real life" I would use a different solution.

load_dotenv(Path(__file__).resolve().parent / ".." / ".env")

conf = os.environ


def get_db_conn_str(driver=None):
    return 'postgresql{driver}://{user}:{password}@{host}:{port}/{db_name}'.format(
        driver="+" + driver if driver else "",
        user=conf.get('DB_USER'),
        password=conf.get('DB_PASSWORD'),
        host=conf.get('DB_HOST'),
        port=conf.get('DB_PORT'),
        db_name=conf.get('DB_NAME')
    )
