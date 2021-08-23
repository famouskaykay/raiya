import requests

from pyrogram import Client, filters

BASE = "https://hastebin.com"


@Client.on_message(filters.command("haste", prefix="!") & filters.reply & ~filters.edited & filters.group)
def haste(client, message):
    reply = message.reply_to_message

    if reply.text is None:
        return

    result = requests.post(
        "{}/documents".format(BASE),
        data=reply.text.encode("UTF-8")
    ).json()

    message.reply(
        "{}/{}.py".format(BASE, result["key"]),
        reply_to_message_id=reply.message_id
    )
