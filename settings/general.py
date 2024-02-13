# -*- coding: utf-8 -*-
__author__ = 'Vadim Arsenev'
__version__ = '1.1.0'
__date__ = '08.02.2024'


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
RESULT_FILE_HDD_SMARTCTL = ['./data/hdd_smartctl.csv']
RESULT_FILE_HDD_STORCLI = ['./data/hdd_storcli.csv']

# for card only
COLUMNS_CARD = './settings/card.txt'
RESULT_FILE_CARD_LSPCI = ['./data/card_lspci.csv']
CARD_TYPE = 'Общая сменная карта'

# for raid only
COLUMNS_RAID = './settings/raid.txt'
RESULT_FILE_RAID = ['./data/raid.csv']
RAID_TYPE = 'Общий RAID-контроллер'
RAID_CAPACITY = '1'
