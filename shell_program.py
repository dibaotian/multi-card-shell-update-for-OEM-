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

# import argparse
# parser = argparse.ArgumentParser(prog='shell_program', description='used for upgrade xilinx alveo card shell')
# parser.add_argument('-f', metavar='N', type=str, help='the path of shell file')
# args = parser.parse_args()

def shell_flash(shell_file, card_bdf):
    try:
        # cmd = "/opt/xilinx/xrt/bin/xbmgmt flash --shell --primary %s --card %s" % (shell_file, card_bdf)
        cmd = "/opt/xilinx/xrt/bin/xbmgmt scan"
        print("命令%s开始运行%s" % (cmd, datetime.datetime.now() ))
        os.system(cmd)
        print("命令%s结束运行%s" % (cmd, datetime.datetime.now()))
    except :       #异常处理,此处声明.没有刻意计划异常处理,(只确保我执行的linux命令键入正确即可),[所以有报错也不会打印如下异常])
        print('命令%s\t 运行失败,失败原因\r\n%s' % (cmd,e))

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print ("Usage: python shell_program <shell_file> <card_bdf>\n")
        exit(1)

    shell_bin = sys.argv[1]
    dev_bdf = sys.argv[2]
        
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
        print ("can not find the shell file, Please input correct file path. Abort!.\n")
        sys.exit(1)

    # get the local bdf list
    bdf_list = []
    exec_cmd = subprocess.Popen(args='lspci -d 10ee:', stdout=subprocess.PIPE, shell=True)
    outs = exec_cmd.stdout.readlines()
    print (outs)
    for out in outs:
        if 'Processing accelerators: Xilinx Corporation Device d03c' in out:
            bdf_list.append(out[0:7])
            
    print (bdf_list)

    if len(bdf_list) == 0:
        print ("Can not find xilinx device, Please Check your system. abort!\n")
        exit(-1)

    # to do bdf检查参数
    if dev_bdf == 'all':
         # start to flash the U30 shell
        # 线程池
        threads = []
        pool = multiprocessing.Pool(processes=16)
        
        print (bdf_list)
        for bdf in bdf_list:
            print (bdf)
            result.append(pool.apply_async(shell_flash, (shell_bin, bdf)))
    else:
        print ("input bdf is %s" % dev_bdf)
        if dev_bdf not in bdf_list:
            print ("The %s is not in the system. abort!\n" % dev_bdf)
            exit(-1)
        else:
            # cmd = "/opt/xilinx/xrt/bin/xbmgmt flash --shell --primary %s --card %s" % (shell_bin, dev_bdf)
            cmd = "/opt/xilinx/xrt/bin/xbmgmt scan"
            exec_cmd = subprocess.Popen(args=cmd, stdout=subprocess.PIPE, shell=True)
            outs = exec_cmd.stdout.readlines()
            

       

    # p = Process(target=fun1,args=(i,)) #实例化进程对象
    # p.start()
    # process_list.append(p)

   
