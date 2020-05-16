
class Contact:

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return "{}: {}".format(self.name, self.number)


def get_contact_list(lt_sheets):
    contact_list = []
    for data_list in lt_sheets.value_l_l_dict["contact"][1:]:
        if "".join(data_list) == "":
            contact_list.append(None)
        else:
            contact_list.append(Contact(*data_list))
    return contact_list


def get_response(lt_sheets, command_list):
    contact_list = get_contact_list(lt_sheets)
    return "\n".join([contact.__str__() if contact else "" for contact in contact_list])
