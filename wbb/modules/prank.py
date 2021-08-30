#famouskaykay made this

from pyrogram import filters
import random
import asyncio
from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.utils.dbfunctions import prank, prank_count

__MODULE__ = "prank"
__HELP__ = "/prank - To Choose Couple Of The Day"

@app.on_message(filters.command("prank"))
@capture_err
async def prank_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a text message to prank."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Reply to a text message to prank."
        )
    m = await message.reply_text("pranking......")
    prank = await make_carbon(message.reply_to_message.text)
    await m.edit("preparing prank......")
    await m.delete()
    prank.close()


@app(pattern="prank")
@capture_err
async def pprank(ult):
    msg = await eor(ult, "**PROMOTING USER..**")
    await asyncio.sleep(1)
    await msg.edit("**PROMOTING USER...**")
    await asyncio.sleep(1)
    await msg.edit("**GIVING RIGHTS**")
    await asyncio.sleep(1)
    await msg.edit("**PROMOTED USER SUCCESSFULLY**")
