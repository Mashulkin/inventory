# -*- coding: utf-8 -*-
"""
Parsing HDD
"""
from simple_settings import settings
from functions.common_modules import write_csv


__author__ = 'Vadim Arsenev'
__version__ = '2.0.0'
__date__ = '13.02.2024'


def getSmartHDD(data, server_serial, ORDER_HDD):
    hdd_serial, hdd_vendor, hdd_product, hdd_capacity, hdd_type, hdd_slot = [''] * 6
    try:
        hdd_serial = data['serial_number']
    except KeyError:
        return
    hdd_vendor = data['model_name'].split(' ')[0]
    hdd_product = data['model_name'].split(' ')[1]
    hdd_capacity = int(data['user_capacity']['bytes'] / 1000 / 1000 / 1000)

    # Data generation and writing to file hdd_smartctl.csv
    data_hdd = {
        'server_serial': server_serial,
        'hdd_serial': hdd_serial,
        'hdd_vendor': hdd_vendor,
        'hdd_product': hdd_product,
        'hdd_capacity': hdd_capacity,
        'hdd_type': hdd_type,
        'hdd_slot': hdd_slot,
    }
    write_csv(settings.RESULT_FILE_HDD_SMARTCTL[0], data_hdd, ORDER_HDD)


def getStorcliHDD(item_raid, data, item_hdd, server_serial, ORDER_HDD):
    # storcli_call
    eid = item_hdd['EID:Slt'].split(':')[0]
    hdd_slot = item_hdd['EID:Slt'].split(':')[1]
    hdd_capacity = float(item_hdd['Size'].split(' ')[0])
    hdd_type = item_hdd['Med']

    # storcli
    disk_key = f'Drive /c{item_raid}/e{eid}/s{hdd_slot} - Detailed Information'
    disk_key_key = f'Drive /c{item_raid}/e{eid}/s{hdd_slot} Device attributes'
    hdd_vendor = data['Controllers'][item_raid]['Response Data'][disk_key][disk_key_key]['Manufacturer Id'].strip()
    hdd_product = data['Controllers'][item_raid]['Response Data'][disk_key][disk_key_key]['Model Number'].strip()

    # vendor wars
    if hdd_vendor == 'SEAGATE':
        hdd_serial = str(data['Controllers'][item_raid]['Response Data'][disk_key][disk_key_key]['SN'].strip())[:8]
    else:
        hdd_serial = data['Controllers'][item_raid]['Response Data'][disk_key][disk_key_key]['SN'].strip()
    
    try:
        if hdd_vendor == 'ATA':
            hdd_vendor = hdd_product.split(' ')[0]
            hdd_product = hdd_product.split(' ')[1]   
    except IndexError:
        hdd_product = ''

    if 'Micron' in hdd_vendor:
        hdd_product = hdd_vendor.split('_')[2]
        hdd_vendor = hdd_vendor.split('_')[0]       

    # Data generation and writing to file hdd_storcli.csv
    data_hdd = {
        'server_serial': server_serial,
        'hdd_serial': hdd_serial,
        'hdd_vendor': hdd_vendor,
        'hdd_product': hdd_product,
        'hdd_capacity': hdd_capacity,
        'hdd_type': hdd_type,
        'hdd_slot': hdd_slot,
    }
    write_csv(settings.RESULT_FILE_HDD_STORCLI[0], data_hdd, ORDER_HDD)
