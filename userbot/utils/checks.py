# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from ..core.logger import logging

LOGS = logging.getLogger(__name__)


# Admin checker by uniborg
async def is_admin(doge, chat_id, userid):
    if not str(chat_id).startswith("-100"):
        return False
    try:
        req_jo = await doge.get_permissions(chat_id, userid)
        chat_participant = req_jo.participant
        if isinstance(
            chat_participant, (ChannelParticipantCreator, ChannelParticipantAdmin)
        ):
            return True
    except Exception as e:
        LOGS.info(str(e))
        return False
    else:
        return False
