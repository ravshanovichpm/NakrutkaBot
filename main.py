import logging
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from keyboards.defaults.default_for_user import socials
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards.defaults.instagram import instagram_paket
from instagpy import InstaGPy
#.env import
from dotenv import load_dotenv
# Set up logging
logging.basicConfig(level=logging.INFO)
from keyboards.inlines.accses import true_false, follow_button, like_button, view_button, comment_button, \
    payment_button, tolov_tasdiqlash

load_dotenv()
import os
ADMIN = os.getenv("ADMIN_ID")
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

son = {
    "user_id": 0
}
user_instagram = {
    "user_id_telegram": "user_name_instagram"
}


class Shogirdchalar(StatesGroup):
    Socials_button_state = State()
    Instagram_state = State()
    YouTube_state = State()
    TikTok_state = State()
    Telegram_state = State()
    username_insta_state = State()
    url_like_state = State()
    views_state = State()
    comment_state = State()
    file_state = State()
    admin_state = State()
    full_acsess = State()
    not_full_acsess = State()

@dp.message_handler(commands='admin')
async def admin(message: types.Message, state: FSMContext):
    await message.answer("Admin parolini kiriting")
    await Shogirdchalar.admin_state.set()


@dp.message_handler(state=Shogirdchalar.admin_state)
async def admin(message: types.Message, state: FSMContext):
    if message.text == "admin1":
        await message.answer("Siz State da siz")
        await Shogirdchalar.full_acsess.set()
@dp.message_handler(commands='start')
async def for_start(message: types.Message, state: FSMContext):
    son[message.from_user.id] = 0
    await message.answer(message.from_user.id)
    await message.answer(f"Assalomu Aleykum <code>{message.from_user.full_name}</code>", reply_markup=socials)
    await Shogirdchalar.Socials_button_state.set()


@dp.message_handler(text="Instagram📱", state=Shogirdchalar.Socials_button_state)
async def insta_logging(message: Message, state: FSMContext):
    await message.answer("Siz Instagram Bo`limini Tanladingiz\n\nTariflardan birini tanlang",
                         reply_markup=instagram_paket)
    await state.finish()
    await Shogirdchalar.Instagram_state.set()


@dp.message_handler(state=Shogirdchalar.Instagram_state, text="Followers👤")
async def followers(message: Message, state: FSMContext):
    await message.answer("Username Kiriting")
    await state.finish()
    await Shogirdchalar.username_insta_state.set()


@dp.message_handler(state=Shogirdchalar.username_insta_state)
async def username(message: Message, state: FSMContext):
    user = message.text
    insta = InstaGPy(use_mutiple_account=False, session_ids=None, min_requests=None, max_requests=None)
    txt = insta.get_user_basic_details(f'{user}')
    print(txt)
    user_instagram[f'{message.from_user.id}'] = txt["username"]
    await message.answer(f"""
Username: {txt["username"]}

Full Name : {txt["full_name"]}

Private : {txt["is_private"]}


<b>Sizning akkauntingizligiga ishonchingiz komilmi?</b>
    """, reply_markup=true_false)


# -----------------------FOLLOW_________________________________________________________


@dp.callback_query_handler(text='ha', state=Shogirdchalar.username_insta_state)
async def followers(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    photo = 'https://img.freepik.com/premium-vector/100k-social-media-followers-design_54625-114.jpg?w=2000'
    await call.message.answer_photo(photo, reply_markup=follow_button, caption="Follow👥")
    await state.finish()


@dp.callback_query_handler(text='plus_follow')
async def plus_follow(call: types.CallbackQuery):
    global son
    son[call.message.chat.id] += 1000
    fake_son = son[call.message.chat.id]
    print(fake_son)
    if fake_son >= 0:
        await update_snecks_follow_button(call.message.chat.id, call.message.message_id, fake_son)
    else:
        await call.answer('Eng kam miqdor 1000 ta')


async def update_snecks_follow_button(chat_id, message_id, new_son):
    follow_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('-1000👤', callback_data='minus_follow'),
                InlineKeyboardButton(f'{new_son}', callback_data='0'),
                InlineKeyboardButton('+1000👤', callback_data='plus_follow')
            ],
            [
                InlineKeyboardButton('Tasdiqlash✅', callback_data='follow_tasdiqlash')
            ]
        ])

    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=follow_button)


