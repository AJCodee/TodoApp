from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from database import Base, sessionmaker
from main import app
from routers.todos import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_override[get_db] = override_get_db

# Havent needed to add .. before any of my imports as it has been finding the files. 
# However, If i start getting import issues then I need to refactor to do ..main instead of just main.