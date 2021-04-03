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

# Scale the output images
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

# Use half-plane method to draw simgple objetcs and buffers
for y in range(row):
    for x in range(col):
        if x>=195 and x<= 235 and y>=15 and y<=35:
            im[y][x] = [255, 255, 255]
        if x <= 4 or x >= 396:
            im[y][x] = [255, 255, 255]
        if y <= 4 or y >= 296:
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

# Create a cost matrix to be updated            
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

# cv2.imshow('map', add_border(im))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# sys.exit()

###
# Part of output visualization, leave commented out during console testing
# print('Active visualization requires a frame storage folder and the path variable updated')
# print('To visualize press 1. ')
# print('Otherwise press 0.')
# vis = input('Please make your selection: ')
# if int(vis) == 1:
#     print('\nOnce the program has stoppped running a visualization file will have been created in')
#     print('the folder where you have run this file.')
###

# User input for step
d = input('Please select step (1-10): ')
d = int(d)
# Ask user for starting point
sx = input(f'Please select starting x coordinate in range 5 to {col-5}: ')
sy = input(f'Please select starting y coordinate in range 5 to {row-5}: ')
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
ex = input(f'Please select ending x coordinate in range 5 to {col-5}: ')
ey = input(f'Please select ending y coordinate in range 5 to {row-5}: ')
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

# Convert theta ro radians
def theta_rad(theta):
    rad = (math.pi*theta)/180
    return rad

# Structure of the movement functions are the same
# Move straight based on orientation
def MoveStraight(x,y,cost,theta):
    # Call radian function
    rad = theta_rad(theta)
    if rad == 0:
        x += d
    if rad == math.pi:
        x -= d
    if rad == (0.5*math.pi):
        y += d
    if rad == (1.5*math.pi):
        y -= d
    
    # Update x and y values
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y -= int(y_step*2)
    # Ensure the new values are valid
    if x >= 0 and y >= 0 and x < col and y < row:
        b, g, r = im[y][x]
        if (b == 0 and g == 0 and r == 0) or (b == 0 and g == 255 and r == 0):
            # Get the Euclidian distance
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            # Update the cost
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
    if x >= 0 and y >= 0 and x < col and y < row:
        b, g, r = im[y][x]
        if (b == 0 and g == 0 and r == 0) or (b == 0 and g == 255 and r == 0):
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
    if x >= 0 and y >= 0 and x < col and y < row:
        b, g, r = im[y][x]
        if (b == 0 and g == 0 and r == 0) or (b == 0 and g == 255 and r == 0):
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
    if x >= 0 and y >= 0 and x < col and y < row:
        b, g, r = im[y][x]
        if (b == 0 and g == 0 and r == 0) or (b == 0 and g == 255 and r == 0):
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
    y_step = d*(math.sin(rad))
    x_step = d*(math.cos(rad))
    x_step = round(x_step * 2) / 2
    y_step = round(y_step * 2) / 2
    x += int(x_step*2)
    y -= int(y_step*2)
    if x >= 0 and y >= 0 and x < col and y < row:
        b, g, r = im[y][x]
        if (b == 0 and g == 0 and r == 0) or (b == 0 and g == 255 and r == 0):
            Euc = math.sqrt((ex_num - x)**2 + (ey_num - y)**2)
            cost += d + Euc
            cost_matrix[y][x] = cost
            
            return x, y, cost, theta
        else:
            return None, None, None, None
    else:
        return None, None, None, None

# Create storage lists
visited = []
secondary_x = []
secondary_y = []
secondary_cost = []
secondary_theta = []
back_path = []

