# -*- coding:utf-8 -*-
import copy

import wx

from functions.default_wl import default_wl
from functions.img_enhancement import unsharpMaskingMeanFilter
from functions.img_flipping import img_flipping
from functions.img_info import img_info
from functions.img_scaling import img_scaling
from functions.label_gray_scale_inversion import label_gray_scale_inversion
from functions.read_img import read_img
from functions.save_img import save_img
from functions.show_img import show_img
from functions.show_img_getvalue import show_img_getvalue
from functions.win_wl_adjust import win_wl_adjust
from functions.show_img_zoom import show_img_zoom


class Frame(wx.Frame):
    def __init__(self):
        # 面板设置
        wx.Frame.__init__(self, None, title='DR简易浏览器（220224790曾诚）', size=(830, 550), name='frame',
                          style=541072448)
        icon = wx.Icon(r'logo.png')
        self.SetIcon(icon)
        self.windows = wx.Panel(self)
        self.windows.SetOwnBackgroundColour((240, 240, 240, 255))
        self.Centre()

        # 大标题设置
        self.app_name = wx.StaticText(self.windows, size=(150, 30), pos=(20, 29), label='DR简易浏览器',
                                      name='staticText', style=2313)
        app_name_font = wx.Font(16, 75, 90, 700, False, '楷体', 28)
        self.app_name.SetFont(app_name_font)

        # 读取图像文件
        self.read_img = wx.Button(self.windows, size=(100, 40), pos=(200, 20), label='读入图像文件', name='button')
        self.read_img.Bind(wx.EVT_BUTTON, self.read_img_clicked)

        # 保存当前图像
        self.save_img = wx.Button(self.windows, size=(100, 40), pos=(340, 20), label='保存当前图像', name='button')
        self.save_img.Bind(wx.EVT_BUTTON, self.save_img_clicked)

        # 当前图像信息
        self.img_info = wx.Button(self.windows, size=(100, 40), pos=(480, 20), label='当前图像信息', name='button')
        self.img_info.Bind(wx.EVT_BUTTON, self.img_info_clicked)

        # 重置图像
        self.reset = wx.Button(self.windows, size=(100, 40), pos=(620, 20), label='重置图像', name='button')
        self.reset.Bind(wx.EVT_BUTTON, self.reset_clicked)

        # 窗宽窗位调整
        self.label_wl_adjust = wx.StaticText(self.windows, size=(80, 24), pos=(110, 100), label='窗宽窗位调整',
                                             name='staticText', style=2321)
        self.label_window_level = wx.StaticText(self.windows, size=(80, 24), pos=(2, 165), label='窗位',
                                                name='staticText', style=2321)
        self.label_window_wide = wx.StaticText(self.windows, size=(80, 24), pos=(2, 255), label='窗宽',
                                               name='staticText', style=2321)
        self.slider_1 = wx.Slider(self.windows, size=(150, 22), pos=(84, 148), name='slider', minValue=0, maxValue=4095,
                                  value=2047, style=25108)
        self.slider_1.SetTickFreq(1)
        self.slider_1.SetPageSize(5)
        self.slider_1.Bind(wx.EVT_SCROLL_THUMBTRACK, self.slider_1_sliding)
        self.slider_2 = wx.Slider(self.windows, size=(150, 22), pos=(85, 241), name='slider', minValue=1, maxValue=4096,
                                  value=2048, style=25108)
        self.slider_2.SetTickFreq(1)
        self.slider_2.SetPageSize(5)
        self.slider_2.Bind(wx.EVT_SCROLL_THUMBTRACK, self.slider_2_sliding)

        # 窗宽窗位重置为该图像的默认值
        self.reset_wl = wx.Button(self.windows, size=(120, 32), pos=(90, 300), label='重置为默认窗位窗宽',
                                  name='button')
        self.reset_wl.Bind(wx.EVT_BUTTON, self.reset_1_clicked)

        # 图像缩放
        self.label_image_zoom = wx.StaticText(self.windows, size=(80, 24), pos=(326, 100), label='图像缩放',
                                              name='staticText', style=2321)
        self.label_zoom_multiple = wx.StaticText(self.windows, size=(80, 24), pos=(277, 143), label='缩放倍数',
                                                 name='staticText', style=2321)
        self.x_label = wx.StaticText(self.windows, size=(80, 24), pos=(275, 187), label='x坐标调整', name='staticText',
                                     style=2321)
        self.y_label = wx.StaticText(self.windows, size=(80, 24), pos=(275, 234), label='y坐标调整', name='staticText',
                                     style=2321)
        self.edit_box1 = wx.TextCtrl(self.windows, size=(80, 22), pos=(365, 140), value='', name='text', style=0)
        self.slider_3 = wx.Slider(self.windows, size=(100, 22), pos=(355, 187), name='slider', minValue=1, maxValue=100,
                                  value=1, style=4)
        self.slider_3.SetTickFreq(10)
        self.slider_3.SetPageSize(5)
        self.slider_3.Bind(wx.EVT_SCROLL_THUMBTRACK, self.slider_3_sliding)
        self.slider_4 = wx.Slider(self.windows, size=(100, 22), pos=(355, 234), name='slider', minValue=1, maxValue=100,
                                  value=1, style=4)
        self.slider_4.SetTickFreq(10)
        self.slider_4.SetPageSize(5)
        self.slider_4.Bind(wx.EVT_SCROLL_THUMBTRACK, self.slider_4_sliding)

        # 图像缩放确认与重置当前图像按钮
        self.confirm_1 = wx.Button(self.windows, size=(80, 32), pos=(365, 280), label='确认', name='button')
        self.confirm_1.Bind(wx.EVT_BUTTON, self.confirm_1_clicked)
        self.reset_2 = wx.Button(self.windows, size=(80, 32), pos=(365, 330), label='重置当前图像', name='button')
        self.reset_2.Bind(wx.EVT_BUTTON, self.reset_2_clicked)

        # 灰度反转与图像翻转
        self.label_gray_scale_inversion = wx.StaticText(self.windows, size=(120, 24), pos=(480, 100),
                                                        label='灰度反转与图像翻转',
                                                        name='staticText', style=2321)

        # 灰度反转与图像翻转按钮
        self.label_gray_scale_inversion = wx.Button(self.windows, size=(80, 32), pos=(500, 140), label='灰度反转',
                                                    name='button')
        self.label_gray_scale_inversion.Bind(wx.EVT_BUTTON, self.label_gray_scale_inversion_clicked)
        self.image_flipping = wx.Button(self.windows, size=(80, 32), pos=(500, 200), label='图像翻转',
                                        name='button')
        self.image_flipping.Bind(wx.EVT_BUTTON, self.img_flipping_clicked)

        # 细节增强
        self.label_detail_enhancement = wx.StaticText(self.windows, size=(80, 24), pos=(656, 100), label='细节增强',
                                                      name='staticText', style=2321)
        self.label_unsharp_masking = wx.StaticText(self.windows, size=(147, 24), pos=(629, 126),
                                                   label='（Unsharp Masking）', name='staticText', style=2321)
        self.label_ksize = wx.StaticText(self.windows, size=(80, 24), pos=(599, 181), label='均值核尺寸',
                                         name='staticText', style=2321)
        self.label_residual_weight = wx.StaticText(self.windows, size=(80, 24), pos=(598, 238), label='残差权重',
                                                   name='staticText', style=2321)
        self.comboBox1 = wx.ComboBox(self.windows, value='', pos=(680, 180), name='comboBox', choices=['3', '5', '7'],
                                     style=16)
        self.comboBox1.SetSize((100, 22))
        self.comboBox2 = wx.ComboBox(self.windows, value='', pos=(680, 235), name='comboBox',
                                     choices=['1.0', '2.0', '3.0', '4.0', '5.0'], style=16)
        self.comboBox2.SetSize((100, 22))

        # 细节增强确认和重置当前图像按钮
        self.confirm_2 = wx.Button(self.windows, size=(80, 32), pos=(680, 280), label='确认', name='button')
        self.confirm_2.Bind(wx.EVT_BUTTON, self.confirm_2_clicked)
        self.reset_3 = wx.Button(self.windows, size=(80, 32), pos=(680, 330), label='重置当前图像', name='button')
        self.reset_3.Bind(wx.EVT_BUTTON, self.reset_3_clicked)

        # 使用说明
        self.label_explaination = wx.StaticText(self.windows, size=(732, 57), pos=(30, 400),
                                                label='使用说明：显示图像信息等输出信息需要配合python终端输出进行使用；'
                                                      '文件目录中出现中文可能会报错；\n\n进行图像缩放等待时间较长，请图像缩放完成后再进行x,y坐标调整;',
                                                name='staticText', style=17)

    # 读取图像按钮函数
    def read_img_clicked(self, event):
        print('\n----------读入图像文件----------')
        self.img, self.img_path = read_img()
        self.h, self.w = self.img.shape
        # 默认窗宽设置
        window_level, window_wide = default_wl(self.img)
        self.slider_1.SetValue(window_level)
        self.slider_2.SetValue(window_wide)
        # 将原始数据进行深拷贝，只对temp临时变量进行操作，后面部分操作类似
        # img则进行存档，便于重置时使用
        self.temp = copy.deepcopy(self.img)
        show_img(self.temp)

    # 保存当前图像按钮函数
    def save_img_clicked(self, event):
        print('\n----------保存当前图像----------')
        save_img(self.temp)

    # 获取图像信息按钮函数
    def img_info_clicked(self, event):
        print('\n----------当前图像信息----------')
        img_info(self.img_path)

    # 将操作后的图像直接重置为原始读取的图像
    def reset_clicked(self, event):
        print('\n----------重置图像----------')
        # 直接将存档的img深拷贝给temp实现重置
        self.temp = copy.deepcopy(self.img)
        show_img(self.temp)

    # 窗位拖动滑块
    def slider_1_sliding(self, event):
        self.temp = win_wl_adjust(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())

    # 窗宽拖动滑块
    def slider_2_sliding(self, event):
        self.temp = win_wl_adjust(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())

    # 重置为默认窗宽窗位按钮
    def reset_1_clicked(self, event):
        print('\n----------重置为默认窗宽窗位值----------')
        # 默认窗宽设置
        window_level, window_wide = default_wl(self.img)
        self.slider_1.SetValue(window_level)
        self.slider_2.SetValue(window_wide)
        self.temp = copy.deepcopy(self.img)
        show_img(self.temp)

    # 图像缩放确认按钮
    def confirm_1_clicked(self, event):
        print('\n----------确认缩放倍数----------')
        self.temp_backup01 = copy.deepcopy(self.temp)
        self.temp = img_scaling(self.temp, self.edit_box1.GetValue())
        # 显示图像的左上角区域
        show_img_zoom(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue(), self.h, self.w, 0, 0)

    # 图像缩放重置按钮,将缩放后的图像重置为缩放前的图像
    def reset_2_clicked(self, event):
        print('\n----------重置为缩放前的图像----------')
        self.temp = copy.deepcopy(self.temp_backup01)
        show_img_getvalue(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())

    # 调整缩放后查看位置的滑块
    def slider_3_sliding(self, event):
        show_img_zoom(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue(), self.h, self.w,
                      self.slider_3.GetValue(), self.slider_4.GetValue())

    def slider_4_sliding(self, event):
        show_img_zoom(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue(), self.h, self.w,
                      self.slider_3.GetValue(), self.slider_4.GetValue())

    # 灰度反转按钮
    def label_gray_scale_inversion_clicked(self, event):
        print('\n----------图像灰度反转----------')
        # 如果只进行反相操作，反相两次也可以实现重置效果
        self.temp = label_gray_scale_inversion(self.temp)
        show_img_getvalue(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())

    # 图像翻转按钮
    def img_flipping_clicked(self, event):
        print("\n----------图像翻转----------")
        self.temp = img_flipping(self.temp)
        show_img_getvalue(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())

    # 细节增强的确认按钮
    def confirm_2_clicked(self, event):
        print('\n----------确认细节增强----------')
        self.temp_backup02 = copy.deepcopy(self.temp)
        self.temp = unsharpMaskingMeanFilter(self.temp, int(self.comboBox1.GetValue()),
                                             float(self.comboBox2.GetValue()))
        show_img_getvalue(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())

    # 细节增强的重置按钮,将细节增强后的图像重置为细节增强前的图像
    def reset_3_clicked(self, event):
        print('\n----------重置为细节增强前的图像----------')
        self.temp = copy.deepcopy(self.temp_backup02)
        show_img_getvalue(self.temp, self.slider_1.GetValue(), self.slider_2.GetValue())
