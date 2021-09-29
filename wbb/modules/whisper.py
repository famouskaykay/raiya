#copy right @aspirer2 2021
from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os
from wbb import app

db = {}

@app.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await app.get_me()).username
    dn = event.builder.article(
            title="It's a whisper!",
            description="It's a whisper!\n(c) @KayAspirerProject",
            text=f"**I can a whisper messages**\n`@{me} wspr UserID|Message`\n**(c) @KayAspirerProject**",
            buttons=[
                [Button.switch_inline(" Go Inline ", query="wspr ")]
                ]
            )
    await event.answer([dn])
    
@app.on(events.InlineQuery(pattern="wspr"))
async def inline(event):
    me = (await app.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Give a message too!",
                switch_pm_param="start"
                )
    try:
        ui = await app(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="Invalid User ID/Username",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
A Whisper Has Been Sent
To [{ui.user.first_name}](tg://user?id={ui.user.id})!
Click The Below Button To See The Message!
**Note:** __Only {ui.user.first_name} can open this!__
    """
    dn = event.builder.article(
            title="Its a secret message! Sssh",
            description="It's a secret message! Sssh!",
            text=text,
            buttons=[
                [Button.inline(" Show Message! ", data="wspr")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="It's a secret message! Sssh",
            switch_pm_param="start"
            )


@app.on(events.CallbackQuery(data="wspr"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 This message is not for you!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Oops!\nIt's looks like message got deleted from my server!", alert=True)
        return
    await event.answer(msg, alert=True)
