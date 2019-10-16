import sys
from PIL import Image
import numpy
from scipy import misc
import os
import datetime

DIFFERENCE_THRESHOLD = 10

def resize_images(baseline_image, compare_image):

    if compare_image.size != baseline_image.size:
        print("WARNING: Size of images does not match.")
    baseline_image_width, baseline_image_height = baseline_image.size
    compare_image = compare_image.resize(baseline_image.size)#Scale to size in case they don't match
    return baseline_image, compare_image


def convert_two_images_to_rgba(images_array):

    baseline_image = images_array[0].convert("RGBA")
    compare_image = images_array[1].convert("RGBA")
    return baseline_image, compare_image


def get_output_image_pixels(mask, compare_image_pixel_values, ignore_mask = None):

    i = 0

    if ignore_mask == None:
        while i < len(compare_image_pixel_values):
            j = 0
            while j < len(compare_image_pixel_values[i]):
                if mask[i][j][0] == True:
                    compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
                j = j + 1
            i = i + 1
    else:
        while i < len(compare_image_pixel_values):
            j = 0
            while j < len(compare_image_pixel_values[i]):
                if mask[i][j][0] == True and ignore_mask[i][j][0] == False: #and scan_region_wave_space[i][j][0] == False:
                    compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
                elif ignore_mask[i][j][0] == True:
                    compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [50, -50, 50, 100])
                #elif scan_region_wave_space[i][j][0] == True:
                    #compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-20, 70, 0, 100])
                j = j + 1
            i = i + 1
    return compare_image_pixel_values


def save_output_image_from_array(pixel_array):

    if not os.path.isdir("../Output"):
        os.mkdir("../Output")

    currentDT = datetime.datetime.now()
    image_name = '../Output/Output_' + str(currentDT) + '.png'
    misc.imsave(image_name, pixel_array)
    output_image = Image.open(image_name)
    output_image = output_image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    output_image.save(image_name)


def adjust_for_ignore_regions(difs, ignore_mask = None):

    if ignore_mask.any():
        difs[ignore_mask] = 0
    return difs


def adjust_for_scan_regions(baseline_image_pixel_values, compare_image_pixel_values, ignore_mask_array, scan_region_sub_image_pixels = None, scan_region_wave_space = None):
 if scan_region_sub_image_pixels.any():
        i = 0
        scan_x = len(scan_region_sub_image_pixels)
        scan_y = len(scan_region_sub_image_pixels[0])
        #Take the sub image out of the baseline image.
        sub_img = baseline_image_pixel_values[:scan_x, :scan_y]
        #if look_for_within(compare_image_pixel_values, sub_image,)
        #while i < scan_x:
        #    j = 0
        #    while j < scan_y:
        #        x = scan_x + i
        #        y = scan_y + j
        #        print scan_y
        #        print x
        #        pixels = baseline_image_pixel_values[:x, :y]#x:x+x
 
        #        pixels = baseline_image_pixel_values[:x, :y]#x:x+x
        #        difs = numpy.subtract(pixels, sub_img)
        #        total_difs = numpy.sum(difs)
        #        if (total_difs == 0):
        #            ignore_mask_array[scan_x + 1][scan_y + j] = True
        #        j = j + 1
        #    i = i + 1``


def count_nonzero(gray_array):
    count = 0
    i = 0
    while i < len(gray_array):
        if(numpy.count_nonzero(gray_array[i]) > 0):
            count = count + 1
        i = i + 1
    return count

#For a perfect match
def look_for_within(container_image, sub_image, start_x, start_y, x_range, y_range):

    for i in range(start_x, start_x + x_range):

        for j in range(start_y, start_y + y_range):

            width, height = sub_image.size
            y1 = j
            x1 = i
            y2 = y1 + height
            x2 = x1 + width

            cropped_image = container_image.crop((x1, y1, x2, y2))
            res = diffs(sub_image, cropped_image)

            if (res > 0):
                return (i, j)
    return None

