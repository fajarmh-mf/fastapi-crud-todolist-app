from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "mysql+mysqlconnector://myuser:myuserpassword@localhost:3306/my_database"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)