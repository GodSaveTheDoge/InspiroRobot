import sys

if sys.version_info.major != 3:
    exit()
if sys.version_info.minor < 6:
    exit()

from api import getPhoto, getMindfulness
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaAudio, \
    InlineQueryResultPhoto
from pyrogram.errors import PeerIdInvalid, UserIsBlocked
import random
import os

if len(sys.argv) < 2:
    bot = Client(
        "InspiroRobot",
        config_file="config.ini")
else:
    if sys.argv[1] == "string":
        bot = Client(
            os.environ["SESSION_STRING"]
        )
    else:
        bot = Client(
            "InspiroRobot",
            api_id=os.environ["API_ID"],
            api_hash=os.environ["API_HASH"],
            bot_token=os.environ["BOT_TOKEN"]
        )

pre = ["/", "."]
userDidNotStart = ["Well, you could at least start me.", "You need to start me, don't you?",
                   "Maybe a little /start could do the trick",
                   "Mommy said I should not talk to strangers who didn't start me",
                   "[400 BAD REQUEST] You did not start the bot.",
                   "You should /start me ;)",
                   "I can start you but you can start me."]
userIsBlocked = ["You should have thought of this before blocking me.", "I don't know, maybe unblock me?",
                 "I will save it only if you unblock me", "But... You blocked me!",
                 "I can't if you block me."]


def _hasMessage(c, query):
    if query.message:
        return True
    return False


def _hasInline(c, query):
    if query.inline_message_id:
        return True
    return False


def _isPhoto(c, query):
    if query.message:
        if query.message.photo:
            return True
    return False


def _isAudio(c, query):
    if query.message:
        if query.message.audio:
            return True
    return False


def _save(c, query):
    if query.data.startswith("save"):
        return True
    return False


def _inspire(c, query):
    if query.data == "inspire":
        return True
    return False


hasMessage = Filters.create(_hasMessage, "hasMessage")
hasInline = Filters.create(_hasInline, "hasInline")
isPhoto = Filters.create(_isPhoto, "isPhoto")
isAudio = Filters.create(_isAudio, "isAudio")
isSave = Filters.create(_save, "save")
isInspire = Filters.create(_inspire, "inspire")


@bot.on_message(Filters.command("start", prefixes=pre))
def start_command(c, msg):
    msg.reply("I'm the unofficial telegram version of <a href=\"https://inspirobot.me/\">InspiroBot</a>.\n"
              "I am an artificial intelligence dedicated to generating unlimited amounts of unique inspirational "
              "quotes for endless enrichment of pointless human existence.",
              disable_web_page_preview=True)


@bot.on_message(Filters.command("inspire", prefixes=pre))
def inspire_command(c, msg):
    bot.send_chat_action(msg.chat.id, "upload_photo")
    bot.send_photo(msg.chat.id, getPhoto(), caption="@InspiroRobot", reply_to_message_id=msg.message_id,
                   reply_markup=InlineKeyboardMarkup([
                       [InlineKeyboardButton("Inspire me again", callback_data="inspire"),
                        InlineKeyboardButton("Save it", callback_data="save")]]))


@bot.on_message(Filters.command("inspiremp3", prefixes=pre))
def inspiremp3_command(c, msg):
    bot.send_chat_action(msg.chat.id, "record_audio")
    data = getMindfulness()
    tmp = bot.send_audio(msg.chat.id, data["audio"], caption="\n\n".join(data["quotes"]) + "\n\n@InspiroRobot",
                         reply_to_message_id=msg.message_id,
                         reply_markup=InlineKeyboardMarkup([
                             [InlineKeyboardButton("Inspire me again", callback_data="inspire"),
                              InlineKeyboardButton("Save it", callback_data="save")]]))


@bot.on_message(Filters.command("info", prefixes=pre))
def info_command(c, msg):
    msg.reply("This bot is made by @GodSaveTheDoge\n"
              "Other projects: @GodSaveTheBots\n"
              "Original Site (not by me): https://inspirobot.me",
              disable_web_page_preview=True)


