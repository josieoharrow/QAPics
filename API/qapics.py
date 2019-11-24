import sys
from PIL import Image
import sys
import os
import json
import datetime
from scipy import misc

QAPicsDir = os.path.dirname(os.path.abspath(__file__)) + "/.."

sys.path.append(QAPicsDir + "/Analysis")
import analyze

baseline_image_path = QAPicsDir + "/Baselines/" + sys.argv[1] + ".png"
compare_image_path = QAPicsDir + "/" + sys.argv[1] + ".png"
mask_json =  QAPicsDir + "/Masks/" + sys.argv[1] + ".json" 

#Could store screenshot in output and adjust it with filters later.
print(mask_json)
baseline_image = Image.open(baseline_image_path, 'r')
compare_image = Image.open(compare_image_path, 'r')

mask_data = None
with open(mask_json) as f:
    mask_data = json.load(f)

if len(sys.argv) > 2:
	mask_data = Image.open(sys.argv[2], 'r')

def get_differences(baseline_image, compare_image, mask_data):
	return analyze.compare(baseline_image, compare_image, mask_data)

def save_output_image_from_array(pixel_array):

    if not os.path.isdir(QAPicsDir + "/Output"):
        os.mkdir(QAPicsDir + "/Output")
    currentDT = datetime.datetime.now()
    image_name = QAPicsDir + '/Output/Output_' + str(currentDT) + '.png'
    misc.imsave(image_name, pixel_array)
    output_image = Image.open(image_name)
    output_image = output_image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    output_image.save(image_name)

val = get_differences(baseline_image, compare_image, mask_data)
save_output_image_from_array(val[1])
print(val[0])
