#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import subprocess as sub
from subprocess import Popen, PIPE, STDOUT
from print_colors import PrintColors
from settings import *
import argparse

p = PrintColors()


class UUP(object):
    """
    Ubuntu Update Packages - script for fast install
    your love programs and packages in work place.
    """

    param = None
    UPDATE_CHOICE = (
        'system',
        'packages',
        'programs',
        'full'
    )

    def __init__(self):
        self.param = vars(self._args_parse())
        super(UUP, self).__init__()

    def _args_parse(self):
        """ Парсим параметры запущенного скрипта """
        uup_parse = argparse.ArgumentParser(description=self.__doc__)
        uup_parse.add_argument('-f', '--full', action='store_true',
                               help='start full update packages')

        subparsers = uup_parse.add_subparsers(help='List of update choice')
        system = subparsers.add_parser('system', help='Update system', aliases=['sys'])
        system.add_argument('system', action='store_true')

        packages = subparsers.add_parser('packages', help='Update packages', aliases=['pack'])
        packages.add_argument('packages', action='store_true')

        programs = subparsers.add_parser('programs', help='Update programs', aliases=['prog'])
        programs.add_argument('programs', action='store_true')

        return uup_parse.parse_args()

    def start_update(self):
        if self.param.get('full'):
            self.update_system()
            self.install_system_libs()
            self.install_my_packages()
        elif self.param.get('system'):
            self.update_system()
        elif self.param.get('packages'):
            self.install_system_libs()
        elif self.param.get('programs'):
            self.install_my_packages()

    def update_system(self):
        """ Стандартное обновление системы """
        print(p.color_print_format('okblue', ' Start Update System '))

        prefix = 'CMD'
        for item in update_system_list:
            try:
                cmd = item['cmd']
                msg = '%s %s' % (prefix, cmd)
                self.pipe_call(cmd, msg=msg, warning_code_list=[item.get('warning_code')])
            except KeyError as err:
                err_msg = '%s \n' % err
                print(p.print_error(err_msg))

        print(p.color_print_format('okblue', ' Finish Update System '))
        print('\n')

    def install_system_libs(self):
        """ Установка дополнительных системных библиотек """
        print(p.color_print_format('okblue', ' Start Install System Libs '))

        for item in update_package_list:
            name_package = item.get('name')
            self.install_package(name_package)

        print(p.color_print_format('okblue', ' Finish Install System Libs '))
        print('\n')

    def install_my_packages(self):
        print(p.color_print_format('okblue', ' Start Install My Packege '))

        for p_info in update_programs_list:
            repo = p_info.get('repo')
            before = p_info.get('before')
            package = p_info.get('name')
            after = p_info.get('after')
            if repo:
                self.add_repository(repo)
            if before:
                cmd = before.get('cmd')
                self.pipe_call(cmd, warning_code_list=[before.get('warning_code')])
            self.install_package(package)
            if after:
                cmd = after.get('cmd')
                self.pipe_call(cmd, warning_code_list=[after.get('warning_code')])

        print(p.color_print_format('okblue', ' Finish Install My Packege '))
        print('\n')

    def add_repository(self, name_repo):
        """ Добавление репозитория для установки пакета """
        prefix = 'Add Repo'
        cmd = 'add-apt-repository -y %s' % name_repo
        msg = '%s %s' % (prefix, name_repo)
        self.pipe_call(cmd, msg=msg, warning_code_list=[0])

    def install_package(self, name_package):
        """ Установка пакета """
        if name_package:
            prefix = 'Install Package'
            cmd = 'apt-get -y install %s' % name_package
            msg = '%s %s' % (prefix, name_package)
            self.pipe_call(cmd, msg=msg)
        else:
            print(p.print_error('Empty Name Packege'))
            exit(1)

    @staticmethod
    def pipe_call(cmd, msg=None, stderr=PIPE, warning_code_list=None):
        print(p.print_info(msg))
        print(cmd)
        pipe = Popen(cmd.split(), stderr=stderr, stdout=PIPE)
        out, err = pipe.communicate()
        print(pipe.returncode)
        if err:
            if warning_code_list and pipe.returncode in warning_code_list:
                print(p.print_warning(err))
            else:
                print(p.print_error(msg))
                print(err)
                exit(1)
        print(p.print_ok_green(msg))


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
    uup = UUP()
    uup.start_update()

