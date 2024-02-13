# -*- coding: utf-8 -*-
"""
Parsing RAID
"""
from simple_settings import settings
from functions.common_modules import write_csv


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '08.02.2024'


def getRAID(data, item, server_serial, ORDER_RAID):
    raid_capacity = settings.RAID_CAPACITY
    raid_type = settings.RAID_TYPE
    raid_product, raid_serial, raid_vendor = [''] * 3

    try:
        raid_product = data['Controllers'][item]['Response Data']['Product Name']
        raid_serial = data['Controllers'][item]['Response Data']['Serial Number']
        raid_vendor = data['Controllers'][item]['Response Data']['Product Name'].split(' ')[0]
    except KeyError:
        return

    # Data generation and writing to file raid.csv
    data_raid = {
        'server_serial': server_serial,
        'raid_serial': raid_serial,
        'raid_vendor': raid_vendor,
        'raid_product': raid_product,
        'raid_capacity': raid_capacity,
        'raid_type': raid_type,
    }
    write_csv(settings.RESULT_FILE_RAID[0], data_raid, ORDER_RAID)
