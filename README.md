# MAC Address Changer

This tool can be used in conjunction with other red-team tactics to evade MAC address filtering by standard firewall configurations.

A couple example firewalls that use MAC Address filtering are in the links below:
 - [Cisco](https://www.cisco.com/assets/sol/sb/RV180W_Emulators/RV180W_Emulator_v1.0.3.14/help/en_US/firewall11.htm#:~:text=To%20enable%20MAC%20address%20filtering,box%20to%20disable%20this%20feature.)
 - [Sophos](https://support.sophos.com/support/s/article/KB-000035664?language=en_US)
 - [Sonicwall](https://www.sonicwall.com/support/knowledge-base/configuring-the-mac-filter-list/170505502972853/)


## Tool Functionality:

- Will allow the generation of a random MAC address
- Will allow the generation of a manually created MAC address
- Will allow for the '-h or --help' flag to be provided for more information
- This tool expects two arguments:
  - '-i or --interface' with default interface (e.g. eth0)
  - '-r or --random' with option 'random' OR '-s or --static' with manual MAC (e.g. 00:11:22:33:44:55)


## Tool Requirements:

- To use the default functionality of this tool, no additional libraries or modules are needed
- This tool needs a ![small](https://user-images.githubusercontent.com/80045938/148561762-9590c4a1-a424-4c7b-a0fb-68190fb7a31c.png) [Python](https://www.python.org/downloads/) interpreter, v3.6 or higher due to string interpolation


## Quick Notes:

- This was designed in its current state to work with a Linux OS. However if desired it can be altered to fit a Windows OS, the subprocess calls will need to change
- I wrote this with Python 2.7 capabilities as well, I commented out that code to avoid errors running in Python3



## Using the Tool:

#### Help Menu: 
Run the binary or standalone exe and pass the '-h or --help flag'.
![help_check](https://user-images.githubusercontent.com/80045938/149645154-c50017e8-0c30-4612-a209-a588d6744cd9.gif)

#### Generate Random MAC Address: 
Run the binary or standalone exe and pass the '-r or --random flag'.
![random_mac](https://user-images.githubusercontent.com/80045938/149645242-ad0eea1a-ddaf-4f4e-8c26-8cd43d4124d8.gif)

#### Generate Static MAC Address: 
Run the binary or standalone exe and pass the '-s or --static flag'.
![static_mac](https://user-images.githubusercontent.com/80045938/149645266-76b62821-5c99-41fd-8540-aead907a8d38.gif)


