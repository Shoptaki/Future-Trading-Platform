import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from cryptography.fernet import Fernet

# ✅ MySQL Connection String
DATABASE_URL = "mysql+mysqlconnector://root:Root%401006@127.0.0.1/trading_platform"

# ✅ Create engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()

# ✅ Encryption Key (Make sure to store this securely!)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    return fernet.decrypt(encrypted_data.encode()).decode()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    email = Column(String(100), unique=True, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    api_key = Column(String(255), nullable=True)
    broker = Column(String(50), nullable=True)

    # ✅ Relationship with BrokerageAccount
    brokerage_accounts = relationship("BrokerageAccount", back_populates="user")

# ✅ BrokerageAccount Model (NEW)
class BrokerageAccount(Base):
    __tablename__ = "brokerage_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker = Column(String(50), nullable=False)
    account_number = Column(String(100), unique=True, nullable=False)

    user = relationship("User", back_populates="brokerage_accounts")

# ✅ Create tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)
