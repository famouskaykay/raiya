import logging
import time

from pyrogram import Client
from wbb.core.decorators.errors import capture_err
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from pyrogram import filters
from wbb.utils.filter_groups import chatbot_group

from pyrogram.types import (Chat, ChatPermissions,
                            InlineKeyboardButton,
                            InlineKeyboardMarkup, Message, User)
from wbb import SUDOERS

from wbb import app
from wbb import BOT_ID
from wbb import db
import time



__HELP__ = """
<b>ForceSubscribe:</b>
- xkaykay can mute members who are not subscribed your channel until they subscribe
- When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them
<b>Setup</b>
1) First of all add me in the group as admin with ban users permission and in the channel as admin.
Note: Only creator of the group can setup me and i will not allow force subscribe again if not done so.
 
<b>Commmands</b>
 - /forcesubscribe - To get the current settings.
Note: /forcesub is an alias of /forcesubscribe
 
"""
__MODULE__ = "Force Subscribe "
