# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 12:22:15 2020

@author: COURAGE
"""

def occulus_view(left_image, right_image):
    from PIL import Image
    import numpy as np
    
    left_eye = Image.open(left_image)
    right_eye = Image.open(right_image)
    
    left_array = np.asarray(left_eye, np.float)
    
    #Create a numpy array of zeros
    background_image = np.zeros((2048, 4096, 3), np.uint8)
    
    #Convert the zero numpy array to two black images
    background1 = Image.fromarray(background_image)
    background2 = Image.fromarray(background_image)
    
    top_left_col = int((background_image.shape[1] - left_array.shape[1])/2)
    top_left_row = int((background_image.shape[0] - left_array.shape[0])/2)
    
    
    #paste both pictures into the dark background
    background1.paste(left_eye,(top_left_col, top_left_row))
    background2.paste(right_eye,(top_left_col, top_left_row))
    
 
    image_1 = np.asarray(background1, np.uint8)
    image_2 = np.asarray(background2, np.uint8)
    
    #Stack both images on one another
    final = np.vstack([image_1, image_2]) 
    
    #Output final image
    Image.fromarray(final).save('out.jpg', quality=95)
    
    
    
occulus_view("left_eye.jpg", "right_eye.jpg")