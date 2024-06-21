import subprocess
import os
import json


# Checks for AWS CLI is installed
def check_for_aws_cli():
    print("----------[Checking for AWS CLI]----------")
    cmd = ['aws', '--version']
    name = 'AWS CLI'
    check_for_dependency(cmd, name)


# Checks to see if MC RCON is installed
def check_for_mcrcon():
    print('----------[Checking for MC RCON]----------')
    cmd = ['pip', 'show', 'mcrcon']
    name = 'MCRCON'
    check_for_dependency(cmd, name)


# Checks to see if a Program is installed
def check_for_dependency(cmd, name_of_dependency):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(name_of_dependency + " is installed.")
            print()
        else:
            print(name_of_dependency + " is not installed.")
            print()
    except FileNotFoundError:
        print(name_of_dependency + " is not installed.")


# Runs a command the results in JSON used for AWS CMDS
def run_command_and_capture_output(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
        return None


# Runs a command with no output capture
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=False, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the command: {e}")
        return None


# Runs an AWS CLI CMD to return a list of EC2 Instance IDs
def return_list_of_ec2():
    result = os.popen('aws ec2 describe-instances --query "Reservations[*].Instances[*].InstanceId" --output text')
    list_of_ec2 = result.read().split('\n')
    return list_of_ec2


# Runs an AWS CLI CMD to return ELASTIC IP Allocation IDs
def return_list_of_elastic_ip():
    result = os.popen('aws ec2 describe-addresses --query "Addresses[*].AllocationId" --output text')
    list_of_elastic_ip = result.read().split('\n')
    return list_of_elastic_ip


# Checks to see if a file exists
def check_for_file(filename, path):
    files = os.listdir(path)
    for file in files:
        if file == filename:
            return True
    return False


# Loads a JSON file to extract parameters
def return_config_param(config_file):
    os.chdir('templates')
    with open(config_file, 'r', encoding='UTF-8') as file_data:
        config_data = json.loads(file_data.read())
        return config_data


# Offloads a JSON Data variable to a file
def dump_to_file(data, filename):
    try:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(root_dir, 'templates')
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
            print(f"Created directory: {templates_dir}")

        file_path = os.path.join(templates_dir, filename)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            file.flush()

    except Exception as e:
        print(f"An error occurred: {e}")


# Checks for the templates dir
def check_for_config_dir(folder_name):
    # Get the current working directory
    current_path = os.getcwd()
    # Combine the current path with the folder name
    folder_path = os.path.join(current_path, folder_name)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        pass
    else:
        print(f"The folder '{folder_name}' does not exist.")
        print('Creating now')
        os.makedirs(folder_path, exist_ok=True)


# Gets all launch templates
def get_launch_templates():
    directory = 'templates'
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files
