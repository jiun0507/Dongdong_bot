import requests
import configparser as cfg
import json


config = ".config.cfg"
class JiraRepository:
    def __init__(self):
        self.domain = self.read_key_from_config_file(config, 'jira_domain')
        self.key = self.read_key_from_config_file(config, 'jira_authorization')

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)

    def get(self):
        headers = {
            'Authorization': self.key,
            'Content-Type': 'application/json',
        }
        params = (
            ('jql', 'assignee=bob'),
        )
        res = requests.get(self.domain, headers=headers, params=params)
        jira_tickets = json.loads(res.content)
        ticket_num = len(jira_tickets)
        print("There are {} of tickets assigned to bob.".format(ticket_num))
        message = ""
        for jira_ticket in jira_tickets['issues']:
            if jira_ticket['fields']['status']['name'] not in ['Done', 'Backlog']:
                ticket = '{}: {} status {}\n'.format(jira_ticket['key'], jira_ticket['fields']['summary'], jira_ticket['fields']['status']['name'])
                message += ticket
        return message

