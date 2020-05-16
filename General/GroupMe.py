import requests
import time


class GroupChat:

    def __init__(self, **kwargs):

        self.id = kwargs.get("id")
        self.groupme_access_token = kwargs.get("groupme_access_token")
        self.bot_list = kwargs.get("bot_list", [])
        self.refresh_rate = kwargs.get("refresh_rate", 1)

    def get_message_list(self, request_params):     # There's some issue here where internet come's back, but it get's stuck in the loop
        while True:
            try:
                overall_response = requests.get(
                    'https://api.groupme.com/v3/groups/' + self.id + '/messages',
                    params=request_params)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                print("No internet")
        if overall_response.status_code == 200:
            return [Message(raw_message) for raw_message in overall_response.json()['response']['messages']]
        return []

    def get_newest_valid_message(self):
        """
        Returns the newest message in the message_list with conditionals.

        Conditions:
        message_list != []
        message["name"] != room_scheduler_bot.name
        message["text"] is not None
        """
        request_params = {'token': self.groupme_access_token}
        message_list = self.get_message_list(request_params)

        if not message_list or message_list[0].name in [bot.name for bot in self.bot_list] or \
                message_list[0].text is None:
            return None
        return message_list[0]

    def get_first_valid_message(self):
        while True:
            curr_message = self.get_newest_valid_message()
            if curr_message:
                return curr_message
            time.sleep(self.refresh_rate)

    def update_message(self, curr_message):
        while True:
            new_message = self.get_newest_valid_message()
            if new_message and curr_message.raw_message != new_message.raw_message:
                return new_message
            time.sleep(self.refresh_rate)


class Message:

    def __init__(self, raw_message):

        self.raw_message = raw_message

        self.attachments = raw_message["attachments"]
        self.avatar_url = raw_message["avatar_url"]
        self.created_at = raw_message["created_at"]
        self.favorited_by = raw_message["favorited_by"]
        self.group_id = raw_message["group_id"]
        self.id = raw_message["id"]
        self.name = raw_message["name"]
        self.sender_id = raw_message["sender_id"]
        self.sender_type = raw_message["sender_type"]
        self.source_guid = raw_message["source_guid"]
        self.system = raw_message["system"]
        self.text = raw_message["text"]
        self.user_id = raw_message["user_id"]
        self.platform = raw_message["platform"]
