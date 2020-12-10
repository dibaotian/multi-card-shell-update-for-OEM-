#!/usr/bin/python3
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
import multiprocessing
import time
import argparse
import hashlib

def md5sum(filename):             
    with open(filename, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
        
    return str(_hash)


def flash_shell(shell_file, card_bdf):

    # judge the input parameter card_bdf type
    if isinstance(card_bdf, bytes):
        # it type is bytes, decode to string
        card_bdf = card_bdf.decode()

    cmd = "/opt/xilinx/xrt/bin/xbmgmt flash --shell --primary %s --card %s" % (shell_bin, card_bdf)
    print("Start program device %s .... \n" %  card_bdf)
    exec_cmd = subprocess.Popen(args=cmd, stdout=subprocess.PIPE, shell=True)

    while True:
        poll = exec_cmd.poll()
        print ("programing device %s ......" % card_bdf)
        if poll != None:
            break
        time.sleep(5)

    outs = exec_cmd.stdout.readlines()
    # print (outs)

    if b'Shell is updated successfully\n' in outs:
        # print ("outs %s" % outs)
        print ("device %s update success！\n" % card_bdf)
        return (card_bdf, 0)
        # sys.exit(0)
    else:
        print ("%s" % outs)
        print ("device %s update fail！\n" % card_bdf)
        return (card_bdf, -1)
        # sys.exit(-1)

return_list = []
def return_log(result):
    return_list.append(result)

if __name__ == '__main__':

    print ("ENV: %s \n" % sys.version)

    # need python3 support
    if sys.version_info[0] < 3:
        print ("Must be using Python 3")
        exit(1)

    # parameter check
    # if len(sys.argv) != 3:
    #     print ("Usage: python3 shell_program <shell_file> <card_bdf>\n ")
    #     print ("example: python3 shell_program ./u30_img.bin all ---program all xilinx device in the system\n ")
    #     print ("example: python3 shell_program ./u30_img.bin 86:00.0 ---program device 86:00.0\n ")
    #     exit(1)

    # shell_bin = sys.argv[1]
    # dev_bdf = sys.argv[2]

    parser = argparse.ArgumentParser(prog='shell_program', description='this program is used for upgrade xilinx alveo card shell')
    parser.add_argument('file', type=str, help='Specify the shell file')
    parser.add_argument('device_bdf', type=str,help='Specify the device, for example all or 86:00.0, "all" mean update all u30 devices in the system')
    args = parser.parse_args()

    if args.file:
        shell_bin = args.file

    if args.device_bdf:
        dev_bdf = args.device_bdf


        
    # program need root user
    if os.geteuid() != 0:
        print ("This program must be run as root. Abort!\n")
        sys.exit(1)

    # check if the xrt is installed
    file = '/opt/xilinx/xrt/bin/xbmgmt'
    if (os.path.exists(file) == False):
        print ("Please Check if the XRT is installed. Abort!\n")
        sys.exit(1)

    # check if the programed bin is exist
    if (os.path.exists(shell_bin) == False):
        print ("Can not find the shell file, Please input correct file path. Abort!.\n")
        sys.exit(1)

    #file check sum
    if (md5sum(shell_bin) != '46729d1a34101090d7a88e840e1053b3'):
        print ("Input file %s md5 check sum error. Abort!.\n" % shell_bin)
        sys.exit(1)

    # get the local bdf list
    bdf_list = []
    exec_cmd = subprocess.Popen(args='lspci -d 10ee:', stdout=subprocess.PIPE, shell=True)
    outs = exec_cmd.stdout.readlines()
    for out in outs:
        # device id d03c mean U30, It can be extend to other device in the future
        if b'Processing accelerators: Xilinx Corporation Device d03c' in out:
            bdf_list.append(out[0:7])        

    if len(bdf_list) == 0:
        print ("Can not find xilinx device, Please Check your system. abort!\n")
        exit(-1)
        

    # to do bdf check
    results = []
    if dev_bdf == 'all':

        # start to flash the U30 shell
        print("Caution!! the program take several mins,  please do not stop the program until it return!")
        print ("update %s devices %s \n" % (len(bdf_list), bdf_list))
        
        # process pool
        pool = multiprocessing.Pool(processes=16)

        for bdf in bdf_list:
            results.append(pool.apply_async(flash_shell, (shell_bin, bdf), callback = return_log))
        
        # [result.wait() for result in results]

        # for result in results:
        #     print ("result %s\n" % result)
                    
        # close pool，do not get process request any more
        pool.close()
        # waiting for all subprocess complete
        pool.join()
        print('update Finish')
        print(return_list)
        sys.exit(0)
    else:
        print ("update device bdf is %s" % dev_bdf)
        if dev_bdf.encode() not in bdf_list:
            print ("The %s is not in the system. abort!\n" % dev_bdf)
            exit(-1)
        else:
            print("Caution!! the program take several mins,  please do not stop the program until it return!")
            flash_shell(shell_bin, dev_bdf)

            # cmd = "/opt/xilinx/xrt/bin/xbmgmt flash --shell --primary %s --card %s" % (shell_bin, dev_bdf)
            # print("caution!! the program take several mins,  please do not stop the program until it return!")
            # exec_cmd = subprocess.Popen(args=cmd, stdout=subprocess.PIPE, shell=True)
            # outs = exec_cmd.stdout.readlines()
            # if b'Shell is updated successfully\n' in outs:
            #     print ("Shell update success！")
            #     print ("outs %s" % outs)
            #     sys.exit(0)
            # else:
            #     print ("Shell update fail！")
            #     print ("outs %s" % outs)
            #     sys.exit(-1)

   
