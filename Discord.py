import requests  # dependency
import json

# discord message styling : https://gist.github.com/Birdie0/78ee79402a4301b1faf412ab5f1cdcf9

WEBHOOK_API_URL = "https://discordapp.com/api/webhooks/744083142708691026/W4lBV90gGQUInTuvEVi80qZmQDotZUYQTpnJSl2Skfqfik7ZpAMs6yVvU68lzMa6Zibi"
class Discord(object):

    @staticmethod
    def Sender(message):
        url = WEBHOOK_API_URL
        data = {}
        # for all params, see
        # https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data["username"] = "Task Bot"
        data["content"] = message
        result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            pass



