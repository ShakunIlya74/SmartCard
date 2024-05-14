import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Config import TG_API_TOKEN


import asyncio

from aiogram import Bot, Dispatcher, types, Router, html
from aiogram.filters import CommandStart, Command

from user_utils.user_utils import select_existing_sets, insert_set, get_user_info, create_user, create_card, \
    get_set_cards, get_random_card, get_card_translation_and_examples_representation_preview, \
    format_translations_and_contexts, get_display_card_dict_string, remove_translation, remove_context_example

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
dp = Dispatcher()
user_router = Router()

# TODO: add settings to change languages
class Form(StatesGroup):
    input_set = State()
    main_menu = State()
    # word actions
    input_word = State()
    edit_card = State()
    # set actions
    set_actions_menu = State()
    set_display = State()
    learning_mode = State()
    random_original_mode = State()
    random_translation_mode = State()


WELCOME_TEXT = "Welcome to the Word Set Bot! Use the buttons below to create a new set, add words to your sets, display your sets or learn words from your sets."

@user_router.message(CommandStart())
@dp.message(Command('start'))
async def on_start(msg: types.Message, state: FSMContext) -> None:
    """Process the command `start`"""
    reply_text = f"Hello, {html.bold(msg.from_user.first_name)}. \n"  + WELCOME_TEXT
    main_buttons = main_menu_msg_buttons()
    # setup user
    user_info = get_user_info(msg.from_user.id)
    print(msg.from_user.id, user_info)
    if not user_info:
        create_user(msg.from_user.id, msg.from_user.first_name)
    await state.set_state(Form.main_menu)
    await state.update_data(user_id=msg.from_user.id)
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

def back_to_set_menu_buttons(): # -> InlineKeyboardMarkup:
    back_to_set_actions = InlineKeyboardButton(text="⬅️", callback_data="back_to_set_menu")
    main_buttons_menu = InlineKeyboardBuilder([[back_to_set_actions]])
    return main_buttons_menu

def learning_modes_buttons(): # -> InlineKeyboardMarkup:
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back_to_set_menu")
    random_original = InlineKeyboardButton(text="Random original", callback_data="random_original")
    random_translation = InlineKeyboardButton(text="Random translation", callback_data="random_translation")
    # todo: add more learning modes
    main_buttons_menu = InlineKeyboardBuilder([[b_back], [random_original], [random_translation]])
    return main_buttons_menu

def random_original_mode_buttons(add_translation=True): # -> InlineKeyboardMarkup:
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back_to_set_menu")
    b_show_translation = InlineKeyboardButton(text="Show translation", callback_data="show_translation")
    b_next = InlineKeyboardButton(text="Next", callback_data="next_random_original")
    if not add_translation:
        main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_next]])
    else:
        main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_show_translation],[b_next]])
    return main_buttons_menu

def random_translation_mode_buttons(add_translation=True): # -> InlineKeyboardMarkup:
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back_to_set_menu")
    b_show_translation = InlineKeyboardButton(text="Show word", callback_data="show_word_card")
    b_next = InlineKeyboardButton(text="Next", callback_data="next_random_translation")
    if not add_translation:
        main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_next]])
    else:
        main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_show_translation],[b_next]])
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


def set_menu_buttons_with_card_edit():
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back")
    b_edit_card = InlineKeyboardButton(text="Edit added card", callback_data="edit_card")
    b_add_word = InlineKeyboardButton(text="Add word", callback_data="add_word")
    b_display_set = InlineKeyboardButton(text="Display set", callback_data="display_set")
    b_learn_set = InlineKeyboardButton(text="Learn set", callback_data="learn_set")

    main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_edit_card], [b_add_word], [b_display_set], [b_learn_set]])
    return main_buttons_menu

