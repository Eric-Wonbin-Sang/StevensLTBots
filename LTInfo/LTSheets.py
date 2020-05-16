from General import Google


class LTSheets:

    def __init__(self):

        self.value_l_l_dict = {sheet.title: sheet.get_all_values() for sheet in Google.get_google_sheets("LT Sheets")}

    def update_value_l_l_dict(self):    # not needed?
        try:
            self.value_l_l_dict = {sheet.title: sheet.get_all_values() for sheet in
                                   Google.get_google_sheets("LT Sheets")}
            return True
        except Exception as e:
            return e

    def sheet_to_simple_response(self, doc_name):
        ret_str = ""
        for i, row in enumerate(self.value_l_l_dict[doc_name]):
            if i != 0:
                ret_str += "\n"
            for cell in row:
                ret_str += cell
        return ret_str
