import os
from pathlib import Path
from dotenv import load_dotenv

# Possible it's not a good solution to use .env that way,
# but this is a quick way to make settings easier to use
# In "real life" I would use a different solution
load_dotenv(Path(__file__).resolve().parent / ".." / ".env")

conf = os.environ
