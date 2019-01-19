import sys
from PIL import Image
import sys
sys.path.append('../Analysis/')
import analyze

baseline_image = Image.open(sys.argv[1], 'r')
compare_image = Image.open(sys.argv[2], 'r')

if sys.argv[3] != None:
	mask_image = Image.open(sys.argv[3], 'r')

def get_differences(baseline_image, compare_image, mask_image):
	print(analyze.diffs(baseline_image, compare_image, mask_image))

get_differences(baseline_image, compare_image, mask_image)
