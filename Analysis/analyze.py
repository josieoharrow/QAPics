import sys
from PIL import Image
import numpy
from scipy import misc

baseline_image = Image.open(sys.argv[1], 'r')
compare_image = Image.open(sys.argv[2], 'r')

if compare_image.size != baseline_image.size:
    print "WARNING: Size of images does not match."

baseline_image_width, baseline_image_height = baseline_image.size
compare_image = compare_image.resize(baseline_image.size)#Scale to size in case they don't
#Match automatically

baseline_image = baseline_image.convert("RGBA")
baseline_image_pixel_values = list(baseline_image.getdata())
baseline_image_pixel_values = numpy.array(baseline_image_pixel_values).reshape(baseline_image_width, baseline_image_height, 4, order="F")

compare_image_width, compare_image_height = compare_image.size
compare_image = compare_image.convert("RGBA")
compare_image_pixel_values = list(compare_image.getdata())
compare_image_pixel_values = numpy.array(compare_image_pixel_values).reshape(compare_image_width, compare_image_height, 4, order="F")

difs = numpy.subtract(compare_image_pixel_values, baseline_image_pixel_values)

squared_difs = numpy.multiply(difs, difs)
total_difs = numpy.sum(squared_difs)
mask = squared_difs > 10

output_image = compare_image
output_image.convert("RGBA")

i = 0
while i < len(compare_image_pixel_values):
    j = 0
    while j < len(compare_image_pixel_values[i]):
        if mask[i][j][0] == True:
           compare_image_pixel_values[i][j] = numpy.subtract(compare_image_pixel_values[i][j], [-50, 50, 50, 100])
        j = j + 1
    i = i + 1

misc.imsave('test.png', compare_image_pixel_values)
output_image.save("mask.png")
print numpy.sqrt(total_difs)
