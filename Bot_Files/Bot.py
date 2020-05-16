import requests
import time

from General import Constants


class Bot:

    def __init__(self, **kwargs):

        self.name = kwargs.get("name")
        self.call_code = kwargs.get("call_code")
        self.id = kwargs.get("id")
        self.group = kwargs.get("group")

        self.update_group_bot_list()

    def update_group_bot_list(self):
        self.group.bot_list.append(self)

    def is_bot_called(self, message):
        curr_string_list = message.text.lower().split(" ")
        return len(curr_string_list) >= 1 and curr_string_list[0] == self.call_code.lower()

    def write_text(self, text, character_limit=Constants.groupme_character_limit):

        str_ret_list = []

        output_string = ""
        for i, split_text in enumerate(text.split("\n")):
            if i != 0:
                output_string += "\n"
            if len(output_string + split_text) >= character_limit:
                if output_string[-1] == "\n":
                    str_ret_list.append(output_string[:-1])     # this removes the trailing newline
                else:
                    str_ret_list.append(output_string)
                output_string = ""
            output_string += split_text
        if output_string != "":
            str_ret_list.append(output_string)

        print("------------ SAL Response ----------")
        for str_ret in str_ret_list:
            for string in [str_ret[0 + i:character_limit + i] for i in range(0, len(str_ret), character_limit)]:
                time.sleep(1)
                print(string)
                post_params = {'bot_id': self.id, 'text': string}
                requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
        print("-----------------------------------")


    def do_help_response(self, *args):
        self.write_text("help method not overwritten")

    def respond(self, message):
        self.write_text("respond method not overwritten")
