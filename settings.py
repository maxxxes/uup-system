# -*- coding: utf-8 -*-


update_system_list = (
    {'cmd': 'apt-get update'},
    {'cmd': 'apt-get -y upgrade',
     'warning_code': 0},
    {'cmd': 'apt-get -y dist-upgrade'},
)

update_package_list = (
    {'name': 'python-dev python3-dev'},
    {'name': 'libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev'},
    {'name': 'libz-dev libjpeg-dev libfreetype6-dev'},
    {'name': 'libmysqlclient-dev'},
)

update_programs_list = (
    # {'name': 'guake'},
    # {'name': 'mc'},
    # {'name': 'git'},
    # {'name': 'mysql-server'},	# Запрашивает пароль рута, нужно потестить
    #  {'name': 'mysql-client'},

    {'name': 'sublime-text-installer',
     'repo': 'ppa:webupd8team/sublime-text-3'},

    {'name': 'telegram',
     'repo': 'ppa:atareao/telegram',
     'after': {'cmd': 'ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/',
               'warning_code': 1}
     },

)

# Slack
# pycharm
# Chrome
