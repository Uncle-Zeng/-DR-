import numpy as np


def label_gray_scale_inversion(img):
    img_h, img_w = img.shape
    img_min = img.min()
    img_max = img.max()
    inversion_img = np.zeros_like(img, dtype=img.dtype)
    for h in range(img_h):
        for w in range(img_w):
            inversion_img[h, w] = img_max + img_min - img[h, w]

    return inversion_img
