# -*- coding: utf-8 -*-
"""
Parsing CPU
"""
from simple_settings import settings
from functions.common_modules import write_csv


__author__ = 'Vadim Arsenev'
__version__ = '1.1.0'
__date__ = '11.12.2023'


def getCPU(data, server_serial, ORDER_CPU):
    cpu_vendor = data['vendor']
    cpu_slot = data['slot']
    cpu_product = data['product']
    cpu_frequency = data['product'].split('@')[1].strip().split('GHz')[0]
    cpu_cores = data['configuration']['cores']

    # Data generation and writing to file
    data_cpu = {
        'server_serial': server_serial,
        'cpu_vendor': cpu_vendor,
        'cpu_slot': cpu_slot,
        'cpu_product': cpu_product,
        'cpu_frequency': cpu_frequency,
        'cpu_cores': cpu_cores,
    }

    write_csv(settings.RESULT_FILE_CPU[0], data_cpu, ORDER_CPU)
