import requests
import configparser as cfg
import json


config = ".config.cfg"


class GoogleMapRepository:
    def __init__(self):
        self.key =  self.read_key_from_config_file(config, 'google_map_key')
        self.url = self.read_key_from_config_file(config, 'geolocation_url')

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)

    def get(self):
        params = (
            ('key={}'.format(self.key))
        )
        res = requests.post(self.url, params=params)
        data = json.loads(res.content)
        message = "You are at lattitude = {}, longtitude = {}".format(data['location']['lat'], data['location']['lng'])
        print(message)
        return message
