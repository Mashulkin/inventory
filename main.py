# -*- coding: utf-8 -*-
"""
Getting 
"""
import os
import subprocess
from simple_settings import settings
from functions.common_modules import json_read, write_csv, read_txt, remove_file
from functions.headline import print_headline
from functions.cpu import getCPU
from functions.ram import getRAM
from functions.hdd import getSmartHDD, getStorcliHDD
from functions.raid import getRAID
from functions.card import getCARD


__author__ = 'Vadim Arsenev'
__version__ = '2.0.0'
__date__ = '13.02.2024'


def getInventory_lshw(rawData):
    """
    The main module for queries to lshw files
        and writing the resulting values to a csv file
    """
    hostname = rawData['id']
    server_vendor = rawData['vendor']
    server_product = rawData['product']
    server_serial = rawData['serial']

    # Data generation and writing to file equipment.csv
    data_equ = {
        'server_serial': server_serial,
        'hostname': hostname,
        'server_vendor': server_vendor,
        'server_product': server_product,
    }
    print_headline(settings.RESULT_FILE_EQU[0], settings.COLUMNS_EQU, ORDER_EQU)
    write_csv(settings.RESULT_FILE_EQU[0], data_equ, ORDER_EQU)

    # Data generation and writing to files cpu.csv, ram.csv
    for raw_item in rawData['children']:
        if raw_item['id'] == 'core':            
            for children in raw_item['children']:
                # *** CPU ***
                print_headline(settings.RESULT_FILE_CPU[0], settings.COLUMNS_CPU, ORDER_CPU)
                try: 
                    if children['class'] == 'processor':
                        getCPU(children, server_serial, ORDER_CPU)
                except KeyError:
                    pass

                # *** RAM ***
                print_headline(settings.RESULT_FILE_RAM[0], settings.COLUMNS_RAM, ORDER_RAM)
                try:
                    if children['class'] == 'memory' and children['description'] == 'System Memory':
                        for item_ram in children['children']:
                            getRAM(item_ram, server_serial, ORDER_RAM)
                except KeyError:
                    pass
    return server_product


def getInventory_smartctl(rawData):
    """
    The main module for queries to smartctl files
        and writing the resulting values to a csv file
    """
    # *** HDD ***
    print_headline(settings.RESULT_FILE_HDD_SMARTCTL[0], settings.COLUMNS_HDD, ORDER_HDD)
    server_serial = rawData[0]['server_serial']
    for item_hdd in rawData:
        getSmartHDD(item_hdd, server_serial, ORDER_HDD)


def getInventory_storcli(rawData, server_serial):
    """
    The main module for queries to storcli files
        and writing the resulting values to a csv file
    """
    # *** RAID ***
    print_headline(settings.RESULT_FILE_RAID[0], settings.COLUMNS_RAID, ORDER_RAID)
    for item_raid in range(len(rawData['Controllers'])):
        getRAID(rawData, item_raid, server_serial, ORDER_RAID)

    # *** HDD ***
    print_headline(settings.RESULT_FILE_HDD_STORCLI[0], settings.COLUMNS_HDD, ORDER_HDD)
    for item_raid in range(len(rawData['Controllers'])):
        # Ignoring errors on controllers
        try:
            for item_hdd in rawData['Controllers'][item_raid]['Response Data']['PD LIST']:
                filename = f'{settings.DIR_STORCLI}storcli-{server_serial}'
                rawDiskData = json_read(filename)
                getStorcliHDD(item_raid, rawDiskData, item_hdd, server_serial, ORDER_HDD)
        except KeyError:
            pass


def getCard_lspci(filename):
    """
    The main module for queries to lspci files
        and writing the resulting values to a csv file
    """
    # Running bash script and writing grep in temp file
    full_filename = f'./scripts/network_lspci.sh {filename}'
    subprocess.run([full_filename], shell=True)

    server_serial = filename.split('-')[1]
    print_headline(settings.RESULT_FILE_CARD_LSPCI[0], settings.COLUMNS_CARD, ORDER_CARD)
    getCARD(server_serial, ORDER_CARD)
    
    remove_file('temp')


def main():
    # *** lshw ***
    for item in os.listdir(settings.DIR_LSHW):
        filename = f'{settings.DIR_LSHW}{item}'
        rawData = json_read(filename)
        getInventory_lshw(rawData)

    # *** smartctl ***
    for item in os.listdir(settings.DIR_SMARTCTL):
        filename = f'{settings.DIR_SMARTCTL}{item}'
        rawData = json_read(filename)
        getInventory_smartctl(rawData)

    # *** storcli
    for item in os.listdir(settings.DIR_STORCLI_CALL):
        filename = f'{settings.DIR_STORCLI_CALL}{item}'
        # not installed smartcli
        try:
            rawData = json_read(filename)
        except ValueError:
            continue

        server_serial = item.split('-')[1]
        getInventory_storcli(rawData, server_serial)

    # *** lspci ***
    for item in os.listdir(settings.DIR_LSPCI):
        filename = f'{settings.DIR_LSPCI}{item}'
        getCard_lspci(filename)


if __name__ == '__main__':
    # deleting all old csv files
    remove_file(settings.RESULT_FILE_EQU[0])
    remove_file(settings.RESULT_FILE_CPU[0])
    remove_file(settings.RESULT_FILE_RAM[0])
    remove_file(settings.RESULT_FILE_HDD_SMARTCTL[0])
    remove_file(settings.RESULT_FILE_HDD_STORCLI[0])
    remove_file(settings.RESULT_FILE_CARD_LSPCI[0])
    remove_file(settings.RESULT_FILE_RAID[0])

    # setting the order of fields in сым files
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
    
    main()
