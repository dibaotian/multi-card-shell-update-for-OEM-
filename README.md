# multi-card-shell-update-for-OEM-
this is a python tool simultaneous upgrade multi-card for OEM

## Function
###This script support both single ALVEO card and multiple cards shell program simultaneously 
###It will create dedicate burn process for each card, So the multi-card update took time is same as one card
##usage:
###python3 shell_program.py <shell_file> <card_bdf>
###Program all u30 card in the system
### #>sudo python3 shell_program.py ../U30_shell.bin all
###Program specified card
### #>sudo python3 shell_program.py ../U30_shell.bin 86:00.0
##Restriction 
###Execute the script need root privilege
###Need the Python3 support
###The script temporally just support ALVEO U30
###Verified under Vitis/XRT 2020.1


