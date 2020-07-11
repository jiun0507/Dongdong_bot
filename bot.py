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

class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_key_from_config_file(config, 'token')
        self.geolocation_url = self.read_key_from_config_file(config, 'geolocation_url')
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        self.base2 = "https://api.telegram.org/bot1348934480:AAFq8Oo9LzcvPcoCK682maOzJzO5HNX9jNY/"

    def get_location(self):
        print(self.geolocation_url)
        res = requests.post(self.geolocation_url, data=payload)
        data = json.loads(res.content)
        message = "You are at lattitude = {}, longtitude = {}".format(data['location']['lat'], data['location']['lng'])
        # message = '지금 어딨는지 잘 몰겠어요.'
        return message

    def get_jira_tickets(self):
        headers = {
            'Authorization': 'Basic Ym9iOldsZGpzOTYwNSE=',
            'Content-Type': 'application/json',
        }

        params = (
            ('jql', 'assignee=bob'),
        )

        res = requests.get('https://jira.kasa.network/rest/api/2/search/', headers=headers, params=params)
        jira_tickets = json.loads(res.content)
        ticket_num = len(jira_tickets)
        print("There are %s of tickets assigned to bob.", ticket_num)
        for jira_ticket in jira_tickets['issues']:
            if jira_ticket['fields']['status']['name'] not in ['Done', 'Backlog']:
                print(jira_ticket['key'],": ",jira_ticket['fields']['summary'], jira_ticket['fields']['status']['name'])

    def get_github(self):
        headers = {'Username':'jkim2@bowdoin.edu', 'Password':'Basic Bowdoin2019!', 'Authorization':'token c6f8247c81e92c34c905ae5d151a37ffaaef1429'}
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

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url, timeout=3)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        
        if msg is not None:
            requests.get(url)
            
    def send_message2(self, msg, chat_id):
        url2 = self.base2 + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url2)        

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)
