import printer
import utils
import server_manager as manager
import launch_configurer as configure

# Pre-Fight Check
utils.check_for_aws_cli()
utils.check_for_mcrcon()

# Main Menu Logic
printer.print_menu_header('Main Menu')
main_options = ['Start Server', 'Stop Server', 'Launch Configurations']
printer.print_options(main_options)
choice = printer.prompt_for_selection('Make your selection')
if choice == 1:
    print()
    manager.launch_sequence()
elif choice == 2:
    print()
    manager.abort()
elif choice == 3:
    print()
    configure.launch_config()
else:
    print('Invalid choice try again')
    exit(2)
