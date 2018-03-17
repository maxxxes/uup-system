#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import subprocess as sub
from subprocess import Popen, PIPE, STDOUT


def add_repositories():
    repo_list = [
        'ppa:webupd8team/sublime-text-3',
        'ppa:atareao/telegram',
    ]

    print('----- Start Add Repositories -----\n')
    for name_repo in repo_list:
        cmd = 'add-apt-repository -y %s' % name_repo
        finish_msg = '----- Add Repo %s - DONE -----\n' % name_repo
        error_message = '----- Add Repo %s ERROR -----\n' % name_repo
        pipe_call(cmd, finish_msg=finish_msg, error_message=error_message, stderr=STDOUT)
    print('----- Finish Add Repositories -----\n')


def update_system():
    update = 'apt-get update'
    upgrade = 'apt-get -y upgrade'
    dist_upgrade = 'apt-get -y dist-upgrade'

    print('----- Start Update System -----\n')
    for i, cmd in enumerate([update, upgrade, dist_upgrade], start=1):
        finish_msg = '----- Update Stage %s - DONE -----\n' % i
        error_message = '----- Update Stage %s ERROR -----\n' % i
	if i == 2:
            pipe_call(cmd, finish_msg=finish_msg, error_message=error_message, stdout=PIPE)
        else:
	    pipe_call(cmd, finish_msg=finish_msg, error_message=error_message)

    print('----- Finish Update System -----\n')


def install_package(name_package):
    cmd = 'apt-get -y install %s' % name_package
    finish_msg = '----- Install Package "%s" - DONE -----\n' % name_package
    error_message = '----- Install Package %s ERROR -----\n' % name_package
    pipe_call(cmd, finish_msg=finish_msg, error_message=error_message)


def pipe_call(cmd, start_msg=None, finish_msg=None, error_message=None, stderr=PIPE, stdout=None):
    # print(start_msg or '----- START -----')
    print(cmd)
    p = Popen(cmd.split(), stderr=stderr)
    out, err = p.communicate()
    if err:
        print(error_message or '----- ERROR -----\n')
        print(err)
        exit(1)
    print(finish_msg or '----- DONE -----\n')


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


def install_my_programs():
    name_packages_list = [
        'guake',
        'git',
	'mc',
        'sublime-text-installer',
        'telegram'
    ]
    other_cmd_to_install = [
        #'ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/',
        'pwd',
    ]

    print('----- Start Install Packages -----\n')
    for package in name_packages_list:
        install_package(package)
    print('----- Finish Base Install Packages -----\n')

    print('----- Start Other Command -----\n')
    for cmd in other_cmd_to_install:
        pipe_call(cmd)
    print('----- Finish Other Command  -----\n')


if __name__ == '__main__':
    # add_repositories()
    # update_system()
    install_my_programs()

