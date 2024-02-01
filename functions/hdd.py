# -*- coding: utf-8 -*-
"""
HDD
"""


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '10.12.2023'


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


def getSmartHDD(data):
    hdd_serial, hdd_vendor, hdd_product, hdd_capacity, hdd_type, hdd_slot = [''] * 6
    try:
        hdd_serial = data['serial_number']
    except KeyError:
        return hdd_serial, hdd_vendor, hdd_product, hdd_capacity, hdd_type, hdd_slot
    hdd_vendor = data['model_name'].split(' ')[0]
    hdd_product = data['model_name'].split(' ')[1]
    hdd_capacity = int(data['user_capacity']['bytes'] / 1000 / 1000 / 1000)
    hdd_type = 'SSD'
    hdd_slot = ''

    return hdd_serial, hdd_vendor, hdd_product, hdd_capacity, hdd_type, hdd_slot


def getStorcliHDD(data, eid, slot):
    disk_key = f'Drive /c0/e{eid}/s{slot} - Detailed Information'
    disk_key_key = f'Drive /c0/e{eid}/s{slot} Device attributes'
    hdd_vendor = data['Controllers'][0]['Response Data'][disk_key][disk_key_key]['Manufacturer Id'].strip()
    hdd_product = data['Controllers'][0]['Response Data'][disk_key][disk_key_key]['Model Number'].strip()
    if hdd_vendor == 'SEAGATE':
        hdd_serial = str(data['Controllers'][0]['Response Data'][disk_key][disk_key_key]['SN'].strip())[:8]
    else:
        hdd_serial = data['Controllers'][0]['Response Data'][disk_key][disk_key_key]['SN'].strip()

    return hdd_serial, hdd_vendor, hdd_product
