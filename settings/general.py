# -*- coding: utf-8 -*-
__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__data__ = '14.01.2024'


INVENTORY = ['./servers_lshw/0109230713-lshw.txt']
DIR_LSHW = './input/lshw/'
DIR_SMARTCTL = './input/smartctl/'
DIR_LSPCI = './input/lspci/'
DIR_STORCLI = './input/storcli/'
DIR_STORCLI_CALL = './input/storcli_call/'

# for equipment only
COLUMNS_EQU = './settings/equipment.txt'
RESULT_FILE_EQU = ['./data/equipment.csv']

# for cpu only
COLUMNS_CPU = './settings/cpu.txt'
RESULT_FILE_CPU = ['./data/cpu.csv']

# for ram only
COLUMNS_RAM = './settings/ram.txt'
RESULT_FILE_RAM = ['./data/ram.csv']
RAM_TYPE = 'Общая RAM'

# for hdd only
COLUMNS_HDD = './settings/hdd.txt'
RESULT_FILE_HDD_LSHW = ['./data/hdd_lshw.csv']

# for hdd only
COLUMNS_HDD = './settings/hdd.txt'
RESULT_FILE_HDD_SMARTCTL = ['./data/hdd_smartctl.csv']

# for hdd only
COLUMNS_HDD = './settings/hdd.txt'
RESULT_FILE_HDD_STORCLI = ['./data/hdd_storcli.csv']

# for card only
COLUMNS_CARD = './settings/card.txt'
RESULT_FILE_CARD = ['./data/card.csv']
CARD_TYPE = 'Общая сменная карта'

# for card only
RESULT_FILE_CARD_LSPCI = ['./data/card_lspci.csv']

# for raid only
COLUMNS_RAID = './settings/raid.txt'
RESULT_FILE_RAID = ['./data/raid.csv']
RAID_TYPE = 'Общий RAID-контроллер'
RAID_CAPACITY = '1'
