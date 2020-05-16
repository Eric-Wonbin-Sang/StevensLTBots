import datetime
from dateutil import parser

from LTInfo import TimeRange
import Stevens


class Worker:

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.day_timerange_list_dict = kwargs.get("day_timerange_list_dict")
        self.total_hours = self.get_total_hours()    # datetime.time object

    def get_total_hours(self):
        total_seconds = 0
        for day_code in self.day_timerange_list_dict:
            total_seconds += sum([timerange.delta.seconds for timerange in self.day_timerange_list_dict[day_code]])
        return datetime.timedelta(seconds=total_seconds)

    def __str__(self, day_code_list=None):

        if day_code_list is None:
            day_code_list = Stevens.get_day_code_list()

        ret_str = "{}".format(self.name)
        for dc_i, day_code in enumerate(day_code_list):
            curr_response = ""
            for day_key in self.day_timerange_list_dict:
                if day_key.lower() == day_code:
                    curr_response = "\n\tDay: {} | ".format(day_key) + ", ".join(
                        [time_range.__str__() for time_range in self.day_timerange_list_dict[day_key]])
                    break
            if curr_response == "":
                curr_response = "\n\t{} does not work on day {}".format(self.name, day_code)
            ret_str += curr_response
        return ret_str


def get_worker_list(lt_sheets):

    value_list_list = lt_sheets.value_l_l_dict["work"]
    key_list = value_list_list[0][1:]

    worker_list = []

    prev_name = ""

    day_timerange_list_dict = {}
    for i, row in enumerate(value_list_list[1:]):
        curr_name = row[0]
        if i == 0:
            prev_name = curr_name
        if curr_name == "":
            curr_name = prev_name

        if curr_name == prev_name:
            for ts_i, time_slot in enumerate(row[1:]):
                if time_slot != "":

                    time_list = []
                    for time in time_slot.split("-"):
                        parsed_datetime = parser.parse(time)
                        # time_list.append(datetime.time(hour=parsed_datetime.hour, minute=parsed_datetime.minute))
                        time_list.append(parsed_datetime)
                    time_range = TimeRange.TimeRange(*time_list)
                    if key_list[ts_i] in day_timerange_list_dict:
                        day_timerange_list_dict[key_list[ts_i]].append(time_range)
                    else:
                        day_timerange_list_dict[key_list[ts_i]] = [time_range]
        else:
            worker_list.append(Worker(name=prev_name, day_timerange_list_dict=day_timerange_list_dict))
            day_timerange_list_dict = {}
            for ts_i, time_slot in enumerate(row[1:]):
                if time_slot != "":
                    time_list = []
                    for time in time_slot.split("-"):
                        parsed_datetime = parser.parse(time)
                        # time_list.append(datetime.time(hour=parsed_datetime.hour, minute=parsed_datetime.minute))
                        time_list.append(parsed_datetime)
                    time_range = TimeRange.TimeRange(*time_list)
                    if key_list[ts_i] in day_timerange_list_dict:
                        day_timerange_list_dict[key_list[ts_i]].append(time_range)
                    else:
                        day_timerange_list_dict[key_list[ts_i]] = [time_range]

        prev_name = curr_name
    worker_list.append(Worker(name=prev_name, day_timerange_list_dict=day_timerange_list_dict))

    return worker_list


def get_response(lt_sheets, command_list=None):
    worker_list = get_worker_list(lt_sheets)
    day_code_list = Stevens.get_day_code_list(command_list)
    return "\n".join([worker.__str__(day_code_list) for worker in worker_list])
