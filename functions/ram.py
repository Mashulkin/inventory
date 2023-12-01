# -*- coding: utf-8 -*-
"""
RAM
"""
from simple_settings import settings


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '29.11.2023'


def getRAM(data):
    ram_capacity = ''

    ram_vendor = data['vendor']
    ram_serial = data['serial']
    ram_type = settings.RAM_TYPE
    ram_slot = data['slot']
    ram_product = data['product']
    try:
        ram_capacity = int(data['size'] / 1024 / 1024)
    except KeyError:
        pass
    
    return ram_vendor, ram_serial, ram_type, ram_slot, ram_product, ram_capacity
