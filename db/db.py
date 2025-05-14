import os

from sqlalchemy import create_engine

from utils.references import References

engine = create_engine(os.path.join("sqlite:///", References.FOLDER_DATAS, "data.db"))