import logging
import time

from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
import asyncio
import re
from pyrogram import Client
from wbb.core.decorators.errors import capture_err
from pyrogram.errors import RPCError
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


logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)






__HELP__ = """
*Force Subscribe:*
❍ Yone can mute members who are not subscribed your channel until they subscribe
❍ When enabled I will mute unsubscribed members and show them a unmute button. When they pressed the button I will unmute them
*Setup*
*Only creator*
❍ Add me in your group as admin
❍ Add me in your channel as admin 
 
*Commmands*
 ❍ /fsub {channel username} - To turn on and setup the channel.
  💡Do this first...
 ❍ /fsub - To get the current settings.
 ❍ /fsub disable - To turn of ForceSubscribe..
  💡If you disable fsub, you need to set again for working.. /fsub {channel username} 
 ❍ /fsub clear - To unmute all members who muted by me.
"""
__MODULE__ = "Force Subscribe "
