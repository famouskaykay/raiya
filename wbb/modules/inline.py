import traceback
from wbb.data import whispers
from pyrogram import Client, filters, emoji

from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, MessageNotModified
)
from typing import Optional
from wbb import app
from wbb.utils.inlinefuncs import *


from pyrogram.types import (
    User,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery,
    ChosenInlineResult
)

__MODULE__ = "Inline"
__HELP__ = """See inline for help related to inline"""

WHISPER_ICON_URL = "https://www.freeiconspng.com/uploads/whisper-icon-0.png"

ANSWER_CALLBACK_QUERY_MAX_LENGTH = 200


@Client.on_inline_query()
async def answer_iq(_, iq: InlineQuery):
    query = iq.query
    split = query.split(' ', 1)
    if query == '' or len(query) > ANSWER_CALLBACK_QUERY_MAX_LENGTH \
            or (query.startswith('@') and len(split) == 1):
        title = f"{emoji.FIRE} Write a whisper message"
        content = ("**Send whisper messages through inline mode**\n\n"
                   "Usage: `@ezWhisperBot [@username|@] text`")
        description = "Usage: @ezWhisperBot [@username|@] text"
        button = InlineKeyboardButton(
            "Learn more...",
            url="https://t.me/xkaykaybot?start=learn"
        )
    elif not query.startswith('@'):
        title = f"{emoji.EYE} Whisper once to the first one who open it"
        content = (
            f"{emoji.EYE} The first one who open the whisper can read it"
        )
        description = f"{emoji.SHUSHING_FACE} {query}"
        button = InlineKeyboardButton(
            f"{emoji.EYE} show message",
            callback_data="show_whisper"
        )
    else:
        # Python 3.8+
        u_target = 'anyone' if (x := split[0]) == '@' else x
        title = f"{emoji.LOCKED} A whisper message to {u_target}"
        content = f"{emoji.LOCKED} A whisper message to {u_target}"
        description = f"{emoji.SHUSHING_FACE} {split[1]}"
        button = InlineKeyboardButton(
            f"{emoji.LOCKED_WITH_KEY} show message",
            callback_data="show_whisper"
        )
    switch_pm_text = f"{emoji.INFORMATION} Learn how to send whispers"
    switch_pm_parameter = "learn"
    await iq.answer(
        results=[
            InlineQueryResultArticle(
                title=title,
                input_message_content=InputTextMessageContent(content),
                description=description,
                thumb_url=WHISPER_ICON_URL,
                reply_markup=InlineKeyboardMarkup([[button]])
            )
        ],
        switch_pm_text=switch_pm_text,
        switch_pm_parameter=switch_pm_parameter
    )

    
    
@Client.on_chosen_inline_result()
async def chosen_inline_result(_, cir: ChosenInlineResult):
    query = cir.query
    split = query.split(' ', 1)
    len_split = len(split)
    if len_split == 0 or len(query) > ANSWER_CALLBACK_QUERY_MAX_LENGTH \
            or (query.startswith('@') and len(split) == 1):
        return
    if len_split == 2 and query.startswith('@'):
        # Python 3.9+
        # receiver_uname, text = split[0].removeprefix('@'), split[1]
        receiver_uname, text = split[0][1:] or '@', split[1]
    else:
        receiver_uname, text = None, query
    sender_uid = cir.from_user.id
    inline_message_id = cir.inline_message_id
    whispers[inline_message_id] = {
        'sender_uid': sender_uid,
        'receiver_uname': receiver_uname,
        'text': text
    }


@Client.on_callback_query(filters.regex("^show_whisper$"))
async def answer_cq(_, cq: CallbackQuery):
    inline_message_id = cq.inline_message_id
    if not inline_message_id or inline_message_id not in whispers:
        try:
            await cq.answer("Can't find the whisper text", show_alert=True)
            await cq.edit_message_text(f"{emoji.NO_ENTRY} invalid whisper")
        except (MessageIdInvalid, MessageNotModified):
            pass
        return
    else:
        whisper = whispers[inline_message_id]
        sender_uid = whisper['sender_uid']
        receiver_uname: Optional[str] = whisper['receiver_uname']
        whisper_text = whisper['text']
        from_user: User = cq.from_user
        if receiver_uname and from_user.username \
                and from_user.username.lower() == receiver_uname.lower():
            await read_the_whisper(cq)
            return
        if from_user.id == sender_uid or receiver_uname == '@':
            await cq.answer(whisper_text, show_alert=True)
            return
        if not receiver_uname:
            await read_the_whisper(cq)
            return
        await cq.answer("This is not for you", show_alert=True)


