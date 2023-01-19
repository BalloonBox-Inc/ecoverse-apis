'''This module manages the creation and insertion of initial data to the database.'''

from config import get_settings
from database import crud, models, session
from security.hashing import SecureHash


settings = get_settings()
ADMIN_MASTER = models.AdminsTable(
    username=settings.ADMIN.USERNAME,
    hashed_password=SecureHash.create(settings.ADMIN.PASSWORD),
    is_active=True
)


def start_database():
    '''Create and start the database.'''

    # initiate the database session
    models.Base.metadata.create_all(bind=session.engine)

    # setup admin
    try:
        db = session.SessionLocal()
        crud.create_object(db=db, object=ADMIN_MASTER)
    except Exception as e:  # noqa: F841 pylint: disable=[W0612,W0703]
        pass
    finally:
        db.close()
