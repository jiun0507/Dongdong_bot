import requests
import json
import configparser as cfg

payload = {
  "homeMobileCountryCode": '450',
  "homeMobileNetworkCode": '03',
  "radioType": "gsm",
  "carrier": "SKT",
  "considerIp": "true",
  "cellTowers": [
  ],
  "wifiAccessPoints": [
  ]
}


class github_bot:
    def get_github(self, token):
        headers = {'Authorization': token}
        res = requests.get("https://api.github.com/user", headers=headers)
        data = json.loads(res.content)
        res = requests.get(data['repos_url'], headers=headers)
        github_data = json.loads(res.content)
        repo_num = len(github_data)
        names = ''
        for repo in github_data:
            names += repo['name'] + ','
        result = 'You have {} repos. They are {}.'.format(repo_num, names[:-1])
        return result

class jira_bot:
 
    def get_jira_tickets(self, key, domain):
        headers = {
            'Authorization': key,
            'Content-Type': 'application/json',
        }
        params = (
            ('jql', 'assignee=bob'),
        )
        res = requests.get(domain, headers=headers, params=params)
        jira_tickets = json.loads(res.content)
        ticket_num = len(jira_tickets)
        print("There are {} of tickets assigned to bob.".format(ticket_num))
        message = ""
        for jira_ticket in jira_tickets['issues']:
            if jira_ticket['fields']['status']['name'] not in ['Done', 'Backlog']:
                ticket = '{}: {} status {}\n'.format(jira_ticket['key'], jira_ticket['fields']['summary'], jira_ticket['fields']['status']['name'])
                message += ticket
        return message
   
class google_map_bot:
    def get_location(self, key, url):
        params = (
            ('key={}'.format(key))
        )
        res = requests.post(url, params=params)
        data = json.loads(res.content)
        message = "You are at lattitude = {}, longtitude = {}".format(data['location']['lat'], data['location']['lng'])
        return message


class telegram_chatbot(github_bot, jira_bot, google_map_bot):

    def __init__(self, config):
        super().__init__()
        self.token = self.read_key_from_config_file(config, 'token')
        self.github_token =  self.read_key_from_config_file(config, 'github_token')
        self.google_map_key =  self.read_key_from_config_file(config, 'google_map_key')
        self.youjin_token = self.read_key_from_config_file(config, 'youjin_token')
        self.jira_authorization = self.read_key_from_config_file(config, 'jira_authorization')

        self.domain = self.read_key_from_config_file(config, 'domain')
        self.geolocation_url = self.read_key_from_config_file(config, 'geolocation_url')
        self.jira_domain = self.read_key_from_config_file(config, 'jira_domain')
        self.base = "{}{}/".format(self.domain, self.token)
        self.base2 = "{}{}/".format(self.domain, self.youjin_token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url, timeout=3)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            res = requests.get(url)
            print(res)

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)


