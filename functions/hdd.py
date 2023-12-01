# -*- coding: utf-8 -*-
"""
HDD
"""


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '29.11.2023'


def getHDD(data):
    hdd_serial = data['serial']
    
    try:
        hdd_vendor = data['vendor']
    except KeyError:
        hdd_vendor = data['product'].split(' ')[0]
    
    try:
        hdd_product = data['product'].split(' ')[1]
    except IndexError:
        hdd_product = data['product'].split(' ')[0]
    
    if data['description'] == 'SCSI Disk':
        hdd_type = 'HDD'
    else:
        hdd_type = 'SSD'

    hdd_slot = data['businfo'].split(':')[1].split('.')[1]
    
    try:
        hdd_capacity = int(data['size'] / 1000 / 1000 / 1000)
    except KeyError:
        pass
    
    return hdd_serial, hdd_vendor, hdd_product, hdd_capacity, hdd_type, hdd_slot
