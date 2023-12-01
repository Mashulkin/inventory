# -*- coding: utf-8 -*-
"""
Writing and reading data to/from json, csv, txt files and removing
"""
import os.path
import json
import csv


__author__ = 'Vadim Arsenev'
__version__ = '1.0.0'
__date__ = '30.07.2021'


def json_write(pathFile, data):
    if not os.path.exists(os.path.dirname(pathFile)):
        os.makedirs(os.path.dirname(pathFile))

    with open(pathFile, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def json_read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_csv(pathFile, data, order):
    if not os.path.exists(os.path.dirname(pathFile)):
        os.makedirs(os.path.dirname(pathFile))

    with open(pathFile, 'a', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


def read_txt(filename):
    with open(filename, 'r') as file:
        text = file.read().strip()
    
    return text


def remove_file(pathFile):
    try:
        os.remove(pathFile)
    except FileNotFoundError:
        pass