async def read_the_whisper(cq: CallbackQuery):
    inline_message_id = cq.inline_message_id
    whisper = whispers[inline_message_id]
    whispers.pop(inline_message_id, None)
    whisper_text = whisper['text']
    await cq.answer(whisper_text, show_alert=True)
    receiver_uname: Optional[str] = whisper['receiver_uname']
    from_user: User = cq.from_user
    user_mention = (
        f"{from_user.first_name} (@{from_user.username})"
        if from_user.username
        else from_user.mention
    )
    try:
        t_emoji = emoji.UNLOCKED if receiver_uname else emoji.EYES
        await cq.edit_message_text(
            f"{t_emoji} {user_mention} read the message"
        )
    except (MessageIdInvalid, MessageNotModified):
        pass

@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.strip() == "":
            answerss = await inline_help_func(__HELP__)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=10
            )
            return
        elif text.split()[0] == "alive":
            answerss = await alive_function(answers)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=10
            )
        elif text.split()[0] == "tr":
            if len(text.split()) < 3:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Translator | tr [LANG] [TEXT]",
                    switch_pm_parameter="inline",
                )
            lang = text.split()[1]
            tex = text.split(None, 2)[2].strip()
            answerss = await translate_func(answers, lang, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "ud":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Urban Dictionary | ud [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await urban_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )
        elif text.split()[0] == "google":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Google Search | google [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await google_search_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )

        elif text.split()[0] == "wall":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    is_gallery=True,
                    switch_pm_text="Wallpapers Search | wall [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await wall_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "torrent":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Torrent Search | torrent [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await torrent_func(answers, tex)
            await client.answer_inline_query(
                query.id,
                results=answerss,
            )

        elif text.split()[0] == "yt":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="YouTube Search | yt [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await youtube_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss
            )

        elif text.split()[0] == "lyrics":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Lyrics Search | lyrics [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await lyrics_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss
            )

        elif text.split()[0] == "search":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Global Message Search. | search [QUERY]",
                    switch_pm_parameter="inline",
                )
            user_id = query.from_user.id
            tex = text.split(None, 1)[1].strip()
            answerss = await tg_search_func(answers, tex, user_id)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "music":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Music Search | music [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await music_inline_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "wiki":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Wikipedia | wiki [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await wiki_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "speedtest":
            answerss = await speedtest_init(query)
            return await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "pmpermit":
            user_id = query.from_user.id
            victim = text.split()[1]
            answerss = await pmpermit_func(answers, user_id, victim)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "ping":
            answerss = await ping_func(answers)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "ytmusic":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="YT Music | ytmusic [url]",
                    switch_pm_parameter="inline",
                )
            tex = query.query.split(None, 1)[1].strip()
            answerss = await yt_music_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "info":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="User Info | info [USERNAME|ID]",
                    switch_pm_parameter="inline",
                )
            tex = text.split()[1].strip()
            answerss = await info_inline_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "tmdb":
            if len(text.split()) < 2:
                answerss = await tmdb_func(answers, "")
                return await client.answer_inline_query(
                    query.id,
                    results=answerss,
                    switch_pm_text="TMDB Search | tmdb [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split()[1].strip()
            answerss = await tmdb_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )

        elif text.split()[0] == "image":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    is_gallery=True,
                    switch_pm_text="Image Search | image [QUERY]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answerss = await image_func(answers, tex)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=3600
            )

        elif text.split()[0] == "exec":
            await execute_code(query)

    except Exception as e:
        e = traceback.format_exc()
        print(e, " InLine")