def edit_card_buttons():
    b_back = InlineKeyboardButton(text="⬅️", callback_data="back_to_set_menu")
    b_rm_1_translation = InlineKeyboardButton(text="Remove 1st translation", callback_data="rm_translation 1")
    b_rm_1_context = InlineKeyboardButton(text="Remove 1st context", callback_data="rm_context 1")
    b_rm_2_translation = InlineKeyboardButton(text="Remove 2nd translation", callback_data="rm_translation 2")
    b_rm_2_context = InlineKeyboardButton(text="Remove 2nd context", callback_data="rm_context 2")
    b_rm_3_translation = InlineKeyboardButton(text="Remove 3rd translation", callback_data="rm_translation 3")
    b_rm_3_context = InlineKeyboardButton(text="Remove 3rd context", callback_data="rm_context 3")
    main_buttons_menu = InlineKeyboardBuilder([[b_back], [b_rm_1_translation], [b_rm_1_context], [b_rm_2_translation], [b_rm_2_context], [b_rm_3_translation], [b_rm_3_context]])
    main_buttons_menu.adjust(1,2,2,2)
    return main_buttons_menu

@user_router.message(Form.main_menu)
@dp.callback_query()
async def on_button_click(call: types.CallbackQuery, state: FSMContext) -> None:
    """Process the button click"""
    user_id = call.from_user.id
    data = await state.get_data()
    set_name = data.get("current_set")
    if call.data == "select_set":
        # await call.message.answer("Select set")
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
        await state.update_data(current_set=call.data[9:])
        await state.set_state(Form.set_actions_menu)
        await call.message.edit_text(f"Your selection: {call.data[9:]} what do you want to do now?", reply_markup=set_menu_buttons().as_markup())
    elif call.data == "add_word":
        await state.set_state(Form.input_word)
        await call.message.edit_text("Enter the word you want to add to the set:", reply_markup=back_to_set_menu_buttons().as_markup())
    elif call.data == "edit_card":
        await state.set_state(Form.edit_card)
        await process_edit_card(call.message, state)
    elif call.data == "display_set":
        await call.message.edit_text(f"Displaying set: {set_name}\n {get_set_display_string(user_id, set_name)}",
                                     reply_markup=back_to_set_menu_buttons().as_markup())
    elif call.data == "back_to_set_menu":
        await state.set_state(Form.set_actions_menu)
        await call.message.edit_text(f"Your selection: {set_name} what do you want to do now?", reply_markup=set_menu_buttons().as_markup())
    elif call.data == "learn_set":
        await state.set_state(Form.learning_mode)
        await call.message.edit_text(f"Select a learning mode: {set_name}", reply_markup=learning_modes_buttons().as_markup())

    # call for learning modes
    if call.data == "random_original":
        await call.message.edit_text(f"Random original: words will be displayed as you added them. Try to remember the translation and came up with a proper usage in context",
                                     reply_markup=random_original_mode_buttons(False).as_markup())
    elif call.data == "next_random_original":
        print("Next random original")
        await state.update_data(random_original_action="next")
        await state.set_state(Form.random_original_mode)
        await random_original(call.message, state, user_id)
    elif call.data == "show_translation":
        await state.update_data(random_original_action="show_translation")
        await state.set_state(Form.random_original_mode)
        await random_original(call.message, state, user_id)
    elif call.data == "random_translation":
        await call.message.edit_text(f"Random translation: you will see a translation. Try to remember the original word and came up with a proper usage in context",
                                     reply_markup=random_translation_mode_buttons(False).as_markup())
    elif call.data == "next_random_translation":
        print("Next random translation")
        await state.update_data(random_translation_action="next")
        await state.set_state(Form.random_translation_mode)
        await random_translation(call.message, state, user_id)
    elif call.data == "show_word_card":
        await state.update_data(random_translation_action="show_word_card")
        await state.set_state(Form.random_translation_mode)
        await random_translation(call.message, state, user_id)

    # calls for card editing
    if call.data.startswith("rm_translation"):
        print("Removing translation")
        await process_edit_card(call.message, state, rm_translation_index=int(call.data.split()[-1]))
    elif call.data.startswith("rm_context"):
        print("Removing context")
        await process_edit_card(call.message, state, rm_context_index=int(call.data.split()[-1]))
    # elif call.data == "back_to_set_menu":
        # await state.set_state(Form.set_actions_menu)
        # await call.message.edit_text(f"Your selection: {set_name} what do you want to do now?", reply_markup=set_menu_buttons().as_markup())



