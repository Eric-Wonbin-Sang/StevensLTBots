import datetime
import pyjokes
import random

import Stevens
from LTInfo import Lamp, Box, Work, URL, Contact
from Bot_Files import Bot

from General import Constants, Functions


class Sal(Bot.Bot):

    def __init__(self, **kwargs):

        super().__init__(name=kwargs.get("name"),
                         call_code=kwargs.get("call_code"),
                         id=kwargs.get("id"),
                         group=kwargs.get("group"))

        self.stevens = kwargs.get("stevens")
        self.lt_sheets = kwargs.get("lt_sheets")

        self.command_func_dict = {
            "room": self.do_room_response,
            "prof": self.do_prof_response,
            "box": self.do_box_response,
            "contact": self.do_contact_response,
            "urls": self.do_urls_response,
            "work": self.do_work_response,
            "lamp": self.do_lamp_response,
            "help": self.do_help_response,
            "update": self.update_lt_sheets
        }

    # Responses -------------------------------------------------------------------------
    def do_room_response(self, command_list):
        """
        command_list ex: [bc122, m, t, wednesday] or [bc122]
        len(command_list) will always be >= 1
        """
        if not command_list:
            self.write_text(self.lt_sheets.sheet_to_simple_response("room"))
        elif command_list[0] == "empty":

            if len(command_list[1:]) >= 1:

                empty_room_list = []
                curr_day = datetime.datetime.now()
                curr_time = datetime.time(hour=curr_day.hour, minute=curr_day.minute)

                room_search = command_list[1]
                day_code_list = Stevens.get_day_code_list()

                for room in self.stevens.room_list:
                    if room_search in room.name.lower():
                        free_section_list = []
                        for day_key in room.day_section_list_dict:
                            if day_key in day_code_list:
                                for section in room.day_section_list_dict[day_key]:
                                    if not(section.start_time <= curr_time <= section.end_time):
                                        free_section_list.append(section)

                        if free_section_list:
                            empty_room_list.append(room)

                str_ret = ""
                for r_i, room in enumerate(empty_room_list):
                    if r_i != 0:
                        str_ret += "\n"
                    str_ret += room.name
                    for i, day_code in enumerate([d_code for d_code in day_code_list if Stevens.is_valid_day(d_code)]):
                        if i != 0:
                            str_ret += "\n{}-----------------------".format(Constants.groupme_tab)
                        if day_code in room.day_section_list_dict:
                            str_ret += "\n" + Functions.shift_string_block(
                                Stevens.section_list_to_string(room.day_section_list_dict[day_code]), Constants.groupme_tab)
                        else:
                            str_ret += "\n{}day_code {} does not exist in current room".format(Constants.groupme_tab, day_code)
                self.write_text(str_ret)

        else:

            room_code = command_list[0]
            day_code_list = Stevens.get_day_code_list(command_list[1:])
            room_list = [room for room in self.stevens.room_list if room_code.lower() in room.name.lower()]

            if len(room_list) == 0:
                self.write_text("No room has code {}".format(room_code))
            elif len(day_code_list) > 0 and day_code_list[0] == "all":
                str_ret = "All rooms containing string '{}':".format(room_code)
                for room in room_list:
                    str_ret += "\n{}{}".format(Constants.groupme_tab, room.name)
                self.write_text(str_ret)
            elif all([not Stevens.is_valid_day(day_code) for day_code in day_code_list]):
                self.write_text("These are not day codes: {}".format(day_code_list))
            else:
                str_ret = ""
                for r_i, room in enumerate(room_list):
                    if r_i != 0:
                        str_ret += "\n"
                    str_ret += room.name
                    for i, day_code in enumerate([d_code for d_code in day_code_list if Stevens.is_valid_day(d_code)]):
                        if i != 0:
                            str_ret += "\n{}-----------------------".format(Constants.groupme_tab)
                        if day_code in room.day_section_list_dict:
                            str_ret += "\n" + Functions.shift_string_block(
                                Stevens.section_list_to_string(room.day_section_list_dict[day_code]), Constants.groupme_tab)
                        else:
                            str_ret += "\n{}day_code {} does not exist in current room".format(Constants.groupme_tab, day_code)
                self.write_text(str_ret)

    def do_prof_response(self, command_list):
        if not command_list:
            self.write_text(self.lt_sheets.sheet_to_simple_response("prof"))
        else:

            prof_name = " ".join(command_list)

            curr_time = datetime.datetime.today()
            prev_time = curr_time - datetime.timedelta(days=1)
            next_time = curr_time - datetime.timedelta(days=-1)

            day_code_list = Stevens.get_day_code_list([prev_time.strftime("%A"),
                                                       curr_time.strftime("%A"),
                                                       next_time.strftime("%A")])

            found_prof_section_list_dict = {}
            for prof_key in self.stevens.prof_section_list_dict:
                if prof_name.lower() in prof_key.lower():
                    found_prof_section_list_dict[prof_key] = self.stevens.prof_section_list_dict[prof_key]

            if len(found_prof_section_list_dict) == 0:
                self.write_text("No professor found")
            elif len(found_prof_section_list_dict) > 1:
                str_ret = "Multiple professors found:"
                for found_prof_key in found_prof_section_list_dict:
                    str_ret += "\n{}{}".format(Constants.groupme_tab, found_prof_key)
                self.write_text(str_ret)
            else:
                str_ret = ""
                for found_prof_key in found_prof_section_list_dict:
                    str_ret += "Professor found: {}".format(found_prof_key)
                    filtered_section_list = []
                    for section in found_prof_section_list_dict[found_prof_key]:
                        if section.day.lower() in day_code_list:
                            filtered_section_list.append(section)

                    if len(filtered_section_list) == 0:
                        str_ret += "\n{}No sections found with day codes [{}]".format(Constants.groupme_tab,
                                                                                      ", ".join(day_code_list))
                    else:
                        for section in filtered_section_list:
                            str_ret += "\n{}Room: {}  |  {}: {} - {}".format(
                                Constants.groupme_tab,
                                section.room.name,
                                Stevens.get_day_from_code(section.day).title()[:3],
                                Functions.get_nice_time_format(section.start_time),
                                Functions.get_nice_time_format(section.end_time))

                self.write_text(str_ret)

    def do_box_response(self, command_list):
        self.write_text(Box.get_response(lt_sheets=self.lt_sheets,
                                         command_list=command_list))

    def do_contact_response(self, command_list):
        self.write_text(Contact.get_response(lt_sheets=self.lt_sheets,
                                             command_list=command_list))

    def do_urls_response(self, command_list):
        self.write_text(URL.get_response(lt_sheets=self.lt_sheets,
                                         command_list=command_list))

    def do_work_response(self, command_list):
        self.write_text(Work.get_response(lt_sheets=self.lt_sheets,
                                          command_list=command_list))

    def do_lamp_response(self, command_list):
        self.write_text(Lamp.get_response(lt_sheets=self.lt_sheets,
                                          command_list=command_list))

    def do_help_response(self, command_list=None):
        self.write_text(self.lt_sheets.sheet_to_simple_response("help"))

    # Maintenance ----------------------------------------------------------------------------
    def update_lt_sheets(self, command_list):
        update_cond = self.lt_sheets.update_value_l_l_dict()
        if update_cond is True:
            self.write_text("LT Sheets object updated successfully.")
        else:
            self.write_text("LT Sheets could not be updated.\n{}".format(update_cond))

    # Easter Eggs ---------------------------------------------------------------------------
    def do_easter_egg(self, message):
        if message.text.lower().strip() == "sal good morning":
            self.write_text("Good morning, {}.".format(message.name.upper()))
            return True

        if message.text.lower().strip() == "sal good night":
            self.write_text("Good night, {}.".format(message.name.upper()))
            return True

        if message.text.lower().strip() == "sal hi" or message.text.lower().strip() == "sal hello":
            self.write_text("Hello, {}.".format(message.name.upper()))
            return True

        if "sal" in message.text.lower().strip() and \
                "joke" in message.text.lower().strip():

            rand_num = random.random()

            if rand_num < .5:
                self.write_text("Evan Thomas Romeo")
            else:
                self.write_text(pyjokes.get_joke())
            return True

        return False

    # Basic ---------------------------------------------------------------------------------
    def respond(self, command_list):
        """ This takes in one command list (ex: [room bc122, m, t] or [help]) """
        if len(command_list) != 0:
            command = command_list[0]
            command_params = command_list[1:]
            if command in self.command_func_dict.keys():
                self.command_func_dict[command](command_params)
            else:
                self.write_text("Command {} does not exist".format(command))
        else:
            self.do_help_response()
