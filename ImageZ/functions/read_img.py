from tkinter import filedialog

import cv2
import tkinter as tk


def read_img():
    # 实例化
    root = tk.Tk()
    root.withdraw()
    # 获取文件路径
    # 请尽量不要出现中文路径,否则容易报错!!
    img_path = filedialog.askopenfilename(title='Open file')
    # 读取图片
    img = cv2.imread(img_path, -1)
    return img, img_path
