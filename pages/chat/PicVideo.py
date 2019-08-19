from appium.webdriver.common.mobileby import MobileBy
import time
from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class PicVideoPage(BasePage):
    """聊天设置-》查找聊天内容-》图片与视频页面"""
    ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.ChatFileActivity'

    __locators = {
        '返回': (MobileBy.XPATH, "//*[contains(@resource-id, 'back')]"),
        '图片与视频标题': (MobileBy.ID, 'com.chinasofti.rcs:id/title'),
        '本月': (MobileBy.ID, 'com.chinasofti.rcs:id/tv_date'),
        '视频': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/iv_thumb"]/..//*[@resource-id="com.chinasofti.rcs:id/video_duration"]'),
        '图片与视频': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_thumb'),
        # 点击图片
        '放大的图片': (MobileBy.XPATH, '//*[@resource-id="com.chinasofti.rcs:id/vp_preview"]/android.widget.ImageView'),
        # 点击视频
        '视频关闭X': (MobileBy.ID, 'com.chinasofti.rcs:id/iv_close'),
        '放大的视频': (MobileBy.ID, 'com.chinasofti.rcs:id/contentFrame'),

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=8, auto_accept_alerts=True):
        """等待图片与视频页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["图片与视频标题"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def is_on_this_page(self, timeout=2, auto_accept_alerts=True):
        """是否在当前页面"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["图片与视频标题"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def is_exist_video(self):
        """是否存在视频"""
        return self._is_element_present(self.__class__.__locators['视频'])

    @TestLogger.log()
    def press_video_to_do(self, text):
        """长按视频进行操作; args: text 为删除、收藏、转发等参数"""
        el = self.get_element(self.__class__.__locators['视频'])
        self.press(el)
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % text))

    @TestLogger.log()
    def delete_video(self):
        """删除视频"""
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            if not self.is_exist_video():
                break
            self.press_video_to_do("删除")
            time.sleep(0.5)

    @TestLogger.log()
    def press_pic_to_do(self, text):
        """长按图片进行操作; args: text 为删除、收藏、转发等参数"""
        self.delete_video()
        el = self.get_element(self.__class__.__locators['图片与视频'])
        self.press(el)
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % text))

    @TestLogger.log()
    def clear_record(self):
        """清除图片与视频记录"""
        current = 0
        while True:
            current += 1
            if current > 20:
                return
            if not self._is_element_present(self.__class__.__locators['图片与视频']):
                break
            el = self.get_element(self.__class__.__locators['图片与视频'])
            self.press(el)
            self.click_element((MobileBy.XPATH, "//*[contains(@text, '删除')]"))
            time.sleep(1)

    @TestLogger.log()
    def get_record_nums(self):
        """获取图片和视频记录数"""
        els = self.get_elements(self.__class__.__locators['图片与视频'])
        return len(els)

    @TestLogger.log()
    def click_pic(self):
        """点击图片"""
        self.delete_video()
        self.click_element(self.__class__.__locators['图片与视频'])

    @TestLogger.log()
    def click_video(self):
        """点击视频"""
        self.click_element(self.__class__.__locators['视频'])

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators['返回'])
        time.sleep(1)

    @TestLogger.log()
    def wait_for_pic_preview_page_load(self, timeout=5, auto_accept_alerts=True):
        """等待图片阅览页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["放大的图片"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def wait_for_play_video_page_load(self, timeout=5, auto_accept_alerts=True):
        """等待视频播放页面加载"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["视频关闭X"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log()
    def close_video(self):
        """关闭视频播放"""
        self.click_element(self.__class__.__locators["视频关闭X"])

    @TestLogger.log()
    def press_preview_pic_to_do(self, text):
        """长按阅览放大的图片进行操作; args: text 为删除、收藏、转发等参数"""
        el = self.get_element(self.__class__.__locators['放大的图片'])
        self.press(el)
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % text))

    @TestLogger.log()
    def close_pic_preview(self):
        """退出图片阅览"""
        self.click_element(self.__class__.__locators['放大的图片'])

    @TestLogger.log()
    def press_preview_video_to_do(self, text):
        """长按播放的视频进行操作; args: text 为删除、收藏、转发等参数"""
        el = self.get_element(self.__class__.__locators['放大的视频'])
        self.press(el)
        self.click_element((MobileBy.XPATH, "//*[contains(@text, '%s')]" % text))
