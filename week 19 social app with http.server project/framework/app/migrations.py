from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite://social-media.db", echo= True)
if __name__ =="__main__":
    Base.metadata.create_all(engine)