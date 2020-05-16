
class Lamp:

    def __init__(self, model, amount, update_date):
        self.model = model
        self.amount = amount
        self.update_date = update_date

    def __str__(self):
        return "Model: {}  Amt: {}  Updated: {}".format(self.model, self.amount, self.update_date)


def get_lamp_list(lt_sheets):
    lamp_list = []
    for data_list in lt_sheets.value_l_l_dict["lamp"][1:]:
        model, amount, update_date = data_list
        lamp_list.append(Lamp(model, amount, update_date))
    return lamp_list


def get_response(lt_sheets, command_list):
    lamp_list = get_lamp_list(lt_sheets)
    return "\n".join([worker.__str__() for worker in lamp_list])
