from bot import telegram_chatbot
import json
import requests

bot = telegram_chatbot("config.cfg")


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
                reply_markup = None
                update_id = item["update_id"]
                try:
                    message = str(item["message"]["text"])
                except:
                    message = None
                from_ = item["message"]["from"]["id"]
                telegram_id = from_
                if message == 'Where am I?':
                    message = bot.get_location(bot.google_map_key, bot.geolocation_url)
                elif message == 'Github':
                    message = bot.get_github(bot.github_token)
                elif message == 'Jira':
                    message = bot.get_jira_tickets(bot.jira_authorization, bot.jira_domain)
                    options = message.split('\n')
                    reply_markup = bot.get_reply_markup(options)
                else:
                    message = '뭐라 해드릴 말이 없군요...'
                
                bot.send_full_message(bot.token, message, from_, reply_markup=reply_markup)
                # bot.send_message(reply, from_)
                updates = bot.get_updates(offset=update_id)
    except requests.exceptions.Timeout:
        if telegram_id == -1:
            message = '지금은 보내드릴게 없습니다.'
            bot.send_message(message, 1346080433)
        return response
    return response

lambda_handler()