@bot.on_message(Filters.text)
def fallback(c, msg):
    cmd = {"start": start_command, "inspiremp3": inspiremp3_command,
           "inspire": inspire_command, "info": info_command}
    for c in cmd:
        for p in pre:
            if msg.text.startswith(p + c):
                cmd[c](c, msg)
                return 0


@bot.on_callback_query(isPhoto & isInspire)
def cb_inspire_message_photo(c, query):
    query.message.edit_media(InputMediaPhoto(getPhoto(), caption="@InspiroRobot"),
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton("Inspire me again", callback_data="inspire"),
                                  InlineKeyboardButton("Save it", callback_data="save")]]))
    query.answer("Inspired")


@bot.on_callback_query(isPhoto & isSave)
def cb_save_message_photo(c, query):
    try:
        bot.send_photo(query.from_user.id, query.message.photo.file_id, file_ref=query.message.photo.file_ref,
                       caption="@InspiroRobot")
        query.answer("Saved!")
    except PeerIdInvalid:
        query.answer(random.choice(userDidNotStart), show_alert=True)
    except UserIsBlocked:
        query.answer(random.choice(userIsBlocked), show_alert=True)
    except Exception as e:
        query.answer("Something went wrong:\n{}".format(e), show_alert=True)


@bot.on_callback_query(isAudio & isInspire)
def cb_inspire_message_audio(c, query):
    data = getMindfulness()
    query.message.edit_media(InputMediaAudio(data["audio"], caption="\n\n".join(data["quotes"]) + "\n\n@InspiroRobot"),
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton("Inspire me again", callback_data="inspire"),
                                  InlineKeyboardButton("Save it", callback_data="save")]]))
    query.answer("Inspired")


@bot.on_callback_query(isAudio & isSave)
def cb_save_message_audio(c, query):
    try:
        bot.send_audio(query.from_user.id, query.message.audio.file_id, file_ref=query.message.audio.file_ref,
                       caption=query.message.caption)
        query.answer("Saved!")
    except PeerIdInvalid:
        query.answer(random.choice(userDidNotStart), show_alert=True)
    except UserIsBlocked:
        query.answer(random.choice(userIsBlocked), show_alert=True)
    except Exception as e:
        query.answer("Something went wrong:\n{}".format(e), show_alert=True)


@bot.on_inline_query()
def inline_inspiremp3(c, query):
    url = getPhoto()
    query.answer([
        InlineQueryResultPhoto(url,
                               thumb_url="https://inspirobot.me/website/images/inspirobot-dark-green.png",
                               title="Inspire me",
                               description="Send an ispirational photo",
                               caption="@InspiroRobot",
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton("Inspire me again", callback_data="inspire"),
                                    InlineKeyboardButton("Save it", callback_data="save-{}".format(url))]])
                               )],
        is_gallery=True,
        is_personal=True,
        cache_time=1)


@bot.on_callback_query(isInspire & ~hasMessage)
def cb_inspire_inline_photo(c, query):
    url = getPhoto()
    bot.edit_inline_media(
        query.inline_message_id,
        InputMediaPhoto(url, caption="@InspiroRobot"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Inspire me again", callback_data="inspire"),
             InlineKeyboardButton("Save it", callback_data="save-{}".format(url))]]))


@bot.on_callback_query(isSave & ~hasMessage)
def cb_save_inline_photo(c, query):
    url = query.data.split("-")[1]
    try:
        bot.send_photo(query.from_user.id, url,
                       caption="@InspiroRobot")
        query.answer("Saved!")
    except PeerIdInvalid:
        query.answer(random.choice(userDidNotStart), show_alert=True)
    except UserIsBlocked:
        query.answer(random.choice(userIsBlocked), show_alert=True)
    except Exception as e:
        query.answer("Something went wrong:\n{}".format(e), show_alert=True)


bot.run()
