from skimage.filters import threshold_otsu
from skimage import io
import numpy as np
import math
from skimage.transform import rotate, rescale


def get_binary_image(x, y, image_location):
    image = io.imread(image_location, as_gray=True)
    ratio = get_rescale_ratio((x, y), image)
    image = rotate(rescale(image, ratio), -90)

    ## pad the image to reach x y
    x_pad_1 = (x - image.shape[0]) // 2
    x_pad_2 = x_pad_1
    if (x - image.shape[0]) % 2:
        x_pad_2 += 1

    y_pad_1 = (y - image.shape[1]) // 2
    y_pad_2 = y_pad_1
    if (y - image.shape[1]) % 2:
        y_pad_2 += 1

    image = np.pad(image, ((x_pad_1, x_pad_2), (y_pad_1, y_pad_2)), 'constant', constant_values=(0, 0))
    thresh = threshold_otsu(image)

    return 1*(image >= thresh)


def get_rescale_ratio(xy, image):
    x, y = xy
    ratio = 1

    if image.shape[0] > x:
        ratio = math.floor(x/image.shape[0] * 10**2) / 10**2

    if image.shape[1]*ratio > y:
        ratio = math.floor(y/image.shape[1] * 10**2) / 10**2

    return ratio

