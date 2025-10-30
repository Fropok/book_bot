from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models.user import User
from database.connection import MyDatabase
from lexicon.lexicon import LEXICON_RU
from keyboards.user_keyboards import UserKeyboard
from service.service import get_user_and_book

router = Router()


@router.message(Command(commands='start'))
async def command_start(message: Message, db: MyDatabase):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    book = db.load_book()

    if str(user_id) not in db.load():
        db.update(User(id=user_id, name=user_name))

    await message.answer(
        text=LEXICON_RU['/start'].format(
            name=user_name,
            title=book.title,
            author=book.author
        )
    )


@router.message(Command(commands='beginning'))
async def command_beginning(message: Message, db: MyDatabase):
    user_id = message.from_user.id
    user, book = get_user_and_book(user_id, db)

    user.last_page = 1
    db.update(user)

    page_text = book.get_page_text(page_number=user.last_page)

    await message.answer(text=page_text,
                         reply_markup=UserKeyboard.pagination(user=user, book=book))


@router.message(Command(commands='continue'))
async def command_continue(message: Message, db: MyDatabase):
    user_id = message.from_user.id
    user, book = get_user_and_book(user_id, db)

    page_text = book.get_page_text(page_number=user.last_page)

    await message.answer(text=page_text,
                         reply_markup=UserKeyboard.pagination(user=user, book=book))


@router.message(Command(commands='bookmarks'))
async def command_bookmarks(message: Message, db: MyDatabase):
    user_id = message.from_user.id
    user, book = get_user_and_book(user_id, db)

    if user.bookmarks:
        await message.answer(
            text=LEXICON_RU['/bookmarks']['yes'],
            reply_markup=UserKeyboard.bookmarks(user=user, book=book)
        )
        return

    await message.answer(text=LEXICON_RU['/bookmarks']['no'])


@router.message(Command(commands='help'))
async def command_help(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