@dp.callback_query_handler(text='minus_follow')
async def minus_follow(call: types.CallbackQuery, state: FSMContext):
    global son
    print(True)
    if son[call.message.chat.id] <= 0:
        await call.answer('Eng kam miqdor 1000 ta')
    else:

        son[call.message.chat.id] -= 1000
        fake_son = son[call.message.chat.id]
        print(fake_son)
        if fake_son >= 0:
            await update_snecks_minus_follow_button1(call.message.chat.id, call.message.message_id, fake_son)
        else:
            await call.answer('Eng kam miqdor 1000 ta')


async def update_snecks_minus_follow_button1(chat_id, message_id, new_son):
    minus_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('-1000👤', callback_data='minus_follow'),
                InlineKeyboardButton(f'{new_son}', callback_data='0'),
                InlineKeyboardButton('+1000👤', callback_data='plus_follow')
            ],
            [
                InlineKeyboardButton('Tasdiqlash✅', callback_data='follow_tasdiqlash')
            ]
        ])

    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=minus_button)


@dp.callback_query_handler(text='follow_tasdiqlash')
async def tasdiq_followers(call: types.CallbackQuery):
    instagram_nomi = user_instagram[f"{call.message.chat.id}"]
    await bot.send_message(ADMIN,
                           f"Yangi Zakaz keldi\nBuyurtmachi: {call.from_user.username}\nTanlov Turi: Obunachi\nSoni: {son[call.message.chat.id]}\nInstagram: https://instagram.com/{instagram_nomi}")
    await call.message.answer("To`lov turini tanlang!", reply_markup=payment_button)


# _____________________________________FOWLLOW_END_____________________________


# --------------------------------------LIKE-----------------------------------


@dp.message_handler(state=Shogirdchalar.Instagram_state, text="Likes❤️")
async def likes(message: Message, state: FSMContext):
    await message.answer("Url kiriting")
    await state.finish()
    await Shogirdchalar.url_like_state.set()


@dp.message_handler(state=Shogirdchalar.url_like_state, content_types=types.ContentType.TEXT)
async def likes(message: Message, state: FSMContext):
    url = message.text
    user_instagram[str(message.from_user.id)] = url

    if url.startswith("https://www.instagram.com"):
        link = "https://avatars.mds.yandex.net/i?id=a21ba0b3957dd0573d399a4891039d13207de203-10139706-images-thumbs&n=13"
        await message.answer_photo(link, caption="Like sonini tanlang", reply_markup=like_button)
        await state.finish()
    #
    else:
        await message.answer("Tentak")


# gi
@dp.callback_query_handler(text='like-')
async def minus_like(call: types.CallbackQuery, state: FSMContext):
    async def update_snecks_minus_like_button1(chat_id, message_id, new_son):
        like_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='-1000 ❤️', callback_data='like-'),
                    InlineKeyboardButton(text=f'{son[call.message.chat.id]}', callback_data='like_true'),
                    InlineKeyboardButton(text='+1000 ❤️', callback_data='like+'),

                ],
                [
                    InlineKeyboardButton(text='Tasdiqlash✅', callback_data='like_tasdiqlash')
                ]
            ],
            resize_keyboard=True,
        )

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=like_button)

    global son
    print(True)
    if son[call.message.chat.id] <= 0:
        await call.answer('Eng kam miqdor 1000 ta')
    else:

        son[call.message.chat.id] -= 1000
        fake_son = son[call.message.chat.id]
        print(fake_son)
        if fake_son >= 0:
            await update_snecks_minus_like_button1(call.message.chat.id, call.message.message_id, fake_son)
        else:
            await call.answer('Eng kam miqdor 1000 ta')


