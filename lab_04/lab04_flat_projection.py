# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:34:19 2020

@author: COURAGE
"""

def flat_projection(input_image_name, output_image_name):
    '''This function creates a flat projection of an input image and gives an output of the projection'''
    from PIL import Image
    import numpy as np
    import math
    
    #Import Image
    image = Image.open(input_image_name)
    
    #Resize Image
    
    ratio = 1024/image.size[0]
    resized_image = image.resize((round(image.size[0]*ratio), round(image.size[1]*ratio)))
    
    resized_image_array = np.asarray(resized_image, np.uint8)
    
    #Initialize a black image
    black_image = np.zeros((2048, 2048, 3), np.uint8)
            
    #Image.fromarray(black_image).show()
    
    N = 2048 #The width and height of the output image
    z = 1024  #The distance of the viewer from the image
    
    # Calculating the maximum latitute and longitude
    max_long = math.atan(black_image.shape[1]/(2*z))
    max_lat = math.atan(black_image.shape[0]/(2*z))
    
    # Declaring a list of a;; the angles to loop through in the image for lat and long
    angles = np.arange(-math.pi/2, math.pi/2, math.pi/N)
    
    # loop through the rows of the output image
    for row in range(black_image.shape[0]):
        lat  = angles[row] #assign values to latitude by indexing into the angles list
        
        #loop through the columns of the output image
        for col in range(black_image.shape[1]):
            long = angles[col] # assign values to the longitude
            
            # Check if the longitude and latitude fall within the range for the max values
            if (long <= max_long) and (lat <= max_lat) and (long >= -max_long) and (lat >= -max_lat):
                
                #Calculate r, x, and y
                r = z / (math.cos(lat) * math.cos(long))
                x = r * math.cos(lat) * math.sin(long)
                y = r * math.sin(lat)
                
                # Convert (x, y) from CICS to PICS (a, b)           
                (c1, c2) = (resized_image_array.shape[1]/2, resized_image_array.shape[0]/2)
                a = round(x + c1)
                b = round(y + c2)
                
                #Check if the PICS equivalent is inside the output image pixel range
                if (a < resized_image_array.shape[1]) and (b < resized_image_array.shape[0]) and (a >= 0) and (b >= 0):
                    #Assign pixel colors to the output image
                    black_image[row, col] = resized_image_array[b, a]
                
    #Show the image
    Image.fromarray(black_image).show()
    
    #Save the image to an output file
    Image.fromarray(black_image).save(output_image_name)
    
    return print("Successfully created a flat projection of %s as %s" %(input_image_name, output_image_name))


# Run the flat projection function on an image
flat_projection("resourceCentre.jpg", "lab04_flatProjectionOutput.jpg")
