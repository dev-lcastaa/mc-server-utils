def print_options(list_of_options):
    for num, option in enumerate(list_of_options):
        print("[ " + str(num + 1) + " ] - " + option)
    print()


def print_menu_header(header):
    print("----------[ " + header + " ]----------")
    print()


def prompt_for_selection(msg):
    print('-------------------------------')
    return int(input(msg + ": "))


def prompt_for_input(msg):
    print('-------------------------------')
    return str(input(msg + ": "))
