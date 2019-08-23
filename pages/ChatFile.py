from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class ChatFilePage(BasePage):
    """查找聊天内容-》文件-》聊天文件页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChatFileActivity'

    __locators = {'': (MobileBy.ID, ''),
                  'com.chinasofti.rcs:id/action_bar_root': (MobileBy.ID, 'com.chinasofti.rcs:id/action_bar_root'),
                  'android:id/content': (MobileBy.ID, 'android:id/content'),
                  'com.chinasofti.rcs:id/toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/toolbar'),
                  'com.chinasofti.rcs:id/id_toolbar': (MobileBy.ID, 'com.chinasofti.rcs:id/id_toolbar'),
                  '返回': (MobileBy.ID, 'com.chinasofti.rcs:id/back'),
                  '聊天文件': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
                  'com.chinasofti.rcs:id/chat_file_list': (MobileBy.ID, 'com.chinasofti.rcs:id/chat_file_list'),
                  '本月': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
                  'com.chinasofti.rcs:id/favorite_layout': (MobileBy.ID, 'com.chinasofti.rcs:id/favorite_layout'),
                  'com.chinasofti.rcs:id/tv_head': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_head'),
                  '我': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_name'),
                  '今天': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_time'),
                  'com.chinasofti.rcs:id/favorite_image_shortcut': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/favorite_image_shortcut'),
                  'com.chinasofti.rcs:id/favorite_file_name_size': (
                      MobileBy.ID, 'com.chinasofti.rcs:id/favorite_file_name_size'),
                  '文件名': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '录制.txt': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '271.0B': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  '445475fa1e154603b4fd64ce34fa8c62.amr': (MobileBy.ID, 'com.chinasofti.rcs:id/file_name'),
                  '3.7KB': (MobileBy.ID, 'com.chinasofti.rcs:id/file_size'),
                  # 文件长按弹窗
                  '收藏': (MobileBy.XPATH, "//*[contains(@text, '收藏')]"),
                  '转发': (MobileBy.XPATH, "//*[contains(@text, '转发')]"),
                  '删除': (MobileBy.XPATH, "//*[contains(@text, '删除')]"),
                  }

    @TestLogger.log()
    def click_back(self):
        """点击 返回"""
        self.click_element(self.__class__.__locators['返回'])
        time.sleep(1)

    @TestLogger.log()
    def delete_file(self, file):
        """长按文件删除"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        self.click_element(self.__class__.__locators['删除'])

    @TestLogger.log()
    def collection_file(self, file):
        """收藏文件"""
        time.sleep(2)
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        time.sleep(3)
        self.click_element(self.__class__.__locators['收藏'])

    @TestLogger.log()
    def forward_file(self, file):
        """转发文件"""
        el = self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))
        self.press(el)
        time.sleep(2)
        self.click_element(self.__class__.__locators['转发'])
        time.sleep(1)

    @TestLogger.log()
    def is_on_this_page(self):
        """是否在此页面"""
        if self.is_text_present("本月"):
            return True
        else:
            return False

    @TestLogger.log()
    def clear_file_record(self):
        """清除文件记录"""
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            els = self.get_elements(self.__class__.__locators['文件名'])
            if not els:
                break
            for el in els:
                self.press(el)
                self.click_element(self.__class__.__locators["删除"])

    @TestLogger.log()
    def page_should_contain_file(self):
        """页面应该有文件记录"""
        self.page_should_contain_element(self.__class__.__locators['文件名'])

    @TestLogger.log()
    def wait_for_page_loads(self, timeout=60):
        """等待 页面加载"""
        try:
            self.wait_until(
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["本月"]),
                timeout=timeout
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log("点击文件")
    def click_file(self, file):
        self.wait_until(
            condition=lambda x: self.get_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % file))).click()