# Movement function
def move(x,y,cost,theta, it):
    
    # Move in the 120 degree spread
    sx, sy, s_cost, theta_s = MoveStraight(x, y, cost, theta)
    u30_x, u30_y, u30_cost, theta_u30 = MoveUp30(x, y, cost, theta)
    u60_x, u60_y, u60_cost, theta_u60 = MoveUp60(x, y, cost, theta)
    d30_x, d30_y, d30_cost, theta_d30 = MoveDown30(x, y, cost, theta)
    d60_x, d60_y, d60_cost, theta_d60 = MoveDown60(x, y, cost, theta) 
    
    # Put outputs into lists and remove all instances of NONE being returned
    select_costs = [s_cost, u30_cost, u60_cost, d30_cost, d60_cost]
    select_x = [sx, u30_x, u60_x, d30_x, d60_x]
    select_y = [sy, u30_y, u60_y, d30_y, d60_y]
    select_theta = [theta_s, theta_u30, theta_u60, theta_d30, theta_d60]
    select_costs = [ x for x in select_costs if type(x) == np.float64]
    select_x = [ x for x in select_x if type(x) == int ]
    select_y = [ x for x in select_y if type(x) == int ]
    select_theta = [ x for x in select_theta if type(x) == int ]
    
    # Draw the spread into the map
    for i in range(len(select_costs)):
        cv2.arrowedLine(im, (x,y), (select_x[i],select_y[i]), (0,255,0))
            
    # print('s cost', select_costs)
    # print('s x', select_x)
    # print('s y', select_y)
    # print('s theta', select_theta)
    
    # Get the new values from the spread
    if select_costs != []:
        cost_index = select_costs.index(min(select_costs))
        new_cost = select_costs.pop(cost_index)
        new_x = select_x.pop(cost_index)
        new_y = select_y.pop(cost_index)
        new_theta = select_theta.pop(cost_index)
        # Ensure current values are not in visited
        n = 1
        while n != 0:
            n = 0
            for i in visited:
                if new_x == i[0] and new_y == i[1]:
                    if select_costs != []:
                        cost_index = select_costs.index(min(select_costs))
                        new_cost = select_costs.pop(cost_index)
                        new_x = select_x.pop(cost_index)
                        new_y = select_y.pop(cost_index)
                        new_theta = select_theta.pop(cost_index)
                        n = 1
                    else: 
                        del back_path[-1]
                        new_cost = secondary_cost[-1]
                        new_x = secondary_x[-1]
                        new_y = secondary_y[-1]
                        new_theta = secondary_theta[-1]
                        break
        # Update path list
        back_path.append([new_x, new_y])
        # If possible create secondary values
        if select_costs != []:
            cost_index = select_costs.index(min(select_costs))
            second_cost = select_costs.pop(cost_index)
            second_x = select_x.pop(cost_index)
            second_y = select_y.pop(cost_index)
            second_theta = select_theta.pop(cost_index)
            
            d = 1
            while d != 0:
                d = 0
                for i in visited:
                    if second_x == i[0] and second_y == i[1]:
                        d = 1
                        if select_costs != []:
                            cost_index = select_costs.index(min(select_costs))
                            second_cost = select_costs.pop(cost_index)
                            second_x = select_x.pop(cost_index)
                            second_y = select_y.pop(cost_index)
                            second_theta = select_theta.pop(cost_index) 
                        else:
                            second_cost = None
                            second_x = None
                            second_y = None
                            second_theta = None
                            break
        else:
            second_cost = None
            second_x = None
            second_y = None
            second_theta = None
                        
    else:   
        it += 1
        new_cost = secondary_cost[-it]
        new_x = secondary_x[-it]
        new_y = secondary_y[-it]
        new_theta = secondary_theta[-it]
        del back_path[-1]
        
        back_path.append([new_x, new_y])
        
        second_cost = None
        second_x = None
        second_y = None
        second_theta = None
    # Update visited list and secondary list        
    visited.append([new_x, new_y])
    if second_cost != None:
        secondary_cost.append(second_cost)
        secondary_x.append(second_x)
        secondary_y.append(second_y)
        secondary_theta.append(second_theta)
        
    # print('new cost', new_cost)
    # print('new x', new_x)
    # print('new y', new_y)
    # print('new theta', new_theta)
    # print('second cost', secondary_cost[-1])
    # print('second x', secondary_x[-1])
    # print('second y', secondary_y[-1])
    # print('second theta', secondary_theta[-1])
    
    return new_x, new_y, new_cost, new_theta, it

# Check if goal is reached
def goal(current_x, current_y):
    if (ex_num-1.5) < current_x < (ex_num+1.5) and (ey_num-1.5) < current_y < (ey_num+1.5):
        print('Goal Found!')
        return True
    else:
        return False

# Backtrack based on path list
def backtrack(mark):
    for i in mark:
        im[i[1]][i[0]] = (0,0,255)
    
    pts = np.array(mark)
    
    cv2.polylines(im, [pts], False, (0,0,255), 2)
    return

# Create video frame generated frames
def visual(frames):
    path = '/home/elliottmcg/Desktop/School/Second Semester/Planning_661/frames/'
    img=[]
    for i in range(0,frames):
        img.append(cv2.imread(path+f'frame{i}.jpg'))
        
    height,width,layers=img[1].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    name = 'project3_phase2_solution.avi'
    video=cv2.VideoWriter(name, fourcc, 15,(width,height))

    for j in range(0,len(img)):
        video.write(img[j])

    cv2.destroyAllWindows()
    video.release()
    return

# Starting conditions
current_x = sx_num
current_y = sy_num
cost = cost_matrix[sy_num][sx_num]
visited.append([current_x, current_y])
back_path.append([current_x, current_y])
if sx_num < ex_num:
    current_theta = 0
if sx_num > ex_num:
    current_theta = 180
count = 0
it = 0

# Loop until goal is reached
while True:
    if goal(current_x, current_y) == True:
        backtrack(back_path)
        break
    
    current_x, current_y, cost, current_theta, it = move(current_x, current_y, cost, current_theta, it)
    
    # Display the map being built
    imS = cv2.resize(add_border(im), (width*Final_scale, height*Final_scale))
    cv2.imshow("Finished", imS)
    cv2.waitKey(1)
    
    ###
    # Part of video creation, replace path variable with frame storage location
    path = '/home/elliottmcg/Desktop/School/Second Semester/Planning_661/frames/'
    cv2.imwrite((path+f'frame{count}.jpg'), imS)
    ###
    count += 1
    
cv2.destroyAllWindows()
# Display the final map with optimal path
imS = cv2.resize(add_border(im), (width*Final_scale, height*Final_scale))
cv2.imshow("Finished", imS)
cv2.waitKey(0)
cv2.destroyAllWindows()

###
# Part of video create, leave commented out    
visual(count)
###