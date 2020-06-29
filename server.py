from bot import telegram_chatbot
import gizoogle

bot = telegram_chatbot("config.cfg")


def make_reply(msg):
    reply = '뭐라 해드릴 말이 없군요....'
    if msg is not None:
        reply = msg
    return reply

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            if message == 'Where am I?':
                message = bot.get_location()
            else:
                message = '뭐라 해드릴 말이 없군요...'
            reply = make_reply(message)
            bot.send_message(reply, from_)