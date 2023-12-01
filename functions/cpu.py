# -*- coding: utf-8 -*-
"""
CPU
"""


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '29.11.2023'


def getCPU(data):
    cpu_vendor = data['vendor']
    cpu_slot = data['slot']
    cpu_product = data['product']
    cpu_frequency = data['product'].split('@')[1].strip().split('GHz')[0]
    cpu_cores = data['configuration']['cores']
    
    return cpu_vendor, cpu_slot, cpu_product, cpu_frequency, cpu_cores
