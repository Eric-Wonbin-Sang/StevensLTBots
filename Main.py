import pickle
import os
import datetime

from LTInfo import LTSheets, URL
import Stevens
import Bot_Files.Sal

from General import Constants, Functions, GroupMe


def get_stevens(path, room_schedule_url):
    print("-----------------------")
    if os.path.exists(path):
        print("{} file found".format(path))
        stevens = pickle.load(open(path, "rb"))

        curr_time = datetime.datetime.today()
        time_elapsed = curr_time - stevens.time_updated

        if time_elapsed.total_seconds() > 10 * 60:
            print("New {} being created (updating old save)".format(path))
            stevens = Stevens.Stevens(room_schedule_url=room_schedule_url)
            Functions.pickle_object(stevens, path)

    else:
        print("New {} being created (creating first save)".format(path))
        stevens = Stevens.Stevens(room_schedule_url=room_schedule_url)
        Functions.pickle_object(stevens, path)

    print("Stevens returned")
    print("-----------------------")
    return stevens


def update_stevens(stevens, stevens_save_filename, room_schedule_url):
    if os.path.exists(stevens_save_filename):
        curr_time = datetime.datetime.today()
        time_elapsed = curr_time - stevens.time_updated
        if time_elapsed.total_seconds() > Constants.stevens_update_duration:
            stevens = Stevens.Stevens(room_schedule_url=room_schedule_url)
            Functions.pickle_object(stevens, stevens_save_filename)
            print("{} - Stevens object updated".format(curr_time))
    return stevens


def get_sal_bot(credentials_path, stevens, lt_sheets):
    credentials_dict = Functions.txt_to_dict(credentials_path)
    group = GroupMe.GroupChat(id=credentials_dict["groupchat id"], groupme_access_token=Constants.groupme_access_token)
    return Bot_Files.Sal.Sal(name=credentials_dict["name"],
                             id=credentials_dict["id"],
                             call_code="sal",
                             group=group,
                             stevens=stevens,
                             lt_sheets=lt_sheets)


def get_real_or_beta_bot(keyword, stevens, lt_sheets):

    real_bot_credentials_path = os.path.dirname(os.getcwd()) + "\\API Keys\\Groupme Bot SAL credentials.txt"
    beta_bot_credentials_path = os.path.dirname(os.getcwd()) + "\\API Keys\\Groupme Bot SAL BETA credentials.txt"

    if keyword == "real" or not os.path.exists(beta_bot_credentials_path):
        credentials_to_use = real_bot_credentials_path
    else:
        credentials_to_use = beta_bot_credentials_path

    return get_sal_bot(
        credentials_path=credentials_to_use,
        stevens=stevens,
        lt_sheets=lt_sheets)


def main():

    lt_sheets = LTSheets.LTSheets()

    stevens_save_filename = "stevens.obj"
    stevens = get_stevens(stevens_save_filename, URL.get_spec_url(lt_sheets, "Room Schedule"))

    sal_bot = get_real_or_beta_bot(Functions.txt_doc_to_str("Bot Type.txt"), stevens, lt_sheets)

    def curr_command_list(curr_text, bot):
        curr_string_list = curr_text.lower().split(" ")
        raw_command_string = " ".join(curr_string_list[1:])
        return Functions.string_to_command_list_list(raw_command_string, bot.command_func_dict.keys())

    prev_message = None
    while True:

        stevens = update_stevens(stevens, stevens_save_filename, URL.get_spec_url(lt_sheets, "Room Schedule"))
        curr_message = sal_bot.group.get_newest_valid_message()

        if curr_message:

            if prev_message and prev_message.text != curr_message.text:
                print("{} - {}: {}".format(curr_message.created_at, curr_message.name, curr_message.text))

            if sal_bot.is_bot_called(curr_message):

                if sal_bot.do_easter_egg(curr_message):
                    continue

                command_list_list = curr_command_list(curr_message.text, sal_bot)
                if not command_list_list:
                    sal_bot.do_help_response()
                for i, command_list in enumerate(command_list_list):
                    sal_bot.respond(command_list)

            prev_message = curr_message


main()
