# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
import importlib
import sys
from pathlib import Path

from .. import CMD_HELP, LOAD_PLUG
from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import edl, eor
from ..core.session import doge
from ..helpers.tools import media_type
from ..helpers.utils import _dogetools, _dogeutils, _format, install_pip, reply_id
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("DogeUserBot")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"userbot/plugins/{shortname}.py")
        name = "userbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("✅ " + shortname + " imported!")
    else:
        if plugin_path is None:
            path = Path(f"userbot/plugins/{shortname}.py")
            name = f"userbot.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = doge
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.tgbot = doge.tgbot
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._dogeutils = _dogeutils
        mod._dogetools = _dogetools
        mod.media_type = media_type
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.edl = edl
        mod.edit_delete = edl
        mod.eor = eor
        mod.edit_or_reply = eor
        mod.logger = logging.getLogger(shortname)
        mod.borg = doge
        mod.catub = doge
        spec.loader.exec_module(mod)
        # For imports;
        sys.modules["userbot.plugins." + shortname] = mod
        LOGS.info("✅ " + shortname + " imported!")


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    doge.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    try:
        for i in LOAD_PLUG[shortname]:
            doge.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    except BaseException:
        pass
    try:
        name = f"userbot.plugins.{shortname}"
        for i in reversed(range(len(doge._event_builders))):
            ev, cb = doge._event_builders[i]
            if cb.__module__ == name:
                del doge._event_builders[i]
    except BaseException:
        raise ValueError
