def print_options(list_of_options):
    # Remove empty strings from the list
    filtered_options = [option for option in list_of_options if option]

    # Print the options
    for num, option in enumerate(filtered_options):
        print("[" + str(num + 1) + "] •---• " + option)
    print()


def print_menu_header(header):
    print("═════════[ " + header + " ]═════════")
    print()


def prompt_for_selection(msg):
    print('═════════════════════════════════════')
    return int(input(msg + ": "))


def prompt_for_input(msg):
    print('════════════════════════════════')
    return str(input(msg + ": "))
