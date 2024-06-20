import json

import printer
import utils
import os


# Main Configuration Menu
def launch_config():
    utils.check_for_config_dir("templates")
    printer.print_menu_header('Config Menu')
    options = ['Create New Launch Template', 'Edit Launch Template', 'Delete Launch Template']
    printer.print_options(options)
    choice = printer.prompt_for_selection('Make your selection')
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
    print('--[ Choose which EC2 to target ]--')
    utils.return_list_of_ec2()
    target_ec2 = printer.prompt_for_input('Enter EC2 ID')
    print()
    print('-- [ Choose which Elastic IP to target ]--')
    utils.return_list_of_elastic_ip()
    target_elastic_ip = printer.prompt_for_input('Enter Elastic IP ID')
    print()
    print('-- [ Extracting Public IP ] --')
    cmd = ['aws', 'ec2', 'describe-addresses', '--allocation-ids', target_elastic_ip]
    data = utils.run_command_and_capture_output(cmd)
    address_data = json.loads(data)
    public_ip = address_data['Addresses'][0]['PublicIp']
    print("Public IP = " + public_ip)
    print()
    print('--[ MC RCON Password ]--')
    rcon_pass = printer.prompt_for_input('Enter RCON Password')
    print()
    print('-- [ MC RCON Port ]--')
    rcon_port = int(printer.prompt_for_input('Enter RCON Port'))
    print()
    print('-- [ RAM Allocation ]--')
    ram = int(printer.prompt_for_input('How many GB?'))
    print(f"""
    -- [ Summary ] --
    target_ec2: {target_ec2}
    target_elastic_ip: {target_elastic_ip}
    public_ip: {public_ip}
    rcon_pass: {rcon_pass}
    rcon_port: {rcon_port}
    ram: {ram}
    """)
    print()
    print()
    print('--[ Save Template]--')
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
            "ram": ram
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
