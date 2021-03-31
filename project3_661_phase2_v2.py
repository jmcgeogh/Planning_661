#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:40:20 2021

@author: elliottmcg
"""

import cv2
import numpy as np
import sys
import math

Final_scale = 3
Illistration_scale = 1

def create_blank(width, height, rgb_color=(0, 0, 0)):
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    # OpenCV uses BGR, convert the color 
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

# Create new blank 400x300 black image
width, height = 400, 300
# Make image base black
black = (0, 0, 0)
im = create_blank(width, height, rgb_color=black)
# Get size of the image
row, col = im.shape[:2]
bottom = im[row-2:row, 0:col]
mean = cv2.mean(bottom)[0]
# Create copies of the image so drawing functions can run properly
obj1 = im.copy()
obj2 = im.copy()
obj3 = im.copy()
obj4 = im.copy()
obj5 = im.copy()

# Get points on drawn lines
def get_points(line):
    points = []
    for x in range(col):
        for y in range(row):
            b,g,r = line[y][x]
            if b == 255:
                points.append([x,y])
    return points

# # Draw angled rectangular objects
# def draw_angled_rec(pt0, pt1, pt2, pt3, img):
#     # Use OpenCV to draw lines
#     left = cv2.line(img, pt0, pt1, (255, 0, 0), 1)
#     cv2.line(img, pt1, pt2, (255, 0, 0), 1)
#     right = cv2.line(img, pt2, pt3, (255, 0, 0), 1)
#     cv2.line(img, pt3, pt0, (255, 0, 0), 1)
#     # Use OpenCV to fill in space between lines
#     left_points = np.array(get_points(left))
#     right_points = np.array(get_points(right))
#     right_points = np.flipud(right_points)
#     points = np.concatenate((left_points,right_points))
#     cv2.fillPoly(img, [points], color=[255,0,0])
    
# def buff(pt0, pt1, pt2, pt3, img):
#     # Use OpenCV to draw lines
#     left = cv2.line(img, pt0, pt1, (255, 255, 255), 1)
#     cv2.line(img, pt1, pt2, (255, 255, 255), 1)
#     right = cv2.line(img, pt2, pt3, (255, 255, 255), 1)
#     cv2.line(img, pt3, pt0, (255, 255, 255), 1)
#     # Use OpenCV to fill in space between lines
#     left_points = np.array(get_points(left))
#     right_points = np.array(get_points(right))
#     right_points = np.flipud(right_points)
#     points = np.concatenate((left_points,right_points))
#     cv2.fillPoly(img, [points], color=[255,255,255])
    
        

# # Call Drawing functions with defined endpoints
# draw_angled_rec((48,192), (37,176), (159,90), (171,106), obj1)
# buff((48,197), (32,176), (37,176), (48,192), obj2)    
# buff((32,176), (159,85), (159,90), (37,176), obj3)
# buff((159,85), (176,106), (171,106), (159,90), obj4)
# buff((176,106), (48,197), (48,192), (171,106), obj5)
        

# Merge the images to one image
im = obj2+obj1+obj3+obj4+obj5
# USe half-plane method to draw simgple objetcs
for y in range(row):
    for x in range(col):
        if x>=195 and x<= 235 and y>=15 and y<=35:
            im[y][x] = [255, 255, 255]
        if x>=200 and x<= 230 and y>=20 and y<=30:
            im[y][x] = [255, 0, 0]
        if x>=195 and x<= 215 and y>30 and y<=60:
            im[y][x] = [255, 255, 255]
        if x>=195 and x<= 235 and y>=55 and y<=75:
            im[y][x] = [255, 255, 255]
        if x>=200 and x<= 210 and y>=30 and y<=60:
            im[y][x] = [255, 0, 0]
        if x>=200 and x<= 230 and y>=60 and y<=70:
            im[y][x] = [255, 0, 0]
        if ((x-90)**2 + (y-230)**2) < 45**2:
            im[y][x] = [255, 255, 255]
        if ((x-90)**2 + (y-230)**2) < 35**2:
            im[y][x] = [255, 0, 0]
        if ((x-246)**2/(60)**2 + (y-155)**2/(30)**2) <= 1.5:
            im[y][x] = [255, 255, 255]
        if ((x-246)**2/(60)**2 + (y-155)**2/(30)**2) <= 1:
            im[y][x] = [255, 0, 0]
        if y < (1.45*x+122.18) and y > (1.33*x-122) and y < (-.7*x+210.56) and y > (-.7*x+180):
            im[y][x] = [255, 0, 0]
        if y > (1.45*x+122.18) and y < (1.45*x+128.18) and y > (-.7*x+185) and y < (-.7*x+215.56):
            im[y][x] = [255, 255, 255]
        if y < (1.33*x-122) and y > (1.33*x-128) and y > (-.7*x+185) and y < (-.7*x+215.56):
            im[y][x] = [255, 255, 255]
        if y > (-.7*x+210.56) and y < (-.7*x+215.56) and y < (1.45*x+128.18) and y > (1.33*x-128):
            im[y][x] = [255, 255, 255]
        if y > (-.7*x+180) and y < (-.7*x+185) and y < (1.45*x+128.18) and y > (1.33*x-128):
            im[y][x] = [255, 255, 255]
            
cost_matrix = np.zeros((row, col))
for x in range(col):
    for y in range(row):
        b,g,r = im[y][x]
        if b == 255:
            cost_matrix[y][x] == '#'
            
# Add borders to the image
def add_border(image):
    bordersize = 10
    border = cv2.copyMakeBorder(
        im,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 0, 0]
        )
    return border

# cv2.imshow('map', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# sys.exit()
# print('Active visualization requires a frame storage folder and the path variable updated')
# print('To visualize press 1. ')
# print('Otherwise press 0.')
# vis = input('Please make your selection: ')
# if int(vis) == 1:
#     print('\nOnce the program has stoppped running a visualization file will have been created in')
#     print('the folder where you have run this file.')
d = input('Please select step (1-10): ')
d = int(d)
# Ask user for starting point
sx = input(f'Please select starting x coordinate in range 0 to {col-1}: ')
sy = input(f'Please select starting y coordinate in range 0 to {row-1}: ')
sx_num = int(sx)
sy_num = int(sy)
# Make sure starting point is not in an object
while True:
    bs, gs, rs = im[sy_num,sx_num]
    print(im[sy_num,sx_num])
    if bs == 255:
        print('Starting coordinates are located inside object')
        sx = input('Please select x coordinate again: ')
        sy = input('Please select y coordinate again: ')
        sx_num = int(sx)
        sy_num = int(sy)
    else: 
        break
# Ask user for ending point
ex = input(f'Please select ending x coordinate in range 0 to {col-1}: ')
ey = input(f'Please select ending y coordinate in range 0 to {row-1}: ')
ex_num = int(ex)
ey_num = int(ey)
# Make sure ending point is not in an object
while True:
    be, ge, re = im[ey_num,ex_num]
    if be == 255:
        print('Ending coordinates are located inside object')
        ex = input('Please select x coordinate again: ')
        ey = input('Please select y coordinate again: ')
        ex_num = int(ex)
        ey_num = int(ey)
    else: 
        im[ey_num,ex_num] = [0,0,255]
        break

def theta_rad(theta):
    rad = (math.pi*theta)/180
    return rad

def MoveStraight(x,y,cost,theta):
    rad = theta_rad(theta)
    if rad == 0:
        x += d
    if rad == math.pi:
        x -= d
    if rad == (0.5*math.pi):
        y += d
    if rad == (1.5*math.pi):
        y -= d
    
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y += int(y_step*2)
    if x >= 0 and y >= 0 and x < row and y < col:
        b, g, r = im[y][x]
        if b == 0 and g == 0 and r == 0: 
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            cost += d + Euc
            cost_matrix[y][x] = cost
            return x, y, cost, theta
        else:
            return None, None, None, None
    else:
        return None, None, None, None

def MoveUp30(x,y,cost,theta):
    theta = theta + 30
    rad = theta_rad(theta)
    if rad == 0:
        x += d
    if rad == math.pi:
        x -= d
    if rad == (0.5*math.pi):
        y += d
    if rad == (1.5*math.pi):
        y -= d
    
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y -= int(y_step*2)
    if x >= 0 and y >= 0 and x < row and y < col:
        b, g, r = im[y][x]
        if b == 0 and g == 0 and r == 0: 
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            cost += d + Euc
            cost_matrix[y][x] = cost
            return x, y, cost, theta
        else:
            return None, None, None, None
    else:
        return None, None, None, None

def MoveUp60(x,y,cost,theta):
    theta = theta + 60
    rad = theta_rad(theta)
    if rad == 0:
        x += d
    if rad == math.pi:
        x -= d
    if rad == (0.5*math.pi):
        y += d
    if rad == (1.5*math.pi):
        y -= d
    
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y -= int(y_step*2)
    if x >= 0 and y >= 0 and x < row and y < col:
        b, g, r = im[y][x]
        if b == 0 and g == 0 and r == 0: 
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            cost += d + Euc
            cost_matrix[y][x] = cost
            
            return x, y, cost, theta
        else:
            return None, None, None, None
    else:
        return None, None, None, None

def MoveDown30(x,y,cost,theta):
    theta = theta - 30
    rad = theta_rad(theta)
    if rad == 0:
        x += d
    if rad == math.pi:
        x -= d
    if rad == (0.5*math.pi):
        y += d
    if rad == (1.5*math.pi):
        y -= d
    
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y -= int(y_step*2)
    if x >= 0 and y >= 0 and x < row and y < col:
        b, g, r = im[y][x]
        if b == 0 and g == 0 and r == 0: 
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            cost += d + Euc
            cost_matrix[y][x] = cost
            
            return x, y, cost, theta
        else:
            return None, None, None, None
    else:
        return None, None, None, None

def MoveDown60(x,y,cost,theta):
    theta = theta - 60
    rad = theta_rad(theta)
    if rad == 0:
        x += d
    if rad == math.pi:
        x -= d
    if rad == (0.5*math.pi):
        y += d
    if rad == (1.5*math.pi):
        y -= d
    print(rad)
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y -= int(y_step*2)
    if x >= 0 and y >= 0 and x < row and y < col:
        b, g, r = im[y][x]
        if b == 0 and g == 0 and r == 0: 
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            cost += d + Euc
            cost_matrix[y][x] = cost
            
            return x, y, cost, theta
        else:
            return None, None, None, None
    else:
        return None, None, None, None

visited = []
def move(x,y,cost,theta):
    visited.append([x,y])
    print('current xy', im[y][x])
    sx, sy, s_cost, theta_s = MoveStraight(x, y, cost, theta)
    u30_x, u30_y, u30_cost, theta_u30 = MoveUp30(x, y, cost, theta)
    u60_x, u60_y, u60_cost, theta_u60 = MoveUp60(x, y, cost, theta)
    d30_x, d30_y, d30_cost, theta_d30 = MoveDown30(x, y, cost, theta)
    d60_x, d60_y, d60_cost, theta_d60 = MoveDown60(x, y, cost, theta) 
    
    select_costs = [s_cost, u30_cost, u60_cost, d30_cost, d60_cost]
    select_x = [sx, u30_x, u60_x, d30_x, d60_x]
    select_y = [sy, u30_y, u60_y, d30_y, d60_y]
    select_theta = [theta_s, theta_u30, theta_u60, theta_d30, theta_d60]
    select_costs = [ x for x in select_costs if type(x) == np.float64]
    select_x = [ x for x in select_x if type(x) == int ]
    select_y = [ x for x in select_y if type(x) == int ]
    select_theta = [ x for x in select_theta if type(x) == int ]
    
    for i in range(len(select_costs)):
        cv2.arrowedLine(im, (y,x), (select_y[i],select_x[i]), (0,255,0))
            
    print('s cost', select_costs)
    print('s x', select_x)
    print('s y', select_y)
    print('s theta', select_theta)
    
    cost_index = select_costs.index(min(select_costs))
    new_cost = select_costs[cost_index]
    new_x = select_x[cost_index]
    new_y = select_y[cost_index]
    new_theta = select_theta[cost_index]
    for i in visited:
        if new_x == i[0] and new_y == i[1]:
            select_costs.pop(cost_index)
            select_x.pop(cost_index)
            select_y.pop(cost_index)
            select_theta.pop(cost_index)
            
            cost_index = select_costs.index(min(select_costs))
            new_cost = select_costs[cost_index]
            new_x = select_x[cost_index]
            new_y = select_y[cost_index]
            new_theta = select_theta[cost_index]
            
    print('new cost', new_cost)
    print('new x', new_x)
    print('new y', new_y)
    print('new theta', new_theta)
    
    return new_x, new_y, new_cost, new_theta
    
def goal(current_x, current_y):
    if (ex_num-1.5) < current_x < (ex_num+1.5) and (ey_num-1.5) < current_y < (ey_num+1.5):
        print('Goal Found!')
        return True
    else:
        return False

current_x = sx_num
current_y = sy_num
cost = cost_matrix[sx_num][sy_num]
current_theta = 0
count = 0
while True:
    if goal(current_x, current_y) == True:
        break
    imS = cv2.resize(add_border(im), (width*Final_scale, height*Final_scale))
    cv2.imshow("Finished", imS)
    cv2.waitKey(0)
    current_x, current_y, cost, current_theta = move(current_x, current_y, cost, current_theta)
    # if count == 2:
    #     break
    # count += 1
    
cv2.destroyAllWindows()
imS = cv2.resize(add_border(im), (width*Final_scale, height*Final_scale))
cv2.imshow("Finished", imS)
cv2.waitKey(0)
cv2.destroyAllWindows()