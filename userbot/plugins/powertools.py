# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio.exceptions import CancelledError
from os import _exit, environ, execle
from sys import executable as sysexecutable
from time import sleep

from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    HEROKU_APP,
    HEROKU_APP_NAME,
    Heroku,
    dgvar,
    doge,
    edl,
    eor,
    gvar,
    logging,
    sgvar,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)


@doge.bot_cmd(
    pattern="restart$",
    command=("restart", plugin_category),
    info={
        "header": "Restarts the bot !!",
        "usage": "{tr}restart",
    },
    disable_errors=True,
)
async def _(event):
    "Restarts the bot !!"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    teledoge = await eor(
        event,
        "Restarted. `.ping` me or `.doge` to check if I am online, actually it takes 1-2 min for restarting",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [teledoge.chat_id, teledoge.id])
    except Exception as e:
        LOGS.error(e)
    if HEROKU_APP is not None:
        try:
            app = Heroku.apps()[HEROKU_APP_NAME]
            dgvar("ipaddress")
            app.restart()
        except BaseException:
            try:
                dgvar("ipaddress")
                executable = sysexecutable.replace(" ", "\\ ")
                args = [executable, "-m", "userbot"]
                execle(executable, *args, environ)
            except CancelledError:
                pass
            except Exception as e:
                LOGS.error(e)
    else:
        try:
            dgvar("ipaddress")
            executable = sysexecutable.replace(" ", "\\ ")
            args = [executable, "-m", "userbot"]
            execle(executable, *args, environ)
        except CancelledError:
            pass
        except Exception as e:
            LOGS.error(e)


@doge.bot_cmd(
    pattern="shutdown$",
    command=("shutdown", plugin_category),
    info={
        "header": "Shutdowns the bot !!",
        "description": "To turn off the dyno of heroku. you can't turn on by bot you need to got to heroku and turn on or use @hk_heroku_bot",
        "usage": "{tr}shutdown",
    },
)
async def _(event):
    "Shutdowns the bot"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down")
    await eor(event, "`Turning off bot now ...Manually turn me on later`")
    if HEROKU_APP is not None:
        try:
            HEROKU_APP.process_formation()["doger"].scale(0)
        except Exception:
            _exit(143)
    else:
        _exit(143)


@doge.bot_cmd(
    pattern="sleep( [0-9]+)?$",
    command=("sleep", plugin_category),
    info={
        "header": "Userbot will stop working for the mentioned time.",
        "usage": "{tr}sleep <seconds>",
        "examples": "{tr}sleep 60",
    },
)
async def _(event):
    "To sleep the userbot"
    if " " not in event.pattern_match.group(1):
        return await eor(event, "Syntax: `.sleep time`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "You put the bot to sleep for " + str(counter) + " seconds",
        )
    event = await eor(event, f"`Okay, let me sleep for {counter} seconds`")
    sleep(counter)
    await event.edit("`OK, I'm awake now.`")


@doge.bot_cmd(
    pattern="notify (on|off)$",
    command=("notify", plugin_category),
    info={
        "header": "To update the your chat after restart or reload .",
        "description": "Will send the ping cmd as reply to the previous last msg of (restart/reload/update cmds).",
        "usage": [
            "{tr}notify <on/off>",
        ],
    },
)
async def set_pmlog(event):
    "To update the your chat after restart or reload."
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        if gvar("restartupdate") is None:
            return await edl(event, "__Notify was already disabled__")
        dgvar("restartupdate")
        return await eor(event, "__Notify was disabled successfully.__")
    if gvar("restartupdate") is None:
        sgvar("restartupdate", "turn-oned")
        return await eor(event, "__Notify was enabled successfully.__")
    await edl(event, "__Notify was already enabled.__")
