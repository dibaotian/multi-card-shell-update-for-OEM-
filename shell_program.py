import os
import sys

import argparse
parser = argparse.ArgumentParser(prog='shell_program', description='used for upgrade xilinx alveo card shell')
parser.add_argument('-f', metavar='N', type=str, help='the path of shell file')


args = parser.parse_args()
print(args.accumulate(args.integers))


# program need root user
if os.geteuid() != 0:
    print "This program must be run as root. Aborting."
    sys.exit(1)


# check if the xrt is installed
file = '/opt/xilinx/xrt/bin/xbmgmt'
if (os.path.exists(file) == False):
    print "Please Check if the XRT is installed. Aborting."
    sys.exit(1)



# check if the programed bin is exist
# if (os.path.exists() == False):
#     print "Please Check if the XRT is installed. Aborting."
#     sys.exit(1)

# /opt/xilinx/xrt/bin/xbmgmt flash --shell --primary /proj/U30/full\ bin/v1r02/test/U30_TEST_v1r07r.bin --card 87:00.0
