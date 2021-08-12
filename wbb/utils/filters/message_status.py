from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from wbb import dp


class NotForwarded(BoundFilter):
    key = "not_forwarded"

    def __init__(self, not_forwarded):
        self.not_forwarded = not_forwarded

    async def check(self, message: types.Message):
        if "forward_from" not in message:
            return True


class NoArgs(BoundFilter):
    key = "no_args"

    def __init__(self, no_args):
        self.no_args = no_args

    async def check(self, message: types.Message):
        if not len(message.text.split(" ")) > 1:
            return True


class HasArgs(BoundFilter):
    key = "has_args"

    def __init__(self, has_args):
        self.has_args = has_args

    async def check(self, message: types.Message):
        if len(message.text.split(" ")) > 1:
            return True


class CmdNotMonospaced(BoundFilter):
    key = "cmd_not_mono"

    def __init__(self, cmd_not_mono):
        self.cmd_not_mono = cmd_not_mono

    async def check(self, message: types.Message):
        if (
            message.entities
            and message.entities[0]["type"] == "code"
            and message.entities[0]["offset"] < 1
        ):
            return False
        return True


dp.filters_factory.bind(NotForwarded)
dp.filters_factory.bind(NoArgs)
dp.filters_factory.bind(HasArgs)
dp.filters_factory.bind(CmdNotMonospaced)
