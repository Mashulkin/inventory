# -*- coding: utf-8 -*-
"""
Parsing CPU
"""
from simple_settings import settings
from functions.common_modules import write_csv


__author__ = 'Vadim Arsenev'
__version__ = '1.1.1'
__date__ = '08.02.2024'


def getCPU(data, server_serial, ORDER_CPU):
    cpu_vendor = data['vendor']
    cpu_slot = data['slot']
    cpu_product = data['product']
    try:
        # only works for Intel
        cpu_frequency = data['product'].split('@')[1].strip().split('GHz')[0]
    except IndexError:
        # for AMD
        cpu_frequency = ''
    cpu_cores = data['configuration']['cores']

    # Data generation and writing to file cpu.csv
    data_cpu = {
        'server_serial': server_serial,
        'cpu_vendor': cpu_vendor,
        'cpu_slot': cpu_slot,
        'cpu_product': cpu_product,
        'cpu_frequency': cpu_frequency,
        'cpu_cores': cpu_cores,
    }
    write_csv(settings.RESULT_FILE_CPU[0], data_cpu, ORDER_CPU)
