import numpy as np


# 双线性插值实现图像缩放
def img_scaling(img, zoom_multi):
    zoom_multi = float(zoom_multi)
    # 获取原始图像的宽高
    img_h, img_w = img.shape
    # 计算缩放后新图像的宽高
    zoom_img_w = int(img_w * zoom_multi)
    zoom_img_h = int(img_h * zoom_multi)
    zoom_img = np.zeros((zoom_img_h, zoom_img_w))
    for h in range(zoom_img_h):
        for w in range(zoom_img_w):
            # 源图像和目标图像几何中心对齐
            img_point_y = (h + 0.5) * (img_h / zoom_img_h) - 0.5
            img_point_x = (w + 0.5) * (img_w / zoom_img_w) - 0.5

            # 取整，用于作差
            img_left_point_y = int(img_point_y)
            img_left_point_x = int(img_point_x)

            # 获取与周边像素的小数作为插值参数，绝对值符号不能少
            distance_y = abs(img_point_y - img_left_point_y)
            distance_x = abs(img_point_x - img_left_point_x)

            # 如果像素处于右下角、最后一行、最后一列时则进行特殊处理
            if img_left_point_y == img_h - 1 and img_left_point_x == img_w - 1:
                point_a = img[img_h - 1, img_w - 1]
                point_b = point_a
                point_c = point_a
                point_d = point_a
            elif img_left_point_y == img_h - 1 and img_left_point_x < img_w - 1:
                point_a = img[img_h - 1, img_left_point_x]
                point_b = img[img_h - 1, img_left_point_x + 1]
                point_c = point_a
                point_d = point_b
            elif img_left_point_x == img_w - 1 and img_left_point_y < img_h - 1:
                point_a = img[img_left_point_y, img_w - 1]
                point_c = img[img_left_point_y + 1, img_w - 1]
                point_b = point_a
                point_d = point_c
            else:
                point_a = img[img_left_point_y, img_left_point_x]
                point_b = img[img_left_point_y + 1, img_left_point_x]
                point_c = img[img_left_point_y, img_left_point_x + 1]
                point_d = img[img_left_point_y + 1, img_left_point_x + 1]

            zoom_img[h, w] = point_a * distance_x * distance_y + point_b * (1 - distance_x) * distance_y + \
                             point_c * distance_x * (1 - distance_y) + point_d * (1 - distance_x) * (1 - distance_y)

    return zoom_img
