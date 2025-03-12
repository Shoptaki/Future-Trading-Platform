from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ MySQL Connection String (Modify username/password accordingly)
DATABASE_URL = "mysql+mysqlconnector://root:Root%401006@127.0.0.1/trading_platform"

# ✅ Create engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# ✅ User Model (Table)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(100), unique=True, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    api_key = Column(String(255), nullable=True)  # Dummy API Key
    broker = Column(String(50), nullable=True)  # IBKR, Tradeovate, etc.

# ✅ Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
