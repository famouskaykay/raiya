import logging
import time

from pyrogram import Client
from wbb.Config import Config
from wbb.core.decorators.errors import capture_err
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid
from pyrogram import filters
from wbb.utils.filter_groups import chatbot_group

from pyrogram.types import (Chat, ChatPermissions,
                            InlineKeyboardButton,
                            InlineKeyboardMarkup, Message, User)
from wbb import SUDOERS

from wbb.sql import forceSubscribe_sql as sql
from wbb import app
from wbb import BOT_ID
from wbb import db
import time


@app.on_callback_query(filters.regex("^onButtonPress$"))
def onButtonPress(client, cb):
  user_id = member.id
  chat_id = message.chat.id
  cws = sql.fs_settings(chat_id)
  if cws:
    channel = cws.channel
    if client.get_chat_member(chat_id, user_id).restricted_by.id == (client.get_me()).id:
      try:
        client.get_chat_member(channel, user_id)
        client.unban_chat_member(chat_id, user_id)
      except UserNotParticipant:
        client.answer_callback_query(cb.id, text="ℹ Join The Channel And Press The Button Again.")
    else:
      client.answer_callback_query(cb.id, text="ℹ You Are Muted By Admins For Other Reasons.", show_alert=True)

    

    
@app.on_message(filters.command(["forcesubscribe", "fsub"]) & ~Filters.private)
def kay(client, message):
  if User.status is "creator" or User.user.id in SUDOERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**🔔 Unmuting All Members Who is Muted By Me...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **UnMuted All Members Which Are Muted By Me.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **I Am Not An Admin In This Chat.**\nI Can not Unmute Members Because I Am Not An Admin in This Chat, Make Me.')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **Force Subscribe is Enabled**\nForce Subscribe is Enabled, All The Group Members Have To Subscribe This [channel](https://t.me/{input_str}) in Order To Send Messages In This Group.", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Not An Admin in The Channel**\nI'm Not An Admin in The [channel](https://t.me/{input_str}). Add Me As A Admin In Order To Enable ForceSubscribe.", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Invalid Channel Username.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Force Subscribe is Enabled in This Chat.**\nFor This [Channel](https://t.me/{sql.fs_settings(chat_id).channel})", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force Subscribe is Disabled in This Chat.**")
  else:
      message.reply_text("❗ **Group Creator Required**\nYou Have To Be The Group Creator To Do That.")



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
