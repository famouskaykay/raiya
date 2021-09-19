import logging
import time
import asyncio
import string
import random
from telethon.utils import get_display_name
import re
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

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


async def get_user_join(id):
    ok = True
    try:
        await app(GetParticipantRequest(channel=channel, participant=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok

@app.on(events.ChatAction())
async def _(event):
    if on_join is False:
        return
    if event.user_joined or event.user_added:
        user = await event.get_user()
        chat = await event.get_chat()
        title = chat.title if chat.title else "this chat"
        pp = await app.get_participants(chat)
        count = len(pp)
        mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
        name = user.first_name
        last = user.last_name
        if last:
            fullname = f"{name} {last}"
        else:
            fullname = name
        uu = user.username
        if uu:
            username = f"@{uu}"
        else:
            username = mention
        x = await get_user_join(user.id)
        if x is True:
            msg = welcome_msg.format(mention=mention, title=title, fullname=fullname, username=username, name=name, last=last, channel=f"@{channel}")
            butt = [Button.url("Channel", url=f"https://t.me/{channel}")]
        else:
            msg = welcome_not_joined.format(mention=mention, title=title, fullname=fullname, username=username, name=name, last=last, channel=f"@{channel}")
            butt = [Button.url("Channel", url=f"https://t.me/{channel}"), Button.inline("UnMute Me", data=f"unmute_{user.id}")]
            await app.edit_permissions(event.chat.id, user.id, until_date=None, send_messages=False)
        
        await event.reply(msg, buttons=butt)


@app.on(events.NewMessage(incoming=True))
async def mute_on_msg(event):
    if event.is_private:
        return
    if on_new_msg is False:
        return
    x = await get_user_join(event.sender_id)
    temp = await app(GetFullUserRequest(event.sender_id))
    if x is False:
        if temp.user.bot:
            return
        nm = temp.user.first_name
        try:
            await BotzHub.edit_permissions(event.chat.id, event.sender_id, until_date=None, send_messages=False)
        except Exception as e:
            print(str(e))
            return
        await event.reply(f"Hey {nm}, seems like you haven't joined our channel. Please join @{channel} and then press the button below to unmute yourself!", buttons=[[Button.url("Channel", url=f"https://t.me/{channel}")], [Button.inline("UnMute Me", data=f"unmute_{event.sender_id}")]])


@app.on(events.callbackquery.CallbackQuery(data=re.compile(b"unmute_(.*)")))
async def _(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if uid == event.sender_id:
        x = await get_user_join(uid)
        nm = (await app(GetFullUserRequest(uid))).user.first_name
        if x is False:
            await event.answer(f"You haven't joined @{channel} yet!", cache_time=0, alert=True)
        elif x is True:
            try:
                await app.edit_permissions(event.chat.id, uid, until_date=None, send_messages=True)
            except Exception as e:
                print(str(e))
                return
            msg = f"Welcome to {(await event.get_chat()).title}, {nm}!\nGood to see you here!"
            butt = [Button.url("Channel", url=f"https://t.me/{channel}")]
            await event.edit(msg, buttons=butt)
    else:
        await event.answer("You are an old member and can speak freely! This isn't for you!", cache_time=0, alert=True)

print("ForceSub Bot has started.\nDo visit @BotzHub!")
app.run_until_disconnected()

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
