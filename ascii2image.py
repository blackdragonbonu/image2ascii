"""
This program converts a given image into an ascii art. For this we first convert the  image into grayscale. Then we follow it up by representing each range of gray scale by an ascii character. 
To view it properly:
    1. Redirect the output to a file
    python image2ascii.py <image path> > <file>
    2. open file in sublime text
    3. Zoom out and adjust font size so that it can be seen properly in the window
    4. Increase sampling factor to reduce detail, min value of sampling factor is 1
    5. Contrast Factor can be used to increase contract, though often not useful
"""

#imports
from __future__ import print_function
import numpy as np
import argparse as ap
from PIL import Image


#Constants being used

#these form the elements to represent grayscale, in increasing order of pixe l values
asciiscale=list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")
#contrast Factor, to increase image contrast
CF=1

#sampling factor
SF=1


def transform_to_grayscale(image):
    return image.convert('L')

#the image passed should be a 2d grayscale image
def convert_to_ascii(input_image):
    #we convert the image into an array
    image=np.array(input_image)

    #Since we are printing in ASCII the characters are wider, so twice sampling rate along y axis than x axis
    (x,y),x_scale,y_scale=image.shape,2*SF,SF

    #Enhancing the contrast by a factor of 5
    image=np.clip(((image-128)*CF+128),0,255)

    #we create an empty char array as output 
    x_out,y_out=x//x_scale,y//y_scale
    out_image=np.chararray((x_out,y_out))

    #we assign each element the corresponding value
    for i in range(x_out):
        for j in range(y_out):
            av_pixel=np.mean(image[i*x_scale:(i+1)*x_scale,j*y_scale:(j+1)*y_scale])
            pixel_density=int((av_pixel*(len(asciiscale)-1)//255))
            out_image[i,j]=asciiscale[pixel_density]
    return out_image


#image must be numpy char array
def display_image(image):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            print(image[i,j],end="")
        print('')



def parse_args():
    parser=ap.ArgumentParser()
    parser.add_argument("file",help="path of the image that you want to be converted")
    args=parser.parse_args()
    return args


if __name__=="__main__":
    args=parse_args()
    image_orig=Image.open(args.file)
    image_gray=transform_to_grayscale(image_orig)
    ascii_array=convert_to_ascii(image_gray)
    display_image(ascii_array)


