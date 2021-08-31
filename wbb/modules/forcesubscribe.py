import logging
import time

from pyrogram import filters
from wbb.core.decorators.errors import capture_err
from pyrogram.errors import RPCError
rom pyrogram.errors.exceptions.bad_request_400 import (
    ChannelPrivate,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)

from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from wbb import app
from wbb import BOT_ID
from wbb.utils.filter_groups import

__MODULE__ = "forcesubscribe"
__HELP__ = """
<b>Commmands</b>
 - /forcesubscribe - To get the current settings.
 - /forcesubscribe no/off/disable - To turn of ForceSubscribe.
 - /forcesubscribe {channel username} - To turn on and setup the channel.
 - /forcesubscribe clear - To unmute all members who muted by me.
Note: /forcesub is an alias of /forcesubscribe
 
"""

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)
# module on progress

