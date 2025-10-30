from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    last_page: int = 1
    bookmarks: list[int] = Field(default_factory=list)

    def del_bookmark(self, page_number: int) -> None:
        if page_number in self.bookmarks:
            self.bookmarks.remove(page_number)