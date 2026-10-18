from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from .config import settings
from sqlalchemy.engine import URL

## SQLALCHEMY_DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=int(settings.database_port),
    database=settings.database_name,
)

engine=create_engine(SQLALCHEMY_DATABASE_URL,
                     pool_pre_ping=True,
                     connect_args={"sslmode":settings.database_sslmode},
                     )

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                             password='password',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print('Database successfully connected')    
#         break
#     except Exception as error:
#         print("connecting to database failed!")
#         print("error: ",error)
#         time.sleep(3)


