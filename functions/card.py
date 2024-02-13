# -*- coding: utf-8 -*-
"""
Parsing CARD
"""
from simple_settings import settings
from functions.common_modules import write_csv


__author__ = 'Vadim Arsenev'
__version__ = '2.0.0'
__date__ = '13.02.2024'


def getCardYadro(card_list, server_serial, ORDER_CARD):
    card_type = settings.CARD_TYPE
    card_vendor, card_remark = [''] * 2

    for item in range(0, len(card_list), 3):
        if card_list[item+1] == 'T6225-CR':
            card_list[item+1] = 'SN1225'
            card_vendor = 'B4Com'
        elif card_list[item+1] == 'T62100-LP-CR':
            card_list[item+1] = 'SN12100'
            card_vendor = 'B4Com'
        elif 'ConnectX' in card_list[item+1]:
            card_vendor = 'Mellanox'
        elif 'QLogic' in card_list[item+1]:
            card_vendor = 'QLogic'
        else:
            card_vendor = ''

        # Data generation and writing to file card_lspci.csv       
        data_card = {
            'server_serial': server_serial,
            'card_product': card_list[item+1],
            'card_vendor': card_vendor,
            'card_remark': card_remark,
            'card_serial': card_list[item+2],
            'card_type': card_type,
            'card_slot': card_list[item],
        }
        write_csv(settings.RESULT_FILE_CARD_LSPCI[0], data_card, ORDER_CARD)


def getCardGraviton(card_list, server_serial, ORDER_CARD):
    card_type = settings.CARD_TYPE
    card_vendor, card_remark, card_slot = [''] * 3

    for item in range(0, len(card_list), 2):
        if card_list[item] == 'T6225-CR':
            card_list[item] = 'SN1225'
            card_vendor = 'B4Com'
        elif card_list[item] == 'T62100-LP-CR':
            card_list[item] = 'SN12100'
            card_vendor = 'B4Com'
        elif 'ConnectX' in card_list[item]:
            card_vendor = 'Mellanox'
        elif 'QLogic' in card_list[item]:
            card_vendor = 'QLogic'
        else:
            card_vendor = ''

        # Data generation and writing to file card_lspci.csv        
        data_card = {
            'server_serial': server_serial,
            'card_product': card_list[item],
            'card_vendor': card_vendor,
            'card_remark': card_remark,
            'card_serial': card_list[item+1],
            'card_type': card_type,
            'card_slot': card_slot,
        }
        write_csv(settings.RESULT_FILE_CARD_LSPCI[0], data_card, ORDER_CARD)


def getCARD(server_serial, ORDER_CARD):
    card_list = []
    step_list = 2
    card_product_temp = ''

    with open('temp', 'r') as file:
        lines = file.readlines()

    # Parsing grep lines
    for item in lines:
        if item.split(':')[0].strip() == 'Product Name' and \
            item.split(':')[1].strip() =='Example VPD':
            continue

        if 'Mellanox' in item and 'controller:' in item:
            card_product_temp = item.split(' controller: ')[1].split('Mellanox Technologies ')[1].strip()
            continue
        elif 'controller:' in item or 'Fibre Channel' in item:
            card_product_temp = ''
            continue

        if item.split(':')[0].strip() == 'Physical Slot':
            card_slot = item.split(':')[1].strip()
            card_list.append(card_slot)
            step_list = 3
            continue

        if item.split(':')[0].strip() == 'Product Name':
            if card_product_temp == '':
                card_product = item.split(':')[1].strip()
            else:
                card_product = card_product_temp
            card_list.append(card_product)
            continue
        
        if item.split(':')[0].strip() == '[SN] Serial number':
            card_serial = item.split(':')[1].strip()
            card_list.append(card_serial)
            continue
    
    # Yadro
    if step_list == 3:
        getCardYadro(card_list, server_serial, ORDER_CARD)
    # Graviton
    elif step_list == 2:
        getCardGraviton(card_list, server_serial, ORDER_CARD)
