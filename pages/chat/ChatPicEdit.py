from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger
import random


class ChatPicEditPage(BasePage):
    """选择照片->预览->编辑 页面"""
    ACTIVITY = 'com.juphoon.imgeditor.PictureEditActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/vs_op': (MobileBy.ID, 'com.chinasofti.rcs:id/vs_op'),
                  '取消': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_cancel'),
                  '保存': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_done'),
                  'com.chinasofti.rcs:id/rg_modes': (MobileBy.ID, 'com.chinasofti.rcs:id/rg_modes'),

                  '文本编辑按钮': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_text'),
                  'com.chinasofti.rcs:id/btn_clip': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_clip'),
                  # 文本编辑页面
                  '文本编辑框': (MobileBy.ID, 'com.chinasofti.rcs:id/et_text'),
                  '涂鸦': (MobileBy.ID, 'com.chinasofti.rcs:id/rb_doodle'),
                  '马赛克': (MobileBy.ID, 'com.chinasofti.rcs:id/rb_mosaic'),
                  '文字': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_text'),
                  '文字输入': (MobileBy.ID, 'com.chinasofti.rcs:id/et_text'),
                  '裁剪': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_clip'),
                  '发送': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send'),
                  '涂鸦控件白色': (MobileBy.ID, 'com.chinasofti.rcs:id/cr_white'),
                  '涂鸦控件红色': (MobileBy.ID, 'com.chinasofti.rcs:id/cr_red'),
                  '马赛克控件': (MobileBy.ID, 'com.chinasofti.rcs:id/cr_30'),
                  '完成': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_done'),
                  '选择': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_select'),
                  'com.chinasofti.rcs:id/image_canvas': (MobileBy.ID, 'com.chinasofti.rcs:id/image_canvas'),
                  }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在群聊天页"""
        el = self.get_elements(self.__locators['涂鸦'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def click_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_cancle(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def click_doodle(self):
        """点击涂鸦"""
        self.click_element(self.__class__.__locators["涂鸦"])

    @TestLogger.log()
    def do_doodle(self):
        """涂鸦操作"""
        a = random.randint(1, 20)
        self.swipe_by_percent_on_screen(20 + a, 60 + a, 40 + a, 30 + a, 700)
        self.swipe_by_percent_on_screen(60 + a, 60 + a, 40 + a, 30 + a, 700)
        self.swipe_by_percent_on_screen(20 + a, 60 + a, 60 + a, 60 + a, 700)

    @TestLogger.log()
    def click_mosaic(self):
        """点击马赛克"""
        self.click_element(self.__class__.__locators["马赛克"])

    @TestLogger.log()
    def do_mosaic(self):
        """马赛克操作"""
        self.swipe_by_percent_on_screen(40, 45, 60, 45, 800)
        self.swipe_by_percent_on_screen(30, 55, 70, 55, 800)

    @TestLogger.log()
    def click_text_edit_btn(self):
        """点击文本编辑按钮"""
        self.click_element(self.__class__.__locators["文本编辑按钮"])

    @TestLogger.log()
    def input_pic_text(self, text="PicTextEdit"):
        """输入编辑文本"""
        self.input_text(self.__class__.__locators["文本编辑框"], text)

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        time.sleep(times)

    @TestLogger.log()
    def click_picture_select(self):
        """点击选择"""
        self.click_element(self.__class__.__locators["选择"])

    @TestLogger.log()
    def click_picture_cancel(self):
        """点击取消"""
        self.click_element(self.__class__.__locators["取消"])

    @TestLogger.log()
    def click_picture_send(self):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])

    @TestLogger.log()
    def click_picture_save(self):
        """点击保存"""
        self.click_element(self.__class__.__locators["保存"])

    @TestLogger.log()
    def click_picture_edit_switch(self):
        """屏幕内滑动	[0,85][1080,2116]"""
        self.swipe_by_percent_on_screen(50,15,60,40,duration=200)
        self.swipe_by_percent_on_screen(40,17,50,50,duration=200)
        self.swipe_by_percent_on_screen(50,17,50,30, duration=200)

    @TestLogger.log()
    def click_picture_edit_crred(self):
        """点击涂鸦红色"""
        self.click_element(self.__class__.__locators["涂鸦控件红色"])

    @TestLogger.log()
    def click_picture_edit(self):
        """点击涂鸦编辑"""
        self.click_element(self.__class__.__locators["涂鸦"])

    @TestLogger.log()
    def click_picture_complete(self):
        """点击涂鸦编辑"""
        self.click_element(self.__class__.__locators["完成"])
        time.sleep(1)

    @TestLogger.log()
    def click_picture_mosaic(self):
        """点击马赛克编辑"""
        self.click_element(self.__class__.__locators["马赛克"])
        self.click_element(self.__class__.__locators["马赛克控件"])

    @TestLogger.log()
    def click_picture_text(self):
        """点击文字"""
        self.click_element(self.__class__.__locators["文字"])

    @TestLogger.log()
    def input_picture_text(self,text):
        """输入文本编辑说"""
        self.input_text(self.__class__.__locators["文字输入"],text)

    @TestLogger.log()
    def click_picture_clip(self):
        """点击裁剪"""
        self.click_element(self.__class__.__locators["裁剪"])

