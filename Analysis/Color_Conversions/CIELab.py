import numpy
ref_Whites = [95.047, 100.0, 108.883]
e = 0.008856
k = 903.3
rgb2XYZ_Map = [[0.4124,0.3576,0.1805],[0.2126,0.715, 0.0722],[0.0193,0.1192,0.9505]]

#Convert entire image to CIELab
def rgb2XYZ(image): #image will be AxBx4 numpy array in RGBA color space

    #Convert to XYZ: http://brucelindbloom.com/index.html?Eqn_ChromAdapt.html
    #Gamma correct for XYZ conversion
    dims = image.shape
    upper_Vals_Gamma_Correct = numpy.multiply( ( ( (image/255) + 0.055 ) / 1.055) **2.4, numpy.greater(image, 0.0405))
    lower_Vals_Gamma_Correct = numpy.multiply( ( (image/255) / 12.92), numpy.less_equal(image, 0.0405))
    gamma_Correct_Image = 100 * (upper_Vals_Gamma_Correct + lower_Vals_Gamma_Correct)
    #Transform to XYZ
    XYZ_array = numpy.zeros(dims)
    #Loop over transformation matrix (just a matrix transformation on the color vector)
    for row in [0,1,2]:
        for col in [0,1,2]:
            XYZ_array[:,:,row] += gamma_Correct_Image[:,:,col] * rgb2XYZ_Map[row][col]
    XYZ_array[:,:,3] = image[:,:,3] #Oppacity remains untouched
    return numpy.round(XYZ_array,4) #array in XYZ color space


def XYZ2lab(image): #image is AxBx4 in XYZ color space
    #Convert from XYZ to CIElab: http://brucelindbloom.com/index.html?Eqn_ChromAdapt.html
    #Divide each color channel by its reference white
    dims = image.shape
    for i in [0,1,2]:
        image[:,:,i] = image[:,:,i] / ref_Whites[i]
    #Calculate values of the f function
    upper_Vals_f = numpy.multiply( image ** (1/3), numpy.greater(image, e))
    lower_Vals_f = numpy.multiply( (k * image +16) / 116 , numpy.less_equal(image, 0.008856))
    XYZ_array_f_Conv = upper_Vals_f + lower_Vals_f
    #Finally, transform to Lab
    lab_array = numpy.zeros(dims)
    lab_array[:,:,0] = 116 * XYZ_array_f_Conv[:,:,1] - 16
    lab_array[:,:,1] = 500 * ( XYZ_array_f_Conv[:,:,0] - XYZ_array_f_Conv[:,:,1])
    lab_array[:,:,2] = 200 * ( XYZ_array_f_Conv[:,:,1] - XYZ_array_f_Conv[:,:,2])
    #Oppacity remains untouched
    lab_array[:,:,3] = image[:,:,3]

    return numpy.round(lab_array,4)


def rgb2lab(image): #Input is AxBx4 numpy array in RGBA color space
    return XYZ2lab(rgb2XYZ(image))