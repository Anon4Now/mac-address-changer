"""Module containing the functions to alter a Linux OS MAC Address"""

# Standard Library imports
import subprocess
import random
import optparse
import re
import string
from typing import Optional, Match, List

# Local App imports
from errors import NoMacAddressFoundError


def get_args() -> optparse.OptionParser.parse_args:
    """
    Function to handle the CLI arguments passed by the user. Will
    return an error message if the required args are not passed.

    :return: The CLI options passed from the user
    """
    parser = optparse.OptionParser()  # call the optparse module and init the class

    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address")  # generate options for args
    parser.add_option("-r", "--random", dest="mac_choice",
                      help="Use this flag to generate a random MAC address (e.g. --random random")  # generate options for args
    parser.add_option("-s", "--static", dest="mac_choice",
                      help="Use this flag to create a new MAC address - has to begin with 00 (e.g. --static 00:11:22:33:44:55")  # generate options for args
    parsing_input = parser.parse_args()

    (options, args) = parsing_input

    if not options.interface:  # provide inline error-handling if needed args are not provided
        parser.error("[-] Please specify an interface, --help for more info")
    elif not options.mac_choice:
        parser.error("[-] Please specify a MAC address flag, --help for more info")
    else:
        return options


out_args = get_args()  # get the user and store in global var


def gen_random_mac_address(mac_str: str) -> str:
    """
    Recursive function that will generate a random
    MAC address string and return it.

    :param mac_str: (required) Starting point of the function, all MAC addresses start with ('00:')
    :return: A MAC address string (e.g., 00:17:AE:59:90:0D)
    """
    letters = ['A', 'B', 'C', 'D', 'E', 'F']  # letters that comply with Hex chars
    numbers = string.digits
    out_char = mac_str

    if len(out_char) < 17:  # check to see if a full MAC has been created
        rand_int = random.randint(1, 99)  # get a seed number
        #  update the var with either a string-num (i.e., '1', '2') OR a string alpha-char (i.e. 'A', 'B')
        out_char += random.choice(letters) if rand_int % 2 == 0 else ''.join(random.choice(numbers) for _ in range(1))
        if ":" not in out_char[-2] and ":" not in out_char[
            -1]:  # check to see if the last 2 chars in the string are not a colon
            out_char += ":"
        gen_random_mac_address(out_char)  # start the recursive call

    else:
        return out_char  # return the full MAC string


def check_mac_address_exists() -> Optional[Match[str]]:
    """
    Function that performs a check parse the user provided
    CLI input and use this to verify that the MAC address exists.
    If the MAC address does exist in the CLI args, return the

    :return: Will either return a string containing a MAC address or None
    """
    read_ifconfig_output = subprocess.check_output(
        ["ifconfig", out_args.interface])  # read the current ifconfig settings
    decoded_bytes_obj = read_ifconfig_output.decode('utf-8')  # decode from bytes to utf-8
    search_for_mac_address = re.search(rf"(?<=ether\s)([\w:]*)(?=\s)",
                                       decoded_bytes_obj)  # regex to parse MAC address string
    return search_for_mac_address


def subprocess_repeat_call(call_list: List[str]) -> None:
    """
    Function that actually performs the subprocess calls based
    on the commands in the param list.
    :param call_list: List that contains commands to execute against the OS
    :return: None
    """
    subprocess.call(call_list)


# main func for script that starts calls
def subprocess_call() -> str or bool:
    """
    Function that creates the subprocess commands as List[str] and passes
    them to the subprocess call function.

    :return: None
    """
    if check_mac_address_exists():
        if 'random' or '00' in out_args.interface:  # user entered everything correctly
            mac_string = gen_random_mac_address('00:') if 'random' in out_args.interface else out_args.interface
            print(f'[+] Bringing {out_args.interface} down')
            subprocess_repeat_call(["ifconfig", out_args.interface, "down"])
            print(f'[+] Attempting MAC address change to {mac_string}')
            subprocess_repeat_call(["ifconfig", out_args.interface, "hw", "ether", mac_string])
            print(f'[+] Bringing {out_args.interface} up')
            subprocess_repeat_call(["ifconfig", out_args.interface, "up"])
            return mac_string
    else:
        raise NoMacAddressFoundError(
            f'[-] {out_args.interface} does not have a MAC address, please enter a valid interface')


if __name__ == '__main__':

    try:
        set_mac_address = subprocess_call()  # set the new MAC address

        if set_mac_address:
            # compare the current MAC address to the 'new' MAC address, if same than change was successful
            get_current_mac_address = check_mac_address_exists().group(0)

            if set_mac_address == get_current_mac_address:
                print(f'[+] The MAC Address was successfully changed to {set_mac_address}')
            else:
                print(f'[-] The MAC Address changed failed, MAC Address is still {get_current_mac_address}')
    except NoMacAddressFoundError as e:
        print(e)
