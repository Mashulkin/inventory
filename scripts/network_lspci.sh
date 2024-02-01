#!/bin/bash
grep -i '.0 Ethernet' -A60 $1 | grep 'Product Name\|Serial number' > temp
grep -i '.0 Infiniband' -A60 $1 | grep 'Product Name\|Serial number' >> temp
