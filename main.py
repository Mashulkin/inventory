# -*- coding: utf-8 -*-
"""
Getting 
"""
import os
import subprocess
from simple_settings import settings
from functions.common_modules import json_read, json_write, write_csv, read_txt, remove_file
from functions.headline import print_headline
from functions.cpu import getCPU
from functions.ram import getRAM
from functions.hdd import getHDD, getSmartHDD, getStorcliHDD
from functions.card import getCARD


__author__ = 'Vadim Arsenev'
__version__ = '1.0.2'
__date__ = '15.01.2024'


ORDER_EQU = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_EQU).split('\n')))
ORDER_CPU = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_CPU).split('\n')))
ORDER_RAM = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_RAM).split('\n')))
ORDER_HDD = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_HDD).split('\n')))
ORDER_CARD = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_CARD).split('\n')))
ORDER_RAID = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_RAID).split('\n')))


def getInventory_lshw(rawData):
    """
    The main module for performing all operations of a request
       and writing to a file
    """
    # ***** Main query *****
    hostname = rawData['id']
    server_vendor = rawData['vendor']
    server_product = rawData['product']
    server_serial = rawData['serial']

    # Data generation and writing to file
    data_equ = {
        'server_serial': server_serial,
        'hostname': hostname,
        'server_vendor': server_vendor,
        'server_product': server_product,
    }

    write_csv(settings.RESULT_FILE_EQU[0], data_equ, ORDER_EQU)

    for raw_item in rawData['children']:
        if raw_item['id'] == 'core':            
            for children in raw_item['children']:
                # *** CPU ***
                try: 
                    if children['class'] == 'processor':
                        print_headline(settings.RESULT_FILE_CPU[0], settings.COLUMNS_CPU, ORDER_CPU)
                        getCPU(children, server_serial, ORDER_CPU)
                except KeyError:
                    pass

                # *** RAM ***
                try:
                    if children['class'] == 'memory' and children['description'] == 'System Memory':
                        print_headline(settings.RESULT_FILE_RAM[0], settings.COLUMNS_RAM, ORDER_RAM)
                        for item_ram in children['children']:
                            getRAM(item_ram, server_serial, ORDER_RAM)
                except KeyError:
                    pass

                # *** HDD ***
                try:
                    if children['class'] == 'bridge' and children['children'][0]['class'] == 'storage':
                        print_headline(settings.RESULT_FILE_HDD_LSHW[0], settings.COLUMNS_HDD, ORDER_HDD)
                        for item_hdd in children['children'][0]['children']:
                            if item_hdd['class'] != 'disk':
                                continue                            
                            hdd_serial, hdd_vendor, hdd_product, \
                                hdd_capacity, hdd_type, hdd_slot = getHDD(item_hdd)

                            # Data generation and writing to file
                            data_hdd = {
                                'server_serial': server_serial,
                                'hdd_serial': hdd_serial,
                                'hdd_vendor': hdd_vendor,
                                'hdd_product': hdd_product,
                                'hdd_capacity': hdd_capacity,
                                'hdd_type': hdd_type,
                                'hdd_slot': hdd_slot,
                            }

                            write_csv(settings.RESULT_FILE_HDD_LSHW[0], data_hdd, ORDER_HDD)

                except KeyError:
                    pass

                # *** CARDS YADRO***
                try:
                    if children['class'] == 'bridge' and children['children'][0]['children'][0]['class'] == 'network':
                        for item in range(len(children['children'][0]['children'])):
                            try:
                                interface_logicalname = children['children'][0]['children'][item]['logicalname']
                            except KeyError:
                                continue
                            quantity_ports = len(children['children'][0]['children']) 
                            card_vendor, card_product, card_remark, \
                                card_serial, card_type = getCARD(children['children'][0]['children'][item], quantity_ports)

                        print_headline(settings.RESULT_FILE_CARD[0], settings.COLUMNS_CARD, ORDER_CARD)
                        card_slot = children['id'].split(':')[1]

                        # Data generation and writing to file
                        data_card = {
                            'server_serial': server_serial,
                            'card_vendor': card_vendor,
                            'card_product': card_product,
                            'card_remark': card_remark,
                            'card_serial': card_serial,
                            'card_type': card_type,
                            'card_slot': card_slot,
                        }

                        write_csv(settings.RESULT_FILE_CARD[0], data_card, ORDER_CARD)

                except KeyError:
                    pass

                # *** CARDS Graviton***
                try:
                    if children['class'] == 'bridge' and children['children'][0]['class'] == 'network':
                        print_headline(settings.RESULT_FILE_CARD[0], settings.COLUMNS_CARD, ORDER_CARD)
                        quantity_ports = len(children['children'])           
                        card_vendor, card_product, card_remark, \
                            card_serial, card_type = getCARD(children['children'][0], quantity_ports)
                        card_slot = children['id'].split(':')[1]

                        # Data generation and writing to file
                        data_card = {
                            'server_serial': server_serial,
                            'card_vendor': card_vendor,
                            'card_product': card_product,
                            'card_remark': card_remark,
                            'card_serial': card_serial,
                            'card_type': card_type,
                            'card_slot': card_slot,
                        }

                        write_csv(settings.RESULT_FILE_CARD[0], data_card, ORDER_CARD)

                except KeyError:
                    pass


def getInventory_smartctl(rawData):
    print_headline(settings.RESULT_FILE_HDD_SMARTCTL[0], settings.COLUMNS_HDD, ORDER_HDD)
    server_serial = rawData[0]['server_serial']
    for item_hdd in rawData:
        hdd_serial, hdd_vendor, hdd_product, \
            hdd_capacity, hdd_type, hdd_slot = getSmartHDD(item_hdd)
        if hdd_serial == hdd_vendor:
            continue

        # Data generation and writing to file
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


