from googletrans import Translator
import unicodedata


def translated_slugify(word):
    translator = Translator()
    translation = translator.translate(word, src='ru', dest='en')
    tag_slug = translation.text
    if ' ' in tag_slug:
        tag_slug = tag_slug.replace(' ', '-').lower()
    return tag_slug
