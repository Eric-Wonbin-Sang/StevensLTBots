
class Box:

    def __init__(self, name, code):

        self.name = name
        self.code = code

    def __str__(self):
        return "Name: {}\tCode: {}".format(self.name, self.code)


def get_box_list(lt_sheets):
    box_list = []
    for data_list in lt_sheets.value_l_l_dict["box"][1:]:
        name, code = data_list
        box_list.append(Box(name, code))
    return box_list


def get_response(lt_sheets, command_list):
    box_list = get_box_list(lt_sheets)
    return "\n".join([box.__str__() for box in box_list])
