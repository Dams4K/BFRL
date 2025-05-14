import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from utils.references import References

engine = create_engine(os.path.join("sqlite:///", References.FOLDER_DATAS, "datas.db"))
session = Session(engine)