@dp.callback_query_handler(text='like+')
async def plus_like(call: types.CallbackQuery):
    async def update_snecks_minus_like_button1(chat_id, message_id, new_son):
        like_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='-1000 ❤️', callback_data='like-'),
                    InlineKeyboardButton(text=f'{son[call.message.chat.id]}', callback_data='like_true'),
                    InlineKeyboardButton(text='+1000 ❤️', callback_data='like+'),

                ],
                [
                    InlineKeyboardButton(text='Tasdiqlash✅', callback_data='like_tasdiqlash')
                ]
            ],
            resize_keyboard=True,
        )

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=like_button)

    global son
    son[call.message.chat.id] += 1000
    fake_son = son[call.message.chat.id]
    print(fake_son)
    if fake_son >= 0:
        await update_snecks_minus_like_button1(call.message.chat.id, call.message.message_id, fake_son)
    else:
        await call.answer('Eng kam miqdor 1000 ta')


@dp.callback_query_handler(text='like_tasdiqlash')
async def tasdiq_likes(call: types.CallbackQuery):
    instagram_nomi = user_instagram[str(call.message.chat.id)]
    await bot.send_message(ADMIN,
                           f"Yangi Zakaz keldi\nBuyurtmachi: {call.from_user.username}\nTanlov Turi: Like\nSoni: {son[call.message.chat.id]}\nInstagram: {instagram_nomi}")
    await call.message.answer("To`lov turini tanlang!", reply_markup=payment_button)


# -------------------------LIKE_end-------------------------------------


# --------------------------VIEWS----------------------------------------


@dp.message_handler(state=Shogirdchalar.Instagram_state, text="Views👁️")
async def views(message: Message, state: FSMContext):
    await message.answer("Url kiriting")
    await state.finish()
    await Shogirdchalar.views_state.set()


# fgfg
@dp.message_handler(state=Shogirdchalar.views_state, content_types=types.ContentType.TEXT)
async def views(message: Message, state: FSMContext):
    url = message.text
    user_instagram[str(message.from_user.id)] = url
    if url.startswith("https://www.instagram.com"):
        link = "https://yt3.googleusercontent.com/VJAWgMbfJ-umoqgiPIh8Zq2R1ZUm2IuGaT75GBY0OHFLrk0nKhR-pt8DrNotRAjk49Qhor0t=s900-c-k-c0x00ffffff-no-rj"
        await message.answer_photo(link, caption="Prasmotr sonini tanlang", reply_markup=view_button)
        await state.finish()
    else:
        await message.answer("Tentak")


@dp.callback_query_handler(text='view-')
async def minus_view(call: types.CallbackQuery, state: FSMContext):
    async def update_snecks_minus_view_button1(chat_id, message_id, new_son):
        view_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='-1000 👁️', callback_data='view-'),
                    InlineKeyboardButton(text=f'{son[call.message.chat.id]}', callback_data='view_true'),
                    InlineKeyboardButton(text='+1000 👁️', callback_data='view+'),

                ],
                [
                    InlineKeyboardButton(text='Tasdiqlash✅', callback_data='view_tasdiqlash')
                ]
            ],
            resize_keyboard=True,
        )

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=view_button)

    global son
    print(True)
    if son[call.message.chat.id] <= 0:
        await call.answer('Eng kam miqdor 1000 ta')
    else:

        son[call.message.chat.id] -= 1000
        fake_son = son[call.message.chat.id]
        print(fake_son)
        if fake_son >= 0:
            await update_snecks_minus_view_button1(call.message.chat.id, call.message.message_id, fake_son)
        else:
            await call.answer('Eng kam miqdor 1000 ta')


