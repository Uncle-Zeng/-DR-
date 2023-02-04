import numpy as np


# 使用均值滤波实现的Unsharp Masking
def unsharpMaskingMeanFilter(img_: np.ndarray, ksize: int, k: float):
    assert k >= 1
    img = np.array(img_, dtype=float)
    smooth_img = smoothFilter(img, ksize, lambda x: sum(x) / len(x))
    # 获取mask
    mask = img - smooth_img
    # 得到叠加后的
    sharpen_img = img + k * mask
    # 标准化
    sharpen_img = reshape_img(sharpen_img, img)
    return np.array(sharpen_img, dtype=img_.dtype)


# 依照原来的图像进行标准化
def reshape_img(sharpen_img, original_img):
    min_1, max_1 = sharpen_img.min(), sharpen_img.max()
    min_2, max_2 = original_img.min(), original_img.max()
    norm = (sharpen_img - min_1) / (max_1 - min_1) * (max_2 - min_2)
    return norm


# 实现均值滤波
def smoothFilter(data: np.ndarray, filterSize: int, replacer) -> np.ndarray:
    h, w = data.shape
    # 周围一圈保留处理
    padding = (filterSize - 1) // 2

    # 获取某像素的邻域及其自身
    def getNeighborAndMe(x, y, padding):
        res = []
        for i in range(-padding, padding + 1):
            for j in range(-padding, padding + 1):
                res.append(data[x + i, y + j])
        return res

    result = np.array(data)
    for i in range(h):
        for j in range(w):
            # 边界保留
            if i < padding or j < padding or i > h - padding - 1 or j > w - padding - 1:
                continue
            result[i, j] = replacer(getNeighborAndMe(i, j, padding))
    return np.array(result, dtype=data.dtype)
