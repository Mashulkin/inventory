# -*- coding: utf-8 -*-
__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__data__ = '29.11.2023'


INVENTORY = ['./servers_lshw/lshw', './servers_lshw/lshw2', './servers_lshw/lshw3', './servers_lshw/lshw4', './servers_lshw/lshw_yadro_altc9f2']
# INVENTORY = ['./servers_lshw/test']

# for cpu only
COLUMNS_CPU = './settings/cpu.txt'
RESULT_FILE_CPU = ['./data/cpu.csv']

# for ram only
COLUMNS_RAM = './settings/ram.txt'
RESULT_FILE_RAM = ['./data/ram.csv']
RAM_TYPE = 'Общая RAM'

# for hdd only
COLUMNS_HDD = './settings/hdd.txt'
RESULT_FILE_HDD = ['./data/hdd.csv']

# for hdd only
COLUMNS_CARD = './settings/card.txt'
RESULT_FILE_CARD = ['./data/card.csv']
CARD_TYPE = 'Общая сменная карта'
