from pyrogram import Client, Message

from main import command
from methods.InspiroApi import Inspiro


@Client.on_message(command("inspire"))
def inspire_cmd(c: Client, msg: Message):
    c.send_chat_action(msg.chat.id, "upload_photo")
    photo_url = Inspiro.generate_image()
    c.send_photo(
        msg.chat.id,
        photo_url,
        caption="@InspiroRobot"
    )
