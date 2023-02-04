# 返回图像默认的窗位窗宽
def default_wl(img):
    img_min, img_max = img.min(), img.max()
    # 默认窗宽设置
    window_level = (img_max - img_min) // 2
    window_wide = img_max - img_min

    return window_level, window_wide
