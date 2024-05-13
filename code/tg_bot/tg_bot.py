from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from Config import TG_API_TOKEN

# Dictionary to store user data
user_data = {}

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! You can create sets of words using this bot.")
    show_menu(update, context)

def show_menu(update: Update, context: CallbackContext) -> None:
    """Show the menu options."""
    user_id = update.effective_user.id
    menu_text = "Choose an option:\n"
    menu_text += "/new_set - Create a new set\n"
    menu_text += "/add_words - Add words to an existing set\n"
    menu_text += "/show_sets - Show your sets of words\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text)

def new_set(update: Update, context: CallbackContext) -> None:
    """Create a new set."""
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=update.effective_chat.id, text="Enter a name for the new set:")
    context.user_data['set_name'] = None
    context.user_data['set_words'] = []
    context.user_data['set_mode'] = 'new'

def add_words(update: Update, context: CallbackContext) -> None:
    """Add words to an existing set."""
    user_id = update.effective_user.id
    user_sets = user_data[user_id]
    if not user_sets:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have any sets yet. Create a new set first.")
        return

    set_names = list(user_sets.keys())
    menu_text = "Select a set to add words to:\n"
    for i, set_name in enumerate(set_names):
        menu_text += f"{i+1}. {set_name}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text)
    context.user_data['set_mode'] = 'add'

def show_sets(update: Update, context: CallbackContext) -> None:
    """Show the user's sets of words."""
    user_id = update.effective_user.id
    user_sets = user_data[user_id]
    if not user_sets:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have any sets yet.")
        return

    message_text = "Your sets of words:\n"
    for set_name, words in user_sets.items():
        message_text += f"{set_name}: {', '.join(words)}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

def input_handler(update: Update, context: CallbackContext) -> None:
    """Handle user input."""
    user_id = update.effective_user.id
    user_input = update.message.text

    if context.user_data.get('set_mode') == 'new':
        if context.user_data['set_name'] is None:
            context.user_data['set_name'] = user_input
            user_data[user_id][user_input] = []
            context.bot.send_message(chat_id=update.effective_chat.id, text="Enter words for the new set (one word per line, send '/done' when finished):")
        else:
            if user_input == '/done':
                show_menu(update, context)
            else:
                context.user_data['set_words'].append(user_input)
                user_data[user_id][context.user_data['set_name']] = context.user_data['set_words']
    elif context.user_data.get('set_mode') == 'add':
        try:
            set_index = int(user_input) - 1
            set_name = list(user_data[user_id].keys())[set_index]
            context.user_data['set_name'] = set_name
            context.user_data['set_words'] = user_data[user_id][set_name]
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Enter words to add to the set '{set_name}' (one word per line, send '/done' when finished):")
        except (ValueError, IndexError):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid choice. Please try again.")
            add_words(update, context)
    else:
        show_menu(update, context)

def main() -> None:
    """Start the bot."""
    # Replace YOUR_TOKEN with your actual Telegram bot token
    updater = Updater(TG_API_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("new_set", new_set))
    dispatcher.add_handler(CommandHandler("add_words", add_words))
    dispatcher.add_handler(CommandHandler("show_sets", show_sets))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, input_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()