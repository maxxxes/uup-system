#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import subprocess as sub
from subprocess import Popen, PIPE, STDOUT
from print_colors import PrintColors
from settings import *

p = PrintColors()


def add_repository(name_repo):
    """ Добавление репозитория для установки пакета """
    prefix = 'Add Repo'
    cmd = 'add-apt-repository -y %s' % name_repo
    info_msg = '----- %s %s - GO -----' % (prefix, name_repo)
    ok_msg = '----- %s %s - DONE -----' % (prefix, name_repo)
    err_msg = '----- %s %s - ERROR -----' % (prefix, name_repo)
    pipe_call(cmd, info_msg=info_msg, ok_msg=ok_msg, err_msg=err_msg, warning_code_list=[0])


def install_package(name_package):
    """ Установка пакета """
    if name_package:
        prefix = 'Install Package'
	    cmd = 'apt-get -y install %s' % name_package
	    info_msg = '----- %s %s - GO -----' % (prefix, name_package)
	    ok_msg = '----- %s %s - DONE -----' % (prefix, name_package)
	    err_msg = '----- %s %s - ERROR -----' % (prefix, name_package)
	    pipe_call(cmd, info_msg=info_msg, ok_msg=ok_msg, err_msg=err_msg)
    else:
	    print(p.color_print('fail', 'Empty Name Packege'))
	    exit(1)

def pipe_call(cmd, info_msg=None, ok_msg=None, err_msg=None, stderr=PIPE, warning_code_list=None):
    print(p.color_print('header', info_msg or '----- START -----'))
    print(cmd)
    pipe = Popen(cmd.split(), stderr=stderr)
    out, err = pipe.communicate()
    print(pipe.returncode)
    # print('out = ', out)
    # print('err = ', err)
    if err:
    	if warning_code_list and pipe.returncode in warning_code_list:
   	        print(p.color_print('warning', err or '----- WARNING -----'))
    	else:
	        print(p.color_print('fail', err_msg or '----- ERROR -----'))
	        print(err)
	        exit(1)
    print(p.color_print('okgreen', ok_msg or '----- DONE -----'))


def update_system():
    """ Стандартное обновление системы """
    print(p.color_print('okblue', '----- Start Update System -----\n'))

    prefix = 'CMD'
    for item in update_system_list:
    	cmd = item.get('cmd')
    	if cmd:
	        info_msg = '----- %s %s - GO -----' % (prefix, cmd)
    	    ok_msg = '----- %s %s - DONE -----' % (prefix, cmd)
            err_msg = '----- %s %s - ERROR -----' % (prefix, cmd)
   	        pipe_call(cmd, info_msg=info_msg, ok_msg=ok_msg, err_msg=err_msg)
    print(p.color_print('okblue', '\n----- Finish Update System -----\n'))


def install_system_libs():
    """ Установка дополнительных системных библиотек """
    print(p.color_print('okblue', '----- Start Install System Libs -----\n'))

    prefix = 'Install'
    for item in system_libs_list:
	    name_package = item.get('name')
        install_package(name_package)
        
    print(p.color_print('okblue', '\n----- Finish Install System Libs -----\n'))


def install_my_packeges():
    print(p.color_print('okblue', '----- Start Install My Packege -----\n'))
    
    for p_info in install_packege_list:
    	repo = p_info.get('repo')
    	befor = p_info.get('befor')
    	package = p_info.get('name')
    	after = p_info.get('after')
    	if repo:
    	    add_repository(repo)
        if befor:
            cmd = befor.get('cmd')
            warning_code = befor.get('warning_code')
            pipe_call(cmd, warning_code_list=[warning_code])
        install_package(package)
        if after:
            cmd = after.get('cmd')
            warning_code = after.get('warning_code')
            pipe_call(cmd, warning_code_list=[warning_code])

    print(p.color_print('okblue', '\n----- Finish Install My Packege -----\n'))


# def remove_packages(name_packages_list):
#     print('----- Start Remove Packages -----\n')
#     for package in name_packages_list:
#         cmd = 'apt-get -y remove %s' % package
#         p = Popen(cmd.split(), stderr=PIPE)
#         out, err = p.communicate()
#         if err:
#             print('----- Remove Package %s ERROR -----\n' % package)
#             print(err)
#             exit(1)
#         print('----- Remove Package %s - DONE -----\n' % package)
#     print('----- Finish Remove Packages -----\n')

if __name__ == '__main__':
    update_system()
    install_system_libs()
    install_my_packeges()

