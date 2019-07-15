from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatPicPreviewPage(BasePage):
    """群聊选择照片->预览 页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.GalleryChangedActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/quit'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '预览(1/2)': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  '编辑': (MobileBy.ID, 'com.chinasofti.rcs:id/edit'),
                  'com.chinasofti.rcs:id/contentFrame': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),
                  'com.chinasofti.rcs:id/vp_preview': (MobileBy.ID, 'com.chinasofti.rcs:id/vp_preview'),
                  'com.chinasofti.rcs:id/pv_item': (MobileBy.ID, 'com.chinasofti.rcs:id/pv_item'),
                  'com.chinasofti.rcs:id/iv_smooth': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_smooth'),
                  'com.chinasofti.rcs:id/rl_select_panel': (MobileBy.ID, 'com.chinasofti.rcs:id/rl_select_panel'),
                  'com.chinasofti.rcs:id/ll_select': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_select'),
                  'com.chinasofti.rcs:id/iv_select': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_select'),
                  '选择': (MobileBy.ID, ''),
                  '原图': (MobileBy.ID, 'com.chinasofti.rcs:id/cb_original_photo'),
                  '发送(2)': (MobileBy.ID, 'com.chinasofti.rcs:id/btn_send'),
                  '发送': (MobileBy.XPATH, "//*[contains(@text, '发送')]"),
                  # 视频预览页面
                  '视频播放三角形': (MobileBy.ID, 'com.chinasofti.rcs:id/pv_item'),
                  '视频页面': (MobileBy.ID, 'com.chinasofti.rcs:id/vp_preview'),
                  '视频关闭': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_close'),
                  }

    @TestLogger.log()
    def is_exist_edit(self):
        """当前页面是否在编辑按钮"""
        return self._is_element_present(self.__class__.__locators["编辑"])

    @TestLogger.log()
    def check_send_number(self, number):
        """当前页面是否在工作台管理页"""
        text = self.get_text(self.__class__.__locators['发送(2)'])
        excepted_text = "发送({})".format(str(number))
        return text == excepted_text

    @TestLogger.log()
    def is_on_gallery_page(self):
        """当前页面是否在工作台管理页"""
        el = self.get_elements(self.__class__.__locators['预览(1/2)'])
        if len(el) > 0:
            return True
        return False

    @TestLogger.log()
    def edit_btn_is_toast(self):
        """获取编辑按钮状态是可点击是否有提示框"""
        return self.is_toast_exist("当前版本仅支持勾选单张图片时进行编辑", 3)

    @TestLogger.log()
    def click_edit(self):
        """点击编辑"""
        self.click_element(self.__class__.__locators["编辑"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=10, auto_accept_alerts=True):
        """等待照片预览页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["预览(1/2)"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def play_video(self):
        """视频播放"""
        self.click_element(self.__class__.__locators["视频播放三角形"])

    @TestLogger.log()
    def close_video(self):
        """关闭视频"""
        self.click_element(self.__class__.__locators["视频关闭"])

    @TestLogger.log()
    def play_video_btn_is_enabled(self):
        """获取视频播放三角形按钮状态是否可点击"""
        return self._is_enabled(self.__class__.__locators["视频播放三角形"])

    @TestLogger.log()
    def wait_for_video_preview_load(self, timeout=10, auto_accept_alerts=True):
        """等待视频预览页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["视频页面"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def get_pic_preview_num(self):
        """获取预览数"""
        el = self.get_element(self.__class__.__locators["预览(1/2)"])
        info = el.text
        num = info[-2]
        return num

    @TestLogger.log()
    def get_pic_preview_info(self):
        """获取预览信息"""
        el = self.get_element(self.__class__.__locators["预览(1/2)"])
        return el.text

    @TestLogger.log()
    def get_pic_send_num(self):
        """获取图片发送数量"""
        el = self.get_element(self.__class__.__locators["发送(2)"])
        info = el.text
        num = info[-2]
        return num

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def click_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送(2)"])
        # 发送图片需要时间
        time.sleep(times)

    @TestLogger.log()
    def click_picture_send(self, times=3):
        """点击发送"""
        self.click_element(self.__class__.__locators["发送"])
        # 发送图片需要时间
        time.sleep(times)

    @TestLogger.log()
    def click_original_photo(self):
        """点击原图"""
        self.click_element(self.__class__.__locators["原图"])
