import time
from datetime import datetime
from configparser import ConfigParser
from pyrogram import Client, Message
from pyrogram import __version__
from pyrogram.raw.all import layer
from pyrogram.types import Message


class Assistant(Client):
    CREATOR_ID = 23122162  # Dan (haskell)
    ASSISTANT_ID = 483849041
    config = ConfigParser()
    chats = []

    def __init__(self):
        name = self.__class__.__name__.lower()

        self.config.read(f"{name}.ini")
        Assistant.chats = [int(c) for c in self.config[name]["chats"].split()]

        super().__init__(
            name,
            config_file=f"{name}.ini",
            workers=16,
            plugins=dict(
                root=f"{name}.plugins",
                exclude=["welcome"]
            ),
            sleep_threshold=180
        )

        self.admins = {
            chat: {Assistant.CREATOR_ID}
            for chat in Assistant.chats
        }

        self.uptime_reference = time.monotonic_ns()
        self.start_datetime = datetime.utcnow()

    async def start(self):
        await super().start()

        me = await self.get_me()
        print(f"Assistant for Pyrogram v{__version__} (Layer {layer}) started on @{me.username}. Hi.")

        # Fetch current admins from chats
        for chat, admins in self.admins.items():
            async for admin in self.iter_chat_members(chat, filter="administrators"):
                admins.add(admin.user.id)

    async def stop(self, *args):
        await super().stop()
        print("Pyrogram Assistant stopped. Bye.")

    def is_admin(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id

        return user_id in self.admins[chat_id]
