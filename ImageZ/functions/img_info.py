import cv2


def img_info(img_path):
    img = cv2.imread(img_path, -1)
    print("文件路径:", img_path)
    print("文件名:", img_path.split("/")[-1])
    print("图像尺寸:", img.shape)
    print("像素值类型:", img.dtype)
    print("最小像素值 : " + str(img.min()) + " , 最大像素值 : " + str(img.max()))
