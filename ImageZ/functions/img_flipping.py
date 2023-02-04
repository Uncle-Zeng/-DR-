import numpy as np


# 图像左右翻转
def img_flipping(img):
    flipping_img = np.zeros_like(img)
    img_h, img_w = img.shape
    for h in range(img_h):
        for w in range(img_w):
            flipping_img[h, w] = img[h, img_w - w - 1]

    return flipping_img
