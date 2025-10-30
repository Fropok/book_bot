from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.book import Book


class ServiceKeyboard:

    @staticmethod
    def create_keyboard(buttons: list[InlineKeyboardButton], width: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(*buttons, width=width)
        return builder.as_markup()

    @staticmethod
    def bookmarks_text(number_page: int, length_text: int, format_text: str, book: Book) -> str:
        page_text = book.get_page_text(number_page)
        text = page_text[:length_text] if len(page_text) > length_text else page_text
        return format_text.format(number_page=number_page, text=text)