def getInventory_storcli(rawData, server_serial):
    print_headline(settings.RESULT_FILE_RAID[0], settings.COLUMNS_RAID, ORDER_RAID)
    # Data generation and writing to file
    raid_capacity = settings.RAID_CAPACITY
    raid_type = settings.RAID_TYPE
    raid_product, raid_serial, raid_vendor = [''] * 3
    try:
        for item_raid in range(len(rawData['Controllers'])):
            raid_product = rawData['Controllers'][item_raid]['Response Data']['Product Name']
            raid_serial = rawData['Controllers'][item_raid]['Response Data']['Serial Number']
            raid_vendor = rawData['Controllers'][item_raid]['Response Data']['Product Name'].split(' ')[0]

            data_raid = {
                'server_serial': server_serial,
                'raid_serial': raid_serial,
                'raid_vendor': raid_vendor,
                'raid_product': raid_product,
                'raid_capacity': raid_capacity,
                'raid_type': raid_type,
            }

            write_csv(settings.RESULT_FILE_RAID[0], data_raid, ORDER_RAID)
    except KeyError:
        pass

    print_headline(settings.RESULT_FILE_HDD_STORCLI[0], settings.COLUMNS_HDD, ORDER_HDD)
    try:
        for item_hdd in rawData['Controllers'][0]['Response Data']['PD LIST']:
            eid = item_hdd['EID:Slt'].split(':')[0]
            slot = item_hdd['EID:Slt'].split(':')[1]
            hdd_capacity = float(item_hdd['Size'].split(' ')[0])
            hdd_type = item_hdd['Med']
            hdd_slot = item_hdd['DID']

            filename = f'{settings.DIR_STORCLI}storcli-{server_serial}'
            rawData = json_read(filename)
            hdd_serial, hdd_vendor, hdd_product = getStorcliHDD(rawData, eid, slot)
            try:
                if hdd_vendor == 'ATA':
                    hdd_vendor = hdd_product.split(' ')[0]
                    hdd_product = hdd_product.split(' ')[1]   
            except IndexError:
                hdd_product = ''       

            # Data generation and writing to file
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
    except KeyError:
        pass


def getCard_lspci(filename):
    server_serial = filename.split('-')[1]
    full_filename = f'./scripts/network_lspci.sh {filename}'
    subprocess.run([full_filename], shell=True)
    card_list = []
    card_type = settings.CARD_TYPE
    card_vendor, card_remark, card_slot = [''] * 3

    with open('temp', 'r') as file:
        lines = file.readlines()
    
    for item in lines:
        if item.split(':')[0].strip() == 'Product Name' and \
            item.split(':')[1].strip() =='Example VPD':
            continue

        if item.split(':')[0].strip() == 'Product Name':
            card_product = item.split(':')[1].strip()
            card_list.append(card_product)
        
        if item.split(':')[0].strip() == '[SN] Serial number':
            card_serial = item.split(':')[1].strip()
            card_list.append(card_serial)
    
    for item in range(0, len(card_list), 2):
        # print(server_serial, card_list[item], card_list[item+1])
        if card_list[item] == 'T6225-CR':
            card_list[item] = 'SN1225'
            card_vendor = 'B4Com'
        elif card_list[item] == 'T62100-LP-CR':
            card_list[item] = 'SN12100'
            card_vendor = 'B4Com'
        elif 'ConnectX' in card_list[item]:
            card_vendor = 'Mellanox'
        else:
            card_vendor = ''
        card_serial = f'{card_list[item+1]}'
        data_card = {
            'server_serial': server_serial,
            'card_product': card_list[item],
            'card_vendor': card_vendor,
            'card_remark': card_remark,
            'card_serial': card_serial,
            'card_type': card_type,
            'card_slot': card_slot,
        }

        write_csv(settings.RESULT_FILE_CARD_LSPCI[0], data_card, ORDER_CARD)
    
    remove_file('temp')


def main():
    for item in os.listdir(settings.DIR_LSHW):
        filename = f'{settings.DIR_LSHW}{item}'
        rawData = json_read(filename)
        getInventory_lshw(rawData)

    for item in os.listdir(settings.DIR_SMARTCTL):
        filename = f'{settings.DIR_SMARTCTL}{item}'
        rawData = json_read(filename)
        getInventory_smartctl(rawData)

    for item in os.listdir(settings.DIR_STORCLI_CALL):
        filename = f'{settings.DIR_STORCLI_CALL}{item}'
        rawData = json_read(filename)
        server_serial = item.split('-')[1]
        getInventory_storcli(rawData, server_serial)

    for item in os.listdir(settings.DIR_LSPCI):
        filename = f'{settings.DIR_LSPCI}{item}'
        getCard_lspci(filename)


if __name__ == '__main__':
    remove_file(settings.RESULT_FILE_EQU[0])
    remove_file(settings.RESULT_FILE_CPU[0])
    remove_file(settings.RESULT_FILE_RAM[0])
    remove_file(settings.RESULT_FILE_HDD_LSHW[0])
    remove_file(settings.RESULT_FILE_HDD_SMARTCTL[0])
    remove_file(settings.RESULT_FILE_HDD_STORCLI[0])
    remove_file(settings.RESULT_FILE_CARD[0])
    remove_file(settings.RESULT_FILE_CARD_LSPCI[0])
    remove_file(settings.RESULT_FILE_RAID[0])
    main()
