import cv2
from numpy import uint8


# 使用UI界面获得的窗位窗宽进行显示
def show_img_getvalue(img, level, wide):
    img_temp = img.copy()
    w, h = img_temp.shape
    # UI界面获得的窗位窗宽值
    window_level = level
    window_wide = wide
    # 计算窗宽所在区间
    left = (window_level * 2 - window_wide) / 2
    right = (window_level * 2 + window_wide) / 2
    # 根据窗宽窗位进行像素值映射
    img_temp[img_temp > right] = right
    img_temp[img_temp < left] = left
    img_temp = uint8((img_temp - left) / (right - left) * 255)
    # 创建窗口并显示图像
    cv2.namedWindow("Image", 0)
    # 由于原图像较大，因此显示为原图像的1/2窗口大小
    cv2.resizeWindow("Image", h // 2, w // 2)
    cv2.imshow("Image", img_temp)
    cv2.waitKey(0)
    # 释放窗口
    cv2.destroyAllWindows()

