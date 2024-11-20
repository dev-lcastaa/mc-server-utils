import json
import os
from time import sleep

import printer
import utils


# Uses a launch configuration to start the server
def launch_sequence():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print()
    printer.print_menu_header('Choose a template')
    files = utils.get_launch_templates()
    template = 0
    choice = 0
    printer.print_options(files)
    while choice == 0:
        choice = printer.prompt_for_selection("Your choice ->")
    template = files[choice - 1]
    print()
    print("Selected ->: " + template)
    print()
    options = ['Start Server', 'Stop Server', 'Send Command', 'EXIT']
    printer.print_options(options)
    choice = printer.prompt_for_selection('Your Choice ->')
    os.chdir(root_dir)
    if choice == 1:
        start_server(template)
    elif choice == 2:
        launch_sequence()
    elif choice == 3:
        send_command(template)
    else:
        exit(2)

def abort():
    print()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    printer.print_menu_header('Select template')
    files = utils.get_launch_templates()
    template = 0
    choice = 0
    printer.print_options(files)
    while choice == 0 or choice > len(files):
        choice = printer.prompt_for_selection("choose a template")
    template = files[choice - 1]
    print()
    print("Chosen Template: " + template)
    print()
    print("Stopping server using template")
    print()
    stop_server(template)

def start_server(template):
    data = utils.return_config_param(template)
    printer.print_menu_header('Launching Server')
    print('Launching server with: ' + template)

    # Associates the target Elastic Ip to target EC2 Instance
    print()
    printer.print_menu_header('Associating elastic IP')
    cmd = ['aws', 'ec2', 'associate-address', '--instance-id', data['target_ec2'], '--allocation-id', data['target_elastic_ip']]
    association_id_response = utils.run_command_and_capture_output(cmd)
    association_id_data = json.loads(association_id_response)
    association_id = association_id_data['AssociationId']
    print('Attached Elastic IP to EC2 instance successfully!!')
    sleep(5)

    # Sends Command to AWS to start EC2 instance using the target_ec2 ID
    print()
    printer.print_menu_header('Starting EC2')
    cmd = ['aws', 'ec2', 'start-instances', '--instance-ids', data['target_ec2']]
    utils.run_command_and_capture_output(cmd)
    print('Started EC2 instance successfully...')
    sleep(5)

    # Sends CMD to Systems Manager Agent running on EC2 instance to launch MC Server
    print()
    printer.print_menu_header('Staring minecraft server')
    print('Waiting for server to initialize...it can be 1 minute..please wait..')
    sleep(75)
    ram_size = str(data['ram'])
    runner = data['runner']
    if runner == "forge":
        launch_cmd = f'commands=["cd /home/admin/", "screen -dms minecraft sudo bash run.sh", "echo \\"Server started\\""]'
        cmd = ['aws', 'ssm', 'send-command', '--instance-ids', data['target_ec2'], '--document-name',
               'AWS-RunShellScript', '--comment', 'Launch Minecraft Server', '--parameters', launch_cmd]
    elif runner == "neoforge":
        print("feature yet to be implemented")
        exit(1)
    else:
        launch_cmd = f'commands=["cd /home/admin/", "screen -dms minecraft java -Xmx{ram_size}G -jar server.jar nogui", "echo \\"Server started\\""]'
        cmd = ['aws', 'ssm', 'send-command', '--instance-ids', data['target_ec2'], '--document-name',
               'AWS-RunShellScript', '--comment', 'Launch Minecraft Server', '--parameters', launch_cmd]
    utils.run_command_and_capture_output(cmd)
    print()
    print('Minecraft server successfully started...')
    print()

    # Prompts user that Minecraft server was started
    printer.print_menu_header('Minecraft Server was STARTED')
    print("Server started on IP ->: " + data['public_ip'])
    print()

    # Prompts user program saving the association id to config template
    printer.print_menu_header('SAVING association ID to template')
    new_data = {
        "target_ec2": data['target_ec2'],
        "target_elastic_ip": data['target_elastic_ip'],
        "association_id": association_id,
        "public_ip": data['public_ip'],
        "rcon_pass": data['rcon_pass'],
        "rcon_port": data['rcon_port'],
        "ram": data['ram'],
        "runner": data['runner']
    }
    utils.dump_to_file(new_data, template)
    print('Saved the association id to template: ' + template + '...')
    print()
    printer.print_menu_header('Server was successfully started')

# allow the sending of commands to a running server
def send_command(template):
    print()
    command_to_send = printer.prompt_for_input('Enter CMD to Send: ')

    # offloads template data to variables to use with f''
    data = utils.return_config_param(template)
    rcon_pass = data['rcon_pass']
    ip_address = data['public_ip']

    save_mc_server_cmd = (f'mcrcon-nsg -H {ip_address} -p {rcon_pass} {command_to_send}')
    os.system(save_mc_server_cmd)





# Uses a launch configuration to stop the server
def stop_server(template):

    # offloads template data to variables to use with f''
    data = utils.return_config_param(template)
    rcon_pass = data['rcon_pass']
    rcon_port = data['rcon_port']
    ip_address = data['public_ip']
    ec2_instance = data['target_ec2']
    association_id = data['association_id']

    # Saves the server using an RCON CMD
    printer.print_menu_header('Saving minecraft server')
    save_mc_server_cmd = f'mcrcon-nsg -H {ip_address} -p {rcon_pass} save-all'
    os.system(save_mc_server_cmd)
    sleep(10)
    print('Saved Minecraft server state..')
    print()

    # Stops the minecraft server using an RCON CMD
    printer.print_menu_header('Stopping minecraft server')
    stop_mc_server_cmd = f'echo "stop" | mcrcon {ip_address} --password {rcon_pass} --port {rcon_port}'
    os.system(stop_mc_server_cmd)
    sleep(10)
    print('Stopped Minecraft server...')
    print()

    # Stops the target EC2 using the 'target_id' in template
    printer.print_menu_header('Now stopping EC2 Instance')
    stop_ec2_instance_cmd = ['aws', 'ec2', 'stop-instances', '--instance-ids', data['target_ec2']]
    utils.run_command_and_capture_output(stop_ec2_instance_cmd)
    sleep(10)
    print('Stopped EC2 instance...')
    print()

    # Disassociates elastic IP from EC2 using 'association_id' in template
    printer.print_menu_header('Disassociating elastic IP')
    disassociate_elastic_ip_cmd = ['aws', 'ec2', 'disassociate-address', '--association-id', data['association_id']]
    utils.run_command(disassociate_elastic_ip_cmd)
    sleep(10)
    print('Disassociated Elastic Ip from EC2...')
    print()

    # Prompts user that server was stopped
    printer.print_menu_header('Minecraft server was stopped')
    sleep(5)
    exit(100)



