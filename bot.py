import requests
import json
import configparser as cfg


class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_key_from_config_file(config, 'token')
        self.geolocation_url = self.read_key_from_config_file(config, 'geolocation_url')
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_location(self):
        print(self.geolocation_url)
        # res = requests.post(self.geolocation_url)
        # data = json.loads(res.content)
        # message = "You are at lattitude = {}, longtitude = {}".format(data['location']['lat'], data['location']['lng'])
        message = '지금 어딨는지 잘 몰겠어요.'
        return message

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)