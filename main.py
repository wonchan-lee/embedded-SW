# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:32:31 2023

@author: wonchan
"""
import sys
import cv2
import serial
import time
sys.path.append('./python_code')

from box_size_detection import get_box_size_and_barcode, plot_trackbar
from struck_code_each_weight_color_added import draw_box_function 


# 카메라 세팅
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# 변수 설정
max_val = 0 # 박스 height 최대값, w_b가 지속적으로 변하기 때문에 크기 고정
B = (1, 1, 1, 1) # 바코드 크기 초기 설정값, 0으로 나누면 에러
lwh = [0, 0, 0] # length, width, height 초기 설정값
valid = 0 # 박스를 인식했는지 확인하는 변수
start, end, time_tmp = (0, 0, 0) # 시간을 재기 위한 함수
real_wb = (1, 1) # 박스 w, l 을 얻기 위한 변수
customer_list = []
code_list = []

# 핵심 변수
customer_num = 5 # customer 숫자를 설정해서 이 숫자를 넘어가면, 프로그램 종료

# conveyor_belt serial 객체
conveyor_belt = serial.Serial(
    port='COM7',
    baudrate=9600,
)

openmanipulator = serial.Serial(
    port='COM8',
    baudrate=115200,
)



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
    # 바코드가 인식된 후 3초 기다린다.
    # 그 후 바코드 번호, 박스 lwh를 반환한다.
    frame, mask, max_val, B, lwh, valid, code, real_wb = get_box_size_and_barcode(cap, lwh, real_wb, valid, max_val, B)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    
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
                tmp_customer = CUSTOMER(lwh, barcode[0], barcode[1], int(barcode[2]))
                customer_list.append(tmp_customer)
                code_list.append(code)
                valid = 0
                start = 0
                end = 0
                max_val = 0
                print(code)
                print("#", tmp_customer.lwh, tmp_customer.seat, tmp_customer.t_class)
                      
                # # box test
                # code_list.append(code)
                # valid = 0
                # start = 0
                # end = 0
                # print(lwh, code)
                
                # 컨베이어 벨트를 작동시켜 다음 박스를 움직이도록 하는 코드
                conveyor_belt.write('A'.encode())
                time.sleep(1)
                if tmp_customer.t_class == 'First':
                    openmanipulator.write('F'.encode())
                elif tmp_customer.t_class == 'Business':
                    openmanipulator.write('B'.encode())
                else:
                    openmanipulator.write('E'.encode())
                
        except:
            valid = 0
            start = 0
            end = 0
    
    # while문을 탈출하는 logic
    
    key = cv2.waitKey(1)
    if key == 27 or (len(code_list) == customer_num) :
        
        #barcode test
        print(customer_list)
        
        # box를 그리는 로직 실행
        draw_box_function(3, customer_list)
        
        break
    
cv2.destroyAllWindows()
