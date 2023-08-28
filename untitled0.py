# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 15:46:31 2023

@author: wonchan
"""
 
import sys
import serial
import time

conveyor_belt = serial.Serial(
    port="COM9",
    baudrate=9600,
)

openmanipulator = serial.Serial(
    port='COM10',
    baudrate=115200,
)

while True:
    test = input("enter B:")
    if test == "B":
        conveyor_belt.write('A'.encode())
        time.sleep(15)
        openmanipulator.write('F'.encode())