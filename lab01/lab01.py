# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 16:55:53 2020

@author: COURAGE
"""


def image_correction(distorted_image_file, corrected_image_file, a_b, c_d):
    '''' This function takes in a distorted image, the coordinates of
    4 points (c_d) in the distorted image and uses 4 arbitrary points (a_b) to correct 
    the perspective distortion of the input image'''
    
    from PIL import Image
    import numpy as np
    import numpy.linalg as LA
    
    input_image = Image.open(distorted_image_file) #importing the image file
    input_image_array = np.asarray(input_image, np.float) #converting the image to a numpy array
    
    #Creation of an A matrix which will be used to find the transformation matrix needed to correct the immage
    A = np.zeros((8,8), np.float)
    
    for i in range(8):
        '''This for loop replaces the zeros in the A matrix with 
        the proper values using values from c_d and a_b '''
        if i%2 == 0:
            A[i] = [c_d[i], c_d[i+1], 1, 0, 0, 0, (-a_b[i]*c_d[i]), (-a_b[i]*c_d[i+1])]
        else:
            A[i] = [0, 0, 0, c_d[i-1], c_d[i], 1, (-a_b[i]*c_d[i-1]), (-a_b[i]*c_d[i])]
    
    a_b = np.transpose(np.asarray([a_b])) #converts a_b to an 8x1 matrix
    # Note that A*h = a_b where h is the values of all components except 1 in the transformation matrix
    # The h matrix is represent as H since it is going to be used to compute the transformation matrix H

    H = np.matmul(LA.inv(A), a_b)
    H  = np.vstack([H, np.asarray([1])]) #Addition of 
    # Creation of the 3x3 transformation matrix used for the image correction
    H = np.reshape(H, (3,3)) 

    corrected_image = np.zeros(input_image_array.shape, np.uint8)
    # The corrected image has the same dimension as the distorted image
    # only that it is created with zero RGB values
    
    for i in range(corrected_image.shape[0]):
        for j in range(corrected_image.shape[1]):
            # This for loop goes through every pixel in the corrected image
            # and transforms all pixel location in the distorted image to the corrected image pixel
            # then copy all pixel values in distorted image to the appropriate locations in the transformed image
            v = np.asarray([[i], [j], [1]]) #convert the pixels from 2-D vectors to homogeneous vectors
            x = np.matmul(LA.inv(H), v) #gets the homogeneous vecor of the transformed pixel
            x_1 = int(np.round(x[0]/x[2])) #converts the homogeneous vectors to points on the 2-D plane
            x_2 = int(np.round(x[1]/x[2]))
            if (x_1 < corrected_image.shape[0]) and (x_2 < corrected_image.shape[1]) and (x_1 >= 0) and (x_2 >= 0):
                corrected_image[i][j] = input_image_array[x_1][x_2] # maps the corrected image to the transformed pixels

    Image.fromarray(corrected_image).save(corrected_image_file)
    
# For PC_test1
ab_1 = [400, 100, 600, 100, 400, 400, 600, 400] 
cd_1= [300, 201, 433, 138, 300, 399, 433, 482]
   
image_correction("PC_test_1.jpg", "PC_test1_Corrected.jpg", ab_1, cd_1)

#For PC_test2
ab_2 = [410, 830, 500, 830, 410, 1000, 500, 1000]
cd_2 = [347, 444, 439, 444, 304, 751, 476, 751]

image_correction("PC_test_2.jpg", "PC_test2_Corrected.jpg", ab_2, cd_2)
