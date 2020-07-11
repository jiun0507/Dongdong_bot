from bot import telegram_chatbot
import json
import requests


class message_handler:
    def __init__(self, bot):
        self.bot = bot
        
    def handle_message(self):
        update_id = None
        telegram_id = -1
        response = {
            "statusCode": 200,
            "body": json.dumps({"message": 'ok'})
        }
        try:
            updates = self.bot.get_updates(offset=update_id)
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
                        message = self.bot.get_location(self.bot.google_map_key, self.bot.geolocation_url)
                    elif message == 'Github':
                        message = self.bot.get_github(self.bot.github_token)
                    elif message == 'Jira':
                        message = self.bot.get_jira_tickets(self.bot.jira_authorization, self.bot.jira_domain)
                        options = message.split('\n')
                        reply_markup = self.bot.get_reply_markup(options)
                    else:
                        message = '뭐라 해드릴 말이 없군요...'
                    
                    self.bot.send_full_message(self.bot.token, message, from_, reply_markup=reply_markup)
                    updates = self.bot.get_updates(offset=update_id)
        except requests.exceptions.Timeout:
            if telegram_id == -1:
                message = '지금은 보내드릴게 없습니다.'
                self.bot.send_message(message, 1346080433)
            return response
        return response
