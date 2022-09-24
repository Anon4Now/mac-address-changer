#!/usr/bin/env python3

import subprocess
import random
import optparse
import re
import string


# pseudo num generator [1-99]
def genSeedVal():
    x = random.randint(1, 99)
    return x


# func for arg handling at the CLI
def get_args():
    parser = optparse.OptionParser()  # call the optparse module and init the class

    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address")  # generate options for args
    parser.add_option("-r", "--random", dest="mac_choice",
                      help="Use this flag to generate a random MAC address (e.g. --random random")  # generate options for args
    parser.add_option("-s", "--static", dest="mac_choice",
                      help="Use this flag to create a new MAC address - has to begin with 00 (e.g. --static 00:11:22:33:44:55")  # generate options for args
    parsingInput = parser.parse_args()

    (options, args) = parsingInput

    if not options.interface:  # provide inline error-handling if needed args are not provided
        parser.error("[-] Please specify an interface, --help for more info")
    elif not options.mac_choice:
        parser.error("[-] Please specify a MAC address flag, --help for more info")
    else:
        return options


outArgs = get_args()


# take input and return pseudo random character
def genRandomCharacters(inputVal):
    letters = ['a', 'b', 'c', 'd', 'e', 'f']
    numbers = string.digits

    if inputVal == 'even':
        resultLetter = random.choice(letters)
        return resultLetter
    elif inputVal == 'odd':
        resultNumber = ''.join(random.choice(numbers) for i in range(1))
        return resultNumber


# generate random concatenated alphanum string between [0-9 a-f] (e.g. a4)
def genRandomMACOctet():
    resultNumber = ''
    resultLetter = ''

    if genSeedVal() % 2 != 0:
        resultNumber += genRandomCharacters('odd')
    else:
        resultLetter += genRandomCharacters('even')

    if genSeedVal() % 2 == 0:
        resultNumber += genRandomCharacters('odd')
    else:
        resultLetter += genRandomCharacters('even')

    return resultNumber + resultLetter


# regex extractor that will capture string after "ether" if possible
def regexFunc():
    readIfconfigOutput = subprocess.check_output(["ifconfig", outArgs.interface])  # read the current ifconfig settings
    decodedBytesObj = readIfconfigOutput.decode('utf-8')  # decode from bytes to utf-8
    searchForMACAddress = re.search(rf"(?<=ether\s)([\w:]*)(?=\s)",
                                    decodedBytesObj)  # regex to parse MAC address string
    return searchForMACAddress


# takes input and evaluates to see if none-type
def macArgParseFunc(inputVar):
    if not regexFunc():  # if MAC address doesn't exist, that means interface is incorrect
        return None
    else:  # if MAC address does exist and was extracted
        if inputVar == "random":  # check what arg was input before deciding output
            random_mac = f'00:{genRandomMACOctet()}:{genRandomMACOctet()}:{genRandomMACOctet()}:{genRandomMACOctet()}:{genRandomMACOctet()}'
            return random_mac
        elif "00:" in inputVar:
            return inputVar
        else:
            return 'invalid options'


# parse list of subprocess args and make the call to OS
def subCallRepeat(callList):
    subprocess.call(callList)


# main func for script that starts calls
def subCall():
    getMACString = macArgParseFunc(outArgs.mac_choice)
    if not getMACString:  # if interface was incorrectly selected
        print(f'[-] {outArgs.interface} does not have a MAC address, please enter a valid interface')
    elif getMACString == 'invalid options':  # if something other than random or static was selected
        print('[-] MAC flags are not valid, please refer to --help')
    else:  # user entered everything correctly
        print(f'[+] Bringing {outArgs.interface} down')
        subCallRepeat(["ifconfig", outArgs.interface, "down"])
        print(f'[+] Attempting MAC address change to {getMACString}')
        subCallRepeat(["ifconfig", outArgs.interface, "hw", "ether", getMACString])
        print(f'[+] Bringing {outArgs.interface} up')
        subCallRepeat(["ifconfig", outArgs.interface, "up"])
        return getMACString


# check to see if MAC address change occurred successfully
def checkOutput():
    newMACAddress = subCall()  # get copy of new MAC address

    if not newMACAddress:  # skip func if none-type is returned
        pass
    else:  # compare the current MAC address to the 'new' MAC address, if same than change was successful
        getCurrentAddress = regexFunc()
        capturedGroup = getCurrentAddress.group(0)

        if newMACAddress == capturedGroup:
            print(f'[+] The MAC Address was successfully changed to {newMACAddress}')
        else:
            print(f'[-] The MAC Address changed failed, MAC Address is still {capturedGroup}')


if __name__ == '__main__':
    checkOutput()
