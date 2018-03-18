#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PrintColorMetaclass(type):
    def __new__(meta_cls, cls_name, cls_parents, cls_attrs):
        for color_name in cls_attrs.get('COLOR_LIST', []):
            def get_func(color_name):
                def getter_color(self):
                    return getattr(self, '_%s' % color_name) if self.active else ''
                return getter_color
            cls_attrs[color_name.lower()] = property(get_func(color_name))
        return type(cls_name, cls_parents, cls_attrs)


class PrintColors:
    """
    Вывод цветного print в console. Lite-версия.
    
    Пример использования
    p = PrintColors()
    p.color_print('header','header')
    p.color_print('okblue','okblue')
    p.color_print('okgreen','okgreen')
    p.color_print('warning','warning')
    print(p.color_print('fail','fail', True))
    """

    __metaclass__ = PrintColorMetaclass

    _HEADER = '\033[95m'
    _OKBLUE = '\033[94m'
    _OKGREEN = '\033[92m'
    _WARNING = '\033[93m'
    _FAIL = '\033[91m'
    _END = '\033[0m'

    COLOR_LIST = [
        'HEADER',
        'OKBLUE',
        'OKGREEN',
        'WARNING',
        'FAIL',
        'END'
    ]

    active = True

    def disable(self):
        self.active = False

    def activate(self):  
        self.active = True

    def color_print(self, color_name, value):
        return getattr(self, color_name) + value + self.end


if __name__ == '__main__':
    p = PrintColors()
    print(p.color_print('header','header'))
    print(p.color_print('okblue','okblue'))
    print(p.color_print('okgreen','okgreen'))
    print(p.color_print('warning','warning'))
    print(p.color_print('fail','fail'))