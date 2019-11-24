import sys
from PIL import Image
import numpy
from scipy import misc
import os
import datetime
import copy

DIFFERENCE_THRESHOLD = 10

def resize_images(baseline_image, compare_image):

    if compare_image.size != baseline_image.size:
        print("WARNING: Size of images does not match.")
    compare_image = compare_image.resize(baseline_image.size)#Scale to size in case they don't match
    return baseline_image, compare_image

def convert_two_images_to_rgba(images_array):

    baseline_image = images_array[0].convert("RGBA")
    compare_image = images_array[1].convert("RGBA")
    return baseline_image, compare_image


def get_output_image_pixels(mask, compare_image_pixel_values, ignore_mask = None):

    i = 0
    if not ignore_mask.any():
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
                if mask[i][j][0] == True and ignore_mask[i][j][0] == False:
                    compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
                elif ignore_mask[i][j][0] == True:
                    compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [50, -50, 50, 100])
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


#Overwrite pixels to be black where there is an ignore mask. Black matches black :)
def adjust_for_ignore_regions(original_pixels, ignore_mask = None):
    if ignore_mask.any():
        original_pixels[ignore_mask] = 0
    return original_pixels


def count_nonzero(gray_array):
    count = 0
    i = 0
    while i < len(gray_array):
        if(numpy.count_nonzero(gray_array[i]) > 0):
            count = count + 1
        i = i + 1
    return count


def get_difs_array(matrix_one, matrix_two):
    if (matrix_one.size != matrix_two.size):
        return "Subtraction is not defined for matrices of different dimensions."
    return numpy.subtract(matrix_one, matrix_two)

def compare(baseline_image, compare_image, ignore_mask_image = None):

    baseline_image, compare_image = convert_two_images_to_rgba(resize_images(baseline_image, compare_image))
    width, height = baseline_image.size

    baseline_image_pixel_values, compare_image_pixel_values = list(baseline_image.getdata()), list(compare_image.getdata())

    baseline_image_pixel_values = numpy.array(baseline_image_pixel_values).reshape(width, height, 4, order="F")
    compare_image_pixel_values = numpy.array(compare_image_pixel_values).reshape(width, height, 4, order="F")
    output_pixels = copy.copy(baseline_image_pixel_values)

    #Populate ignore_mask_array
    if ignore_mask_image != None:
        pixels = list(ignore_mask_image.getdata())
        pixels = numpy.array(pixels).reshape(width, height, 4, order="F")
        ignore_mask_array = pixels < 68

    #Adjust pixels by overwriting ignore regions
    baseline_image_pixel_values = adjust_for_ignore_regions(baseline_image_pixel_values, ignore_mask_array)
    compare_image_pixel_values = adjust_for_ignore_regions(compare_image_pixel_values, ignore_mask_array)

    #Getting diffs
    difs = get_difs_array(compare_image_pixel_values, baseline_image_pixel_values)
    squared_difs = numpy.multiply(difs, difs)
    total_difs = numpy.sum(squared_difs)
    mask = squared_difs > DIFFERENCE_THRESHOLD

    #Get output image and save
    arr = get_output_image_pixels(mask, output_pixels, ignore_mask_array)
    save_output_image_from_array(arr)

    #Return diffs count
    return numpy.sqrt(total_difs)