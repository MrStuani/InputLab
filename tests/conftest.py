import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401  (registra as tabelas)
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = settings.database_url.rsplit("/", 1)[0] + "/inputlab_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSession = sessionmaker(bind=engine, autoflush=False)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()