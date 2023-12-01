# -*- coding: utf-8 -*-
"""
Getting 
"""
from simple_settings import settings
from functions.common_modules import json_read, json_write, write_csv, read_txt, remove_file
from functions.headline import print_headline
from functions.cpu import getCPU
from functions.ram import getRAM
from functions.hdd import getHDD
from functions.card import getCARD


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '29.11.2023'


ORDER_CPU = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_CPU).split('\n')))
ORDER_RAM = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_RAM).split('\n')))
ORDER_HDD = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_HDD).split('\n')))
ORDER_CARD = list(map(lambda x: x.split(':')[0].strip(), \
    read_txt(settings.COLUMNS_CARD).split('\n')))


def getInventoryCPU(rawData):
    """
    The main module for performing all operations of a request
       and writing to a file
    """
    # ***** Main query *****
    hostname = rawData['id']
    server_vendor = rawData['vendor']
    server_product = rawData['product']
    server_serial = rawData['serial']

    for raw_item in rawData['children']:
        if raw_item['id'] == 'core':            
            for children in raw_item['children']:
                # if children['description'] == 'PCI bridge':
                #     print(children)
                # *** CPU ***
                try: 
                    if children['class'] == 'processor':
                        print_headline(settings.RESULT_FILE_CPU[0], settings.COLUMNS_CPU, ORDER_CPU)
                        cpu_vendor, cpu_slot, cpu_product, cpu_frequency, \
                            cpu_cores = getCPU(children)

                        # Data generation and writing to file
                        data_cpu = {
                            'hostname': hostname,
                            'server_vendor': server_vendor,
                            'server_product': server_product,
                            'server_serial': server_serial,
                            'cpu_vendor': cpu_vendor,
                            'cpu_slot': cpu_slot,
                            'cpu_product': cpu_product,
                            'cpu_frequency': cpu_frequency,
                            'cpu_cores': cpu_cores,
                        }

                        write_csv(settings.RESULT_FILE_CPU[0], data_cpu, ORDER_CPU)

                except KeyError:
                    pass

                # *** RAM ***
                try:
                    if children['class'] == 'memory' and children['description'] == 'System Memory':
                        print_headline(settings.RESULT_FILE_RAM[0], settings.COLUMNS_RAM, ORDER_RAM)
                        for item_ram in children['children']:
                            ram_vendor, ram_serial, ram_type, ram_slot, \
                                ram_product, ram_capacity = getRAM(item_ram)
                            if ram_vendor == 'NO DIMM':
                                continue

                            # Data generation and writing to file
                            data_ram = {
                                'server_serial': server_serial,
                                'ram_vendor': ram_vendor,
                                'ram_serial': ram_serial,
                                'ram_type': ram_type,
                                'ram_slot': ram_slot,
                                'ram_product': ram_product,
                                'ram_capacity': ram_capacity,
                            }

                            write_csv(settings.RESULT_FILE_RAM[0], data_ram, ORDER_RAM)

                except KeyError:
                    pass

                # *** HDD ***
                try:
                    if children['class'] == 'bridge' and children['children'][0]['class'] == 'storage':
                        print_headline(settings.RESULT_FILE_HDD[0], settings.COLUMNS_HDD, ORDER_HDD)
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

                            write_csv(settings.RESULT_FILE_HDD[0], data_hdd, ORDER_HDD)

                except KeyError:
                    pass

                # *** CARD ***
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


def main():
    for item in settings.INVENTORY:
        rawData = json_read(item)
        getInventoryCPU(rawData)


if __name__ == '__main__':
    remove_file(settings.RESULT_FILE_CPU[0])
    remove_file(settings.RESULT_FILE_RAM[0])
    remove_file(settings.RESULT_FILE_HDD[0])
    remove_file(settings.RESULT_FILE_CARD[0])
    main()
