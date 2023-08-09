# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:32:31 2023

@author: wonchan
"""

from box_size_detection import get_box_size_and_barcode, plot_trackbar
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

# 카메라 세팅
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# 변수 설정
max_val = 0 # 박스 height 최대값, w_b가 지속적으로 변하기 때문에 크기 고정

# trackbar 열기
plot_trackbar()

while True:
    
    # 박스 크기 및 바코드 인식
    # 바코드가 인식된 후 2초 기다린다.
    # 그 후 바코드 번호, 박스 lwh를 반환한다.
    frame, mask, max_val = get_box_size_and_barcode(cap, max_val)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cv2.destroyAllWindows()
