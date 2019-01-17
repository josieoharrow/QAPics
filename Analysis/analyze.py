import sys
from PIL import Image
import numpy
from scipy import misc

def resize_images(baseline_image, compare_image):

    if compare_image.size != baseline_image.size:
        print "WARNING: Size of images does not match."

    baseline_image_width, baseline_image_height = baseline_image.size
    compare_image = compare_image.resize(baseline_image.size)#Scale to size in case they don't match

    return baseline_image, compare_image


def convert_to_rgba(images_array):

    baseline_image = images_array[0].convert("RGBA")
    compare_image = images_array[1].convert("RGBA")
    return baseline_image, compare_image


def diffs(baseline_image, compare_image):

    baseline_image, compare_image = convert_to_rgba(resize_images(baseline_image, compare_image))

    width, height = baseline_image.size

    baseline_image_pixel_values = list(baseline_image.getdata())
    baseline_image_pixel_values = numpy.array(baseline_image_pixel_values).reshape(width, height, 4, order="F")

    compare_image_pixel_values = list(compare_image.getdata())
    compare_image_pixel_values = numpy.array(compare_image_pixel_values).reshape(width, height, 4, order="F")

    difs = numpy.subtract(compare_image_pixel_values, baseline_image_pixel_values)

    squared_difs = numpy.multiply(difs, difs)
    total_difs = numpy.sum(squared_difs)
    mask = squared_difs > 10

    i = 0
    while i < len(compare_image_pixel_values):
        j = 0
        while j < len(compare_image_pixel_values[i]):
            if mask[i][j][0] == True:
               compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
            j = j + 1
        i = i + 1

    misc.imsave('../Output/Output.png', compare_image_pixel_values)
    output_image = Image.open("../Output/Output.png")
    output_image = output_image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    output_image.save("../Output/Output.png")
    print "Total differences: " + str(numpy.sqrt(total_difs))
    return numpy.sqrt(total_difs)
