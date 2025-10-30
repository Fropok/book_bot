import json
from threading import Lock
from models.book import Book
from models.user import User


class MyDatabase:

    def __init__(self, db_path: str, book_path: str) -> None:
        self.db_path = db_path
        self.book_path = book_path
        self._lock = Lock()

    def load_book(self) -> Book:
        with self._lock:
            with open(self.book_path, 'r', encoding='utf-8') as f:
                book_json = json.load(f)
                book = Book(**book_json)
                return book

    def load(self) -> dict:
        with self._lock:
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

    def save(self, db) -> None:
        with self._lock:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, indent=4)

    def update(self, user: User) -> None:
        db = self.load()
        db[str(user.id)] = user.model_dump()
        self.save(db)

    def get_user(self, user_id: int) -> User:
        db = self.load()
        user = User(**db[str(user_id)])
        return user
