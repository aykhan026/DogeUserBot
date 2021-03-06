# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from json import dumps
from random import choice

from requests import post

from . import doge, edl, eor, gvar, reply_id

plugin_category = "fun"

category = ["classic", "kids", "party", "hot", "mixed"]
game_code = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
game_name = [
    "Tic-Tac-Toe",
    "Tic-Tac-Four",
    "Elephant XO",
    "Connect Four",
    "Rock-Paper-Scissors",
    "Rock-Paper-Scissors-Lizard-Spock",
    "Russian Roulette",
    "Checkers",
    "Pool Checkers",
]
game = dict(zip(game_code, game_name))


async def get_task(mode, cchoice):
    url = "https://psycatgames.com/api/tod-v2/"
    data = {
        "id": "truth-or-dare",
        "language": gvar("DOGELANG"),
        "category": category[cchoice],
        "type": mode,
    }
    headers = {
        "referer": "https://psycatgames.com/app/truth-or-dare/?utm_campaign=tod_website&utm_source=tod_en&utm_medium=website"
    }
    response = post(url, headers=headers, data=dumps(data))
    result = response.json()["results"]
    return choice(result)


@doge.bot_cmd(
    pattern="(task|truth|dare)(?: |$)([1-5]+)?$",
    command=("task", plugin_category),
    info={
        "header": "Get a random truth or dare task.",
        "description": "if no input is given then task will be from classic or kids category. if you want specific category then give input.",
        "note": "U need to give input as 1 for classic, 2 for kids, 3 for party, 4 for hot and 5 for mixed. if you want to give multiple catgories then use numbers without space like 12",
        "example": [
            "{tr}task",
            "{tr}task 2",
            "{tr}task 123",
        ],
    },
)
async def truth_dare_task(event):
    "Get a random task either truth or dare."
    taskmode = event.pattern_match.group(1)
    if taskmode == "task":
        dogevent = await eor(event, "Getting a random task for you.....")
        taskmode = choice(["truth", "dare"])
    else:
        dogevent = await eor(event, f"Getting a random {taskmode} task for you.....")
    category = event.pattern_match.group(2)
    category = int(choice(category)) if category else choice([1, 2])
    try:
        task = await get_task(taskmode, category)
        if taskmode == "truth":
            await dogevent.edit(f"**The truth task for you is**\n`{task}`")
        else:
            await dogevent.edit(f"**The dare task for you is**\n`{task}`")
    except Exception as e:
        await edl(dogevent, f"**Error while getting task**\n`{e}`", 7)


@doge.bot_cmd(
    command=("truth", plugin_category),
    info={
        "header": "Get a random truth task.",
        "description": "if no input is given then task will be from classic or kids category. if you want specific category then give input.",
        "note": "U need to give input as 1 for classic, 2 for kids, 3 for party, 4 for hot and 5 for mixed. if you want to give multiple catgories then use numbers without space like 12",
        "example": [
            "{tr}truth",
            "{tr}truth 2",
            "{tr}truth 123",
        ],
    },
)
async def truth_task(event):
    "Get a random truth task."
    # just to show in help menu as seperate


@doge.bot_cmd(
    command=("dare", plugin_category),
    info={
        "header": "Get a random dare task.",
        "description": "if no input is given then task will be from classic or kids category. if you want specific category then give input.",
        "note": "U need to give input as 1 for classic, 2 for kids, 3 for party, 4 for hot and 5 for mixed. if you want to give multiple catgories then use numbers without space like 12",
        "example": [
            "{tr}dare",
            "{tr}dare 2",
            "{tr}dare 123",
        ],
    },
)
async def dare_task(event):
    "Get a random dare task."
    # just to show in help menu as seperate


@doge.bot_cmd(
    pattern="game(?:\s|$)([\s\S]*)",
    command=("game", plugin_category),
    info={
        "header": "Play inline games",
        "description": "Start an inline game by inlinegamebot",
        "Game code & Name": game,
        "usage": "{tr}game <game code>",
        "examples": "{tr}game 3 ",
    },
)
async def igame(event):
    "Fun game by inline"
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    game_list = "".join(
        f"**{i}.** `{item}`: __{game[item]}__\n" for i, item in enumerate(game, start=1)
    )
    if not input_str:
        await edl(event, f"**Available Game Codes & Names:**\n\n{game_list}", 60)
        return
    if input_str not in game_code:
        dogevent = await eor(event, "`Give me a correct game code...`")
        await sleep(1)
        await edl(dogevent, f"**Available Game Codes & Names:**\n\n{game_list}", 60)
    else:
        await eor(
            event,
            f"**Game code `{input_str}` is selected for game:** __{game[input_str]}__",
        )
        await sleep(1)
        bot = "@inlinegamesbot"
        results = await event.client.inline_query(bot, input_str)
        await results[game_code.index(input_str)].click(
            event.chat_id, reply_to=reply_to_id
        )
        await event.delete()
