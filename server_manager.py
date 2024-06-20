import json
import os
from time import sleep

import printer
import utils


# Uses a launch configuration to start the server
def launch_sequence():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print('--[ Select your launch template ]--')
    files = utils.get_launch_templates()
    template = 0
    choice = 0
    printer.print_options(files)
    while choice == 0:
        choice = printer.prompt_for_selection("choose a template")
    template = files[choice - 1]
    print()
    print("Chosen Template: " + template)
    print()
    options = [' !!- LAUNCH -!!', 'ABORT']
    printer.print_options(options)
    choice = printer.prompt_for_selection('Choose what to do')
    os.chdir(root_dir)
    if choice == 1:
        start_server(template)
    elif choice == 2:
        launch_sequence()
    else:
        exit(2)


def abort():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print('--[ Select your launch template ]--')
    files = utils.get_launch_templates()
    template = 0
    choice = 0
    printer.print_options(files)
    while choice == 0:
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
    print(template)
    print()
    print('-- ASSOCIATING ELASTIC IP WITH EC2 INSTANCE --')
    cmd = ['aws', 'ec2', 'associate-address', '--instance-id', data['target_ec2'], '--allocation-id', data['target_elastic_ip']]
    association_id_response = utils.run_command_and_capture_output(cmd)
    association_id_data = json.loads(association_id_response)
    association_id = association_id_data['AssociationId']
    sleep(5)
    print()
    print('-- STARTING EC2 INSTANCE --')
    cmd = ['aws', 'ec2', 'start-instances', '--instance-ids', data['target_ec2']]
    utils.run_command(cmd)
    sleep(10)
    print()
    print('-- LAUNCHING JAVA MC SERVER --')
    print('Waiting for server to initialize...it can be 1 minute..please wait..')
    sleep(90)
    ram_size = str(data['ram'])

    launch_cmd = f'commands=["cd /home/admin/", "screen -dms minecraft java -Xmx{ram_size}G -jar server.jar nogui", "echo \\"Server started\\""]'
    cmd = ['aws', 'ssm', 'send-command', '--instance-ids', data['target_ec2'], '--document-name',
           'AWS-RunShellScript', '--comment', 'Launch Minecraft Server', '--parameters', launch_cmd]
    utils.run_command(cmd)
    print()
    print("-- MINECRAFT SERVER HAS BEEN STARTED -- ")
    print("IP: " + data['public_ip'])
    print()
    print("SAVING ASSOCIATION ID TO TEMPLATE..")
    new_data = {
        "target_ec2": data['target_ec2'],
        "target_elastic_ip": data['target_elastic_ip'],
        "association_id": association_id,
        "public_ip": data['public_ip'],
        "rcon_pass": data['rcon_pass'],
        "rcon_port": data['rcon_port'],
        "ram": data['ram']
    }
    utils.dump_to_file(new_data, template)


# Uses a launch configuration to stop the server
def stop_server(template):
    data = utils.return_config_param(template)
    rcon_pass = data['rcon_pass']
    rcon_port = data['rcon_port']
    ip_address = data['public_ip']
    ec2_instance = data['target_ec2']
    association_id = data['association_id']

    print('Saving server using RCON')
    sleep(5)
    save_mc_server_cmd = f'echo "save-all" | mcrcon {ip_address} --password {rcon_pass} --port {rcon_port}'
    os.system(save_mc_server_cmd)
    sleep(5)
    print()

    print('Now stopping server using RCON')
    sleep(5)
    stop_mc_server_cmd = f'echo "stop" | mcrcon {ip_address} --password {rcon_pass} --port {rcon_port}'
    os.system(stop_mc_server_cmd)

    print('Now stopping EC2 Instance')
    stop_ec2_instance_cmd = ['aws', 'ec2', 'stop-instances', '--instance-ids', data['target_ec2']]
    utils.run_command(stop_ec2_instance_cmd)
    sleep(5)
    print()
    print('Now disassociating Elastic IP from instance')
    disassociate_elastic_ip_cmd = ['aws', 'ec2', 'disassociate-address', '--association-id', data['association_id']]
    utils.run_command(disassociate_elastic_ip_cmd)
    sleep(5)
    print()
    print('MCSERVER WAS SUCCESSFULLY STOPPED')
    exit(100)



