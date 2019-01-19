import sys
from PIL import Image
import sys
sys.path.append('../Analysis/')
import analyze

baseline_image = Image.open(sys.argv[1], 'r')
compare_image = Image.open(sys.argv[2], 'r')

def get_differences(baseline_image, compare_image):
	print(analyze.diffs(baseline_image, compare_image, [33, 20, 10, 10]))

get_differences(baseline_image, compare_image)
