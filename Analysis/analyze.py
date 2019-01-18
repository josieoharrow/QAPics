import sys
from PIL import Image
import numpy
from scipy import misc

DIFFERENCE_THRESHOLD = 10

def resize_images(baseline_image, compare_image):

    if compare_image.size != baseline_image.size:
        print "WARNING: Size of images does not match."
    baseline_image_width, baseline_image_height = baseline_image.size
    compare_image = compare_image.resize(baseline_image.size)#Scale to size in case they don't match
    return baseline_image, compare_image


def convert_two_images_to_rgba(images_array):

    baseline_image = images_array[0].convert("RGBA")
    compare_image = images_array[1].convert("RGBA")
    return baseline_image, compare_image


def get_output_image_pixels(mask, compare_image_pixel_values):

    i = 0
    while i < len(compare_image_pixel_values):
        j = 0
        while j < len(compare_image_pixel_values[i]):
            if mask[i][j][0] == True:
                compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
            j = j + 1
        i = i + 1
    return compare_image_pixel_values


def save_output_image_from_array(pixel_array):

    misc.imsave('../Output/Output.png', pixel_array)
    output_image = Image.open("../Output/Output.png")
    output_image = output_image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    output_image.save("../Output/Output.png")


def adjust_for_ignore_regions(difs, ignoreMask):

    if ignoreMask:
        difs[mask] = 0
    return difs


def diffs(baseline_image, compare_image, ignoreMask = None):

    baseline_image, compare_image = convert_two_images_to_rgba(resize_images(baseline_image, compare_image))
    width, height = baseline_image.size

    baseline_image_pixel_values, compare_image_pixel_values = list(baseline_image.getdata()), list(compare_image.getdata())

    baseline_image_pixel_values = numpy.array(baseline_image_pixel_values).reshape(width, height, 4, order="F")
    compare_image_pixel_values = numpy.array(compare_image_pixel_values).reshape(width, height, 4, order="F")

    difs = numpy.subtract(compare_image_pixel_values, baseline_image_pixel_values)

    difs = adjust_for_ignore_regions(difs, ignoreMask)

    squared_difs = numpy.multiply(difs, difs)
    total_difs = numpy.sum(squared_difs)
    mask = squared_difs > DIFFERENCE_THRESHOLD

    arr = get_output_image_pixels(mask, compare_image_pixel_values)
    save_output_image_from_array(arr)

    return numpy.sqrt(total_difs)


