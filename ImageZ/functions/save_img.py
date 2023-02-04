import cv2
import tkinter
import tkinter.filedialog


def save_img(img):
    # imwrite 不支持中文路径和文件名，读取失败，但不会报错
    file_path = tkinter.filedialog.asksaveasfilename(title='Save file')
    cv2.imwrite(file_path + '.tif', img)
