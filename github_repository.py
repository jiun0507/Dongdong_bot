
import requests
import configparser as cfg
import json


config = ".config.cfg"
class GithubRepository:
    def __init__(self):
        self.token = self.read_key_from_config_file(config, 'github_token')

        self.headers = {'Authorization': self.token}

    def read_key_from_config_file(self, config, key):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', key)

    # TODO Github response error. Bad Credentials ( check the token value )
    def get(self):
        res = requests.get("https://api.github.com/user", headers=self.headers)
        data = json.loads(res.content)
        try:
            res = requests.get(data['repos_url'], headers=self.headers)
        except KeyError:
            print(data)
        github_data = json.loads(res.content)
        repo_num = len(github_data)
        names = ''
        for repo in github_data:
            names += repo['name'] + '\n'
        message = 'You have {} repos. \nThey are : \n{}.'.format(repo_num, names[:-1])
        return message