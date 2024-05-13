import logging

from aiogram.dispatcher import router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Config import TG_API_TOKEN


import asyncio

from aiogram import Bot, Dispatcher, types, Router, html
from aiogram.filters import CommandStart, Command

from aiogram.utils.markdown import hbold

from user_utils.user_utils import select_existing_sets, insert_set, get_user_info, create_user, create_card

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
dp = Dispatcher()
user_router = Router()

# TODO: add settings to change languages
class Form(StatesGroup):
    input_set = State()
    input_word = State()
    main_menu = State()
    set_actions_menu = State()

WELCOME_TEXT = "Welcome to the Word Set Bot! Use the buttons below to create a new set, add words to your sets, display your sets or learn words from your sets."

@user_router.message(CommandStart())
@dp.message(Command('start'))
async def on_start(msg: types.Message, state: FSMContext) -> None:
    """Process the command `start`"""
    reply_text = f"Hello, {msg.from_user.first_name}. \n"  + WELCOME_TEXT #html.bold(msg.from_user.first_name)
    main_buttons = main_menu_msg_buttons()
    # setup user
    user_info = get_user_info(msg.from_user.id)
    if not user_info:
        create_user(msg.from_user.id, msg.from_user.first_name)
    await state.set_state(Form.main_menu)
    await msg.answer(
        text=reply_text, reply_markup=main_buttons.as_markup()
    )


def main_menu_msg_buttons(): # -> InlineKeyboardMarkup:
    b_select_set = InlineKeyboardButton(text="Select set", callback_data="select_set")
    b_create_set = InlineKeyboardButton(text="Create set", callback_data="create_set")
    main_buttons_menu = InlineKeyboardBuilder([[b_select_set], [b_create_set]])
    main_buttons_menu.adjust(2)
    return main_buttons_menu


def back_to_menu_buttons(): # -> InlineKeyboardMarkup:
    back = InlineKeyboardButton(text="⬅️", callback_data="back")
    main_buttons_menu = InlineKeyboardBuilder([[back]])
    return main_buttons_menu


def set_buttons(user_id): # -> InlineKeyboardMarkup:
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back")
    sets = select_existing_sets(user_id)
    buttons = [[InlineKeyboardButton(text=set_name, callback_data='set_menu:'+set_name)] for set_name in sets]
    list_of_all_buttons = [[b_back], *buttons]
    main_buttons_menu = InlineKeyboardBuilder(list_of_all_buttons)
    # print(sets, list_of_all_buttons)
    return main_buttons_menu


def set_menu_buttons():
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back")
    b_add_word = InlineKeyboardButton(text="Add word", callback_data="add_word")
    b_display_set = InlineKeyboardButton(text="Display set", callback_data="display_set")
    b_learn_set = InlineKeyboardButton(text="Learn set", callback_data="learn_set")
    main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_add_word], [b_display_set], [b_learn_set]])
    return main_buttons_menu


@user_router.message(Form.main_menu)
@dp.callback_query()
async def on_button_click(call: types.CallbackQuery, state: FSMContext) -> None:
    """Process the button click"""
    if call.data == "select_set":
        # await call.message.answer("Select set")
        user_id = call.from_user.id
        print(f"Select sets for user: {user_id}")
        await call.message.edit_text("Your sets:", reply_markup=set_buttons(user_id).as_markup())
    elif call.data == "create_set":
        print("Create set")
        await state.set_state(Form.input_set)
        await call.message.edit_text("Enter the name for your new set:", reply_markup=back_to_menu_buttons().as_markup())
    elif call.data == "back":
        await state.set_state(Form.main_menu)
        await call.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_msg_buttons().as_markup())
    elif call.data.startswith("set_menu"):
        print("Set menu")
        data = await state.update_data(current_set=call.data[9:])
        await state.set_state(Form.set_actions_menu)
        await call.message.edit_text(f"Set {call.data[9:]}.", reply_markup=set_menu_buttons().as_markup())
    elif call.data == "add_word":
        await state.set_state(Form.input_word)
        await call.message.edit_text("Enter the word you want to add to the set:", reply_markup=back_to_menu_buttons().as_markup())


@user_router.message(Form.input_set)
async def process_new_set(message: types.Message, state: FSMContext):
    set_name = message.text
    insert_set( message.from_user.id, set_name)
    print(f"Set name: {set_name}")
    await state.update_data(current_set=message.text)
    await state.set_state(Form.main_menu)
    await message.reply(f"{set_name} added to your sets.", reply_markup= main_menu_msg_buttons().as_markup())


@user_router.message(Form.input_word)
async def process_new_word(message: types.Message, state: FSMContext):
    new_word = message.text
    data = await state.get_data()
    set_name = data.get("current_set")
    print(f"Adding {new_word}: {set_name}")
    create_card(user_id=message.from_user.id, phrase=new_word, set_name=set_name)
    await state.set_state(Form.input_word)
    await message.reply(f"{new_word} added to {set_name}.", reply_markup=set_menu_buttons().as_markup())




async def main() -> None:
    """Entry Point"""
    logging.info("Starting the bot...")
    bot = Bot(
        token=TG_API_TOKEN,
    )
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

    # Importing required libraries
    # from aiogram import Bot, Dispatcher, types
    # from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    # from aiogram.dispatcher import executor
    #
    #
    # # Put the token that you received from BotFather in the quotes
    # bot = Bot(token=TG_API_TOKEN)
    #
    # # Initializing the dispatcher object
    # dp = Dispatcher(bot)
    #
    # # Defining and adding buttons
    # button1 = InlineKeyboardButton(text="button1", callback_data="In_First_button")
    # button2 = InlineKeyboardButton(
    #     text="button2", callback_data="In_Second_button")
    # keyboard_inline = InlineKeyboardMarkup().add(button1, button2)

    # Message handler for the /button1 command

    # @dp.message_handler(commands=['start'])
    # async def check(message: types.Message):
    #     await message.reply("hi! how are you", reply_markup=keyboard_inline)
    #
    #
    # # Callback query handler for the inline keyboard buttons
    #
    #
    # @dp.callback_query_handler(text=["In_First_button", "In_Second_button"])
    # async def check_button(call: types.CallbackQuery):
    #     # Checking which button is pressed and respond accordingly
    #     if call.data == "In_First_button":
    #         await call.message.answer("Hi! This is the first inline keyboard button.")
    #     if call.data == "In_Second_button":
    #         await call.message.answer("Hi! This is the second inline keyboard button.")
    #         # Notify the Telegram server that the callback query is answered successfully
    #     await call.answer()