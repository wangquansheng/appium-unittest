from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatSelectFilePage(BasePage):
    """聊天选择文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChooseLocalFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/pop_10g_window_drop_view': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/pop_10g_window_drop_view'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/left_back'),
                  'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn': (
                  MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_back_btn'),
                  '选择文件': (MobileBy.ID, 'com.chinasofti.rcs:id/select_picture_custom_toolbar_title_text'),
                  'com.chinasofti.rcs:id/fl_container': (MobileBy.ID, 'com.chinasofti.rcs:id/fl_container'),
                  '本地文件': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_mobile_memory'),
                  '视频': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_vedio'),
                  '照片': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_pic'),
                  '音乐': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_music'),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待选择文件页面加载 """
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["选择文件"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(timeout)
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def click_local_file(self):
        """点击本地文件"""
        self.click_element(self.__class__.__locators["本地文件"])
        time.sleep(1)

    @TestLogger.log()
    def click_video(self):
        """点击视频"""
        self.click_element(self.__class__.__locators["视频"])

    @TestLogger.log()
    def click_pic(self):
        """点击照片"""
        self.click_element(self.__class__.__locators["照片"])

    @TestLogger.log()
    def click_music(self):
        """点击音乐"""
        self.click_element(self.__class__.__locators["音乐"])

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在选择文件界面"""
        el = self.get_elements(self.__locators['本地文件'])
        if len(el) > 0:
            return True
        return False
