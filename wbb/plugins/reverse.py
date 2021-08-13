from pyrogram import Client, filters



@Client.on_message(filters.text & filters.private)

def echo(client, message):
    message.reply(message.text)



@Client.on_message(filters.text & filters.private, group=1)

def echo_reversed(client, message):
    message.reply(message.text[::-1])
