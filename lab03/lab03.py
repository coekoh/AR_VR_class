# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:29:05 2020

@author: COURAGE
"""

from PIL import Image
import numpy as np

#Open the tif image using Pillow
rwanda = Image.open("Rwanda_SRTM30meters.tif")

#Parsing the image as numpy array
rwanda_array = np.asarray(rwanda, np.uint16)

rwanda_min = rwanda_array.min() #Getting the minimum elevation of Rwanda // min = 914

#Setting all max values (Places outside Rwanda) to zero or black
rwanda_original = np.where(rwanda_array == rwanda_array.max(), 0, rwanda_array)

rwanda_max = rwanda_original.max() #Getting the maximum elevation of //max = 4501

#Linearly rescaling so array takes on values fro 0 to 255
rwanda_array = np.interp(rwanda_original, [0, rwanda_max], [0, 255]).astype(np.uint8)

#Converting the array to image
Image.fromarray(rwanda_array).save('rwanda_monochrome.jpg')

#Subsampling by a factor of 10m on both sides
new_array = np.zeros((round(rwanda_original.shape[0]/10), round(rwanda_original.shape[1]/10)), np.uint8)

for i in range(new_array.shape[0]):
    for j in range(new_array.shape[1]):
        row = i*10
        col = j*10
        new_array[i][j] = rwanda_original[row:row+10,col:col+10].max()
     
f = "f -3 -2 -1\n"

file = open("rwanda_topology.obj", "w")

#Threshhold = 3000

for i in range(new_array.shape[0] - 1):
    for j in range(new_array.shape[1] - 1):
        file.write("v %d %d %d\n" %(j, i, new_array[i][j]))
        file.write("v %d %d %d\n" %(j+1, i, new_array[i][j+1]))
        file.write("v %d %d %d\n" %(j, i+1, new_array[i+1][j]))
        file.write(f)
        file.write("v %d %d %d\n" %(j, i+1, new_array[i+1][j]))
        file.write("v %d %d %d\n" %(j+1, i, new_array[i][j+1]))
        file.write("v %d %d %d\n" %(j+1, i+1, new_array[i+1][j+1]))
        file.write(f)
        
        
file.close()