@user_router.message(Form.input_set)
async def process_new_set(message: types.Message, state: FSMContext):
    set_name = message.text
    insert_set( message.from_user.id, set_name)
    print(f"Set name: {set_name}")
    await state.update_data(current_set=message.text)
    await state.set_state(Form.main_menu)
    await message.answer(f"{set_name} added to your sets.", reply_markup= main_menu_msg_buttons().as_markup())


@user_router.message(Form.input_word)
async def process_new_word(message: types.Message, state: FSMContext):
    new_word = message.text
    data = await state.get_data()
    set_name = data.get("current_set")
    print(f"Adding {new_word}: {set_name}")
    card_id = create_card(user_id=message.from_user.id, phrase=new_word, set_name=set_name)
    card = get_card_translation_and_examples_representation_preview(card_id, return_pure_dicts=True)
    display_string = get_display_card_dict_string(card)
    await state.update_data(current_card_id=card_id)
    await message.answer(f"{new_word} added to {set_name}. Card preview:\n\n {display_string}",
                         reply_markup=set_menu_buttons_with_card_edit().as_markup())


@user_router.message(Form.edit_card)
async def process_edit_card(message: types.Message, state: FSMContext, rm_translation_index=None, rm_context_index=None):
    data = await state.get_data()
    card_id = data.get("current_card_id")
    if rm_translation_index:
        print(f"Removing translation {rm_translation_index}")
        remove_translation(card_id, rm_translation_index)
    if rm_context_index:
        print(f"Removing context {rm_context_index}")
        remove_context_example(card_id, rm_context_index)
    card = get_card_translation_and_examples_representation_preview(card_id, return_pure_dicts=True)
    display_string = get_display_card_dict_string(card)
    await message.edit_text(f"🛠 Editing {display_string}", reply_markup=edit_card_buttons().as_markup())



def get_set_display_string(user_id, set_name, mode="word_list"):
    set_cards = get_set_cards(user_id=user_id, set_name=set_name)
    display_string = "\n"
    if mode == "word_list":
        for i, card in enumerate(set_cards):
            display_string += f"{i+1}. {card['phrase']}\n"
    return display_string


@user_router.message(Form.random_original_mode)
async def random_original(message: types.Message, state: FSMContext, user_id: int):
    print("Random original mode")
    data = await state.get_data()
    set_name = data.get("current_set")
    if data.get("random_original_action") == "next":
        print('Next')
        # get random card from the set
        print(f"Getting random card from {set_name}")
        card = get_random_card(user_id, set_name)
        spoiler_translation = f"{html.spoiler(card['translations_dicts'][0]['translation'])}"
        await state.update_data(current_card_id=card['card_id'])
        await message.answer(f"{html.bold(card['phrase'])}\n\n{spoiler_translation}", reply_markup=random_original_mode_buttons().as_markup())
    elif data.get("random_original_action") == "show_translation":
        print("translation")
        card = get_card_translation_and_examples_representation_preview(data.get("current_card_id"), return_pure_dicts=True)
        display_string = get_display_card_dict_string(card)
        await message.edit_text(display_string, reply_markup=random_original_mode_buttons().as_markup())


@user_router.message(Form.random_translation_mode)
async def random_translation(message: types.Message, state: FSMContext, user_id: int):
    print("Random translation mode")
    data = await state.get_data()
    set_name = data.get("current_set")
    if data.get("random_translation_action") == "next":
        print('Next')
        # get random card from the set
        print(f"Getting random card from {set_name}")
        card = get_random_card(user_id, set_name)
        spoiler_word = f"{html.spoiler(card['phrase'])}"
        await state.update_data(current_card_id=card['card_id'])
        # todo: show random translation from the top3 translations
        await message.answer(f"{html.bold(card['translations_dicts'][0]['translation'])}\n\n{spoiler_word}",
                             reply_markup=random_translation_mode_buttons().as_markup())
    elif data.get("random_translation_action") == "show_word_card":
        print("show word card")
        card = get_card_translation_and_examples_representation_preview(data.get("current_card_id"), return_pure_dicts=True)
        display_string = get_display_card_dict_string(card)
        await message.edit_text(display_string, reply_markup=random_translation_mode_buttons().as_markup())







async def main() -> None:
    """Entry Point"""
    logging.info("Starting the bot...")
    bot = Bot(
        token=TG_API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())