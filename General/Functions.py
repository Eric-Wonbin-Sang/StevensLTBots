import pickle
import os


def txt_doc_to_str(some_path):
    if os.path.exists(some_path):
        txt_doc = open(some_path, "r")
        str_ret = txt_doc.read()
        txt_doc.close()
    else:
        str_ret = "Path {} not found".format(some_path)
    return str_ret


def pickle_object(obj, path):
    print("Pickling {}".format(obj))
    pickle_out = open(path, "wb")
    pickle.dump(obj, pickle_out)
    pickle_out.close()
    print("Done pickling")


def remove_none_from_list(data_list):
    return [data for data in data_list if data is not None]


def string_to_command_list_list(string, command_name_list):

    raw_command_list = [part for part in string.lower().split(" ") if part != ""]

    start_index = None
    command_list_list = []
    for c_i, command in enumerate(raw_command_list):
        if command in command_name_list:
            if start_index is not None:
                command_list_list.append(raw_command_list[start_index:c_i])
            start_index = c_i
    last_command_list = raw_command_list[start_index:]
    if last_command_list:
        command_list_list.append(last_command_list)
    return command_list_list


def decrement_repeating_returns(string):
    str_ret = ""
    for part in string.split("\n"):
        str_ret += part
        if part == "":
            str_ret += "\n"
    return str_ret


def get_nice_time_format(some_time):
    return some_time.strftime("%I:%M%p")


def shift_string_block(string_block, spacer):
    return spacer + string_block.replace("\n", "\n{}".format(spacer))


def txt_to_dict(txt_path):
    ret_dict = {}
    for line in open(txt_path):
        key, value = [obj.strip() for obj in line.split(":")]
        ret_dict[key] = value
    return ret_dict


def get_curr_parent_dir(path_addition=None):
    return os.path.dirname(os.getcwd()) + path_addition if path_addition is not None else ""


def rotate_list_list(data_list_list):
    return [list(x) for x in zip(*data_list_list)]
