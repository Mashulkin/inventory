#!/bin/bash
grep -i '.0 Ethernet' -A60 $1 | grep 'controller: Mellanox\|controller: Chelsio\|Physical Slot\|Product Name\|Serial number' > temp
grep -i '.0 Infiniband' -A60 $1 | grep 'controller: Mellanox\|Physical Slot\|Product Name\|Serial number' >> temp
grep -i '.0 Fibre' -A60 $1 | grep 'Fibre Channel:\|Physical Slot\|Product Name\|Serial number' >> temp
