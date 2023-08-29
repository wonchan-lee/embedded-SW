# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 14:41:37 2023

@author: wonchan
"""

import serial
import time
import cv2
import pyzbar.pyzbar as pyzbar

import numpy as np
import sys
import cv2
import serial
import time
sys.path.append('./python_code')

split1 = ['A', 'B', 'C', 'D', 'E']
split2 = ['F', 'G', 'H', 'I', 'J']

# Box 객체 설정
class CUSTOMER:
    def __init__(self, t_class, seat, weight):
        self.t_class = t_class
        self.seat = seat
        self.weight = weight
    
    def get_customer_info(self):
        return [self.t_class, self.seat, self.weight]




# while문 안에 작성하고, 바깥에 break할 키를 설정해준다.
# + cv2.destroyAllWindows()
def get_barcode(cap, valid=0):
    
    my_code = None
    biggest_contour=None

    
    success, frame = cap.read()
    
    # barcode and height ###################
    for code in pyzbar.decode(frame):
        ## 높이 측정###### barcode#####################
        try:
            x_b, y_b, w_b, h_b = code.rect
            my_code = code.data.decode('utf-8')
            frame=cv2.rectangle(frame, (x_b, y_b), (x_b + w_b, y_b + h_b), (0, 0, 255), 2)
            frame=cv2.putText(frame, my_code, (x_b , y_b - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        except: 
            pass
        
    # barcode and height ###################
    
    
    # 바코드가 인식되면 time을 0으로 주어 trigger 신호를 보낸다.
    if not(my_code == None):
        valid = 1

    return (frame, valid, my_code)

def stack_box(cap, customer_num, port_conv, port_op):
    
    sucess, frame = cap.read()
    # 변수 설정
    valid = 0 # 박스를 인식했는지 확인하는 변수
    start, end, time_tmp = (0, 0, 0) # 시간을 재기 위한 함수
    customer_list = []
    code_list = []

    # 핵심 변수
    customer_num = customer_num # customer 숫자를 설정해서 이 숫자를 넘어가면, 프로그램 종료


    # conveyor_belt serial 객체
    # conveyor_belt = serial.Serial(
    #     port=port_conv,
    #     baudrate=9600,
    # )

    # openmanupulator serial 객체
    # openmanipulator = serial.Serial(
    #     port=port_op,
    #     baudrate=115200,
    # )
    
    while True:
        # 박스 크기 및 바코드 인식
        # 바코드가 인식된 후 3초 기다린다.
        # 그 후 바코드 번호, 박스 lwh를 반환한다.
        frame, valid, code = get_barcode(cap, valid)
        cv2.imshow("frame", frame)

        if valid == 1 and start == 0:
            start = time.time()
            
        if valid == 1:
            end = time.time()
        
        # valid한 바코드가 인식된 후 지난 시간
        time_tmp = int(end - start)
        
        # 바코드를 인식한 후 3초가 지나면
        if time_tmp >= 2 and valid==1:
            # 바코드: "클래스 좌석 무게"
            try:
                barcode = code.split()
                ## temp로 code가 있으면 pass
                if code_list.__contains__(code):
                    valid = 0
                    start = 0
                    end = 0
                    print("중복된 값입니다.")
                    
                    # 컨베이어 벨트를 작동시켜 다음 박스를 움직이도록 하는 코드
                    
                else:
                    
                    # barcode test
                    tmp_customer = CUSTOMER(barcode[0], barcode[1], int(barcode[2]))
                    customer_list.append(tmp_customer)
                    code_list.append(code)
                    valid = 0
                    start = 0
                    end = 0
                    print(code)
                    print("#", tmp_customer.seat, tmp_customer.t_class)
                          
                    
                    # 컨베이어 벨트를 작동시켜 다음 박스를 움직이도록 하는 코드
                    print('AAA')
                    #conveyor_belt.write('A'.encode())
                    # time.sleep(15)
                    # if tmp_customer.t_class == 'First':
                    #     openmanipulator.write('F'.encode())
                    # elif tmp_customer.t_class == 'Business':
                    #     openmanipulator.write('B'.encode())
                    # else:
                    #     if tmp_customer.seat[0] in split1:
                    #         openmanipulator.write('E'.encode())
                    #     elif tmp_customer.seat[0] in split2:
                    #         openmanipulator.write('G'.encode())
                    #     else:
                    #         openmanipulator.write('H'.encode())
                    
            except:
                valid = 0
                start = 0
                end = 0
        
        # while문을 탈출하는 logic
        
        key = cv2.waitKey(1)
        if key == 27 or (len(code_list) == customer_num) :
            
            #barcode test
            print(customer_list)
            break
        
    cv2.destroyAllWindows()
