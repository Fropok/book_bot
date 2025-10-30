from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from service.service_keyboards import ServiceKeyboard
from models.book import Book
from models.user import User
from lexicon.lexicon import LEXICON_RU
from keyboards.callbacks import Callbacks


class UserKeyboard:

    @staticmethod
    def pagination(user: User, book: Book) -> InlineKeyboardMarkup:
        current_page = user.last_page
        pages_count = book.pages_count

        btn_back = InlineKeyboardButton(
            text=LEXICON_RU['kb_btn_back'],
            callback_data=Callbacks.BACK
        )

        btn_current = InlineKeyboardButton(
            text=f'{current_page}/{pages_count}',
            callback_data=Callbacks.CURRENT
        )

        btn_next = InlineKeyboardButton(
            text=LEXICON_RU['kb_btn_next'],
            callback_data=Callbacks.NEXT
        )

        return ServiceKeyboard.create_keyboard(
            buttons=[btn_back, btn_current, btn_next],
            width=3
        )

    @staticmethod
    def bookmarks(user: User, book: Book) -> InlineKeyboardMarkup:
        user_bookmarks = user.bookmarks

        buttons = [InlineKeyboardButton(
            text=ServiceKeyboard.bookmarks_text(
                number_page=number_page,
                length_text=20,
                format_text=LEXICON_RU['bookmarks_text'],
                book=book),
            callback_data=f'page:{number_page}') for number_page in user_bookmarks
        ]

        btn_cancel = InlineKeyboardButton(
            text='kb_btn_cancel',
            callback_data=Callbacks.CANCEL)

        btn_edit = InlineKeyboardButton(
            text='kb_btn_edit',
            callback_data=Callbacks.EDIT)

        builder = InlineKeyboardBuilder()
        builder.row(*buttons, width=1)
        builder.row(btn_cancel, btn_edit, width=2)

        return builder.as_markup()

    @staticmethod
    def bookmarks_edit(user: User, book: Book) -> InlineKeyboardMarkup:
        user_bookmarks = user.bookmarks

        buttons = [InlineKeyboardButton(
            text=ServiceKeyboard.bookmarks_text(
                number_page=number_page,
                length_text=15,
                format_text=LEXICON_RU['bookmarks_edit_text'],
                book=book),
            callback_data=f'page_del:{number_page}') for number_page in user_bookmarks
        ]

        btn_cancel = InlineKeyboardButton(
            text='kb_btn_cancel',
            callback_data=Callbacks.CANCEL)

        buttons.append(btn_cancel)

        return ServiceKeyboard.create_keyboard(
            buttons=buttons,
            width=1
        )
