#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@Author  :   Minxie
@License :   (C) Copyright 2013-2020
@Contact :   Minx@xilinx.com
@Software:   multi alveo card shell upgrade
@File    :   shell_program.py
@Time    :   2020-12-01
@Desc    :
'''

import os
import sys
import subprocess

# import argparse
# parser = argparse.ArgumentParser(prog='shell_program', description='used for upgrade xilinx alveo card shell')
# parser.add_argument('-f', metavar='N', type=str, help='the path of shell file')
# args = parser.parse_args()

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: python shell_program <shell_file> <card_bdf>'
        exit(1)

    shell_bin = sys.argv[1]
    dev_bdf = sys.argv[2]
        
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
    if (os.path.exists(shell_bin) == False):
        print "can not find the shell file, Please input correct file path. Aborting."
        sys.exit(1)

    # get the local bdf list
    drv_list = ['xclmgmt']
    cmd = subprocess.Popen(args='lspci -vd 10ee:', stdout=subprocess.PIPE, shell=True)
    out, err = cmd.communicate()

    print out
    if 'Xilinx Corporation Device' in out:
         if any(drv in out for drv in drv_list):
            local_bdf = out[0:8]
            print ('local_bdf',local_bdf)
    else:
        print "Can not find xilinx device, Please Check your system"
        exit(-1)

    # /opt/xilinx/xrt/bin/xbmgmt flash --shell --primary /proj/U30/full\ bin/v1r02/test/U30_TEST_v1r07r.bin --card 87:00.0
