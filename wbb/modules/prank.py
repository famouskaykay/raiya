"""
✘ Commands Available
/pprank
    Show Fake Promotion
"""

import asyncio
from wbb import app




@app(pattern="pprank")
async def pprank(ult):
    msg = await eor(ult, "**PROMOTING USER..**")
    await asyncio.sleep(1)
    await msg.edit("**PROMOTING USER...**")
    await asyncio.sleep(1)
    await msg.edit("**GIVING RIGHTS**")
    await asyncio.sleep(1)
    await msg.edit("**PROMOTED USER SUCCESSFULLY**")
