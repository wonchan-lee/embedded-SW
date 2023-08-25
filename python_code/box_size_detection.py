import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar


# while문 안에 작성하고, 바깥에 break할 키를 설정해준다.
# + cv2.destroyAllWindows()
def get_box_size_and_barcode(cap, lwh, real_wb=(1, 1), valid=0, max_val = 0, B=(1, 1, 1, 1), real_w_b=2.8, cam_height=32.3):
    
    # local variable 처리
    x_b = B[0]
    y_b = B[1]
    w_b = B[2]
    h_b = B[3]
    real_w = real_wb[0]
    real_h = real_wb[1]
    my_code = None
    biggest_contour=None

    # 변수
    # 바코드 길이(cm)
    real_w_b=real_w_b
    # 카메라 중간까지 높이(cm)
    cam_height=cam_height
    
    success, frame = cap.read()
    frame_b = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # barcode and height ###################
    for code in pyzbar.decode(frame_b):
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
        
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")
    
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])


    # mask지정해주기
    mask = cv2.inRange(hsv, l_b, u_b)
    # mask의 경계선을 표시해준다
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    # 표시해주는 범위를 사각형으로 표시해줌
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    try:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    except:
        pass
    x, y, w, h = cv2.boundingRect(biggest_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #5.5, 3.5 | 355, 240 | 32.3 | ratio = 길이xcam_height/실제길이 = 2,084.8181, 2,214.8571 | 2,149.8376
   

    if max_val < round(((w_b/real_w_b)/cam_height)*6.7, 2):
        max_val = round(((w_b/real_w_b)/cam_height)*6.7, 2)
        last_real_w_b = real_w_b
        real_w = round((w/w_b)*(last_real_w_b), 2)
        real_h = round((h/w_b)*(last_real_w_b), 2)
        
        
    try:
        real_w = 3# round((w/w_b)*(last_real_w_b), 2)
        real_h = 3#round((h/w_b)*(last_real_w_b), 2)
    except:
        pass
        
    height = 3# max_val
            
    
    if real_w < 1 or real_h < 1:
        max_val = 0
        height=0
    
    # 원래 y-20
    frame=cv2.putText(frame, f'width:{real_w}, length:{real_h}, height:{height}', (x , y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return (frame, mask, max_val, B, [real_w, real_h, height], valid, my_code, (real_w, real_h))

def plot_trackbar():
    
    def nothing(x):
        pass
    
    cv2.namedWindow("Tracking", flags=cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(winname='Tracking', width=400, height=300)
    cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)    
 
    