@dp.callback_query_handler(text='view+')
async def plus_view(call: types.CallbackQuery):
    async def update_snecks_minus_view_button1(chat_id, message_id, new_son):
        view_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='-1000 👁️', callback_data='view-'),
                    InlineKeyboardButton(text=f'{son[call.message.chat.id]}', callback_data='view_true'),
                    InlineKeyboardButton(text='+1000 👁️', callback_data='view+'),

                ],
                [
                    InlineKeyboardButton(text='Tasdiqlash✅', callback_data='view_tasdiqlash')
                ]
            ],
            resize_keyboard=True,
        )

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=view_button)

    global son
    son[call.message.chat.id] += 1000
    fake_son = son[call.message.chat.id]
    print(fake_son)
    if fake_son >= 0:
        await update_snecks_minus_view_button1(call.message.chat.id, call.message.message_id, fake_son)
    else:
        await call.answer('Eng kam miqdor 1000 ta')

@dp.callback_query_handler(text='view_tasdiqlash')
async def tasdiq_view(call: types.CallbackQuery):
    instagram_nomi = user_instagram[f"{call.message.chat.id}"]
    await bot.send_message(ADMIN,
                           f"Yangi Zakaz keldi\nBuyurtmachi: {call.from_user.username}\nTanlov Turi: View\nSoni: {son[call.message.chat.id]}\nInstagram: {instagram_nomi}")
    await call.message.answer("To`lov turini tanlang!", reply_markup=payment_button)


# ------------------------------------------VIEW_end-------------------------------------------------------


# ------------------------------------------COMMENT----------------------------------------------------------


@dp.message_handler(state=Shogirdchalar.Instagram_state, text="Comments💬")
async def comments(message: Message, state: FSMContext):
    await message.answer("Url kiriting")
    await state.finish()
    await Shogirdchalar.comment_state.set()


@dp.message_handler(state=Shogirdchalar.comment_state, content_types=types.ContentType.TEXT)
async def comments(message: Message, state: FSMContext):
    url = message.text
    user_instagram[str(message.from_user.id)] = url
    if url.startswith("https://www.instagram.com"):
        link = "https://lh3.googleusercontent.com/eZ95Z-mlPgDczM1CgYwafA6IYAmbD1FPhr8BXOBxEEzB7h5nfPWOeyKqCjABSpMuLVyHnLxRHd_NJQfrUvOTgnuBbalMOYzY88J96uQ7GJspdK1f7od-VCQHe2bw3-Kgi4OvkaY"
        await message.answer_photo(link, caption="Kamentariya sonini tanlang", reply_markup=comment_button)
        await state.finish()
    else:
        await message.answer("Mol faxim")


@dp.callback_query_handler(text='comment-')
async def minus_comment(call: types.CallbackQuery, state: FSMContext):
    async def update_snecks_minus_comment_button1(chat_id, message_id, new_son):
        comment_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='-1000 💬', callback_data='comment-'),
                    InlineKeyboardButton(text=f'{son[call.message.chat.id]}', callback_data='comment_true'),
                    InlineKeyboardButton(text='+1000 💬', callback_data='comment+'),

                ],
                [
                    InlineKeyboardButton(text='Tasdiqlash✅', callback_data='comment_tasdiqlash')
                ]
            ],
            resize_keyboard=True,
        )

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=comment_button)

    global son
    print(True)
    if son[call.message.chat.id] <= 0:
        await call.answer('Eng kam miqdor 1000 ta')
    else:

        son[call.message.chat.id] -= 1000
        fake_son = son[call.message.chat.id]
        print(fake_son)
        if fake_son >= 0:
            await update_snecks_minus_comment_button1(call.message.chat.id, call.message.message_id, fake_son)
        else:
            await call.answer('Eng kam miqdor 1000 ta')

