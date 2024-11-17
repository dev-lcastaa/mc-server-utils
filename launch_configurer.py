import json

import printer
import utils


# Configuration Menu Selection
def launch_config():
    utils.check_for_config_dir("templates")
    printer.print_menu_header('Config Menu')
    options = ['Create launch template', 'Edit launch template', 'Delete launch template']
    printer.print_options(options)
    choice = printer.prompt_for_selection('Your choice ->')
    if choice == 1:
        print()
        create()
    elif choice == 2:
        print()
        edit()
    elif choice == 3:
        print()
        delete()
    else:
        exit(2)

# Allows you to create a new template
def create():
    # Allows you to select an EC2 instance ID
    print()
    printer.print_menu_header('Select EC2 ID')
    list_of_ec2 = utils.return_list_of_ec2()
    printer.print_options(list_of_ec2)
    target_ec2 = 0
    while target_ec2 == 0 or target_ec2 > len(list_of_ec2):
        target_ec2 = printer.prompt_for_selection('Your choice ->')
    target_ec2 = list_of_ec2[target_ec2 - 1]
    print()

    # Allows you to select an Elastic Ip Allocation ID
    print()
    printer.print_menu_header('Select Elastic Ip')
    list_of_elastic_id = utils.return_list_of_elastic_ip()
    printer.print_options(list_of_elastic_id)
    target_elastic_ip = 0
    while target_elastic_ip == 0 or target_elastic_ip > len(list_of_elastic_id):
        target_elastic_ip = printer.prompt_for_selection('Your choice ->')
    target_elastic_ip = list_of_elastic_id[target_elastic_ip - 1]
    print()

    # Extracts the Public IP from the selected Elastic IP
    print()
    printer.print_menu_header('Obtaining public IP')
    cmd = ['aws', 'ec2', 'describe-addresses', '--allocation-ids', target_elastic_ip]
    data = utils.run_command_and_capture_output(cmd)
    address_data = json.loads(data)
    public_ip = address_data['Addresses'][0]['PublicIp']
    print("The public IP is: " + public_ip)
    print()

    # Prompts for RCON Password
    print()
    rcon_pass = printer.prompt_for_input('RCON Password ->')
    print()

    # Prompts for RCON Port
    rcon_port = int(printer.prompt_for_input('RCON Port ->'))
    print()

    # Prompts for Server RAM
    ram = int(printer.prompt_for_input('Run with GB of RAM->'))
    print()

    # Prompts for Mod loader runner type
    runner = printer.prompt_for_input('Mod Loader type ->')
    print()

    # Prints a summary of the configuration
    printer.print_menu_header('Summary')
    print(f'target_ec2: {target_ec2}')
    print(f'target_elastic_ip: {target_elastic_ip}')
    print(f'public_ip: {public_ip}')
    print(f'rcon_pass: {rcon_pass}')
    print(f'rcon_port: {rcon_port}')
    print(f'ram: {ram}')
    print(f'runner: {runner}')

    # Saves Template or Aborts
    print()
    printer.print_menu_header('Save Template?')
    options = ['Save', 'Abort']
    printer.print_options(options)
    select = int(printer.prompt_for_selection('Make your selection'))
    if select == 1:
        name = printer.prompt_for_input('Enter Name of Template') + ".json"
        data = {
            "target_ec2": target_ec2,
            "target_elastic_ip": target_elastic_ip,
            "association_id": "",
            "public_ip": public_ip,
            "rcon_pass": rcon_pass,
            "rcon_port": rcon_port,
            "ram": ram,
            "runner" : runner
        }
        utils.dump_to_file(data, name)
    elif select == 2:
        launch_config()
    else:
        exit(2)

# Allows you to edit templates
def edit():
    pass

# Allows you to delete templates
def delete():
    pass
