from pyrogram import filters
from pyrogram.types import Message

from wbb import BOT_ID, SUDOERS, USERBOT_PREFIX, app2
from wbb.core.decorators.errors import capture_err
from wbb.modules.userbot import edit_or_reply
from wbb.utils.dbfunctions import add_sudo, get_sudoers, remove_sudo
from wbb.utils.functions import restart

__MODULE__ = "Sudo"
__HELP__ = """
**MODULI HII NI KWA AJILI YA DEVELOPERS TU**

.useradd - Kuongeza Mtumiaji Katika Sudoers.
.userdel - Kutoa Mtumiaji Katika Sudoers
.sudoers - Kuorodhesha Watumiaji wa Sudo.

**NOTE:**

Wala msiongezee mwenye kufuru, isipo kuwa kwa kuamini.
watumiaji wa sudo wanaweza kufanya chochote na akaunti yako,
inaweza hata kufuta akaunti yako.
"""


@app2.on_message(
    filters.command("useradd", prefixes=USERBOT_PREFIX)
    & filters.user(SUDOERS)
)
@capture_err
async def useradd(_, message: Message):
    if not message.reply_to_message:
        return await edit_or_reply(
            message,
            text="Jibu ujumbe wa mtu wa kumongeza kwa sudoer.",
        )
    user_id = message.reply_to_message.from_user.id
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await edit_or_reply(
            message, text="Mtumiaji tayari yuko katika sudoer."
        )
    if user_id == BOT_ID:
        return await edit_or_reply(
            message, text="Huwezi kuongeza bot msaidizi katika sudoers."
        )
    added = await add_sudo(user_id)
    if added:
        await edit_or_reply(
            message,
            text="Imefanikiwa kuongeza mtumiaji katika sudoers, Bot itaanzishwa upya sasa.",
        )
        return await restart(None)
    await edit_or_reply(
        message, text="Kitu kibaya kilitokea, angalia logs."
    )


@app2.on_message(
    filters.command("userdel", prefixes=USERBOT_PREFIX)
    & filters.user(SUDOERS)
)
@capture_err
async def userdel(_, message: Message):
    if not message.reply_to_message:
        return await edit_or_reply(
            message,
            text="Jibu ujumbe wa mtu wa kumwondoa kwenye sudoers.",
        )
    user_id = message.reply_to_message.from_user.id
    if user_id not in await get_sudoers():
        return await edit_or_reply(
            message, text="mtumiaji hayuko sudoers."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await edit_or_reply(
            message,
            text="Imefanikiwa kuondolewa mtumiaji kutoka kwa sudoer, Bot itaanzishwa upya sasa.",
        )
        return await restart(None)
    await edit_or_reply(
        message, text="Kitu kibaya kilitokea, angalia logs."
    )


@app2.on_message(
    filters.command("sudoers", prefixes=USERBOT_PREFIX)
    & filters.user(SUDOERS)
)
@capture_err
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = ""
    for count, user_id in enumerate(sudoers, 1):
        user = await app2.get_users(user_id)
        user = user.first_name if not user.mention else user.mention
        text += f"{count}. {user}\n"
    await edit_or_reply(message, text=text)
