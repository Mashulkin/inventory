# -*- coding: utf-8 -*-
"""
Parsing RAM
"""
from simple_settings import settings
from functions.common_modules import write_csv


__author__ = 'Vadim Arsenev'
__version__ = '1.1.0'
__date__ = '10.12.2023'


def getRAM(data, server_serial, ORDER_RAM):
    ram_vendor = data['vendor']
    if ram_vendor == 'NO DIMM':
        return

    ram_serial = data['serial']
    ram_type = settings.RAM_TYPE
    ram_slot = data['slot']
    ram_product = data['product']
    try:
        ram_capacity = int(data['size'] / 1024 / 1024)
    except KeyError:
        ram_capacity = ''

    data_ram = {
        'server_serial': server_serial,
        'ram_vendor': ram_vendor,
        'ram_serial': ram_serial,
        'ram_type': ram_type,
        'ram_slot': ram_slot,
        'ram_product': ram_product,
        'ram_capacity': ram_capacity,
    }

    write_csv(settings.RESULT_FILE_RAM[0], data_ram, ORDER_RAM)
