#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:40:20 2021

@author: elliottmcg
"""

import cv2
import numpy as np
import sys
import math
 
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

# Get points on drawn lines
def get_points(line):
    points = []
    for x in range(col):
        for y in range(row):
            b,g,r = line[y][x]
            if b == 255:
                points.append([x,y])
    return points

# Draw angled rectangular objects
def draw_angled_rec(pt0, pt1, pt2, pt3, img):
    # Use OpenCV to draw lines
    left = cv2.line(img, pt0, pt1, (255, 0, 0), 1)
    cv2.line(img, pt1, pt2, (255, 0, 0), 1)
    right = cv2.line(img, pt2, pt3, (255, 0, 0), 1)
    cv2.line(img, pt3, pt0, (255, 0, 0), 1)
    # Use OpenCV to fill in space between lines
    left_points = np.array(get_points(left))
    right_points = np.array(get_points(right))
    right_points = np.flipud(right_points)
    points = np.concatenate((left_points,right_points))
    cv2.fillPoly(img, [points], color=[255,0,0])
    
# Draw angled non-rectangular objects
def draw_obj(pt0, pt1, pt2, pt3, pt4, img):
    # Use OpenCV to draw lines
    cv2.line(img, pt0, pt1, (255, 0, 0), 1)
    cv2.line(img, pt1, pt2, (255, 0, 0), 1)
    line1 = cv2.line(img, pt2, pt3, (255, 0, 0), 1)
    cv2.line(img, pt3, pt4, (255, 0, 0), 1)
    line2 = cv2.line(img, pt4, pt0, (255, 0, 0), 1)
    # Use OpenCV to fill in space between lines
    points1 = np.array(get_points(line1))
    points2 = np.array(get_points(line2))
    points2 = np.flipud(points2)
    points = np.concatenate((points1,points2))
    cv2.fillPoly(img, [points], color=[255,0,0])

# Call Drawing functions with defined endpoints
draw_angled_rec((48,192), (37,176), (159,90), (171,106), obj1)
draw_angled_rec((328,237), (286,195), (328,153), (370,195), obj2)
draw_obj((328,153), (348,156), (381,129), (381,184), (370,195), obj3)

# Merge the images to one image
im = obj1 + obj2 + obj3
# USe half-plane method to draw simgple objetcs
for y in range(row):
    for x in range(col):
        if x>=200 and x<= 230 and y>=20 and y<=30:
            im[y][x] = [255, 0, 0]
        if x>=200 and x<= 210 and y>=30 and y<=60:
            im[y][x] = [255, 0, 0]
        if x>=200 and x<= 230 and y>=60 and y<=70:
            im[y][x] = [255, 0, 0]
        if ((x-90)**2 + (y-230)**2) < 35**2:
            im[y][x] = [255, 0, 0]
        if ((x-246)**2/(60)**2 + (y-155)**2/(30)**2) <= 1:
            im[y][x] = [255, 0, 0]
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
# Ask user for starting point
sx = input(f'Please select starting x coordinate in range 0 to {col-1}: ')
sy = input(f'Please select starting y coordinate in range 0 to {row-1}: ')
sx_num = int(sx)
sy_num = int(sy)
# Make sure starting point is not in an object
while True:
    bs, gs, rs = im[sy_num,sx_num]
    if bs == 255:
        print('Starting coordinates are located inside object')
        sx = input('Please select x coordinate again: ')
        sy = input('Please select y coordinate again: ')
        sx_num = int(sx)
        sy_num = int(sy)
    else: 
        start = [sy_num,sx_num]
        break
# Ask user for ending point
ex = input(f'Please select starting x coordinate in range 0 to {col-1}: ')
ey = input(f'Please select starting y coordinate in range 0 to {row-1}: ')
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
# Create tree for bfs
tree = {1: [sy_num,sx_num]} 
# Function to check if goal has been reached
def goal(x,y, parent, child):
    scale = 5
    cv2.destroyAllWindows()
    imS = cv2.resize(add_border(im), (width*scale, height*scale))
    # Find optimal path from ghoal node to start
    path(parent, child)
    cv2.imshow("Finished", imS)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit()
# Function to output the optimal path based on tracking dictionary
def path(parent, child):
    # Print track dict to see all parent child combinations
    print(track)
    print('Optimal Node Path: ')
    # Convert keys and values to lists 
    key_list = list(track.keys())
    val_list = list(track.values())
    # Create path list
    opt_path = [child, parent]
    # Create corrisponding coordiante list
    coord_path = []
    # Iterate through track from gaol parent and child to starting
    while True:
        if opt_path[-1] == 1:
            print(opt_path)
            print('Corresponding Coordinates:')
            for node in opt_path:
                # Add prevouse node to the list
                coord_path.append(tree[node])
            print(coord_path)
            break
        # Creat lsit of corrisponding coordinates
        for value in val_list:
            for i in range(len(value)):
                if value[i] == parent:
                    position = val_list.index(value)
                    parent = key_list[position]
                    opt_path.append(parent)
                    
    return
# Check the pixel up from the current pixel
def up(x,y,state, count):
    up = y - 1 
    # Check if out of bounds
    if up >= 0:
        # check pixel color
        b,g,r = (im[up,x])
        # If black the pixel is not visited
        if b == 0 and g == 0 and r == 0:
            # Make the pixel white
            im[up,x] = [255,255,255]
            # Update tree with next location to visit in the while loop
            tree[state] = [up,x]
            # Log location as child of current parent 
            track[count].append(state)
            # Initialize next child number
            state += 1
            # Return updated child number
            return state
        # If red it is the goal pixel
        elif b == 0 and g == 0 and r == 255:
            # Log current coordinates
            tree[state] = [up,x]
            # Log current parent child combination
            track[count].append(state)
            print(f'Goal found at child {state}, inside parent {count}')
            # Run through goal function
            goal(x, up, count, state)
        else:
            # Return unchange child number
            return state
    else:
        return state
# All following movement function are the same structure
# Check the pixel up and right from the current pixel
def up_right(x,y,state, count):
    up = y - 1
    right = x + 1
    if up >= 0 and right < col:
        b,g,r = (im[up,right])
        if b == 0 and g == 0 and r == 0:
            im[up,right] = [255,255,255]
            tree[state] = [up,right]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [up,right]
            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(right, up, count, state)
        else:
            return state
    else:
        return state
# Check the pixel right from the current pixel    
def right(x,y,state, count):
    right = x + 1
    if right < col:
        b,g,r = (im[y,right])
        if b == 0 and g == 0 and r == 0:
            im[y,right] = [255,255,255]
            tree[state] = [y,right]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [y,right]
            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(right, y, count, state)
        else: 
            return state
    else: 
        return state
# Check the pixel down and right from the current pixel
def down_right(x,y,state, count):
    down = y + 1
    right = x + 1
    if down < row and right < col:
        b,g,r = (im[down,right])
        if b == 0 and g == 0 and r == 0:
            im[down,right] = [255,255,255]
            tree[state] = [down,right]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [down,right]
            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(right, down, count, state)
        else: 
            return state
    else: 
        return state
# Check the pixel down from the current pixel
def down(x,y,state, count):
    down = y + 1
    if down < row:
        b,g,r = (im[down,x])
        if b == 0 and g == 0 and r == 0:
            im[down,x] = [255,255,255]
            tree[state] = [down,x]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [down,x]
            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(x, down, count, state)
        else: 
            return state
    else:
        return state
# Check the pixel down and left from the current pixel
def down_left(x,y,state, count):
    down = y + 1
    left = x - 1
    if down < row and left >= 0:
        b,g,r = (im[down,left])
        if b == 0 and g == 0 and r == 0:
            im[down,left] = [255,255,255]
            tree[state] = [down,left]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [down,left]

            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(left, down, count, state)
        else: 
            return state
    else:
        return state
# Check the pixel left from the current pixel
def left(x,y,state, count):
    left = x - 1 
    if left >= 0:
        b,g,r = (im[y,left])
        if b == 0 and g == 0 and r == 0:
            im[y,left] = [255,255,255]
            tree[state] = [y,left]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [y,left]
            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(left, y, count, state)
        else:
            return state
    else:
        return state
# Check the pixel up and left from the current pixel
def up_left(x,y,state, count):
    up = y - 1
    left = x - 1
    if up >= 0 and left >= 0:
        b,g,r = (im[up,left])
        if b == 0 and g == 0 and r == 0:
            im[up,left] = [255,255,255]
            tree[state] = [up,left]
            track[count].append(state)
            state += 1
            return state
        elif b == 0 and g == 0 and r == 255:
            tree[state] = [up,left]
            track[count].append(state)
            print(f'Goal found at child {state} of parent {count}')
            goal(left, up, count, state)
        else:
            return state
    else: 
        return state
# Start the count at 1 for the {key} of the tree dictionary
count = 1
# Start the state at 2 for the {value} of the track dictionary
state = 2
# initialize the track dictionary to log parent and child relationships
track = {1: []}
# iterate until goal is found
while True:
    # Get the starting position
    current_x = tree[count][1]
    current_y = tree[count][0]
    # Check color of current pixel
    b,g,r = (im[current_y,current_x])
    # If the color is red then it is the goal pixel
    if b == 0 and g == 0 and r == 255:
        print(f'Goal found at start, position {current_y, current_x}')
        break
    # if it is balck make it white
    if b == 0 and r == 0 and g == 0:
        im[current_y,current_x] = [255,255,255]
    # Initialize the next parent in the track dictionary
    track[count] = []
    # Iterate through the positions with updating state
    state = up(current_x, current_y, state, count)
    state = up_right(current_x, current_y, state, count)
    state = right(current_x, current_y, state, count)
    state = down_right(current_x, current_y, state, count)
    state = down(current_x, current_y, state, count)
    state = down_left(current_x, current_y, state, count)
    state = left(current_x, current_y, state, count)
    state = up_left(current_x, current_y, state, count)
    # Scale the output image to your liking
    scale = 1
    imS = cv2.resize(add_border(im), (width*scale, height*scale))
    cv2.imshow("Building", imS)
    cv2.waitKey(1)
    count += 1
    
cv2.destroyAllWindows()
scale = 5
imS = cv2.resize(add_border(im), (width*scale, height*scale))
cv2.imshow("Finished", imS)
cv2.waitKey(0)
cv2.destroyAllWindows()