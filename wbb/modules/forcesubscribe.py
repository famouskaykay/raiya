import logging
import time

from pyrogram import Client, filters
from wbb.core.decorators.errors import capture_err
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.bad_request_400 import (
    ChannelPrivate,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)

from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from wbb import app
from wbb import BOT_ID


logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)
# module on progress




__HELP__ = """
<b>ForceSubscribe:</b>
- xkaykay can mute members who are not subscribed your channel until they subscribe
- When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them
<b>Setup</b>
1) First of all add me in the group as admin with ban users permission and in the channel as admin.
Note: Only creator of the group can setup me and i will not allow force subscribe again if not done so.
 
<b>Commmands</b>
 - /forcesubscribe - To get the current settings.
 - /forcesubscribe no/off/disable - To turn of ForceSubscribe.
 - /forcesubscribe {channel username} - To turn on and setup the channel.
 - /forcesubscribe clear - To unmute all members who muted by me.
Note: /forcesub is an alias of /forcesubscribe
 
"""
__MODULE__ = "Force Subscribe "
