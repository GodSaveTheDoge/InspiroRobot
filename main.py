import re

from pyrogram import Client, Filters

prefixes = (
    "/",
)

command_regex = r"^({}){{}}((@)([A-z]|[0-9])+bot)?(\ |$)".format("|".join([re.escape(i) for i in prefixes]))


# ({}) prefixes
# {{}} the command (later used with .format()) {{ is { escaped
# ((@)([A-z]|[0-9])+bot)? to include commands like /start@InspiroRobot (the name must end in bot)
# ^....(\ |$) to make sure it's not matched in the middle of a string
# so "/start@InspiroRobot myargument" works as well as "/start@InspiroRobot"
# but "mytext /start@InspiroRobot" or "/start@InspiroRobotSometext" don't

def command(cmd: str):
    return Filters.create(
        lambda flt, message: bool(re.match(command_regex.format(cmd), message.text or message.caption or "")),
        data=cmd
    )


bot = Client("Inspiro")

if __name__ == "__main__":
    bot.run()
