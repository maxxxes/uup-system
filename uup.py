#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import subprocess as sub
from subprocess import Popen, PIPE, STDOUT
from print_colors import PrintColors
from settings import *
import argparse
import sys

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
        programs.add_argument('-p', dest='program', help='Name programs for install')
        programs.add_argument('-r', '--remove', action='store_true', help='Flag programs for remove')

        if len(sys.argv) == 1:
            uup_parse.print_usage()
        return uup_parse.parse_args()

    def start_update(self):
        if self.param.get('full'):
            self.update_system(system_list)
            self.install_package_list(packages_list)
            self.install_programs_list(programs_list)
        elif self.param.get('system'):
            self.update_system(system_list)
        elif self.param.get('packages'):
            self.install_package_list(packages_list)
        elif self.param.get('programs'):
            if self.param.get('remove'):
                self.remove_programs_list(programs_list)
            else:
                self.install_programs_list(programs_list)

    def update_system(self, cmd_list):
        """ Стандартное обновление системы """
        print(p.color_print_format('okblue', ' Start Update System '))

        prefix = 'CMD'
        for item in cmd_list:
            try:
                cmd = item['cmd']
                msg = '%s %s' % (prefix, cmd)
                self.pipe_call(cmd, msg=msg, warning_code_list=[item.get('warning_code')])
            except KeyError as err:
                err_msg = '%s \n' % err
                print(p.print_error(err_msg))

        print(p.color_print_format('okblue', ' Finish Update System '))
        print('\n')

    def install_package_list(self, package_list):
        """ Установка дополнительных системных библиотек """
        print(p.color_print_format('okblue', ' Start Install System Libs '))

        for item in package_list:
            name_package = item.get('name')
            self.install_package(name_package)

        print(p.color_print_format('okblue', ' Finish Install System Libs '))
        print('\n')

    def install_programs_list(self, program_list, dep=None):
        print_start = ' Start Install %s Programs ' % (dep or 'My')
        print(p.color_print_format('okblue', print_start))

        name_program = self.param.get('program')
        if name_program:
            p_info = self.get_info_programs(name_program, program_list)
            self.install_program(p_info)
        else:
            for p_info in program_list:
                self.install_program(p_info)

        print_stop = ' Finish Install %s Programs ' % (dep or 'My')
        print(p.color_print_format('okblue', print_stop))
        print('\n')

    @staticmethod
    def get_info_programs(name_program, program_list):
        """" Поиск информации о программе из списка """
        for p_info in program_list:
            if name_program in p_info.values():
                return p_info
        print(p.print_error('%s is not defined' % name_program))
        exit(1)

    def add_repository(self, name_repo):
        """ Добавление репозитория для установки пакета """
        prefix = 'Add Repo'
        cmd = 'add-apt-repository -y %s' % name_repo
        msg = '%s %s' % (prefix, name_repo)
        self.pipe_call(cmd, msg=msg, warning_code_list=[0])

    def install_program(self, p_info):
        """ Подготовка и установка программы """
        repo = p_info.get('repo')
        before = p_info.get('before')
        dep = p_info.get('dep')
        package = p_info.get('name')
        after = p_info.get('after')
        install = p_info.get('install')
        # Добавление репозитория
        if repo:
            self.add_repository(repo)
        # Выполнение команд до установки программы
        if before:
            for step in before:
                cmd = step.get('cmd')
                self.pipe_call(cmd, warning_code_list=[step.get('warning_code')])
        # Установка зависимых к программе пакетов
        if dep:
            self.install_programs_list(dep, dep='Dep')
        # Установка программы иным способом
        if install:
            for step in install:
                cmd = step.get('cmd')
                warning_code = step.get('warning_code')
                self.install_package(package, cmd=cmd, warning_code_list=[warning_code])
        else:
            self.install_package(package)
        if after:
            cmd = after.get('cmd')
            self.pipe_call(cmd, warning_code_list=[after.get('warning_code')])

    def install_package(self, name_package, cmd=None, warning_code_list=None):
        """ Установка пакета """
        prefix = 'Install Package'
        msg = '%s %s' % (prefix, name_package)
        if cmd:
            self.pipe_call(cmd, msg=msg, warning_code_list=warning_code_list)
        elif name_package:
            cmd = 'apt-get -y install %s' % name_package
            self.pipe_call(cmd, msg=msg)
        else:
            print(p.print_error('Empty Name or Install in settings package'))
            exit(1)

    def remove_programs_list(self, program_list):
        print_start = ' Start Remove Programs '
        print(p.color_print_format('okblue', print_start))

        name_program = self.param.get('program')
        p_info = self.get_info_programs(name_program, program_list)
        if name_program:
            self.remove_program(p_info)

        print_stop = ' Finish Remove Programs '
        print(p.color_print_format('okblue', print_stop))

    def remove_program(self, p_info):
        """ Подготовка и удаление программы """
        program = p_info.get('name')
        remove = p_info.get('remove')

        # Если прописана отдельные команды для удаления
        if remove:
            for step in remove:
                cmd = step.get('cmd')
                self.remove_package(program, cmd=cmd)
        else:
            self.remove_package(program)

    def remove_package(self, name_package, cmd=None):
        """ Удаление пакета """
        prefix = 'Remove Package'
        msg = '%s %s' % (prefix, name_package)
        if cmd:
            self.pipe_call(cmd, msg=msg)
        elif name_package:
            cmd = 'apt-get -y remove %s' % name_package
            self.pipe_call(cmd, msg=msg)
        else:
            print(p.print_error('Empty Name or Remove in settings package'))
            exit(1)

    @staticmethod
    def pipe_call(cmd, msg=None, stderr=PIPE, warning_code_list=None):
        print(p.print_info(msg))
        print(cmd)
        pipe = Popen(cmd.split(), stderr=stderr)
        out, err = pipe.communicate()
        print(pipe.returncode)
        if err:
            if warning_code_list and pipe.returncode in warning_code_list:
                print(p.print_warning(err.decode('utf-8')))
            else:
                print(p.print_error(msg))
                print(err.decode('utf-8'))
                exit(1)
        print(p.print_ok_green(msg))


if __name__ == '__main__':
    uup = UUP()
    uup.start_update()

