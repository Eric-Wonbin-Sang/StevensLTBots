
class URL:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return "{}: {}".format(self.name, self.url)


def get_url_list(lt_sheets):
    url_list = []
    for data_list in lt_sheets.value_l_l_dict["urls"][1:]:
        name, url = data_list
        url_list.append(URL(name, url))
    return url_list


def get_response(lt_sheets, command_list):
    url_list = get_url_list(lt_sheets)
    return "\n".join([url.__str__() for url in url_list])


def get_spec_url(lt_sheets, keyword):
    for url in get_url_list(lt_sheets):
        if url.name == keyword:
            return url.url
    return None
