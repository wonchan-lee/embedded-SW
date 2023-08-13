# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 21:15:52 2023

@author: wonchan
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import mpl_toolkits.mplot3d.art3d as art3d
import random

############################################################## for draw test


def draw_box_function(class_num=1, customer_list = None, ):   
    
    # 설정 변수
    ## Size of truck(1cm unit)
    TRUCK_L = 30    #x
    TRUCK_W = 30    # y
    TRUCK_H = 30    # z
            
    TOP_CLASS = 1
    #Econom를 split한 수
    Economy_split_num = 3
    test = [3, 10, 10, 10, 5]
    
    # weight, lwh setting for test, 추후에 수정
    WEIGHT = [[customer.weight for customer in customer_list ]]
    LWH = [[[int(customer.lwh[0]), int(customer.lwh[1]), int(customer.lwh[2])] for customer in customer_list]]
    
    # sort by weight
    W_LWH = [[[WEIGHT[i][j], LWH[i][j]] for j in range(test[i])] for i in range(TOP_CLASS)]
    W_LWH_temp = W_LWH
    weight_sorted = []
    
    def rect_prism(x_range, y_range, z_range):
          yy, zz = np.meshgrid(y_range, z_range)
          ax.plot_wireframe(x_range[0], yy, zz, color="black")
          ax.plot_wireframe(x_range[1], yy, zz, color="black")
    
          xx, zz = np.meshgrid(x_range, z_range)
          ax.plot_wireframe(xx, y_range[0], zz, color="black")
          ax.plot_wireframe(xx, y_range[1], zz, color="black")
    
    ############################################################### for draw test
    
    # 각 좌표 범위에서 겹치는 부분이 있는지 검사하는 코드 
    def axis_invasion_test(grid1, grid2):
        num = 0
        
        for i in range(grid1[0], grid1[1]+1):
            for j in range(grid2[0], grid2[1]+1):
                if i==j: num+=1
                
        if num > 1:
            return True
        else:
            return False
    
    def invasion_test(grids1, grids2):
        x_check = axis_invasion_test(grids1[0], grids2[0])
        y_check = axis_invasion_test(grids1[1], grids2[1])   
        z_check = axis_invasion_test(grids1[2], grids2[2])
        return x_check and y_check and z_check
    
    
    class Box:
        
        # pos[x, y, z]: 박스 위치, lwh[l, w, h]: 박스 크기, color'color': 박스 색깔
        def __init__(self, pos, lwh, color, weight):
            self.pos_X = pos[0]
            self.pos_Y = pos[1]
            self.pos_Z = pos[2]
            self.l = lwh[0]
            self.w = lwh[1]
            self.h = lwh[2]
            self.color = color
            self.weight = weight
        
        # self Box의 position을 바꾸는 함수
        def chage_pos(self, pos):
            self.pos_X = pos[0]
            self.pos_Y = pos[1]
            self.pos_Z = pos[2]
            
        # self Box의 position을 바꾸는 함수
        def chage_lwh(self, lwh):
            self.l = lwh[0]
            self.w = lwh[1]
            self.h = lwh[2]
        
        # 현재 박스가 차지하는 공간을 return {'x':x축 범위, 'y':y축 범위, 'z':z축 범위}
        def occupied_space(self):
            return [[self.pos_X, self.pos_X + self.l], [self.pos_Y, self.pos_Y + self.w], [self.pos_Z, self.pos_Z+self.h]]
        
        # subject Box가 self Box를 침범하는지 확인하는 코드
        # True : 해당 박스를 침범, False : 해당 박스를 침범하지 않음
        
        
        # box를 좌표계에 추가해주는 코드
        def draw_Box(self, ax):
            side = Rectangle((self.pos_X, self.pos_Y), self.l, self.w, fill=True, facecolor=self.color, edgecolor='black')
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=self.pos_Z, zdir='z')
            ## 윗면
            side = Rectangle((self.pos_X, self.pos_Y), self.l, self.w, fill=True, facecolor=self.color, edgecolor='black')
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=self.pos_Z+self.h, zdir='z')
            ## 뒷면
            side = Rectangle((self.pos_Y, self.pos_Z), self.w, self.h, fill=True, facecolor=self.color, edgecolor='black')
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=self.pos_X, zdir='x')
            ## 앞면
            side = Rectangle((self.pos_Y, self.pos_Z), self.w, self.h, fill=True, facecolor=self.color, edgecolor='black')
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=self.pos_X+self.l, zdir='x')
            ## 왼쪽
            side = Rectangle((self.pos_X, self.pos_Z), self.l, self.h, fill=True, facecolor=self.color, edgecolor='black')
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=self.pos_Y, zdir='y')
            ## 오른쪽
            side = Rectangle((self.pos_X, self.pos_Z), self.l, self.h, fill=True, facecolor=self.color, edgecolor='black')
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=self.pos_Y+self.w, zdir='y')
        
    def get_hex_color(i, j):
        val = hex(int((W_LWH_temp[i][j][0])*255/W_LWH_temp[i][test[i]-1][0]))[2:]
        if len(val) == 1:
            val = f'0{val}'
            
        if i < Economy_split_num:
            val = f'#{val}0000'
        elif i == Economy_split_num:
            val = f'#00{val}00'
        else: 
            val = f'#0000{val}'
        # print(i, j, val)
        return val   
        
    # Truck 범위를 넘는지 확인하는 함수
    def check_in_truck(pos, lwh):
        x = pos[0] + lwh[0]
        y = pos[1] + lwh[1]
        z = pos[2] + lwh[2]
        return x <= TRUCK_L and y <= TRUCK_W and z <= TRUCK_H
    
    ########################################################################## stack Test
    # CLASS, BOX NUM
    
    # 색깔 부여
    TOP_COLORS=[]
    for i in range(Economy_split_num):
        TOP_COLORS.append('#ff0000')
    TOP_COLORS.append('#00ff00') # Business 색깔
    TOP_COLORS.append('#0000ff') # First 색깔
    
    
    
    # 무게가 무거운 순
    for i in range(TOP_CLASS):
        W_LWH[i].sort(key=lambda x:x[0], reverse=True)
    
    for j in range(test[0]):
        weight_sorted.append(W_LWH[0][j][0])
    
    # 무게가 가벼운 순 : 색깔을 진한게 무거운 것으로 설정하 위함
    for i in range(TOP_CLASS):
        W_LWH_temp[i].sort(key=lambda x:x[0])    
    
    # 무게에 따른 색갈 부여
    COLORS = [ [ get_hex_color(i, j) for j in range(test[i])] for i in range(TOP_CLASS)]
    
    TEST_LIST = []
    total_iter_num = 0
    for TEST in range(TOP_CLASS):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_aspect('auto')
        rect_prism(np.array([0, TRUCK_L]), np.array([0, TRUCK_W]), np.array([0, TRUCK_H]))
        CLASS = 1
        BOX_NUM = [test[TEST]]
        #COLORS = [TOP_COLORS[TEST]]
        BOX = []
        #WEIGHT = [ [ j for j in reversed(range(BOX_NUM[i]))] for i in range(CLASS)]
        # POS, LWH
        S_POSITION= [0, 0, 0]
        S_POSITION_tmp = [0, 0, 0]
        # LWH = [5, 5, 5]
        
        # set empty BOX, LWH assign
        BOX = [[0 for j in range(BOX_NUM[i])] for i in range(CLASS)]
        
        # set color
        
        ####
        total_num = 0
        for i in range(CLASS):
            total_num += BOX_NUM[i]
        
        BOX_tmp = [0 for i in range(total_num)]

        
        # 첫 번째 BOX 만들기
        BOX[0][0] = Box(S_POSITION, W_LWH[TEST][0][1], COLORS[TEST][0], W_LWH[TEST][0][0])
        BOX_tmp[0] = Box(S_POSITION, W_LWH[TEST][0][1], COLORS[TEST][0], W_LWH[TEST][0][0])
        
        # GRID의 순서로 우선순위 정함
        TEST_GRID = [[i, j, k] for k in range(TRUCK_H) for j in range(TRUCK_W) for i in range(TRUCK_L)]
        iter_num = 0
        start = 0
        valid_box = 0
        
        
        for i in range(CLASS):
              for j in range(BOX_NUM[i]):
                  
                # i == 0 and j == 0일 땐 Box 생성 XS
                if i == 0 and j == 0:
                    BOX[i][j].draw_Box(ax)
                    continue
                start+=1
                # BOX 생성
                test_truck = TRUCK_H*TRUCK_L*TRUCK_W
                
                for i_count in range(test_truck):
                    for tmp in range(start):
        
                            grids1 = BOX_tmp[tmp].occupied_space()
                            grids2 = [[TEST_GRID[i_count][0], TEST_GRID[i_count][0]+LWH[i][j][0]], [TEST_GRID[i_count][1], TEST_GRID[i_count][1]+LWH[i][j][0]], [TEST_GRID[i_count][2], TEST_GRID[i_count][2]+LWH[i][j][0]]]
        
                            iter_num +=1
                            total_iter_num += 1
                            #print(iter_num)
                            if not(invasion_test(grids1, grids2)) and check_in_truck(TEST_GRID[i_count], LWH[i][j]):
                                valid_box += 1
        
                    if valid_box == start : 
                        S_POSITION = TEST_GRID[i_count]
                        BOX[i][j] = Box(S_POSITION, LWH[i][j], COLORS[TEST][j], WEIGHT[i][j])
                        #print(COLORS[start])
                        BOX_tmp[start] = Box(S_POSITION, LWH[i][j], COLORS[TEST][j], WEIGHT[i][j])
                        BOX[i][j].draw_Box(ax)
                        valid_box = 0
                        break
                    
                    valid_box = 0
        TEST_LIST.append(iter_num)
        plt.draw() 
    
    print(f"iter_nums:{TEST_LIST}, totla_iter_num: {total_iter_num}\n")
    print(f"origin weight:{WEIGHT[0]} \n\nsorted weight:{weight_sorted}")