import sys
import requests
import logging
from .models.udto_message import UDTO_Position, UDTO_ChatMessage

logger = logging.getLogger('iobtServerRest')
logger.setLevel(logging.DEBUG)  # set logger level
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)


class IobtServerRest:
    azureURL: str

    def __init__(self, url: str) -> None:
        self.azureURL = url

    def processJsonResult(self, result):
        if (result['hasError'] == True):
            print(result['message'])
            return []
        else:
            payload = result['payload']
            return payload

    def flushCentralModel(self):
        try:
            url = F"{self.azureURL}/api/ClientHub/FlushCentralModel"
            response = requests.get(url)
            return self.processJsonResult(response.json())
        except:
            msg = sys.exc_info()[0]
            print(F"Error ${msg}")
            return []

    def centralModel(self):
        try:
            url = F"{self.azureURL}/api/ClientHub/CentralModel"
            response = requests.get(url)

            return self.processJsonResult(response.json())

        except:
            msg = sys.exc_info()[0]
            print(F"Error ${msg}")
            return []

    def currentChatMessage(self):
        try:
            url = F"{self.azureURL}/api/ClientHub/CurrentChatMessage"
            response = requests.get(url)

            return self.processJsonResult(response.json())

        except:
            msg = sys.exc_info()[0]
            print(F"Error ${msg}")
            return []

    def chatMessage(self, obj: UDTO_ChatMessage):
        try:
            headers = dict({'Content-type': 'application/json',
                           'Accept': 'application/json'})

            url = F"{self.azureURL}/api/ClientHub/ChatMessage"
            response = requests.post(
                url=url, json=obj.toDICT(), headers=headers)
            print(response)

            return self.processJsonResult(response.json())

        except:
            print(F"Error ${sys.exc_info()[0]}")
            return []

    def ping(self):
        try:
            headers = dict({'Content-type': 'application/json',
                           'Accept': 'application/json'})

            url = F"{self.azureURL}/api/ClientHub/Ping"
            logger.debug(f"in ping before get url={url}")
            response = requests.get(url=url, headers=headers)
            logger.debug(f"response.headers={response.headers}")
            print(response.headers)

            return response

        except:
            print(F"Error ${sys.exc_info()[0]}")
            return []
