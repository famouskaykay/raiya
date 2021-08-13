from pyrogram import Client

plugins = dict(root="plugins")

Client("my_account", plugins=plugins).run()
