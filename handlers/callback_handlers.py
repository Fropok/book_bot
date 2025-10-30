from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.connection import MyDatabase
from keyboards.callbacks import Callbacks
from keyboards.user_keyboards import UserKeyboard
from lexicon.lexicon import LEXICON_RU
from service.service import get_user_and_book
from service.service_handlers import ServiceHandler

router = Router()


# Листает страницу назад
@router.callback_query(F.data == Callbacks.BACK)
async def press_back(callback: CallbackQuery, db: MyDatabase):
    user_id = callback.from_user.id
    user, book = get_user_and_book(user_id, db)

    if user.last_page == 1:
        await callback.answer(text=LEXICON_RU['cb_back'])
        return

    user.last_page -= 1
    db.update(user)

    page_text = book.get_page_text(page_number=user.last_page)

    await callback.message.edit_text(
        text=page_text,
        reply_markup=UserKeyboard.pagination(user=user, book=book))


# Сохраняет в закладки страницу
@router.callback_query(F.data == Callbacks.CURRENT)
async def press_current(callback: CallbackQuery, db: MyDatabase):
    user_id = callback.from_user.id
    user = db.get_user(user_id)

    if user.last_page in user.bookmarks:
        await callback.answer(
            text=LEXICON_RU['cb_current']['no_add'].format(current_page=user.last_page)
        )
        return

    user.bookmarks.append(user.last_page)
    db.update(user)

    await callback.answer(
        text=LEXICON_RU['cb_current']['add'].format(current_page=user.last_page)
    )


# Листает страницу вперед
@router.callback_query(F.data == Callbacks.NEXT)
async def press_next(callback: CallbackQuery, db: MyDatabase):
    user_id = callback.from_user.id
    user, book = get_user_and_book(user_id, db)

    if user.last_page == book.pages_count:
        await callback.answer(text=LEXICON_RU['cb_next'])
        return

    user.last_page += 1
    db.update(user)

    page_text = book.get_page_text(page_number=user.last_page)

    await callback.message.edit_text(
        text=page_text,
        reply_markup=UserKeyboard.pagination(user=user, book=book))


# Перелистывает на закладку
@router.callback_query(F.data.startswith('page:'))
async def press_page(callback: CallbackQuery, db: MyDatabase):
    user_id = callback.from_user.id
    user, book = get_user_and_book(user_id, db)

    page_number = ServiceHandler.get_int_page_callback(callback_data=callback.data)
    page_text = book.get_page_text(page_number=page_number)

    user.last_page = page_number
    db.update(user)

    await callback.message.edit_text(
        text=page_text,
        reply_markup=UserKeyboard.pagination(user=user, book=book)
    )


# Режим редактирования закладок
@router.callback_query(F.data == Callbacks.EDIT)
async def press_edit(callback: CallbackQuery, db: MyDatabase):
    user_id = callback.from_user.id
    user, book = get_user_and_book(user_id, db)

    await callback.message.edit_text(
        text=LEXICON_RU['cb_edit'],
        reply_markup=UserKeyboard.bookmarks_edit(user=user, book=book)
    )


# Режим удаления закладок
@router.callback_query(F.data.startswith('page_del:'))
async def press_page_del(callback: CallbackQuery, db: MyDatabase):
    user_id = callback.from_user.id
    user, book = get_user_and_book(user_id, db)

    page_number = ServiceHandler.get_int_page_callback(callback_data=callback.data)

    user.del_bookmark(page_number)
    db.update(user)

    await callback.answer(
        text=LEXICON_RU['cb_page_del'].format(page_number=page_number)
    )

    if db.get_user(user.id).bookmarks:
        await callback.message.edit_text(
            text=LEXICON_RU['cb_edit'],
            reply_markup=UserKeyboard.bookmarks_edit(user=user, book=book)
        )
        return

    await callback.message.edit_text(text=LEXICON_RU['/bookmarks']['no'])


# Отменяет редактирование
@router.callback_query(F.data == Callbacks.CANCEL)
async def press_cancel(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU['cb_cancel'])
