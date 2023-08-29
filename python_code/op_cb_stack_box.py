# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:41:37 2023

@author: wonchan
"""

import serial
import time

split1 = ['A', 'B', 'C', 'D', 'E']
split2 = ['F', 'G', 'H', 'I', 'J']


def stack_box(customer_list, port_conv, port_op):
    
    # conveyor_belt serial 객체
    conveyor_belt = serial.Serial(
        port=port_conv,
        baudrate=9600,
    )

    # openmanupulator serial 객체
    openmanipulator = serial.Serial(
        port=port_op,
        baudrate=115200,
    )
    
    for customer in customer_list:
        conveyor_belt.write('A'.encode())
        time.sleep(15)
        if customer.t_class == 'First':
            openmanipulator.write('F'.encode())
        elif customer.t_class == 'Business':
            openmanipulator.write('B'.encode())
        else:
            if customer.seat[0] in split1:
                openmanipulator.write('E'.encode())
            elif customer.seat[0] in split2:
                openmanipulator.write('G'.encode())
            else:
                openmanipulator.write('H'.encode())