#Convert one rgb pixel to lab
def Pxl_rgb2lab(pixel): #pixel will be a 4-D array RGBa (a ignored)
    #Convert to XYZ
    ref_Whites = numpy.array([95.047, 100.0, 108.883, 1])
    for i in range(3):
        val = pixel[i] / 255
        if val > 0.04045:
            val= ( ( (val) + 0.055 ) / 1.055) ** 2.4
        else:
            val = val / 12.92
        pixel[i] = round(val * 100, 4)
    X = pixel [0] * 0.4124 + pixel [1] * 0.3576 + pixel [2] * 0.1805
    Y = pixel [0] * 0.2126 + pixel [1] * 0.7152 + pixel [2] * 0.0722
    Z = pixel [0] * 0.0193 + pixel [1] * 0.1192 + pixel [2] * 0.9505
    pixel = numpy.array([X,Y,Z,pixel[3]])
    #Convert to lab
    for i in range(3):

        val = pixel[i] / ref_Whites[i]
        if val > 0.008856:
            val = val ** (1/3)
        else:
            val = (903.3 * val + 16 )/ 116
        pixel[i] = val
    
    L = round(( 116 * pixel[1] ) - 16, 4)
    a = round(500 * ( pixel[0] - pixel[1] ), 4)
    b = round(200 * ( pixel[1] - pixel[2] ), 4)
    return numpy.array([L, a , b, pixel[3]])


def Img_rgb2lab(image): #Image is a XxYx4 numpy array or list

    dims = image.shape
    for n in range(dims[1]):

        for m in range(dims[2]):
            
            image[m,n,:] = Pxl_rgb2lab(image[m,n,:])

    return image        


def diffs(baseline_image, compare_image, ignore_mask_image = None):

    baseline_image, compare_image = convert_two_images_to_rgba(resize_images(baseline_image, compare_image))
    width, height = baseline_image.size

    baseline_image_pixel_values, compare_image_pixel_values = list(baseline_image.getdata()), list(compare_image.getdata())

    baseline_image_pixel_values = numpy.array(baseline_image_pixel_values).reshape(width, height, 4, order="F")
    compare_image_pixel_values = numpy.array(compare_image_pixel_values).reshape(width, height, 4, order="F")

    difs = numpy.subtract(compare_image_pixel_values, baseline_image_pixel_values)
    #ignore_mask_array = None

    if ignore_mask_image != None:
        pixels = list(ignore_mask_image.getdata())
        pixels = numpy.array(pixels).reshape(width, height, 4, order="F")
        ignore_mask_array = pixels < 68

        #Color thresholds based on SPECIFIC gray values, where (68, 68, 68) is the sub-image and
        #light gray is the scan region.
        #TODO1 This could be optimized to only look @ one axis very easily
        image_pixels_greater_than_zero = pixels > 0
        image_pixels_greater_than_sixty_eight = pixels > 68
        image_pixels_less_than_two_hundred = pixels < 200

        #Get scan & sub-image boxes
        scan_region_sub_image_pixels = image_pixels_greater_than_sixty_eight != image_pixels_greater_than_zero      
        scan_region_wave_space = image_pixels_greater_than_sixty_eight == image_pixels_less_than_two_hundred

        #get x and get y
        
        scan_x = count_nonzero(scan_region_sub_image_pixels)
        scan_y = count_nonzero(scan_region_sub_image_pixels[scan_x])

        #Will need changes for multiple scan regions
        sub_image = baseline_image_pixel_values[:scan_x, :scan_y]


    difs = adjust_for_scan_regions(baseline_image_pixel_values, compare_image_pixel_values, ignore_mask_array, sub_image, scan_region_wave_space)
    #print(ignore_mask_array)
    difs = adjust_for_ignore_regions(difs, ignore_mask_array)

    #Probably more useful to return total pixels different instead of total color space different
    squared_difs = numpy.multiply(difs, difs)
    total_difs = numpy.sum(squared_difs)
    mask = squared_difs > DIFFERENCE_THRESHOLD

    arr = get_output_image_pixels(mask, compare_image_pixel_values, ignore_mask_array)#Would like to have mask display optional
    save_output_image_from_array(arr)

    return numpy.sqrt(total_difs)