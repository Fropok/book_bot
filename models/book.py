from pydantic import BaseModel, Field


class Book(BaseModel):
    title: str
    author: str
    pages: list[str] = Field(default_factory=list)

    @property
    def pages_count(self) -> int:
        return len(self.pages)

    def get_page_text(self, page_number: int) -> str | None:
        page_text = self.pages[page_number - 1] if self.pages else None
        return page_text
