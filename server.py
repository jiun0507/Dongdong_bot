from bot import telegram_chatbot
import json
import requests
bot = telegram_chatbot("config.cfg")


def make_reply(msg):
    reply = '뭐라 해드릴 말이 없군요....'
    if msg is not None:
        reply = msg
    return reply

def lambda_handler(event=None, context=None):
    update_id = None
    telegram_id = -1
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": 'ok'})
    }
    try:
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
                telegram_id = from_
                if message == 'Where am I?':
                    message = bot.get_location()
                elif message == 'Github':
                    message = bot.get_github()
                else:
                    message = '뭐라 해드릴 말이 없군요...'
                reply = make_reply(message)
                bot.send_message(reply, from_)
                updates = bot.get_updates(offset=update_id)
    except requests.exceptions.Timeout:
        if telegram_id == -1:
            message = '지금은 보내드릴게 없습니다.'
            # message = bot.get_location()
            reply = make_reply(message)
            bot.send_message(reply, 1346080433)
        return response
    return response