from alpaca_use_case import AlpacaUseCase
from github_repository import GithubRepository
from github_use_case import GithubUseCase
from google_map_repository import GoogleMapRepository
from google_map_use_case import GoogleMapUseCase
from handler import (GithubView, GoogleMapView, JiraView, TelegramInterface,
                     AlpacaView)
from jira_repository import JiraRepository
from jira_use_case import JiraUseCase
from alpaca_repository import AlpacaRepository
from alpaca_use_case import AlpacaUseCase

def lambda_handler(event=None, context=None):
    telegram = TelegramInterface(".config.cfg")
    requests = telegram.gather_messages()

    for request in requests:
        messages = []
        if request == 'Jira':
            result = JiraView(JiraUseCase(JiraRepository())).get()
            messages.append(result)
        # elif request == 'Github':
        #     result = GithubView(GithubUseCase(GithubRepository())).get()
        #     print(result)
        elif request == 'Gmap':
            result = GoogleMapView(GoogleMapUseCase(GoogleMapRepository())).get()
            messages.append(result)
        elif request == 'Alpa':
            result = AlpacaView(AlpacaUseCase(AlpacaRepository())).get()
            messages.append(result)
        print(messages)
        for message in messages:
            telegram.send_full_message(text=message)
