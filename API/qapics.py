import sys
from PIL import Image
import sys
sys.path.append('../Analysis/')
import analyze

baseline_image_path = "../Baselines/" + sys.argv[1] + ".png"
compare_image_path = "../" + sys.argv[1] + ".png"
mask_image =  "../Masks/" + sys.argv[1] + ".png" 
#Could store screenshot in output and adjust it with filters later.

baseline_image = Image.open(baseline_image_path, 'r')
compare_image = Image.open(compare_image_path, 'r')
mask_image = Image.open(mask_image, 'r')

if len(sys.argv) > 2:
	mask_image = Image.open(sys.argv[2], 'r')

def get_differences(baseline_image, compare_image, mask_image):
	print(analyze.diffs(baseline_image, compare_image, mask_image))

get_differences(baseline_image, compare_image, mask_image)
