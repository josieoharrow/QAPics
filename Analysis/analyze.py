import sys
from PIL import Image
import numpy
import os
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
    while i < len(compare_image_pixel_values):
        j = 0
        while j < len(compare_image_pixel_values[i]):
            if mask[i][j][0] == True:# and ignore_mask[i][j][0] == False:
                compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
            else:#if ignore_mask[i][j][0] == True:
                compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [50, -50, 50, 100])
            j = j + 1
        i = i + 1
    return compare_image_pixel_values




#Overwrite pixels to be black where there is an ignore mask. Black matches black :)
def adjust_for_ignore_regions(original_pixels, ignore_blocks):
    i = 0
    while i < len(ignore_blocks):
        x = int(ignore_blocks[i]["startX"])
        y = int(ignore_blocks[i]["startY"])
        width = int(ignore_blocks[i]["width"])
        height = int(ignore_blocks[i]["height"])
        original_pixels[y - 1: height, x - 1: width] = 0
        i = i + 1
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

def compare(baseline_image, compare_image, ignore_mask):

    baseline_image, compare_image = convert_two_images_to_rgba(resize_images(baseline_image, compare_image))
    width, height = baseline_image.size

    baseline_image_pixel_values, compare_image_pixel_values = list(baseline_image.getdata()), list(compare_image.getdata())

    baseline_image_pixel_values = numpy.array(baseline_image_pixel_values).reshape(width, height, 4, order="F")
    compare_image_pixel_values = numpy.array(compare_image_pixel_values).reshape(width, height, 4, order="F")
    output_pixels = copy.copy(baseline_image_pixel_values)

    ignore_blocks = ignore_mask["ignore"]

    #Adjust pixels by overwriting ignore regions
    baseline_image_pixel_values = adjust_for_ignore_regions(baseline_image_pixel_values, ignore_blocks)
    compare_image_pixel_values = adjust_for_ignore_regions(compare_image_pixel_values, ignore_blocks)

    #Getting diffs
    difs = get_difs_array(compare_image_pixel_values, baseline_image_pixel_values)
    squared_difs = numpy.multiply(difs, difs)
    total_difs = numpy.sum(squared_difs)
    mask = squared_difs > DIFFERENCE_THRESHOLD

    #Get output image and save
    arr = get_output_image_pixels(mask, output_pixels, ignore_blocks)

    #Return diffs count
    return ([numpy.sqrt(total_difs), arr])