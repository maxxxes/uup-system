#!/usr/bin/env python
# -*- coding: utf-8 -*-


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    # Source: https://github.com/django/django/blob/master/django/utils/six.py#L798
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})


class PrintColorMetaclass(type):
    def __new__(mcs, cls_name, cls_parents, cls_kwargs):
        """ Конструктор методов для включеня/отключения цветной печати через свойство """
        for color_name in cls_kwargs.get('COLOR_LIST', []):
            def get_func(c_name):
                def getter_color(self):
                    return getattr(self, '_%s' % c_name) if self.active else ''
                return getter_color
            cls_kwargs[color_name.lower()] = property(get_func(color_name))
        return type(cls_name, cls_parents, cls_kwargs)


class PrintColors(with_metaclass(PrintColorMetaclass)):
    """
    Вывод цветного print в console. Lite-версия.

    Пример использования
    p = PrintColors()
    print(p.color_print('header', 'header'))
    print(p.color_print('okblue', 'okblue'))
    print(p.color_print('okgreen', 'okgreen'))
    print(p.color_print('warning', 'warning'))
    print(p.color_print('error', 'error'))
    """

    _HEADER = '\033[95m'
    _OKBLUE = '\033[94m'
    _OKGREEN = '\033[92m'
    _WARNING = '\033[93m'
    _ERROR = '\033[91m'
    _END = '\033[0m'

    COLOR_LIST = [
        'HEADER',
        'OKBLUE',
        'OKGREEN',
        'WARNING',
        'ERROR',
        'END'
    ]

    class DefaultMessages:
        with_print = 50
        base_print = '{:-^%s}' % with_print
        info = ' GO '
        warning = ' WARNING '
        error = ' ERROR '
        ok = ' DONE '
        start = ' START '

    active = True

    def disable(self):
        self.active = False

    def activate(self):
        self.active = True

    def color_print_format(self, color_name, value):
        """ Форматированный метод цветной печати """
        return getattr(self, color_name) + self.DefaultMessages.base_print.format(value) + getattr(self, 'end')

    def color_print(self, color_name, value):
        """ Базовый метод цветной печати """
        return getattr(self, color_name) + value + getattr(self, 'end')

    def get_base_print(self):
        """ Стандарт печати логов """
        return self.DefaultMessages.base_print

    def print_info(self, info_msg=None):
        msg = ' %s - GO ' % info_msg if info_msg else self.DefaultMessages.info
        return self.color_print_format('header', msg)

    def print_warning(self, war_msg=None):
        msg = u' %s - WARNING ' % war_msg.decode('utf-8') if war_msg else self.DefaultMessages.warning
        return self.color_print_format('warning', msg)

    def print_error(self, err_msg=None):
        msg = ' %s - ERROR ' % err_msg if err_msg else self.DefaultMessages.error
        return self.color_print_format('error', msg)

    def print_ok_green(self, ok_msg=None):
        msg = ' %s - DONE ' % ok_msg if ok_msg else self.DefaultMessages.ok
        return self.color_print_format('okgreen', msg)

    def print_ok_blue(self, ok_msg=None):
        msg = ' %s - START ' % ok_msg if ok_msg else self.DefaultMessages.start
        return self.color_print_format('okblue', msg)


if __name__ == '__main__':
    p = PrintColors()
    print(p.color_print('header', 'header'))
    print(p.color_print('okblue', 'okblue'))
    print(p.color_print('okgreen', 'okgreen'))
    print(p.color_print('warning', 'warning'))
    print(p.color_print('error', 'error'))
    print(p.print_info('Let\'s'))
    print(p.print_warning())
    print(p.print_error())
    print(p.print_ok_green())
    print(p.print_ok_blue())