#
@dp.callback_query_handler(text='comment+')
async def plus_comment(call: types.CallbackQuery):
    async def update_snecks_minus_comment_button1(chat_id, message_id, new_son):
        comment_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='-1000 💬', callback_data='comment-'),
                    InlineKeyboardButton(text=f'{son[call.message.chat.id]}', callback_data='comment_true'),
                    InlineKeyboardButton(text='+1000 💬', callback_data='comment+'),

                ],
                [
                    InlineKeyboardButton(text='Tasdiqlash✅', callback_data='comment_tasdiqlash')
                ]
            ],
            resize_keyboard=True,
        )

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=comment_button)

    global son
    son[call.message.chat.id] += 1000
    fake_son = son[call.message.chat.id]
    print(fake_son)
    if fake_son >= 0:
        await update_snecks_minus_comment_button1(call.message.chat.id, call.message.message_id, fake_son)
    else:
        await call.answer('Eng kam miqdor 1000 ta')

@dp.callback_query_handler(text='comment_tasdiqlash')
async def tasdiq_comment(call: types.CallbackQuery):
    instagram_nomi = user_instagram[f"{call.message.chat.id}"]
    await bot.send_message(ADMIN,
                           f"Yangi Zakaz keldi\nBuyurtmachi: {call.from_user.username}\nTanlov Turi: Comment\nSoni: {son[call.message.chat.id]}\nInstagram:{instagram_nomi}")
    await call.message.answer("To`lov turini tanlang!", reply_markup=payment_button)


@dp.callback_query_handler(text="Click")
async def click(call: types.CallbackQuery, state: FSMContext):
    narx = son[call.message.chat.id]
    await call.message.answer(
        f"""Bu karta raqamiga <b>{int(son[call.message.chat.id])*15}</b> so'm tashlang\n💳Karta raqam: <code>3452872164901084</code>""")
    await call.message.answer("To`lov Chekini Tashlang")
    await Shogirdchalar.file_state.set()


@dp.callback_query_handler(text="Payme")
async def payme(call: types.CallbackQuery, state: FSMContext):
    narx = son[call.message.chat.id]
    await call.message.answer(
        f"""Bu karta raqamiga {son[call.message.chat.id]}so'm tashlang:  <code>3452872164901084</code>""")
    await call.message.answer("To`lov Chekini Tashlang")
    await Shogirdchalar.file_state.set()

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

@dp.message_handler(state=Shogirdchalar.file_state, content_types=types.ContentTypes.PHOTO)
async def check_send_to_admin(message: Message, state: FSMContext):
    file = message.photo
    tolamoqchi.append(message.from_user.id)
    print(file[0])
    await bot.send_photo(ADMIN, file[0]['file_id'],caption= f"User id si {message.from_user.id}", reply_markup=tolov_tasdiqlash)
    #add button for addmin list of tolamoqchi
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(tolamoqchi)):
        button.add(str(tolamoqchi[i]))
    await bot.send_message(ADMIN, "Tolamoqchi listi", reply_markup=button)
    await state.finish()
#tolamoqchi bolganlarni hammasini bir joga yog`ish kerak
tolamoqchi = []

@dp.callback_query_handler(text='Tolandi')
async def tolov(call: types.CallbackQuery):
    await call.message.answer("Tolov muvaffaqiyatli amalga oshirildi")


@dp.callback_query_handler(text='Tolanmadi')
async def tolov_tasdiqlanmadi(call: types.CallbackQuery):
    await call.message.answer("Tolov muvaffaqiyatli amalga oshirilmadi")


@dp.message_handler(state=Shogirdchalar.full_acsess)
async def admin(message: Message):
    await message.answer("Siz Tolandi State da siz")
    if message.text == "tolanmadi":
        await Shogirdchalar.not_full_acsess.set()
    id = message.text
    await bot.send_message(id,"Sizning to`lovingiz tasdiqlandi yaqin orada buyurtmangiz amalga oshiriladi tel: +998 99 999 99 99")

@dp.message_handler(state=Shogirdchalar.not_full_acsess)
async def admin(message: Message):
    await message.answer("Siz Tolanmadi State da siz")
    if message.text == "tolandi":
        await Shogirdchalar.full_acsess.set()
    id = message.text
    await bot.send_message(id,"Sizning to`lovingiz tasdiqlanmadi!")
#
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
