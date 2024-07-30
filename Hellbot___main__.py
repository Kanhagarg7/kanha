from pyrogram import idle
import dns.resolver
import socket

from Hellbot import __version__
from Hellbot.core import (
    Config,
    ForcesubSetup,
    GachaBotsSetup,
    TemplateSetup,
    UserSetup,
    db,
    hellbot,
)
from Hellbot.functions.tools import initialize_git
from Hellbot.functions.utility import BList, Flood, TGraph

def custom_resolver(hostname):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8", "8.8.4.4"]  # Using Google's DNS servers
    answers = resolver.resolve(hostname, "A")
    return answers[0].address


original_getaddrinfo = socket.getaddrinfo


def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        ip = custom_resolver(host)
        return [(socket.AF_INET, socket.SOCK_STREAM, proto, "", (ip, port))]
    except Exception as e:
        return original_getaddrinfo(host, port, family, type, proto, flags)


socket.getaddrinfo = custom_getaddrinfo

async def main():
    await hellbot.startup()
    await db.connect()
    await UserSetup()
    await ForcesubSetup()
    await GachaBotsSetup()
    await TemplateSetup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await TGraph.setup()
    await initialize_git(Config.PLUGINS_REPO)
    await hellbot.start_message(__version__)
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
