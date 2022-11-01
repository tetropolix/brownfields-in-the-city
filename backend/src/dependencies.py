from database.database import Session

def get_session():
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()