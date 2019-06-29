from contextlib import contextmanager
from core import Session
from core import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# @contextmanager
# def session_scope():
#     """Provide a transactional scope around a series of operations."""
#     session = db()
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()

# engine = create_engine('postgresql://scott:tiger@localhost/')
@contextmanager
def dbconnect(func):
    def inner(*args, **kwargs):
        session = db.Session()  # (this is now a scoped session)
        try:
            func(*args, **kwargs) # No need to pass session explicitly
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    return inner