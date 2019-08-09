from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class WebMore(BasePage):
    """打开的网页消息界面"""
    # ACTIVITY = 'com.cmcc.cmrcs.android.ui.activities.QRCodeActivity'
    # ACTIVITY = 'com.android.browser'

    __locators = {
        '刷新': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_refresh'),
        '复制连接': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_copy'),
        '在浏览器中打开': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_open_in_browser'),
        '转发给QQ好友': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_send_to_qq'),
        '转发到朋友圈': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_send_to_wechat_moment'),
        '转发给微信好友': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_send_wechat'),
        '转发给朋友': (MobileBy.ID, 'com.chinasofti.rcs:id/ll_send'),
        '允许': (MobileBy.XPATH, '//*[@text="允许"]'),
    }

    @TestLogger.log('等待加载完毕')
    def wait_for_loading_animation_end(self):
        self.mobile.wait_until(
            condition=lambda d: self.get_element(self.__locators['com.chinasofti.rcs:id/btn_more']),
            timeout=60
        )

    @TestLogger.log("点击允许权限")
    def click_allow_button(self):
        if self._is_element_present(self.__class__.__locators['允许']):
            self.click_element(self.__class__.__locators['允许'])
        return True

    @TestLogger.log('刷新')
    def click_refresh(self):
        self.click_element(self.__locators['刷新'])

    @TestLogger.log('复制连接')
    def click_copy(self):
        self.click_element(self.__locators['复制连接'])

    @TestLogger.log('在浏览器中打开')
    def click_open_in_browser(self):
        self.click_element(self.__locators['在浏览器中打开'])

    @TestLogger.log('转发给QQ好友')
    def click_send_to_qq(self):
        self.click_element(self.__locators['转发给QQ好友'])

    @TestLogger.log('转发到朋友圈')
    def click_send_to_wechat_moment(self):
        self.click_element(self.__locators['转发到朋友圈'])

    @TestLogger.log('转发给微信好友')
    def click_send_wechat(self):
        self.click_element(self.__locators['转发给微信好友'])

    @TestLogger.log('转发给朋友')
    def click_send(self):
        self.click_element(self.__locators['转发给朋友'])

    # @TestLogger.log('等待页面跳转')
    # def wait_for_page_jump_out_automatically(self, max_wait_time=16):
    #     self.wait_until(
    #         condition=lambda d: self.mobile.current_activity == self.__class__.ACTIVITY,
    #         timeout=max_wait_time,
    #     )

    @TestLogger.log('当前页面是否包含此元素')
    def is_element_exist(self, text):
        """当前页面是否包含此元素"""
        return self._is_element_present(self.__locators[text])
