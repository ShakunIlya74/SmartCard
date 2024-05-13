import json

from reverso_api.context import ReversoContextAPI

from research.reversoAPI import get_translations, get_reverso_examples
from sql_utils.database_utils import sql_execute


# ------------------ Backend: helper functions  ------------------

def select_existing_sets(user_id):
    # select all sets for the user
    sets = sql_execute("""
    SELECT set_name
    FROM sets
    WHERE user_id = :user_id
    """, user_id=user_id)
    sets = [set[0] for set in sets]
    return sets

if __name__ == '__main__':
    print(select_existing_sets(297723680))


def insert_set(user_id, set_name):
    # insert a new set for the user
    sql_execute("""
    INSERT INTO sets (set_name, user_id)
    VALUES (:set_name, :user_id)
    """, set_name=set_name, user_id=user_id)


def create_card(user_id, phrase, set_name, translations=None, context_examples=None, n=5):
    # create a new card
    if translations is None and context_examples is None:
        translations, context_examples = prepare_card_for_user(user_id, phrase, n)
        translations = json.dumps(translations)
        context_examples = json.dumps(context_examples)
    card_id = sql_execute("""
    INSERT INTO cards (user_id, phrase, translations, context_examples)
    VALUES (:user_id, :phrase, :translations, :context_examples) RETURNING card_id
    """, user_id=user_id, phrase=phrase, translations=translations, context_examples=context_examples)
    card_id = card_id[0][0]
    sql_execute("""
    INSERT INTO set_content (set_id, card_id, user_id)
    VALUES ((SELECT set_id FROM sets WHERE set_name = :set_name AND user_id = :user_id), :card_id, :user_id)
    """, set_name=set_name, user_id=user_id, card_id=card_id)


def get_user_info(user_id):
    # check if the user is new
    user = sql_execute("""
    SELECT user_name, l1, l2
    FROM users
    WHERE user_id = :user_id
    """, user_id=user_id)
    if not user:
        return None
    return user[0][0], user[0][1], user[0][2]


def create_user(user_id, user_name, l1='ru', l2='de'):
    # create a new user
    sql_execute("""
    INSERT INTO users (user_id, user_name, l1, l2)
    VALUES (:user_id, :user_name, :l1, :l2)
    """, user_id=user_id, user_name=user_name, l1=l1, l2=l2)



# ------------------ User Interface: helper functions  ------------------


def get_card_translation_and_examples_representation_preview(card_id, n=3, return_pure_dicts=False):
    # get translations and context examples for the card
    card = sql_execute("""
    SELECT phrase, translations, context_examples
    FROM cards
    WHERE card_id = :card_id
    """, card_id=card_id)
    phrse, translations, context_examples = card[0]
    translations = json.loads(translations)
    context_examples = json.loads(context_examples)
    if return_pure_dicts:
        return {"phrase": phrse, "translations_dicts": translations, "contexts_dicts": context_examples}
    else:
        translations_str = str([f'{i}. '+translation['translation']+'\n' for i,translation in enumerate(translations[:n])])
        context_examples_str = str([f'{i}. '+example['source']+'\n' for i,example in enumerate(context_examples[:n])])
        context_translations_str = str([f'{i}. '+example['target']+'\n' for i,example in enumerate(context_examples[:n])])
        return {"phrase": phrse, "translations": translations_str, "context_examples":
            context_examples_str, "context_translations": context_translations_str}


def get_set_cards(user_id, set_name):
    # get all cards for the set
    card_ids = sql_execute("""
    SELECT card_id
    FROM set_content
    WHERE set_id = (SELECT set_id FROM sets WHERE set_name = :set_name AND user_id = :user_id)
    """, set_name=set_name, user_id=user_id)
    card_ids = [card[0] for card in card_ids]
    cards = [get_card_translation_and_examples_representation_preview(card_id) for card_id in card_ids]
    return cards


def prepare_card_for_user(user_id, phrase, n=5):
    name, l1, l2 = get_user_info(user_id)
    api = ReversoContextAPI(source_text=phrase, target_text="", source_lang=l2, target_lang=l1)
    translations = get_translations(phrase, l2, l1, n, API_instance=api)
    context_examples = get_reverso_examples(phrase, l2, l1, n, API_instance=api)
    return translations, context_examples


if __name__== '__main__':
    print(select_existing_sets(1))