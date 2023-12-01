# -*- coding: utf-8 -*-
"""
CARD
"""
from simple_settings import settings


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '30.11.2023'


def getCARD(data, quantity_ports):
    card_vendor = data['vendor'].split(' ')[0]
    card_product = data['product']
    if quantity_ports == 2:
        card_remark = 'Ethernet 2 x '
    else:
        card_remark = 'Ethernet'
    card_serial = data['serial']
    card_type = settings.CARD_TYPE
    
    return card_vendor, card_product, card_remark, card_serial, card_type