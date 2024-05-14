from reverso_api.context import ReversoContextAPI

# api = ReversoContextAPI(source_text="пример", target_text="", source_lang="ru", target_lang="en")
SUPPORTED_LANGUAGES =  {
    "🇸🇦": "ar",  # Saudi Arabia (Arabic)
    "🇩🇪": "de",  # Germany (German)
    "🇪🇸": "es",  # Spain (Spanish)
    "🇫🇷": "fr",  # France (French)
    "🇮🇱": "he",  # Israel (Hebrew)
    "🇮🇹": "it",  # Italy (Italian)
    "🇯🇵": "ja",  # Japan (Japanese)
    "🇰🇷": "ko",  # South Korea (Korean)
    "🇳🇱": "nl",  # Netherlands (Dutch)
    "🇵🇱": "pl",  # Poland (Polish)
    "🇵🇹": "pt",  # Portugal (Portuguese)
    "🇷🇴": "ro",  # Romania (Romanian)
    "🇷🇺": "ru",  # Russia (Russian)
    "🇸🇪": "sv",  # Sweden (Swedish)
    "🇹🇷": "tr",  # Turkey (Turkish)
    "🇺🇦": "uk",  # Ukraine (Ukrainian)
    "🇨🇳": "zh",  # China (Chinese)
    "🇬🇧": "en"   # United Kingdom (English)
}

SUPPORTED_LANGUAGES_INVERS = {
    "ar": "🇸🇦",  # Arabic (Saudi Arabia)
    "de": "🇩🇪",  # German (Germany)
    "es": "🇪🇸",  # Spanish (Spain)
    "fr": "🇫🇷",  # French (France)
    "he": "🇮🇱",  # Hebrew (Israel)
    "it": "🇮🇹",  # Italian (Italy)
    "ja": "🇯🇵",  # Japanese (Japan)
    "ko": "🇰🇷",  # Korean (South Korea)
    "nl": "🇳🇱",  # Dutch (Netherlands)
    "pl": "🇵🇱",  # Polish (Poland)
    "pt": "🇵🇹",  # Portuguese (Portugal)
    "ro": "🇷🇴",  # Romanian (Romania)
    "ru": "🇷🇺",  # Russian (Russia)
    "sv": "🇸🇪",  # Swedish (Sweden)
    "tr": "🇹🇷",  # Turkish (Turkey)
    "uk": "🇺🇦",  # Ukrainian (Ukraine)
    "zh": "🇨🇳",  # Chinese (China)
    "en": "🇬🇧"   # English (United Kingdom)
}

def get_translations(phrase, l2='de', l1='ru', n=5, API_instance=None, target_text=""):
    if not API_instance:
        API_instance = ReversoContextAPI(source_text=phrase, target_text=target_text, source_lang=l2, target_lang=l1)
    translations = []
    i = 0
    for source_word, translation, frequency, part_of_speech, inflected_forms in API_instance.get_translations():
        translations.append({"source_word": source_word, "translation": translation, "frequency": frequency,
                             "part_of_speech": part_of_speech, "inflected_forms": inflected_forms})
        i += 1
        if i >= n:
            break
    return translations
        # print(source_word, "==", translation)
        # print("Frequency (how many word usage examples contain this word):", frequency)
        # print("Part of speech:", part_of_speech if part_of_speech else "unknown")
        # if inflected_forms:
        #     print("Inflected forms:", end=" ")
        #     print(", ".join(inflected_form.translation for inflected_form in inflected_forms))
        # print()


def get_reverso_examples(phrase, l2='de', l1='ru', n=5, API_instance=None, target_text=""):
    if not API_instance:
        API_instance = ReversoContextAPI(source_text=phrase, target_text=target_text, source_lang=l2, target_lang=l1)
    examples = []
    i = 0
    for source, target in API_instance.get_examples():
        examples.append({"source": source.text, "source_highlighted": source.highlighted, "target": target.text,
                         "target_highlighted": target.highlighted})
        i += 1
        if i >= n:
            break
    return examples
        # print(source.text, source.highlighted, "==", target.text, target.highlighted)

# todo: add bold highlighting to the words in context

if __name__ == '__main__':
    # print(get_translations("hund"))
    print(get_reverso_examples("Hund"))


