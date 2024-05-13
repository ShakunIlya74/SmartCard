# from Config import TG_API_TOKEN
#
#
# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
# import logging
#
# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#
# # Dictionary to store user sets
# user_sets = {}
#
# # States
# SELECT_SET, CREATE_SET, SET_SELECTED_ADD_WORD, DISPLAY_SET_CONTENT = range(4)
#
# # Define command handlers
# def start(update, context):
#     user_id = update.message.chat_id
#     logging.info(f"User {user_id} started the conversation.")
#     update.message.reply_text("Welcome to the Word Set Bot! Use the buttons below to create a new set, add words to your sets, display your sets or learn words from your sets.", reply_markup=get_main_keyboard())
#
# def get_main_keyboard():
#     keyboard = [["Create Set"], ["Select set"]]
#     return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
#
# def create_set(update, context):
#     user_id = update.message.chat_id
#     logging.info(f"User {user_id} is creating a new set.")
#     update.message.reply_text("Enter the name for your new set:")
#     return SET_NAME
#
# def set_name(update, context):
#     user_id = update.message.chat_id
#     set_name = update.message.text
#     user_sets.setdefault(user_id, {})[set_name] = []
#     logging.info(f"User {user_id} created a new set named '{set_name}'.")
#     update.message.reply_text(f"Set '{set_name}' created successfully!", ) # reply_markup=get_main_keyboard()
#
# def add_word(update, context):
#     user_id = update.message.chat_id
#     logging.info(f"User {user_id} is adding a word to a set.")
#     sets = user_sets.get(user_id, {})
#     if not sets:
#         update.message.reply_text("You don't have any sets yet. Use the 'Create Set' button to create a new set.")
#         return
#     set_names = list(sets.keys())
#     reply_markup = ReplyKeyboardMarkup([[set_name] for set_name in set_names], one_time_keyboard=True)
#     update.message.reply_text("Choose the set to add the word:", reply_markup=reply_markup)
#     return SET_CHOICE
#
# def set_choice(update, context):
#     user_id = update.message.chat_id
#     chosen_set = update.message.text
#     logging.info(f"User {user_id} chose the set '{chosen_set}'.")
#     update.message.reply_text(f"Enter the word(s) to add to '{chosen_set}':")
#     context.user_data["chosen_set"] = chosen_set
#     return ADD_WORD
#
# def add_word_to_set(update, context):
#     user_id = update.message.chat_id
#     chosen_set = context.user_data.get("chosen_set")
#     word = update.message.text
#     user_sets[user_id][chosen_set].append(word)
#     logging.info(f"User {user_id} added the word '{word}' to the set '{chosen_set}'.")
#     update.message.reply_text(f"'{word}' added to '{chosen_set}' successfully!", )# reply_markup=get_main_keyboard()
#     return ConversationHandler.END
#
# def switch_to_display_set(update, context):
#     user_id = update.message.chat_id
#     logging.info(f"User {user_id} requested to display their sets.")
#     sets = user_sets.get(user_id, {})
#     if not sets:
#         update.message.reply_text("You don't have any sets yet. Use the 'Create Set' button to create a new set.", reply_markup=get_main_keyboard())
#         return
#     buttons = [[set_name] for set_name in sets.keys()]
#     update.message.reply_text("Select a set to display:", reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
#
#
# def display_set(update, context):
#     user_id = update.message.chat_id
#     chosen_set = update.message.text
#     logging.info(f"User {user_id} chose to display the set '{chosen_set}'.")
#     sets = user_sets.get(user_id, {})
#     if chosen_set in sets:
#         update.message.reply_text(f"Words in set '{chosen_set}': {', '.join(sets[chosen_set])}", reply_markup=get_main_keyboard())
#     else:
#         update.message.reply_text("Invalid set selection. Please try again.", reply_markup=get_main_keyboard())
#
# # def cancel(update, context):
# #     user_id = update.message.chat_id
# #     logging.info(f"User {user_id} canceled the operation.")
# #     update.message.reply_text("Operation canceled.", reply_markup=get_main_keyboard())
# #     return ConversationHandler.END
#
#
# def main():
#     updater = Updater(TG_API_TOKEN, use_context=True)
#
#     dp = updater.dispatcher
#
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={
#             # SET_NAME: [MessageHandler(Filters.text & ~Filters.command, set_name)],
#             # ADD_WORD: [MessageHandler(Filters.text & ~Filters.command, add_word_to_set)],
#             # SET_CHOICE: [MessageHandler(Filters.text & ~Filters.command, set_choice)],
#             SELECT_SET: [MessageHandler(Filters.text & ~Filters.command, set_name)],
#             CREATE_SET,
#             ADD_WORD,
#             DISPLAY_SET_CONTENT
#         },
#         # fallbacks=[CommandHandler('cancel', cancel)],
#     )
#
#     dp.add_handler(conv_handler)
#     dp.add_handler(CommandHandler('select_set', switch_to_display_set))
#     dp.add_handler(CommandHandler('create_set', create_set))
#     # dp.add_handler(CommandHandler('add_word', add_word))
#     # dp.add_handler(CommandHandler('display_set', switch_to_display_set))
#     # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, display_set))
#
#     updater.start_polling()
#     updater.idle()
#
# if __name__ == '__main__':
#     main()
#
