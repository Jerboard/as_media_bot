from dotenv import load_dotenv
from os import getenv

import json


load_dotenv ()

DEBUG = bool(int(getenv('DEBUG')))


class config:
    token = getenv('TOKEN')
    tz = 'Europe/Moscow'
    db_url = getenv('DB_URL')
    admins = [524275902, 1456925942, 519861062]
    path = 'temp'
    wait_media_group = 20
