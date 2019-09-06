import time

from appium.webdriver.common.mobileby import MobileBy

from library.core.BasePage import BasePage
from library.core.TestLogger import TestLogger


class GroupMessengerPage(BasePage):
    """群发信使首页"""

    ACTIVITY = 'com.cmicc.module_enterprise.ui.activity.EnterpriseH5ProcessActivity'

    __locators = {
        '新建短信': (MobileBy.XPATH, '//*[@text="新建短信"]'),
        '返回': (MobileBy.ID, "com.chinasofti.rcs:id/btn_back_actionbar"),
        '右上角帮助图标': (MobileBy.ID, "com.chinasofti.rcs:id/ib_right1")

    }

    @TestLogger.log()
    def wait_for_page_load(self, timeout=60, auto_accept_alerts=True):
        """等待群发信使首页加载"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新建短信"])
            )
        except:
            raise AssertionError("页面在{}s内，没有加载成功".format(str(timeout)))
        return self

    @TestLogger.log()
    def is_on_group_messenger_page(self, timeout=20, auto_accept_alerts=True):
        """当前页面是否在群发信使首页"""

        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["新建短信"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def click_help_icon(self):
        """点击右上角帮助图标"""
        self.click_element(self.__class__.__locators["右上角帮助图标"])

    @TestLogger.log()
    def click_new_message(self):
        """点击新建短信"""
        self.click_element(self.__class__.__locators["新建短信"])
        time.sleep(2)

    @TestLogger.log()
    def click_back(self):
        """点击返回"""
        self.click_element(self.__class__.__locators["返回"])


