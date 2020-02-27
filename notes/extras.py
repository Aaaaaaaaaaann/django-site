import random
import time

from googletrans import Translator
from PIL import Image, ImageFont, ImageDraw

from nfbooknotes.settings import STATIC_ROOT, MEDIA_ROOT


def translate_and_slugify(word):
    translator = Translator()
    translation = translator.translate(word, src='ru', dest='en')
    tag_slug = translation.text.lower()
    if ' ' in tag_slug:
        tag_slug = tag_slug.replace(' ', '-')
    return tag_slug


def make_picture(username):
    picture = Image.new('RGB', (65, 65), (255, 255, 255))
    font = ImageFont.truetype(font=f'{STATIC_ROOT}/fonts/BadScript-Regular.ttf', size=32, encoding='unic')
    draw = ImageDraw.Draw(picture)
    draw.text((21, 0), username[0], font=font, fill=tuple(random.choices(range(256), k=3)))
    picture_name = f'{username.replace(" ", "_").lower()}_{time.time_ns()}.png'
    picture.save(f'{MEDIA_ROOT}/users/' + picture_name)
    return 'users/' + picture_name
