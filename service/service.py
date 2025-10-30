from database.connection import MyDatabase

def get_user_and_book(user_id: int, db: MyDatabase):
    user = db.get_user(user_id)
    book = db.load_book()
    return user, book