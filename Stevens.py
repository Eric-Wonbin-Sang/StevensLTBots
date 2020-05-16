import datetime
import requests

from General import Functions

day_code_dict = {"m": "monday",
                 "t": "tuesday",
                 "w": "wednesday",
                 "r": "thursday",
                 "f": "friday",
                 "s": "saturday",
                 "u": "sunday",
                 "monday": "m",
                 "tuesday": "t",
                 "wednesday": "w",
                 "thursday": "r",
                 "friday": "f",
                 "saturday": "s",
                 "sunday": "u"}


# ----------------------------------------------------------------------------------------------------------


def is_valid_day(data):
    return data.lower() in day_code_dict


def get_day_code_list(raw_day_list=None):
    if not raw_day_list:
        return [day_code_dict[datetime.datetime.today().strftime("%A").lower()]]
    day_code_list = []
    for raw_day in raw_day_list:
        day_code = day_code_dict.get(raw_day.lower()) if len(raw_day) > 1 else raw_day.lower()
        if day_code:
            day_code_list.append(day_code)
        else:
            day_code_list.append(raw_day)
    return day_code_list


def get_day_from_code(day_code):
    return day_code_dict[day_code.lower()]


def section_list_to_string(section_list):
    str_ret = ""
    for i, section in enumerate(section_list):
        if i != 0:
            str_ret += "\n"
        str_ret += "{}: {} - {} | {} ({})".format(get_day_from_code(section.day.lower())[:3].title(),
                                                  Functions.get_nice_time_format(section.start_time),
                                                  Functions.get_nice_time_format(section.end_time),
                                                  section.course_name,
                                                  section.professor)
    return str_ret


# ----------------------------------------------------------------------------------------------------------


class Section:

    def __init__(self, day, room, html_chunk):
        """
        str day
        str html_chunk: initial html part for parsing
        """
        self.html_chunk = html_chunk

        self.day = day
        self.room = room
        self.course_name, self.professor, self.start_time, self.end_time = self.get_data()

    def get_data(self):
        line = self.html_chunk.split("colspan=")[1]
        raw_course_name = line.split("<br>")[0].split(">")[1].split("(")[0]
        raw_professor, raw_times = line.split("<br>")[1].split("[")

        raw_times = raw_times[:-1].split("-")
        raw_times[1] = raw_times[1].split("]")[0]

        course_name = raw_course_name
        professor = raw_professor
        start_time = datetime.time(int(raw_times[0][:-2]), int(raw_times[0][-2:]))
        end_time = datetime.time(int(raw_times[1][:-2]), int(raw_times[1][-2:]))

        return course_name, professor, start_time, end_time

    def __str__(self):
        str_ret = "Course Name: {}\nProfessor: {}\nStart Time: {}\nEnd Time: {}\n".format(
            self.course_name,
            self.professor,
            self.start_time,
            self.end_time)
        return str_ret


class Room:

    def __init__(self, html_chunk):
        """
        str html_chunk: initial html part for parsing
        """
        self.html_chunk = html_chunk

        self.name = self.get_name()
        self.day_section_list_dict = self.get_day_section_list_dict()

    def get_name(self):
        return self.html_chunk[:self.html_chunk.index(">")]

    def get_day_section_list_dict(self):
        day_section_list_dict = {}
        html_list_list = [line for line in self.html_chunk.split("\n") if "</tr><tr><td>" in line]
        if len(html_list_list) != 1:
            print("Confusing input: section list html encountered 0 or 1+ lines")
            return day_section_list_dict

        html = html_list_list[0]
        for line in html.split("<tr><td>")[1:]:
            day = line[:line.index("</td>")].lower()
            section_list = [Section(day=day, room=self, html_chunk=html_chunk)
                            for html_chunk in line.split("bgcolor=")[1:]]
            day_section_list_dict[day.lower()] = section_list
        return day_section_list_dict

    def __str__(self):
        ret_str = "Room: {}".format(self.name)
        for day in self.day_section_list_dict:
            ret_str += "\n\t{}: ".format(day_code_dict[day.lower()])
            for section in self.day_section_list_dict[day]:
                ret_str += "\n{}".format("\t\t" + section.__str__().replace("\n", "\n\t\t"))
        return ret_str


class Stevens:

    def __init__(self, room_schedule_url):

        self.name = "Stevens Institute of Technology"\

        self.room_schedule_url = room_schedule_url
        self.room_list = self.get_room_list()
        self.prof_section_list_dict = self.get_prof_section_list_dict()

        self.time_updated = datetime.datetime.today()

    def get_room_list(self):
        r = requests.get(self.room_schedule_url)
        return [Room(html_chunk) for html_chunk in r.text.split('<b id=')[1:]]

    def get_prof_section_list_dict(self):
        prof_section_list_dict = {}
        for room in self.room_list:
            for day_key in room.day_section_list_dict:
                for section in room.day_section_list_dict[day_key]:
                    if section.professor in prof_section_list_dict:
                        prof_section_list_dict[section.professor] += [section]
                    else:
                        prof_section_list_dict[section.professor] = [section]
        return prof_section_list_dict

    def find_schedule(self):
        pass
