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
import time

# 카메라 세팅
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# 변수 설정
max_val = 0 # 박스 height 최대값, w_b가 지속적으로 변하기 때문에 크기 고정
B = (1, 1, 1, 1) # 바코드 크기 초기 설정값, 0으로 나누면 에러
lwh = [0, 0, 0] # length, width, height 초기 설정값
valid = 0 # 박스를 인식했는지 확인하는 변수
start, end, time_tmp = (0, 0, 0) # 시간을 재기 위한 함수
customer_num = 20 # customer 숫자를 설정해서 이 숫자를 넘어가면, 
customer_list = []

# Box 객체 설정
class CUSTOMER:
    def __init__(self, lwh, t_class, seat, weight):
        self.lwh = lwh
        self.t_class = t_class
        self.seat = seat
        self.weight = weight
    
    def get_customer_info(self):
        return [self.lwh, self.t_class, self.seat, self.weight]


# trackbar 열기
plot_trackbar()

while True:
    # 박스 크기 및 바코드 인식
    # 바코드가 인식된 후 2초 기다린다.
    # 그 후 바코드 번호, 박스 lwh를 반환한다.
    frame, mask, max_val, B, lwh, valid, code = get_box_size_and_barcode(cap, lwh, valid, max_val, B)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    
    if valid == 1 and start == 0:
        start = time.time()
        
    if valid == 1:
        end = time.time()
    
    # valid한 바코드가 인식된 후 지난 시간
    time_tmp = int(end - start)
    
    # 바코드를 인식한 후 2초가 지나면
    if time_tmp == 2 and valid==1:
        # 바코드: "클래스 좌석 무게"
        barcode = code.split()
        tmp_customer = CUSTOMER(lwh, barcode[0], barcode[1], barcode[2])
        customer_list.append(tmp_customer)
        valid = 0
        start = 0
        end = 0
        # 컨베이어 벨트를 작동시켜 다음 박스를 움직이도록 하는 코드
    
    # while문을 탈출하는 logic
    key = cv2.waitKey(1)
    if key == 27 or (len(customer_list) == customer_num):
        # box를 그리는 로직 실행
        break
    
cv2.destroyAllWindows()
