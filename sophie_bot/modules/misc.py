# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2019 Aiogram

#
# This file is part of SophieBot.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

from sophie_bot.decorator import register
from .utils.connections import chat_connection
from .utils.disable import disableable_dec
from .utils.language import get_strings_dec
from .utils.user_details import get_user_dec, get_user_link


@register(cmds=["id", "chatid", "userid"])
@disableable_dec('id')
@get_user_dec(allow_self=True)
@get_strings_dec('misc')
@chat_connection()
async def get_id(message, user, strings, chat):
    user_id = message.from_user.id

    text = strings["your_id"].format(id=user_id)
    if message.chat.id != user_id:
        text += strings["chat_id"].format(id=message.chat.id)

    if chat['status'] is True:
        text += strings["conn_chat_id"].format(id=chat['chat_id'])

    if not user['user_id'] == user_id:
        text += strings["user_id"].format(
            user=await get_user_link(user['user_id']),
            id=user['user_id']
        )

    if "reply_to_message" in message and "forward_from" in message.reply_to_message and not \
            message.reply_to_message.forward_from.id == message.reply_to_message.from_user.id:
        text += strings["user_id"].format(
            user=await get_user_link(message.reply_to_message.forward_from.id),
            id=message.reply_to_message.forward_from.id
        )

    await message.reply(text)


@register(cmds="runs")
@get_strings_dec("RUNS", mas_name="RANDOM_STRINGS")
@disableable_dec('runs')
async def runs(message, strings):
    await message.reply(random.choice(list(strings)))


@register(cmds='cancel', state='*', allow_kwargs=True)
async def cancel_handle(message, state, **kwargs):
    await state.finish()
    await message.reply('Cancelled.')
